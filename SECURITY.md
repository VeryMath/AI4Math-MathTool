# Security policy

Security fixes are applied to the current `main` branch and the latest tagged
release.

After the public repository exists, report suspected vulnerabilities privately
through GitHub Security Advisories. Do not include API keys, private glossaries,
course intake archives, or copyrighted source materials in a public issue.

The glossary Web UI is a local development interface without authentication.
It binds to `127.0.0.1` by default. Do not expose it to an untrusted network;
binding a non-loopback address requires the explicit `--allow-remote` flag.

AI enrichment sends selected terms to the endpoint configured by the user.
Review the endpoint's privacy and data-retention terms before using real
research data. Never store API keys in a glossary, command history, log, or
repository file.

The MATLAB runner may ask a connected MATLAB MCP server to execute code or
write files. Review generated or third-party `.m` files before execution, use
the narrowest requested capability, and keep destructive file operations under
explicit user control. The package does not store MATLAB licenses, VPN
credentials, MCP secrets, or local executable paths. Keep those values in the
user's local client or environment configuration and never commit them.
Do not expose one MATLAB MCP Server as a shared multi-user service; the
upstream licensing guidance requires contacting MathWorks for shared or
centralized deployments.
