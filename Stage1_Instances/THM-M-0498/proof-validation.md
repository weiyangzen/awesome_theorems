# THM-M-0498 proof attempt

Item: `S56-M-0498-PROOF`  
Date: `2026-07-12`  
Base revision: `b781ef440e9de69e6413b608ce5542eed8c0070e`

## Verdict

`blocked`: the exact Riemann-von Mangoldt weighted-psi formula has no eligible
proof body in the repository or pinned mathlib closure. The existing theorem
`root_of_analytic_package` checks only the conditional implication from
`AnalyticExplicitFormulaPackage` to the canonical target. No declaration
inhabits that package.

The minimal open root cut is `M0498-T-ANALYTIC`. Closing it requires the frozen
Perron, contour, residue, trivial-zero, and ordered zero-sum obligations. The
historical file merely projects a desired equality supplied as data, and the
audited external finite-height formula is non-exact and incomplete. Neither is
a legal proof body. No weaker theorem was substituted and no assumption,
placeholder, or unsafe proof device was introduced.

Because this proof phase is not complete, this attempt deliberately leaves no
`.stage1-worker-selftest.json`.

## Narrow validation evidence

Commands ran inside the worker clone on 2026-07-12. The pre-existing untracked
`Formalizations/Lean/.lake` link points at canonical pinned artifacts and was
not modified. No Lake update/build, dependency clone/fetch, or other dependency
mutation was run.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Passed 15 assurance groups and 1546 uniform-L0 targets. |
| `python3 scripts/stage1_target.py check` | 0 | Passed 1546 unique targets at ranks 1 through 1546, all L0/rework-required. |
| `python3 scripts/stage1_target.py show THM-M-0498` | 0 | Confirmed rank 258, planned lifecycle, hard-mathlib-anchor lane, and theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0498/check_obligation_tree.py` | 0 | Passed 15 obligations and 33 typed edges; root remains open at M4 with `M0498-T-ANALYTIC` open. |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0498/Statement.lean` | 0 | Exact canonical target and definitional expanded transport elaborated with pinned Lean 4.29.0. |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0498/AnchorAudit.lean` | 0 | Nine supporting pinned mathlib declarations elaborated; none is terminal for the root. |
| `rg -n '^\\s*(sorry\|admit\|axiom)(\\s\|$)' Stage1_Instances/THM-M-0498 --glob '*.lean'` | 1 | No prohibited Lean declaration token found; exit 1 means no match. |
| `rg -n -i 'Riemann.?von.?Mangoldt\|RiemannVonMangoldtTarget\|nontrivial zeta zero\|zeroPartialSum\|explicit formula.{0,100}(prime\|psi\|zeta\|zero)' Stage1_Instances Formalizations/Lean/AwesomeTheorems Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'` | 0 | Matches were the dossier, historical conditional/data-packaging artifact, and adjacent metadata; no terminal exact proof declaration was found in pinned mathlib. |

The available Lean executable reports version `4.29.0`, commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`; installed mathlib is exactly
`8a178386ffc0f5fef0b77738bb5449d50efeea95`.

## Required unblock condition

Supply placeholder-free bodies at the frozen types for the analytic package
and its Perron, contour, residue, correction-term, and zero-sum dependencies,
or pin a compatible immutable dependency containing those bodies. Only after
exact-type, composition, transitive trust, and provenance checks pass can this
proof item receive `[_]`. The root remains `[H3, M4, R4]` and the theorem is
not complete.
