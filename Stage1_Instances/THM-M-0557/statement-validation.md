# Statement validation record

Item: `S56-M-0557-STATEMENT`  
Base revision: `bdfc69baefbe6cfce9a205be72f3d46cb31458e8`

## Frozen target

`Stage1Instances.THM_M_0557.HomotopyGroupStructureTarget` freezes the construction claim selected
from the intake family: every `pi_(n+1)` of a pointed topological space has a group structure, and
every `pi_(n+2)` has a commutative group structure. Its sole direct import is
`Mathlib.Topology.Homotopy.HomotopyGroup`. The pinned encoding is the quotient of generalized cube
loops relative to their boundary. Sphere-map and iterated-loop presentations receive no unchecked
transport credit.

The exact expression uses `Nonempty (Group ...)` and `Nonempty (CommGroup ...)` so the proposition
asserts existence of the structures while retaining the concrete mathlib carrier. It adds no
connectedness or separation hypothesis. The historical source locator remains at `H1`; this node
does not claim source acceptance or theorem completion.

## Commands and results

All commands ran in this worker clone. Lean commands used the existing pinned Lake environment from
`Formalizations/Lean`; no dependency operation was run and `.lake` was not intentionally mutated.

| Command | Exit | Result |
|---|---:|---|
| `lake env lean ../../Stage1_Instances/THM-M-0557/Statement.lean` | 0 | target, four mutations, and dimension-one/two boundary witnesses elaborated; explicit expression printed |
| `python3 ../../Stage1_Instances/THM-M-0557/check_statement.py` | 0 | expression SHA-256 `c194bd11441b036272cf4faff6e11fdcf62c833b4ba822276ffb2b0061845e70`; all mutations distinguished |
| `lake env lean --version` (from `Formalizations/Lean`) | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `sha256sum Stage1_Instances/THM-M-0557/Statement.lean Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | hashes `1ec079...4fa`, `651c8a...1d2`, and `321626...d81` |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0557` | 0 | rank 605, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |

An accidental root-directory invocation of `lake env lean --version` exited nonzero because no
default Elan toolchain is configured; the prescribed invocation from `Formalizations/Lean` succeeds
and is the pinned evidence above.

## Mutation and boundary policy

The validator rejects extending group structure to dimension zero, extending commutativity to
dimension one, specializing the family to dimension two, and replacing the universal pointed
basepoint with an existential one. Kernel-checked witnesses exercise the first admitted group and
commutative-group dimensions. This is statement-only evidence pending master acceptance.
