# Publishing AI4Math-MathTool

This document describes the one-time publication of the tested local release
candidate. Creating the public repository, pushing, tagging, and releasing are
separate external write actions.

## 1. Validate the candidate

From the repository root:

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install \
  -r skills/math-glossary/requirements.txt \
  -r skills/math-glossary/requirements-ai.txt
python -m unittest discover -s tests -v
python -m unittest discover -s skills/math-glossary/tests -v
python -m unittest discover -s skills/matlab-runner/tests -v
git status --short
```

Only publish a tested commit with no unintended tracked changes. The private
`.intake/` archive must remain ignored and must never be pushed.

## 2. Create the public GitHub repository

Authenticate an account that may create repositories in the `VeryMath`
organization, then create an empty public repository without generated files:

```bash
gh auth status
gh repo create VeryMath/AI4Math-MathTool \
  --public \
  --source=. \
  --remote=origin
```

Publish the tested commit as the initial `main` branch:

```bash
git switch -c main
git push -u origin main
```

The included GitHub Actions workflow will run the repository and package test
suites on supported Python versions.

## 3. Verify and release

Wait for CI to pass, inspect the public file list, and confirm that `.intake/`,
credentials, runtime glossaries, and generated workbooks are absent. Then:

```bash
gh run list --limit 5
git tag -a v0.1.0 -m "AI4Math-MathTool v0.1.0"
git push origin v0.1.0
gh release create v0.1.0 \
  --title "AI4Math-MathTool v0.1.0" \
  --generate-notes
```

## 4. Connect the ecosystem

After the remote URL and passing CI run exist:

1. add the repository to the AI4Math Skill Library catalog;
2. add the `math-glossary` entry to VeryMath with the GitHub and documentation
   links;
3. keep the original course ZIP only in the private teacher-controlled intake
   archive.

## 中文说明

发布分成四个可核验动作：先在干净环境跑完测试，再创建空的公开仓库，将当前已测试
提交作为 `main` 推送，CI 通过后再创建 `v0.1.0` Release。最后才同步
AI4Math-Skill-Library 与 VeryMath 页面。任何一步都不得上传 `.intake/`、密钥、真实
术语库或课程原始材料。

## Adding later packages

Later packages such as `matlab-runner` are integrated through a reviewed pull
request rather than by rewriting the historical `v0.1.0` release. Validate the
root suite and every affected package suite, inspect the public tree, and merge
before deciding whether a new repository tag is warranted. Static adapter tests
must not be described as MATLAB execution evidence.
