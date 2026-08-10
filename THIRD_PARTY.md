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

## MATLAB Runner boundaries

`skills/matlab-runner` contains routing instructions, references, tests, and
small original MATLAB examples. It does not vendor MATLAB, MathWorks products,
the MATLAB MCP Server, the MATLAB Agentic Toolkit, OpenCode, or another coding
agent. It is a community adapter and is not an official MathWorks or OpenCode
package.

The following software, when selected by a user, is installed separately and
remains governed by its upstream terms:

| Dependency | Purpose | Upstream terms |
| --- | --- | --- |
| [MATLAB](https://www.mathworks.com/products/matlab.html) and optional toolboxes | Numerical runtime and product-specific functions | MathWorks product license selected by the user or institution |
| [MATLAB MCP Server](https://github.com/matlab/matlab-mcp-server#licensing-and-usage) | Expose MATLAB execution capabilities to an MCP client | Upstream `LICENSE.md`; use only with MATLAB, do not share one server among multiple users, and contact MathWorks for shared or centralized use |
| [MATLAB Agentic Toolkit](https://github.com/matlab/matlab-agentic-toolkit) | Optional upstream agentic components | Upstream `LICENSE.md`, including the MathWorks-products use condition |
| [OpenCode](https://github.com/anomalyco/opencode) | One optional coding-agent client; not required by this package | MIT |

The repository MIT license applies to the normalized `matlab-runner` package,
not to separately installed MATLAB or MathWorks components. Users must provide
their own valid MATLAB installation and license and follow each dependency's
terms.
