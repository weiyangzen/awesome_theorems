# THM-M-0586 proof recheck at `874745ff` (slot37)

Item: `S56-M-0586-PROOF`

Intent: `prove`

Recorded: `2026-07-15T06:49:58+08:00`

Base revision: `874745ff39044c1e45ed30a04111d3d84aa0e348`

Base tree: `6e4fd01c84ebee3b7e65ad42efcfe307b2f88fc4`

## Verdict

`blocked`. No eligible placeholder-free Lean body inhabits the exact frozen
`Stage1Instances.THMM0586.HighDimensionalPoincareTarget`. The target is the
substantive high-dimensional generalized Poincare theorem: for every `n >= 5`,
a compact Hausdorff smooth boundaryless `n`-manifold homotopy equivalent to the
unit `n`-sphere is homeomorphic to that sphere.

`highDimensionalPoincare_of_dimension_packages` kernel-checks at trust level
zero, but it consumes `DimensionFivePackage` and `StableDimensionPackage`.
Those are exactly the two missing terminal mathematical proofs. The natural
wrapper around mathlib's matching name fails with `Unknown constant` because
`ContinuousMap.HomotopyEquiv.nonempty_homeomorph_sphere` occurs only under
`proof_wanted`. The immutable external candidate already recorded by the
anchor audit proves only the dimension-zero generalized case.

Since the prior proof recheck at base `6cf20c1a`, the material owned Lean
sources, registry, graph, validation spec, dependency lock, and toolchain pin
are byte-identical. A fresh pinned-package search found only mathlib's
`proof_wanted` source marker and an unrelated local sphere-chart line, not an
h-/s-cobordism, surgery, Smale, or sphere-homeomorphism body. No premise,
axiom, placeholder, weaker theorem, changed dimension range, or moving
dependency was introduced.

The root remains `[H2, M3, R4]`; the proof item remains `[ ]`; audit and theorem
completion remain false. This file and its JSON companion are current-base
blocker evidence, not a proof receipt. Because the requested positive proof
phase is incomplete, `.stage1-worker-selftest.json` is deliberately absent.

## Split Gate

Seventeen prior tracked root-sized proof rechecks under this owned path all
record `blocked`. This exceeds the five-unresolved-tick split threshold in
rev-5.6 section 10.2, while the authoritative DAG still records zero attempts
and no children. This worker cannot edit the authoritative DAG or generated
checklist. The master must not schedule another unsplit root-sized retry.

The first failed proof gate remains terminal proof-body availability for the
minimal cut set `M0586-T-FIVE` and `M0586-T-STABLE`. The master-side split
should create dependency-legal children for the frozen open proof route:

```text
M0586-C-DISKS
M0586-C-COBORDISM
M0586-N-PUNCTURE
M0586-L-HCOB
M0586-C-GLUE
M0586-L-FIVE
M0586-L-STABLE
M0586-T-FIVE
M0586-T-STABLE
```

Resume a child only when its exact placeholder-free body can be implemented,
or an immutable license-compatible Lean 4 body can be pinned, exact-type
transported, and kernel checked. A source marker, conditional composer, or
out-of-range theorem does not satisfy this condition.

## Smallest Real Validation

All checks used the existing Lean 4.29.0 toolchain and canonical pinned Lake
artifacts. The automation-provided untracked `Formalizations/Lean/.lake`
symlink was reused read-only. No `lake update`, `lake build`, dependency
clone/fetch, network request, or `.lake` mutation was performed. Temporary
Lean sources and objects were created under `/tmp` and removed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets at ranks 1 through 1546 passed |
| `python3 scripts/stage1_target.py show THM-M-0586` | 0 | rank 117, planned, legacy artifacts unaccepted, theorem incomplete |
| `python3 Stage1_Instances/THM-M-0586/check_obligation_tree.py` | 0 | 18 obligations and 38 typed edges passed; denominator `bbeb74bb...07b3e`; root M3 and both terminal packages M4 |
| `python3 Stage1_Instances/THM-M-0586/check_anchor_audit.py` | 0 | anchor inventory, `proof_wanted` boundary, eight probes, and immutable pins passed |
| isolated temporary-olean `lake env` Lean replay of `Statement.lean` and `ObligationTree.lean` with `--trust=0 -t0` | 0 | exact statement and conditional composition elaborated; composition axioms were `[propext, Classical.choice, Quot.sound]`; stdout hashes were `13268e72...ade7` and `b5b6811e...f70`; stderr streams were empty |
| temporary trust-zero probe with three `#check_failure` commands for the Poincare marker names | 0 | all three were absent; stdout SHA-256 `21a44249...d2c2`; stderr empty |
| natural exact wrapper attempt using `ContinuousMap.HomotopyEquiv.nonempty_homeomorph_sphere` | 1 (expected) | `error(lean.unknownIdentifier): Unknown constant`; output SHA-256 `6b9dfd16...704d` |
| bounded search over pinned packages, the owned dossier, and the legacy exact slot | 0 | no terminal high-dimensional proof body found; the only relevant dependency hit is mathlib's `proof_wanted` marker |
| prohibited-construct scan over owned `*.lean` | 1 (expected) | no `sorry`, `admit`, custom axiom/constant/opaque, `sorryAx`, unsafe/oracle, extern, implementation override, or native-decision shortcut matched |
| material-delta comparison from base `6cf20c1a` | 0 | statement, composition, audit, registry, graph, validation spec, lockfile, and toolchain are unchanged |
| dependency revision/tree/status checks | 0 | mathlib `8a178386...` / `bdc39a31...`; `flt-regular` `56161b6e...` / `32c9eace...`; batteries `756e3321...` / `02666252...`; all three dependency worktrees clean |

Lean is version `4.29.0`, commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`. Exact hashes, outcomes,
the open cut, and the required split are recorded in the paired JSON. This
artifact does not satisfy `S56-M-0586-PROOF`, propose worker provisional
state, change scheduler state, or claim M0, validation, release, receipt
acceptance, audit completion, theorem completion, or master acceptance.
