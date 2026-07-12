# THM-M-1018 proof-phase blocker

Item: `S56-M-1018-PROOF`  
Attempt date: 2026-07-12  
Base revision: `4344dc4263d0bcc8c386ec0ae1ad4e508c910b1e`

## Result

The proof phase is blocked and is not self-tested as complete. No unconditional Lean proof body for
`Stage1Instances.THM_M_1018.LevyInversionTarget` was added, and this artifact makes no theorem,
audit, release, or master-acceptance claim. The existing `root_compose` theorem only returns an
explicit analytic premise and therefore cannot close the root.

The exact remaining root cut is `M1018-T-ANALYTIC`. The pinned mathlib revision contains useful
characteristic-function/Fubini infrastructure, notably `integral_charFun_Icc`, but no Levy inversion
declaration for interval mass. A focused source scan also found no Dirichlet sine-integral limit
that could discharge `M1018-L-DIRICHLET`. Consequently there is neither a proof body that can be
wrapped nor an immutable external dependency already present in the clone that can be pinned and
checked. Fetching a moving dependency is forbidden for this worker.

Closing the phase requires new formalization of the frozen analytic route: the endpoint kernel
construction and Fubini identity, translation/scaling, the Dirichlet sine-integral limits, passage
of their pointwise limit through an arbitrary probability measure, and the atom-free endpoint mass
identity. These are the open obligations `M1018-C-APPROX`, `M1018-N-FUBINI`, `M1018-N-SCALE`,
`M1018-L-DIRICHLET`, `M1018-L-INTEGRAL-LIMIT`, `M1018-B-POSITION`, and
`M1018-L-ENDPOINTS`, composing into `M1018-T-ANALYTIC`.

No `sorry`, axiom, placeholder declaration, weakened theorem, or substituted Fourier/density
inversion result was introduced. Per the worker contract, `.stage1-worker-selftest.json` is absent.

## Validation evidence

Commands ran in the worker clone on 2026-07-12. The Lean commands used the existing canonical
pinned `.lake` artifacts and did not mutate dependencies.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok` for 15 assurance groups and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique ordered targets passed |
| `python3 scripts/stage1_target.py show THM-M-1018` | 0 | rank 494; lane `hard_mathlib_anchor_and_wrapper`; lifecycle `planned`; theorem incomplete |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the recorded mathlib pin |
| `lake env lean ../../Stage1_Instances/THM-M-1018/Statement.lean` from `Formalizations/Lean` | 0 | exact frozen target and checked transport elaborated |
| `lake env lean ../../Stage1_Instances/THM-M-1018/ObligationTree.lean` from `Formalizations/Lean` | 0 | conditional composition elaborated; reported axioms `[propext, Classical.choice, Quot.sound]` |
| `rg -ni --glob '*.lean' 'levy.*inversion\|lévy.*inversion\|inversion.*levy\|charFun.*Ioc\|Ioc.*charFun' Formalizations/Lean/.lake/packages/mathlib/Mathlib` | 1 | expected no-match result; no exact pinned mathlib anchor found |
| `rg -ni --glob '*.lean' 'dirichlet.*integral\|integral.*sin.*/\|integral.*sin.*inv\|sin.*integral.*pi\|tendsto.*sinc\|integral_sinc\|sinc.*integral' Formalizations/Lean/.lake/packages/mathlib/Mathlib` | 0 | only unrelated/noise matches; no Dirichlet sine-integral limit declaration found |

The combined exploratory shell command containing both `rg` scans exited 1 because the final exact
anchor scan intentionally had no matches; all preflight commands preceding it exited 0. The
pre-existing untracked `Formalizations/Lean/.lake` worker link/artifact was observed and not changed.

