# SMRITI UI & Agent Verification Governance Rules

To prevent unverified or phantom claims of code completion and testing, all coding assistant agents MUST follow these strict rules before declaring a task "done" or reporting test results:

## 1. Verifiable Code Diffs (MANDATORY)
For every file modified, created, or deleted, you MUST run a git diff and paste the literal `git diff` output for that exact file.
- Do NOT paraphrase the diff in prose.
- If a file is claimed to be modified but no diff can be produced, state that it was not actually committed or changed.

## 2. Literal Terminal Test Outputs
Do not summarize test results in tables or bullet points (e.g., "9/9 passed") without providing the literal terminal output of the test run.
- Paste the exact command executed.
- Paste the literal stdout and stderr returned by the test runner.

## 3. Mandatory Validator/Linter Re-run
After editing any file, you must run the relevant validator or linter script (e.g. `validate_tokens.py` for CSS/style changes) and paste the exact console output of the linter execution.
- If no linter exists for the modified file type, state so explicitly.

## 4. Measurement Evidence for Metrics
Do not claim metrics (e.g. "80% query reduction", "0 console errors") unless you provide the exact before-and-after measurements taken.
- If a metric was not measured, do not state a percentage or integer; describe the qualitative changes instead.

## 5. Verify Prior Session Claims
Do not build on top of a previous session summary's claims without first inspecting the actual codebase to verify those claims are true.

## 6. Granular and Enumerated Scope
Do not summarize file changes under high-level descriptions (e.g., "fixed the whole module" or "updated all templates") unless you list every single affected file and confirm the changes for each one individually.

## 7. Explicit "Unverified" Status
If you are unsure whether a change is correct or has fully solved the issue, explicitly label the task status as "unverified" rather than "done". Do not round up unverified items.

## 8. Git Diff Against Previous Committed State
If the agent has shell/file access, it is explicitly required to run `git diff` against the previous committed state (e.g., `git diff` or `git diff HEAD~1`) and paste that literal diff output in the response. This ensures changes are verified on disk and not just assumed.

## 9. No Prose-Only Metric Claims
Never claim a metrics improvement or successful test verification in prose unless accompanied by the literal, raw output (e.g., terminal output, test results, or linter runs) proving the assertion.
