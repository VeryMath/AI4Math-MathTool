from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest import mock


PACKAGE_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = PACKAGE_ROOT / "scripts"


def load_script(module_name: str, filename: str):
    path = SCRIPTS_DIR / filename
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def sample_terms(*, missing_examples: bool = False):
    return [
        {
            "term_id": "manifold",
            "en": "manifold",
            "cn": "流形",
            "idx": 1,
            "pos": "名词",
            "field": ["拓扑学"],
            "source": "test fixture",
            "examples": [] if missing_examples else [
                {
                    "en": "A sphere is a manifold.",
                    "cn": "球面是一个流形。",
                }
            ],
            "created_at": "2026-07-01",
            "updated_at": "2026-07-01",
        },
        {
            "term_id": "abelian group",
            "en": "abelian group",
            "cn": "阿贝尔群",
            "idx": 2,
            "pos": "名词",
            "field": ["代数学"],
            "source": "test fixture",
            "examples": [
                {
                    "en": "Every cyclic group is abelian.",
                    "cn": "每个循环群都是阿贝尔群。",
                }
            ],
            "created_at": "2026-07-01",
            "updated_at": "2026-07-01",
        },
    ]


class BackupTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.backup = load_script(
            "math_glossary_backup_test",
            "glossary_backup.py",
        )

    def test_backup_preserves_bytes_and_never_overwrites(self):
        with tempfile.TemporaryDirectory() as temporary_dir:
            glossary = Path(temporary_dir) / "glossary.json"
            original = b'[{"term_id":"x","en":"x","cn":"x"}]\n'
            glossary.write_bytes(original)

            first = Path(self.backup.backup_glossary(glossary))
            second = Path(self.backup.backup_glossary(glossary))

            self.assertNotEqual(first, second)
            self.assertEqual(first.read_bytes(), original)
            self.assertEqual(second.read_bytes(), original)

    def test_missing_source_returns_none(self):
        with tempfile.TemporaryDirectory() as temporary_dir:
            missing = Path(temporary_dir) / "missing.json"
            self.assertIsNone(self.backup.backup_glossary(missing))


class StructuredBuildTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.builder = load_script(
            "math_glossary_build_test",
            "glossary_build.py",
        )

    def test_csv_build_has_unique_ids_fields_sorting_and_trace(self):
        csv_text = (
            "English,中文,词性,子领域\n"
            "manifold,流形,名词,拓扑学 / 微分几何\n"
            "homology,同源性,名词,代数拓扑\n"
            "homology,同调,名词,代数拓扑\n"
            "ring,环,名词,代数学\n"
        )
        with tempfile.TemporaryDirectory() as temporary_dir:
            source = Path(temporary_dir) / "terms.csv"
            source.write_text(csv_text, encoding="utf-8")
            records = self.builder.read_structured_source(source)
            terms = self.builder.build_terms(
                records,
                source_label="课程样例",
            )

            self.assertEqual(
                [term["en"] for term in terms],
                ["homology", "homology", "manifold", "ring"],
            )
            self.assertEqual(
                {term["term_id"] for term in terms},
                {"homology", "homology__1", "manifold", "ring"},
            )
            self.assertEqual([term["idx"] for term in terms], [1, 2, 3, 4])
            manifold = next(term for term in terms if term["en"] == "manifold")
            self.assertEqual(
                manifold["field"],
                ["拓扑学", "微分几何"],
            )
            self.assertEqual(
                manifold["source"],
                "课程样例; terms.csv:line 2",
            )

    def test_json_mapping_and_no_excel_cli(self):
        with tempfile.TemporaryDirectory() as temporary_dir:
            root = Path(temporary_dir)
            source = root / "terms.json"
            source.write_text(
                json.dumps(
                    {
                        "Banach space": "巴拿赫空间",
                        "compact set": "紧集",
                    },
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )
            output = root / "result" / "glossary.json"
            exit_code = self.builder.main([
                str(source),
                "--output",
                str(output),
                "--no-excel",
            ])
            terms = json.loads(output.read_text(encoding="utf-8"))

            self.assertEqual(exit_code, 0)
            self.assertEqual(len(terms), 2)
            self.assertTrue(all(term["source"] for term in terms))
            self.assertEqual(
                self.builder.main([
                    str(source),
                    "--output",
                    str(output),
                    "--no-excel",
                ]),
                2,
            )

    def test_schema_json_preserves_unique_term_ids(self):
        records = [
            ({
                "term_id": "measure",
                "en": "measure",
                "cn": "测度",
            }, "terms.json:record 1"),
            ({
                "term_id": "measure__4",
                "en": "measure",
                "cn": "度量",
            }, "terms.json:record 2"),
        ]
        terms = self.builder.build_terms(records)
        self.assertEqual(
            {term["term_id"] for term in terms},
            {"measure", "measure__4"},
        )

    def test_excel_failure_reports_partial_and_keeps_old_export(self):
        with tempfile.TemporaryDirectory() as temporary_dir:
            root = Path(temporary_dir)
            source = root / "terms.csv"
            source.write_text(
                "English,中文\nmanifold,流形\n",
                encoding="utf-8",
            )
            output = root / "术语库" / "glossary.json"
            output.parent.mkdir(parents=True)
            old_export = output.parent / "glossary_2026-07-01.xlsx"
            old_export.write_bytes(b"old-review-copy")

            with mock.patch.object(
                self.builder,
                "_load_export_function",
                side_effect=ImportError("openpyxl unavailable"),
            ):
                exit_code = self.builder.main([
                    str(source),
                    "--output",
                    str(output),
                ])

            self.assertEqual(exit_code, 3)
            self.assertTrue(output.is_file())
            self.assertEqual(old_export.read_bytes(), b"old-review-copy")


class SchemaDocumentTests(unittest.TestCase):
    def test_machine_readable_schema_is_valid_json_and_matches_core_fields(self):
        schema = json.loads(
            (
                PACKAGE_ROOT
                / "references"
                / "glossary.schema.json"
            ).read_text(encoding="utf-8")
        )
        self.assertEqual(schema["type"], "array")
        item_schema = schema["items"]
        self.assertEqual(
            set(item_schema["required"]),
            {"term_id", "en", "cn", "created_at", "updated_at"},
        )
        self.assertEqual(
            item_schema["properties"]["field"]["type"],
            "array",
        )


class WebSourceSafetyTests(unittest.TestCase):
    def test_inline_click_handler_reads_escaped_data_attribute(self):
        source = (SCRIPTS_DIR / "glossary_web.py").read_text(
            encoding="utf-8"
        )
        self.assertIn(
            'data-term-id="\' + esc(t.term_id) + \'"',
            source,
        )
        self.assertIn("openDetail(this.dataset.termId)", source)
        self.assertNotIn("openDetail(\\'\\' + esc(t.term_id)", source)

    def test_change_log_html_is_canonicalized_server_side(self):
        source = (SCRIPTS_DIR / "glossary_web.py").read_text(
            encoding="utf-8"
        )
        self.assertIn("html.escape(html.unescape(part), quote=True)", source)


try:
    import openpyxl  # noqa: F401
except ImportError:
    HAS_OPENPYXL = False
else:
    HAS_OPENPYXL = True


@unittest.skipUnless(HAS_OPENPYXL, "openpyxl is not installed")
class ExcelRoundTripTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.exporter = load_script(
            "math_glossary_export_test",
            "glossary_export.py",
        )
        cls.builder = load_script(
            "math_glossary_build_excel_test",
            "glossary_build.py",
        )

    def test_structured_build_cli_generates_json_and_excel(self):
        with tempfile.TemporaryDirectory() as temporary_dir:
            root = Path(temporary_dir)
            source = root / "terms.csv"
            source.write_text(
                "English,中文\nmanifold,流形\nring,环\n",
                encoding="utf-8",
            )
            output = root / "术语库" / "glossary.json"
            self.assertEqual(
                self.builder.main([
                    str(source),
                    "--output",
                    str(output),
                ]),
                0,
            )
            self.assertTrue(output.is_file())
            self.assertEqual(
                len(list(output.parent.glob("glossary_*.xlsx"))),
                1,
            )

    def test_export_import_round_trip_and_unique_alias_ids(self):
        with tempfile.TemporaryDirectory() as temporary_dir:
            root = Path(temporary_dir)
            source = root / "glossary.json"
            terms = sample_terms()
            terms.append({
                **terms[0],
                "term_id": "manifold__1",
                "cn": "多样体",
                "idx": 3,
            })
            source.write_text(
                json.dumps(terms, ensure_ascii=False),
                encoding="utf-8",
            )

            workbook = Path(
                self.exporter.export_to_excel(source, root / "exports")
            )
            imported_path = root / "round-trip" / "glossary.json"
            imported = self.exporter.import_from_excel(
                workbook,
                imported_path,
            )

            self.assertTrue(workbook.is_file())
            self.assertEqual(
                [term["en"] for term in imported],
                ["abelian group", "manifold", "manifold"],
            )
            self.assertEqual(
                [term["term_id"] for term in imported],
                ["abelian group", "manifold", "manifold__1"],
            )
            self.assertEqual(
                [term["idx"] for term in imported],
                [1, 2, 3],
            )
            self.assertEqual(imported[0]["field"], ["代数学"])
            self.assertEqual(
                json.loads(imported_path.read_text(encoding="utf-8")),
                imported,
            )
            self.assertEqual(
                list(imported_path.parent.glob(f".{imported_path.name}.*")),
                [],
            )

    def test_export_rejects_invalid_schema_before_writing(self):
        with tempfile.TemporaryDirectory() as temporary_dir:
            root = Path(temporary_dir)
            source = root / "glossary.json"
            source.write_text('{"manifold": "流形"}', encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "顶层必须"):
                self.exporter.export_to_excel(source, root / "exports")
            self.assertFalse((root / "exports").exists())

    def test_excel_formula_text_is_neutralized_and_restored(self):
        with tempfile.TemporaryDirectory() as temporary_dir:
            root = Path(temporary_dir)
            source = root / "glossary.json"
            terms = sample_terms()
            terms[0]["term_id"] = "=formula"
            terms[0]["en"] = "=1+1"
            terms[0]["cn"] = "@SUM(A1:A2)"
            source.write_text(
                json.dumps(terms, ensure_ascii=False),
                encoding="utf-8",
            )

            workbook_path = Path(
                self.exporter.export_to_excel(source, root / "exports")
            )
            workbook = openpyxl.load_workbook(
                workbook_path,
                read_only=True,
                data_only=False,
            )
            try:
                worksheet = workbook.active
                self.assertEqual(worksheet.cell(2, 2).value, "'=1+1")
                self.assertEqual(
                    worksheet.cell(2, 3).value,
                    "'@SUM(A1:A2)",
                )
                self.assertEqual(worksheet.cell(2, 2).data_type, "s")
            finally:
                workbook.close()

            imported = self.exporter.import_from_excel(
                workbook_path,
                root / "imported.json",
            )
            formula_term = next(
                term for term in imported if term["en"] == "=1+1"
            )
            self.assertEqual(formula_term["cn"], "@SUM(A1:A2)")


class EnrichmentTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.enricher = load_script(
            "math_glossary_enrichment_test",
            "glossary_enrich_examples.py",
        )

    def test_fake_client_enriches_without_openai_dependency(self):
        payload = json.dumps({
            "results": [{
                "en": "manifold",
                "example_en": "A torus is a manifold.",
                "example_cn": "环面是一个流形。",
            }]
        })
        response = SimpleNamespace(
            choices=[
                SimpleNamespace(
                    message=SimpleNamespace(content=payload)
                )
            ]
        )
        completions = SimpleNamespace(
            create=lambda **_kwargs: response
        )
        fake_client = SimpleNamespace(
            chat=SimpleNamespace(completions=completions)
        )

        with tempfile.TemporaryDirectory() as temporary_dir:
            path = Path(temporary_dir) / "glossary.json"
            path.write_text(
                json.dumps(
                    sample_terms(missing_examples=True),
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )
            updated, missing = self.enricher.enrich_glossary(
                path,
                api_key="test-key",
                model="test-model",
                batch_size=10,
                export_excel=False,
                delay_seconds=0,
                client=fake_client,
            )
            result = json.loads(path.read_text(encoding="utf-8"))

            self.assertEqual((updated, missing), (1, 1))
            self.assertEqual(
                [term["en"] for term in result],
                ["abelian group", "manifold"],
            )
            self.assertEqual(
                result[1]["examples"],
                [{
                    "en": "A torus is a manifold.",
                    "cn": "环面是一个流形。",
                }],
            )
            self.assertEqual([term["idx"] for term in result], [1, 2])

    def test_explicit_model_and_key_are_required(self):
        with tempfile.TemporaryDirectory() as temporary_dir:
            path = Path(temporary_dir) / "glossary.json"
            path.write_text(
                json.dumps(
                    sample_terms(missing_examples=True),
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )
            with self.assertRaisesRegex(ValueError, "api-key"):
                self.enricher.enrich_glossary(
                    path,
                    api_key="",
                    model="test-model",
                    export_excel=False,
                )
            with self.assertRaisesRegex(ValueError, "model"):
                self.enricher.enrich_glossary(
                    path,
                    api_key="test-key",
                    model="",
                    export_excel=False,
                )

    def test_noop_glossary_does_not_require_external_configuration(self):
        with tempfile.TemporaryDirectory() as temporary_dir:
            path = Path(temporary_dir) / "glossary.json"
            path.write_text(
                json.dumps(sample_terms(), ensure_ascii=False),
                encoding="utf-8",
            )
            self.assertEqual(
                self.enricher.enrich_glossary(
                    path,
                    api_key="",
                    model="",
                    export_excel=False,
                ),
                (0, 0),
            )


try:
    import flask  # noqa: F401
except ImportError:
    HAS_FLASK = False
else:
    HAS_FLASK = True


@unittest.skipUnless(HAS_FLASK, "Flask is not installed")
class WebApiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.web = load_script(
            "math_glossary_web_test",
            "glossary_web.py",
        )
        cls.web.app.config.update(TESTING=True)

    def setUp(self):
        self.temporary_dir = tempfile.TemporaryDirectory()
        self.glossary = Path(self.temporary_dir.name) / "glossary.json"
        self.glossary.write_text(
            json.dumps(sample_terms(), ensure_ascii=False),
            encoding="utf-8",
        )
        self.web.configure(self.glossary, PACKAGE_ROOT)
        self.client = self.web.app.test_client()

    def tearDown(self):
        self.temporary_dir.cleanup()

    def test_web_cli_defaults_to_loopback_and_rejects_implicit_remote_binding(
        self,
    ):
        parsed = self.web.build_parser().parse_args([
            "--glossary",
            str(self.glossary),
        ])
        self.assertEqual(parsed.host, "127.0.0.1")
        self.assertFalse(parsed.allow_remote)

        with mock.patch.object(self.web, "configure") as configure:
            self.assertEqual(
                self.web.main([
                    "--glossary",
                    str(self.glossary),
                    "--host",
                    "0.0.0.0",
                    "--no-browser",
                ]),
                2,
            )
        configure.assert_not_called()

    def test_read_search_stats_and_shutdown_fallback(self):
        terms = self.client.get("/api/terms?q=man").get_json()
        self.assertEqual(terms["total"], 1)
        self.assertEqual(terms["terms"][0]["term_id"], "manifold")

        stats = self.client.get("/api/stats").get_json()
        self.assertEqual(stats["total"], 2)

        shutdown = self.client.post("/api/shutdown")
        self.assertEqual(shutdown.status_code, 501)
        self.assertIn("Ctrl+C", shutdown.get_json()["error"])

    @unittest.skipUnless(HAS_OPENPYXL, "openpyxl is not installed")
    def test_create_conflict_then_create_refreshes_json_and_excel(self):
        conflict = self.client.post(
            "/api/terms",
            json={"en": "manifold", "cn": "多样体"},
        )
        self.assertEqual(conflict.status_code, 409)

        created = self.client.post(
            "/api/terms",
            json={
                "en": "Banach space",
                "cn": "巴拿赫空间",
                "field": "泛函分析 / 分析学",
            },
        )
        self.assertEqual(created.status_code, 201)
        stored = json.loads(self.glossary.read_text(encoding="utf-8"))
        self.assertEqual(
            [term["en"] for term in stored],
            ["abelian group", "Banach space", "manifold"],
        )
        self.assertEqual([term["idx"] for term in stored], [1, 2, 3])
        self.assertEqual(stored[1]["field"], ["泛函分析", "分析学"])
        self.assertEqual(
            len(list(self.glossary.parent.glob("glossary_*.xlsx"))),
            1,
        )


if __name__ == "__main__":
    unittest.main()
