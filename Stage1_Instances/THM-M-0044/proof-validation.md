# THM-M-0044 proof-phase validation

Item: `S56-M-0044-PROOF`. Base revision `c5f6fb269f6eb84efa935ee66c4e9bab92495e61`
(tree `7a41063c920c1b9cb849aa35c2f02ec4a4733655`).

## Implemented proof

`Proof.lean` proves the exact `SingularValueDecompositionTarget`, hence full rectangular SVD for
every Real and Complex matrix, including empty dimensions. For a tall matrix, it diagonalizes the
Gram map `L.adjoint.comp L`, normalizes the nonzero images of its orthonormal eigenbasis, extends
them to a full left orthonormal basis, converts both bases to unitary matrices, and verifies the
explicit dependent rectangular diagonal and entrywise matrix equality. For a wide matrix it
applies the tall construction to the conjugate transpose and reverses the factorization.

This is a repository-local proof body over pinned mathlib. It contains no `sorry`, `admit`, custom
axiom, `sorryAx`, unsafe or opaque declaration, native oracle, external implementation, numerical
experiment, or changed statement. Lean reports exactly `propext`, `Classical.choice`, and
`Quot.sound` for the exact root declaration.

## Commands and results

Validation used the automation-provided canonical `.lake` symlink read-only. No `lake update`,
`lake build`, dependency clone/fetch, or `.lake` mutation ran.

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and 1546 uniform-L0 targets passed

python3 scripts/stage1_target.py check
  exit 0: 1546 unique ordered targets passed

python3 scripts/stage1_target.py show THM-M-0044
  exit 0: rank 1084, planned, theorem_complete false

cd Formalizations/Lean && bash ../../Stage1_Instances/THM-M-0044/check_proof.sh
  exit 0: isolated Statement and ObligationTree oleans built outside the repository; Proof.lean
  elaborated; the root axiom report was [propext, Classical.choice, Quot.sound]

python3 -B Stage1_Instances/THM-M-0044/check_proof.py
  exit 0: exact source, frozen inputs, DAG identity, receipt, dependency pin, hygiene, and worker
  packet passed; authoritative root state unchanged

rg -n prohibited-pattern Stage1_Instances/THM-M-0044/Proof.lean
  exit 1 as expected: no prohibited proof constructs found

git diff --check -- Stage1_Instances/THM-M-0044 .stage1-worker-selftest.json
  exit 0: no tracked whitespace diagnostics
```

Pinned environment: Lean 4.29.0 commit `98dc76e3...fab16740`, mathlib
`8a178386...ea95` (tree `bdc39a31...c2b`). `Proof.lean` SHA-256 is
`aed09e85710bdfd9527a25881fcdf147f757b2c268531d05dd0e800a7a4060bc`.

## Status boundary

This is provisional proof-node evidence. It proposes kernel closure of the exact root only after
dependency-ordered master acceptance. Validation, release, primary-source H0, independently
reviewed R0, full transitive provenance/trust, hermetic cold replay, independent verification, and
deterministic release evidence remain open. Neither audit completion nor theorem completion is
claimed by this worker.
