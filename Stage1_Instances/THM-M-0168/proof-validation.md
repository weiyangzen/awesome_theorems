# THM-M-0168 proof-phase attempt

Item: `S56-M-0168-PROOF`  
Date: `2026-07-12` (`Asia/Shanghai`)  
Base revision: `d41c33c7ad196cf30c996231fabd214f4d9f5248`

## Verdict

`blocked`: the exact Bernstein minimal-graph theorem is not closed by any
eligible proof body in the repository or pinned mathlib closure. The first
substantive unavailable package is `M0168-C-GRAPH`, followed by the
PDE-to-minimality, stability, logarithmic-cutoff, curvature-vanishing, and
derivative-rigidity packages. Together these packages must prove
`M0168-L-DERIVATIVE-RIGIDITY`; no inhabitant of the frozen
`DerivativeRigidity` proposition is available.

`Proof.lean` does add a real placeholder-free proof of the independent
calculus package `M0168-T-INTEGRATE`. The theorem
`constantPartials_to_affine` reconstructs the full Frechet derivative from
the two coordinate directions, compares it with an explicit affine function,
and applies mathlib's connected-domain mean-value theorem. The wrapper
`bernstein_of_derivativeRigidity` therefore leaves exactly
`DerivativeRigidity` as a premise. It does not assert or weaken the missing
geometric theorem and supplies no root-completion credit.

Root debt remains `M2`, `root_closed=false`, and `theorem_complete=false`.
Because the assigned proof phase is incomplete,
`.stage1-worker-selftest.json` is deliberately absent.

## Narrow validation evidence

All commands ran in this worker clone and reused the canonical pinned Lake
artifacts. No `lake update`, `lake build`, dependency clone/fetch, or `.lake`
mutation was performed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0168` | 0 | rank 665; planned; hard-statement-first partial-verification lane; theorem incomplete |
| `python3 Stage1_Instances/THM-M-0168/check_obligation_tree.py` | 0 | 11 nodes, typed acyclic proof graph, frozen open root |
| compile `Statement.lean` and `ObligationTree.lean` to temporary local oleans, then run `Proof.lean` with `lake env lean` and the pinned `LEAN_PATH`; remove both oleans | 0 | local integration body and conditional root wrapper elaborated; both axiom reports were exactly `propext`, `Classical.choice`, and `Quot.sound` |
| `rg -n -i 'Bernstein.*minimal\|minimal.*Bernstein\|SatisfiesMinimalSurfaceEquation\|DerivativeRigidity' --glob '*.lean' Stage1_Instances Formalizations/Lean/AwesomeTheorems Formalizations/Lean/.lake/packages/mathlib/Mathlib` | 0 | all exact predicate and rigidity hits were confined to this dossier; no terminal Bernstein body was found in the pinned closure |
| `rg -n '^\s*(sorry\|admit\|axiom)(\s\|$)\|native_decide' Stage1_Instances/THM-M-0168/Proof.lean` | 1 | expected no-match result: no forbidden proof-gap, custom-axiom, or oracle token |
| `git diff --check -- Stage1_Instances/THM-M-0168 .stage1-worker-selftest.json` | 0 | no whitespace errors |

Toolchain evidence: Lean `4.29.0`, commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`; pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. SHA-256:

- `Statement.lean`: `5e773260e93f29c5da263e749b8bd5208a7b61e344d45b588ad9cda65d311a78`
- `ObligationTree.lean`: `642153a1f88af5d71a954b417b136fd95d1eaf82b8d1fdf176d60b3ace3bf24e`
- `Proof.lean`: `2906d501962f5d41c4c6c12a1f68f13a1f1857f244eff00769c97ab282d8299d`
- `obligation-registry.json`: `883e0c0a98c6d3b6e5e77adb9c5fb376c87f043dd7b80b4e882cbdb0045ed9ba`

## Reopen condition

Resume after either a placeholder-free implementation of the frozen graph,
minimality, stability, cutoff, curvature, and rigidity packages, or discovery
of an immutable compatible Lean 4 proof that can be pinned, exact-type
transported, and checked in the repository closure.
