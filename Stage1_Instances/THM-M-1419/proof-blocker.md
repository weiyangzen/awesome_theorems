# Proof-phase blocker

Item: `S56-M-1419-PROOF`  
Theorem: `THM-M-1419`  
Base revision: `bdd92f30d924027320c18f282eed9ed56478eba5`  
Attempt date: `2026-07-12`

## Verdict

The proof phase is blocked and remains open. No proof body, axiom, declaration,
placeholder, or weakened replacement theorem was added.

The exact canonical target elaborates, and the existing
`target_of_construction_package` theorem checks only the identity implication
from `OseledetsConstructionPackage`, which is definitionally the whole target.
Consequently it supplies no proof of that package. The frozen root-relevant
obligations for the Kingman/exterior-power limit, forward and backward
filtrations, measurable splitting, exact equivariance, and vector-growth limit
remain without terminal bodies in the pinned dependency closure.

The complete pinned mathlib search recorded by the accepted prerequisite audit
found neither a Kingman subadditive ergodic theorem nor an Oseledets theorem.
The only discovered substantive Lean 4 implementation is the anchor-only
external candidate
`marcmorningstar/lean4-ergodic-theory@3882faed7d0a9c332d3e7c0fb38a5f6d48f29864`.
It is not an exact statement match, is absent from this Lake closure, and uses
Lean `4.30.0-rc2` with mathlib `34f7a6cd...`, whereas this clone is pinned to
Lean `4.29.0` and mathlib `8a178386...`. Worker policy forbids fetching it or
mutating `.lake`, and no compatible prebuilt artifact is present.

The first failed gate is terminal proof-body availability for
`M1419-E-KINGMAN`, upstream of the construction package and root. A retry
requires either (1) a real local formalization of the frozen obligations, or
(2) an immutable, license-compatible, toolchain-compatible vendoring/pin of a
substantive implementation plus checked transports proving the exact canonical
target. Merely importing the currently identified external theorem would not
be sufficient because its hypotheses, cocycle, norm, measurable-subspace API,
and output indexing differ from the target.

## Validation evidence

All commands ran from the worker clone unless a subshell is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | rev-5.6 standard and 1546-target projection consistent |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all uniform L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1419` | 0 | rank 688; lifecycle planned; theorem incomplete |
| `git rev-parse HEAD` | 0 | `bdd92f30d924027320c18f282eed9ed56478eba5` |
| `(cd Formalizations/Lean && lake env lean --root=../../Stage1_Instances/THM-M-1419 -o ../../Stage1_Instances/THM-M-1419/OseledetsStatement.olean ../../Stage1_Instances/THM-M-1419/OseledetsStatement.lean)` | 0 | exact target elaborated under the pinned toolchain |
| `(cd Formalizations/Lean && LEAN_PATH="../../Stage1_Instances/THM-M-1419:$(lake env printenv LEAN_PATH)" lake env lean --root=../../Stage1_Instances/THM-M-1419 ../../Stage1_Instances/THM-M-1419/ObligationTree.lean)` | 0 | conditional wrapper checked; axiom report was `[propext, Classical.choice, Quot.sound]` |
| `rg -n -i "oseledets\|multiplicative ergodic\|lyapunov (exponent\|filtration)\|subadditive ergodic\|kingman" Formalizations/Lean/Mathlib Formalizations/Lean/.lake/packages/mathlib/Mathlib` | 1 | no terminal candidate in the available pinned source paths |

The temporary `OseledetsStatement.olean` produced for the dependent narrow
check was removed. The existing untracked `Formalizations/Lean/.lake` link or
directory was not modified by dependency update, fetch, clone, or build.

## Status boundary

This artifact is negative evidence for the assigned proof attempt, not a proof
receipt. Machine debt remains `M3`; audit completion and theorem completion are
both false. No `.stage1-worker-selftest.json` is emitted because the requested
proof phase did not pass its completion gate.
