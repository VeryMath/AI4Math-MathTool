# MATLAB Runner normalization record

This public review candidate preserves the contributor's trigger boundary,
lightweight preflight, MATLAB implementation and execution flow, unit-testing
rules, numerical validation rules, error taxonomy, and completion summary.

The following repository-edition changes were made on 2026-08-10:

- moved the canonical package from a client-specific `.opencode` layout to
  `skills/matlab-runner/`;
- replaced fixed OpenCode paths and Windows configuration with a relative,
  coding-agent-neutral setup reference;
- replaced fixed MCP tool prefixes with runtime discovery by capability and
  argument schema;
- added bilingual package documentation, provenance, tests, and repository
  metadata;
- excluded `.DS_Store`, local client configuration, the original archive, and
  historical review/evidence files from the public package;
- excluded `FINAL_SUBMISSION_AUDIT.md` because it described a `NOTICE.md` file
  that was not present in the submitted archive;
- retained the historical changelog as contributor-supplied context without
  treating its review statements as current CI or MATLAB execution evidence.

The normalization tests check repository shape and adapter portability. MATLAB
was not executed by those Python tests, so this record makes no MATLAB runtime,
license, toolbox, or numerical-success claim.
