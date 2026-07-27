# Third-party materials

The repository does not vendor third-party source code, dictionaries, corpora,
PDFs, fonts, images, or Web assets. The CSS uses system-font fallback names
only. The original course submission and the normalized package were reviewed
for these material classes before the MIT release candidate was prepared.

The following packages are installed separately by users and retain their own
licenses:

| Dependency | Declared range | Purpose | Upstream license |
| --- | --- | --- | --- |
| [Flask](https://github.com/pallets/flask) | `>=3.0,<4` | Optional local Web UI | BSD-3-Clause |
| [openpyxl](https://foss.heptapod.net/openpyxl/openpyxl) | `>=3.1,<4` | Excel import and export | MIT/Expat |
| [PyYAML](https://github.com/yaml/pyyaml) | `>=6,<7` | YAML import | MIT |
| [openai-python](https://github.com/openai/openai-python) | `>=1,<3` | Optional AI example enrichment | Apache-2.0 |
| [mdict-utils](https://pypi.org/project/mdict-utils/) | user-installed optional tool | Optional MDX extraction | MIT |

Transitive dependencies selected by package installers are not redistributed
in this repository and remain subject to their own license terms. The
repository MIT license applies only to material for which the repository
contributors can grant that license.

User-supplied dictionaries, corpora, papers, scans, PDFs, spreadsheets, and
other source materials are not part of this repository. Users are responsible
for confirming that they may process and redistribute any derived glossary
content.
