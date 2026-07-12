# THM-M-0510 proof-phase attempt

Item: `S56-M-0510-PROOF`  
Date: `2026-07-12` (`Asia/Shanghai`)  
Base revision: `e3d0fd205c9c81486cb86f68cdc66d4d4e5bb264`

## Verdict

`blocked`; no proof body was added and no proof credit is claimed.

The exact target
`Stage1Instances.THM_M_0510.HardyRamanujanAsymptoticTarget` re-elaborates in the pinned Lean
environment. The existing checked bodies prove only definitional statement transport, the value of
the comparison term at zero, and the conditional identity transport
`root_of_finalAsymptotic`. The last declaration requires `FinalAsymptoticPackage`, which is itself
definitionally the canonical target, so it supplies no inhabitant and closes no analytic package.

The first unavailable frozen body is `M0510-N-EULER-PRODUCT`. Pinned mathlib supplies a general
weighted partition generating function, but its `Partition/GenFun.lean` module explicitly marks
the specialization to the ordinary partition function as TODO. A broader pinned-source search
found Dedekind eta definitions and unrelated transformation infrastructure, but no
Hardy-Ramanujan asymptotic declaration, analytic circle-method package, or eligible terminal proof.
The prerequisite anchor audit likewise located no immutable compatible external proof to pin.

Consequently the coefficient and contour reductions, arc split, modular local estimate, exact
major-arc integral and asymptotic, minor-arc bound, and final recombination all remain open. The
frozen root cut also retains source and foundation gates. Introducing any missing package as an
axiom or premise would be a placeholder, while returning the existing conditional transport would
substitute a weaker theorem. Root debt remains `M3`, `root_closed=false`, and
`theorem_complete=false`. Because the assigned proof phase is incomplete,
`.stage1-worker-selftest.json` is deliberately absent.

## Narrow validation evidence

All commands ran in this worker clone and reused the existing pinned Lake artifacts. No
`lake update`, `lake build`, dependency clone/fetch, or intentional `.lake` mutation was performed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0510` | 0 | rank 884; planned; L0/rework-required; theorem incomplete |
| `python3 Stage1_Instances/THM-M-0510/check_obligation_tree.py` | 0 | 17 obligations and 59 typed edges passed; denominator `59e9147c...167dd`; root open at M3 |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0510/Statement.lean` | 0 | exact canonical target elaborated and its explicit expression printed |
| Lake-selected `lean` compiling a temporary local `Statement.olean`, then `ObligationTree.lean`, followed by removal of the temporary olean | 0 | conditional transport elaborated; axiom report was `propext`, `Classical.choice`, and `Quot.sound` |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| Pinned mathlib `rg` search for Hardy-Ramanujan, partition asymptotics, circle-method arcs, Dedekind eta, and modular transformations | 0 | no Hardy-Ramanujan or analytic major/minor-arc proof; Dedekind eta infrastructure and the unrelated Katona circle method were the relevant broad-name hits |
| `rg -n -i 'partition|TODO' .../Partition/GenFun.lean` | 0 | module documentation says ordinary partition-function specialization is TODO |
| placeholder scan over owned Lean files | 1 | empty output: no `sorry`, `admit`, `axiom`, or `unsafe` declaration |
| `sha256sum` on statement, obligation tree, registry, and anchor audit | 0 | `2bdbd944...d049`; `d75993a5...982b`; `678c2652...36b2`; `ec5b4e09...0c6c2` |

## Reopen condition

Resume only after a placeholder-free implementation of the frozen analytic packages, or discovery
of an immutable compatible Lean 4 proof that can be pinned, exact-type transported, and validated
inside the repository closure.
