# THM-M-0995 anchor audit

Item: `S56-M-0995-ANCHOR_AUDIT`  
Base revision: `b15861ce0ba012fa04e8c728e6bacbc35a359aea`  
Search cutoff: 2026-07-12

## Verdict

No exact Lean 4 proof of the frozen `StatementShape` was located. The root remains `M3`: its exact
statement is elaborated, while its proof is open. Pinned mathlib contains kernel-checked Chernoff,
sub-Gaussian sum, Hoeffding-lemma, and independent-variance anchors, classified `M2` for this root.
They do not produce the variance-sensitive denominator `2 * (v + b*t/3)`.

The external HighDimProb repository contains a real scalar Bernstein development at immutable
revision `8d4eec8bc06d80e8436ab3505000fca999b46546`, including
`upperTailProb_le_exp_neg_quarter_bernsteinRate_of_centeredSubExponentialMGFLIntegral_sum` and
`bernstein_sum_subExponential`. It is `M5` for this target because its assumptions, min-form
exponent, tail codomain, positivity boundary, and constants materially differ. It is not a proof of
the canonical target and was not fetched into `.lake`.

## Search ledger

The search order was repo-local, pinned mathlib, then public Lean 4 repositories. Local queries
covered `Bernstein`, `Bennett`, `subexponential`, `mgf`, `measure_sum_ge_le`, `variance_sum`, and
`bounded independent variance tail`. Mathlib was inspected at commit
`8a178386ffc0f5fef0b77738bb5449d50efeea95` from its clean existing dependency checkout.

GitHub repository search for `Bernstein inequality Lean` returned HighDimProb. Its source, manifest,
toolchain, license, API smoke test, commit/tree identities, and CI result were read through immutable
GitHub API/raw URLs. Anonymous GitHub code search returned HTTP 401, and grep.app returned a Vercel
security checkpoint rather than search results. Thus this is a replayable bounded search, not a
claim of exhaustive discovery.

## Validation

Commands used no dependency update, clone, or fetch:

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | rev-5.6 standard passed |
| `python3 scripts/stage1_target.py check` | 0 | all 1546 manifest targets passed |
| `python3 scripts/stage1_target.py show THM-M-0995` | 0 | rank 275, uniform L0/rework target confirmed |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0995/AnchorAudit.lean` | 0 | all seven pinned declarations resolved; four axiom reports printed |
| `python3 -m json.tool Stage1_Instances/THM-M-0995/anchor-audit.json` | 0 | structured inventory parsed |
| `git diff --check -- Stage1_Instances/THM-M-0995` | 0 | no whitespace errors |

This audit completes only candidate discovery and classification pending master acceptance. It does
not close any proof obligation, establish `AUDIT-Z`, or claim theorem completion.
