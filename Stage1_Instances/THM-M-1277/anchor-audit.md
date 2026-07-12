# Anchor audit

## Verdict

No exact Lean 4 anchor was found for `Stage1Rev56.THMM1277.Statement`.
The closest pinned mathlib declarations are useful background infrastructure,
but none proves either root conjunct. The disposition is therefore **direct
formalization required**, with the root remaining `[H1, M3, R3]`.

## Immutable mathlib audit

The audited checkout is mathlib commit
`8a178386ffc0f5fef0b77738bb5449d50efeea95` (commit date
`2026-03-30T18:47:58Z`) under Lean 4.29.0. A literal search of all its Lean
sources found no occurrence of `Trudinger`, `Moser-Trudinger`, or
`MoserTrudinger`.

The nearest substantive file is
`Mathlib.Analysis.FunctionalSpaces.SobolevInequality`. Its relevant public
declarations are:

| Declaration | What it establishes | Exact-target gap |
|---|---|---|
| `lintegral_pow_le_pow_lintegral_fderiv` | A finite-power Gagliardo-Nirenberg-Sobolev lintegral bound for a smooth compactly supported function | No exponential, critical `p = 2` endpoint, completion, or sharpness |
| `eLpNorm_le_eLpNorm_fderiv_one` | The `L^1` derivative form with Holder-conjugate target exponent | Wrong derivative exponent and no endpoint exponential |
| `eLpNorm_le_eLpNorm_fderiv_of_eq` | A finite `L^p -> L^p'` bound under the Sobolev exponent equation | Requires the subcritical regime `p < dim`; at the target `p = dim = 2`, the finite exponent construction degenerates |
| `eLpNorm_le_eLpNorm_fderiv_of_le` | A bounded-support finite-`q` corollary | Still assumes `p < dim`, addresses smooth functions rather than the selected completion, and contains no `4*pi` or supercritical divergence |

`AnchorAudit.lean` elaborates all four names and runs `#print axioms`. Lean
reports only `propext`, `Classical.choice`, and `Quot.sound`; inspection of the
pinned source shows ordinary `by` proof bodies, no placeholder declaration,
and no unsafe/oracle boundary. These facts make them credible supporting
lemmas, but cannot turn them into an anchor for a different theorem.

## Repository and external audit

Repository-wide searches found only prose describing this target and the
nearby, deliberately distinct sphere and higher-dimensional targets. No local
Lean implementation was found outside the canonical statement surface.

On 2026-07-12, Sourcegraph's public global code index was queried for Lean
files, including archived repositories and forks, with `Trudinger`,
`MoserTrudinger`, and the exact string `Moser-Trudinger`. Each completed with
zero matches. This is bounded negative discovery evidence, not an assertion
that an unindexed private or future project cannot exist. Since there was no
candidate, no mutable external branch was fetched and no external proof credit
is assigned. GitHub and grep.app unauthenticated endpoints returned 403/429;
those failures are not counted as successful searches.

## Validation record

| Command | Exit | Result |
|---|---:|---|
| `lake env lean ../../Stage1_Instances/THM-M-1277/AnchorAudit.lean` (from `Formalizations/Lean`) | 0 | All four pinned declarations elaborated; each axiom report was exactly `[propext, Classical.choice, Quot.sound]` |
| `lake env lean ../../Stage1_Instances/THM-M-1277/Statement.lean` (from `Formalizations/Lean`) | 0 | Canonical target still elaborated as `Stage1Rev56.THMM1277.Statement : Prop` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | Returned the audited immutable revision |
| `python3 -m json.tool Stage1_Instances/THM-M-1277/anchor-audit.json` | 0 | Structured audit receipt is valid JSON |
| `rg -n 'sorry\\b|^\\s*axiom\\b|^\\s*unsafe\\b' Stage1_Instances/THM-M-1277/AnchorAudit.lean` | 1 | No forbidden Lean constructs; `rg` exit 1 means no match |
| `git diff --check -- Stage1_Instances/THM-M-1277 .stage1-worker-selftest.json` | 0 | No whitespace errors |

This audit is node-local evidence only. It does not prove the theorem or
authorize a checklist transition; only the master lane can accept the node.
