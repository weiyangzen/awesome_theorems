# Anchor audit

Item: `S56-M-1291-ANCHOR_AUDIT`. Audit date: 2026-07-12.

## Pinned inventory

The installed manifest pins Lean `v4.29.0` and mathlib commit
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. The dependency checkout reports
that exact revision. A case-insensitive scan of all pinned `Mathlib/**/*.lean`
sources found no `Brezis`, `BrezisLieb`, or `Brezis-Lieb` declaration.

The nearest useful APIs are dominated convergence, finite `lintegral` results
for real powers, and `eLpNorm`/power-integral transports. `AnchorAudit.lean`
checks five representative declarations against the pinned kernel environment.
They are substrate, not terminal candidates: dominated convergence assumes one
integrable pointwise dominator, which the frozen target does not assume, and
the power-integral lemmas do not supply the Brezis-Lieb remainder identity.

The repository-wide Lean scan found no other Brezis-Lieb implementation. The
local `BrezisLiebTarget` is an exact proposition definition and has no proof
body, so it remains `M3` statement evidence and receives no closure credit.

## External Lean 4 search

On 2026-07-12, four GitHub repository-metadata queries returned zero results:
`Brezis Lieb Lean`, `Brezis-Lieb Lean4`, `Brezis Lieb theorem prover`, and
`Brezis Lieb formalization`. Sourcegraph's public Lean index returned zero
matches for the hyphenated, spaced, underscore, and camel-case names. GitHub
code search returned HTTP 401 because authentication was unavailable; that
lane is recorded as blocked, not counted as negative evidence. No candidate
was discovered, so no moving dependency was fetched and no immutable external
revision can truthfully be integrated.

## Classification

The exact root is `M4`: no formal proof candidate is known after this bounded
inventory. The principal missing route is the pointwise Brezis-Lieb remainder
estimate together with its uniform-integrability/truncation argument for all
real `p > 0`, including the quasi-norm range `0 < p < 1`. Replacing the uniform
power-integral bound with an integrable dominator would strengthen and
substitute the theorem.

This phase supplies no `H0`, obligation tree, proof, release receipt, or theorem
completion. Its self-tested result remains pending master acceptance.

## Validation receipt

Commands were run from the worker repository root on 2026-07-12.

| Command | Exit | Result |
|---|---:|---|
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | exact pinned mathlib commit |
| `rg -ni --glob '*.lean' 'brezis|brézis|lieb lemma|brezis.?lieb' Formalizations/Lean/.lake/packages/mathlib/Mathlib` | 1 | expected no-match result |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1291/AnchorAudit.lean` | 0 | all five pinned supporting declarations elaborated and printed |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1291/Statement.lean` | 0 | the frozen exact target still elaborated |
| `python3 -m json.tool Stage1_Instances/THM-M-1291/anchor-audit.json` | 0 | structured audit parsed |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets and ranks 1 through 1546 passed |
| `git diff --check -- Stage1_Instances/THM-M-1291 .stage1-worker-selftest.json` | 0 | no whitespace errors |
