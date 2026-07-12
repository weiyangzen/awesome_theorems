# THM-M-1063 proof-phase attempt

Item: `S56-M-1063-PROOF`  
Attempt date: `2026-07-12` (`Asia/Shanghai`)  
Base revision: `7947d9e5d8986f9781776dbcebf381a3c9c000c5`

## Verdict

`blocked`; no proof body was added and no proof credit is claimed.

The exact target in `DonskerTarget.lean` and the frozen architecture in
`ObligationTree.lean` both re-elaborate in the pinned Lean environment. The only checked theorem
in the architecture is `exactRoot_of_exactRoot`; it accepts the complete Donsker proposition as a
hypothesis and returns it unchanged. It therefore supplies an exact-type interface, not an
inhabitant of the target.

The pinned mathlib tree contains useful general substrate: scalar central limit theorems,
Prokhorov compactness, Levy-Prokhorov convergence, tight measures, and Gaussian-process
definitions. The scoped source search found no Donsker or functional central limit theorem. The
prerequisite immutable anchor audit also found no compatible external terminal body. In
particular, none of the available declarations proves tightness of the polygonal path laws under
only the frozen finite-second-moment hypotheses or identifies every continuous-path subsequential
limit with the specified Brownian law.

The first unavailable proof package on the selected route is `M1063-C-PATH`: the pinned closure
has no construction theorem packaging the frozen floor-based interpolation as a continuous path.
The substantive convergence cut then remains the weighted triangular-array CLT
(`M1063-L-CLT`), finite-second-moment modulus estimate (`M1063-L-MODULUS`), compact containment
(`M1063-L-ASCOLI`), Prokhorov extraction specialized to these laws (`M1063-L-PROKHOROV`),
continuous Brownian-law uniqueness (`M1063-L-LAW-UNIQUE`), and final distribution API transport
(`M1063-T-API`). Introducing any package as an axiom or premise, assuming tightness or Donsker's
theorem, requiring stronger moments, or proving only scalar convergence would violate the frozen
target.

Consequently all 29 machine-required obligations remain without terminal proof-body IDs, the root
remains open at `M4`, and `theorem_complete=false`. Because the assigned proof deliverable is not
self-tested as complete, `.stage1-worker-selftest.json` is deliberately absent.

## Narrow validation evidence

All commands ran in this worker clone using the existing pinned Lake artifacts. No `lake update`,
`lake build`, dependency clone/fetch, or `.lake` mutation was performed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Stage1_Instances/THM-M-1063/check_obligation_tree.py` | 0 | 31 obligations and 125 typed edges passed; denominator `a55c3e2...26a7703`; root open `M4` |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1063/DonskerTarget.lean` | 0 | exact target and definitional expansion elaborated; printed `DonskerInvariancePrinciple : Prop` |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1063/ObligationTree.lean` | 0 | exact-root identity interface elaborated; its displayed input and output are both the complete open target |
| `rg -n -i '\\b(donsker|functional[ _-]+central[ _-]+limit|invariance[ _-]+principle|prokhorov|tightness)\\b' Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'` | 0 | only Prokhorov, Levy-Prokhorov, and generic tightness substrate matched; no Donsker or functional-CLT declaration |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release |
| `sha256sum Stage1_Instances/THM-M-1063/{DonskerTarget.lean,ObligationTree.lean,obligation-registry.json,typed-graphs.json}` | 0 | `de889c4...a1847`, `047c49f...1425`, `7886d9c...d5e8`, `e63f2ce...75b5` |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1,546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1,546 unique targets, ranks 1 through 1,546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1063` | 0 | rank 506; planned; L0/rework-required; theorem incomplete |

## Reopen condition

Resume after implementing the frozen path construction, finite-dimensional convergence,
finite-second-moment tightness, limit identification, and API composition packages without
placeholders, or after locating an immutable compatible Lean 4 Donsker proof whose exact type,
terminal bodies, dependencies, axioms, license, and provenance can be validated in the pinned
environment.
