# MATLAB Runner

[中文说明](README.zh-CN.md)

`matlab-runner` is a lightweight adapter for coding agents that need to use an
available MATLAB MCP server. It defines when MATLAB should be invoked, how to
choose the narrowest exposed capability, and how to report execution, tests,
and numerical validation honestly.

The package is a review candidate based on contributor version `v0.1.8`. It is
not an official MathWorks package and does not bundle MATLAB, a MATLAB license,
the MATLAB MCP Server, or the MATLAB Agentic Toolkit.

## Author

- Original author: `njustar2002`
- GitHub email: `njustar2002@vip.163.com`

## When it runs

The adapter is loaded only when the user explicitly requests MATLAB, the task
operates on MATLAB `.m` files, or a MATLAB-specific toolbox, license, session,
or runtime result is genuinely required. Ordinary mathematics and generic
programming tasks do not trigger it merely because MATLAB could be used.

## Workflow

1. Check only the environment capability needed for the task.
2. Inspect the coding agent's current tool catalog.
3. Match the required MATLAB MCP capability and its argument schema.
4. Implement or inspect the MATLAB code.
5. Execute through the available MATLAB MCP server when execution is requested.
6. Run MATLAB unit tests and numerical checks when applicable.
7. Report the actual tool calls, files, tests, validation criteria, and limits.

Tool names are not hard-coded. The coding agent must use the actual exposed
name for a capability such as `evaluate_matlab_code`, whether its client shows
that name bare, with a server prefix, or with a namespace.

## Setup

Place this package where the coding agent can load skills, then configure a
compatible MATLAB MCP server in that client. See
[`references/client-setup.md`](references/client-setup.md). The canonical
workflow contains no client-specific installation path.

## Validation

The included Python tests validate package structure and portable routing
rules. They do not claim to execute MATLAB:

```bash
python3 -m unittest discover -s skills/matlab-runner/tests -v
```

See [`PROVENANCE.yaml`](PROVENANCE.yaml) for authorship and publication
authorization, and [`NORMALIZATION.md`](NORMALIZATION.md) for the public
edition changes.
