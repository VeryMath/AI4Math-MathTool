# math-glossary normalization record

## Scope

This file records the mapping from the original course submission identified by
the SHA-256 in `PROVENANCE.yaml` to the local VeryMath course edition. The
original archive remains byte-for-byte unchanged in a teacher-controlled,
Git-ignored intake area.

The first phase deliberately keeps `math-glossary` independent. No existing
VeryMath skill is imported, inherited, merged, or used as hidden runtime logic.

## Mechanical moves

| Original package path | Course-edition path | Semantic change |
| --- | --- | --- |
| `.gitignore` | repository `.gitignore` | Expanded to exclude private intake and runtime outputs |
| `SKILL.md` | `SKILL.md` | Core workflow retained; adapter, dependency, path, and safety instructions made portable |
| `glossary_backup.py` | `scripts/glossary_backup.py` | Backup behavior retained; timestamp made collision-resistant |
| `glossary_enrich_examples.py` | `scripts/glossary_enrich_examples.py` | See portability changes below |
| `glossary_export.py` | `scripts/glossary_export.py` | See safety changes below |
| `glossary_web.py` | `scripts/glossary_web.py` | See portability and safety changes below |
| `glossary-schema.md` | `references/glossary-schema.md` | Path and consistency corrections only |
| `glossary-usage-guide.md` | `references/glossary-usage-guide.md` | Portable commands and paths |
| `glossary-web-template.md` | `references/glossary-web-template.md` | Portable launch instructions |
| `user-manual.md` | `references/user-manual.md` | Portable launch and dependency instructions |

CRLF line endings and the UTF-8 BOM in copied text files were normalized without
changing their content meaning.

## Release-only additions

- Added bilingual package README files and a machine-readable JSON Schema.
- Added a narrow offline `glossary_build.py` entry point for the structured
  CSV/TSV/JSON/YAML formats already promised by the original workflow.
- Added `PROVENANCE.yaml`, this normalization record, dependency manifests,
  generated OpenAI agent metadata, and isolated tests.
- Added the repository router, registry, contribution record, and explicit
  license-status gate.

## Portability and safety changes

- Replaced `.claude` and `%USERPROFILE%` runtime assumptions with paths derived
  from the installed package plus explicit CLI arguments.
- Replaced the fixed DeepSeek proxy URL, model, and placeholder API key with
  explicit CLI flags or environment variables. AI enrichment remains optional;
  offline backup/import/export/Web behavior does not require the OpenAI client.
- Added portable Web options for glossary path, host, port, and browser opening.
- Replaced immediate `os._exit(0)` shutdown with a best-effort development
  server shutdown response.
- Made JSON writes atomic and removed stale Excel exports only after a new
  export succeeds.
- Made CLI and Web writes report JSON-complete/Excel-pending as a partial
  success instead of losing the JSON result or claiming full synchronization.
- Neutralized formula-leading user text during Excel export and restored the
  literal text on import.
- Added schema validation at script boundaries so invalid top-level JSON or
  missing required fields fail clearly before overwriting data.
- Replaced automatic dependency installation instructions with explicit checks
  and user-approved installation commands.

## Preserved behavior

- JSON remains the source of truth.
- Entries retain the original fields and bilingual examples.
- Sorting remains case-insensitive by English term and then Chinese translation;
  `idx` is reassigned continuously after writes.
- Excel remains a human-review export.
- The local Web interface retains search, statistics, add, edit, delete, log,
  and refresh behavior.
- Example enrichment still batches missing examples through an
  OpenAI-compatible chat-completions API when explicitly configured.

## Pending confirmation

- Contributor approval of this normalization diff
- Preferred public display name
- Authorization to publish the contribution
- Repository license
- Third-party dictionary, corpus, font, template, and Web asset review

Until these items are confirmed, this course edition must remain private and
must not be described as released.
