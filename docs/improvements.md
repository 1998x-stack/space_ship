# Portfolio Improvement History

### 2026-11-06 05:22 UTC — ChatGPT Portfolio Iteration
- Run ID: 20261106T052200Z-18cd5c
- Repo / Base SHA: 1998x-stack/space_ship / e67956a51021e9e27c5d1fa7229c714b77e8bdf1
- Historical context: First initialization; docs/improvements.md returned 404 on default branch before source edits. No PRs returned by repository PR search. Recent commits inspected.
- Product problem & expected user value: A player finishing a lower-scoring run should retain their earlier best score; a new best should persist.
- Engineering diagnosis & evidence: systems/scoring.py Scoring.save_high_score unconditionally wrote self.score, overwriting an existing higher record. Local baseline regression failed: expected 900, observed 100.
- Options & decision: P1 high-score regression selected (benefit 5 + correctness 5 + evidence 5 + testability 5 - cost 1 - risk 2 = 17); other candidates: settings.py finite numeric validation (4+3+3+4-2-2=10), game.py QUIT event post-processing (3+3+3+3-2-2=8). Other candidates require further reproduction.
- Changes: systems/scoring.py now writes only if current score exceeds loaded record; tests/test_scoring_regression.py covers lower score, new record and missing file. Public API and file format unchanged.
- Validation: B baseline python -m pytest -q tests/test_scoring_regression.py: 1 failed, 2 passed; A modified implementation same command: 3 passed; C python -m compileall -q systems/scoring.py tests/test_scoring_regression.py: passed. These were executed in an isolated local copy of the fetched scoring module, not a full repository checkout. Existing repository suite, pygame integration and browser E2E not run.
- Security & regression review: No keys, workflows, deployment, permission, LICENSE or SECURITY changes. Persistence remains best-effort; concurrent writes and corrupt existing scores are outside this patch.
- Risk & rollback: Low-scope persistence behavior change; revert the PR's scoring and regression-test commits if unexpected behavior occurs. Manual integration check recommended.
- Follow-up: Run full repository pytest and browser gameplay smoke; independently reproduce settings finite-value validation issue.
- Commit: pending
- PR: pending
