# THM-M-1146 proof-phase attempt

Item: `S56-M-1146-PROOF`  
Date: `2026-07-14`  
Base revision: `c45f3c7090cb4adf616d45e5414985f956e807b2`

## Verdict

`blocked`: the exact Schwarz-reflection root remains open. `Proof.lean` supplies real proof bodies
for conjugation preservation and both strict off-axis branches. In particular, it proves directly
from second-derivative calculus that the real Laplacian commutes with complex conjugation, packages
that result as pointwise and setwise harmonicity theorems, and transfers harmonicity through the
piecewise definition above and below the axis.

The first unavailable analytic package is `M1146-L-GLUING`. At a point on the real axis,
`HarmonicAt` requires a `ContDiffAt Real 2` germ and a locally zero Laplacian. Continuity of the odd
reflection together with harmonicity on both strict sides does not establish this definitionally.
Pinned mathlib has only the forward theorem from harmonicity to the circle-average identity; it has
no converse mean-value, harmonic-gluing, or reflection theorem. Treating gluing as a premise would
be a conditional substitute rather than a proof of `SchwarzReflectionTarget`.

Because the assigned deliverable is incomplete, `.stage1-worker-selftest.json` is deliberately
absent. The root remains `M3`, its immediate cut remains `M1146-B-MERGE`, and theorem completion is
false.

## Implemented Bodies

`laplacian_comp_conj`, `harmonicAt_comp_conj`, and `harmonicOnNhd_comp_conj` implement
`M1146-L-CONJUGATION`. `oddReflection_harmonicOnNhd_upperPart` implements the upper branch.
`oddReflection_harmonicAt_of_mem_negative` combines symmetry, conjugate membership, output
negation, and local branch equality for the lower branch. The two local identities are also checked
ingredients for `M1146-C-REFLECTION`; its axis-continuity portion remains open.

Every printed declaration has axiom set exactly `propext`, `Classical.choice`, and `Quot.sound`.
There is no `sorryAx`, bodyless axiom, unsafe declaration, oracle, placeholder, or altered target.

## Narrow Validation

All commands ran in this worker clone against the existing canonical pinned `.lake` symlink. No
Lake update/build, dependency clone/fetch, or `.lake` mutation was performed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-1146` | 0 | Rank 351; planned; L0/rework-required; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1146/check_obligation_tree.py` | 0 | Frozen 18-obligation, 40-edge architecture passes; root open M3 and reflected package M4. |
| `TARGET=Stage1_Instances/THM-M-1146; LEAN_BIN=$(cd Formalizations/Lean && lake env which lean); LEAN_PATH_BASE=$(cd Formalizations/Lean && lake env printenv LEAN_PATH); cd "$TARGET"; cleanup() { rm -f Statement.olean ObligationTree.olean; }; trap cleanup EXIT; LEAN_PATH="$LEAN_PATH_BASE" "$LEAN_BIN" -o Statement.olean Statement.lean; LEAN_PATH=".:$LEAN_PATH_BASE" "$LEAN_BIN" -o ObligationTree.olean ObligationTree.lean; LEAN_PATH=".:$LEAN_PATH_BASE" "$LEAN_BIN" Proof.lean` | 0 | All proof bodies elaborate. `#print axioms` reports only `[propext, Classical.choice, Quot.sound]`. |
| `python3 -m json.tool Stage1_Instances/THM-M-1146/proof-blocker.json >/dev/null` | 0 | Structured blocker is valid JSON. |
| `rg -n '^\\s*(sorry|admit|axiom)(\\s|$)|sorryAx|\\bunsafe\\b' Stage1_Instances/THM-M-1146/Proof.lean` | 1 | Expected clean no-match result. |
| `git diff --check -- Stage1_Instances/THM-M-1146` | 0 | No whitespace errors. |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release. |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95`. |

Canonical target expression SHA-256:
`14336b88fd9aa11228ee9c7a86cc56a3473702bc2f8d77e266f2b4d37deef53d`.
Statement source SHA-256:
`1eed15359d2a23379ba77f1c8773588f4644b8b73f3b21fd981dc68271bdf5dd`.
Proof source SHA-256:
`31c325c832dab8fbab4eea3f820ed43c4defa9ed182842a2542fa916d759d0c4`.

## Reopen Condition

Resume after a placeholder-free axis-gluing proof and the required construction/boundary
prerequisites, or an eligible immutable Lean 4 proof that can be pinned, imported, and exact-type
checked. Until then `ReflectedHarmonicPackage` and the exact root remain unproved, downstream
validation/release are ineligible, and no theorem-completion claim is made.
