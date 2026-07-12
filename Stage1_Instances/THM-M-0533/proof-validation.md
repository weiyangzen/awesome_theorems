# THM-M-0533 proof-phase attempt

Item: `S56-M-0533-PROOF`  
Date: `2026-07-12` (`Asia/Shanghai`)  
Base revision: `0d96c69f4ed36252336c9f7f535191869f854cf6`

## Verdict

`blocked`; no proof body was added and no proof credit is claimed.

The exact target `AwesomeTheorems.THM_M_0533.MayerVietorisSequence` and the
existing conditional composition theorem re-elaborate in the pinned Lean
environment. The latter accepts a `ConstructionPackage` and its complete
`ExactnessPackage` as premises; it does not construct either package.

The prerequisite anchor audit and a fresh scoped source check agree that the
pinned mathlib revision supplies absolute singular chains and homology but no
singular-homology excision theorem, cover-small-chain quasi-isomorphism,
relative singular homology, or singular Mayer-Vietoris theorem. The available
Mayer-Vietoris declarations are for sheaf cohomology and cannot be transported
to this covariant singular-homology target. The first unavailable frozen leaf
is therefore `M0533-C-SUBDIVISION`.

The immediate semantic root cut remains `M0533-T-CONSTRUCTION`, the three
recurring exactness positions, and `M0533-T-DEGREE-ZERO`. Introducing these as
axioms or assumptions would be a placeholder; using the sheaf theorem would
substitute a different theorem. The root consequently remains open at `M3`,
and `.stage1-worker-selftest.json` is deliberately absent because the assigned
proof deliverable is not complete.

## Narrow validation evidence

All checks ran in this worker clone using the existing pinned Lake artifacts.
No `lake update`, `lake build`, dependency clone/fetch, or `.lake` mutation was
performed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0533` | 0 | rank 590; planned; L0/rework-required; theorem incomplete |
| `python3 Stage1_Instances/THM-M-0533/check_obligation_tree.py` | 0 | 19 obligations and 37 typed edges passed; denominator `238242df...8dfc`; root open M3 |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0533/Statement.lean` | 0 | exact target elaborated and printed as `Prop`; three mutation-fixture unused-variable warnings |
| compile `Statement.lean` to a temporary local `Statement.olean`, then elaborate `ObligationTree.lean` with `lake env which lean` and `lake env printenv LEAN_PATH`; remove the temporary artifacts | 0 | conditional composition elaborated; `#print axioms` reported exactly `propext`, `Classical.choice`, and `Quot.sound` |
| `rg -n -i 'mayer.?vietoris\|mayerVietoris\|excision\|subdivision\|small.*chain\|relativeSingular' Formalizations/Lean/.lake/packages/mathlib/Mathlib/AlgebraicTopology Formalizations/Lean/.lake/packages/mathlib/Mathlib` | 0 | Mayer-Vietoris hits were sheaf/site cohomology only; no singular-homology terminal proof or required chain/excision package was found |
| forbidden-token scan of the target's Lean files | 1 | expected no-match result; no `sorry`, `admit`, `sorryAx`, bodyless `axiom`/`constant`, or `unsafe` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release |
| `sha256sum Stage1_Instances/THM-M-0533/{Statement.lean,ObligationTree.lean,obligation-registry.json}` | 0 | `cbe35890...18bce`; `ded027e2...3b1`; `cd0411fc...b630` |

## Reopen condition

Resume after implementing the frozen subdivision, small-chain, signed chain
sequence, boundary, naturality, and exactness packages without placeholders,
or after locating an immutable exact Lean 4 proof whose terminal bodies,
dependencies, trust closure, and exact-type transport validate in the pinned
environment.
