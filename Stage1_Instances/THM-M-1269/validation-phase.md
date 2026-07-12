# THM-M-1269 validation-phase record

Item: `S56-M-1269-VALIDATION`. Base revision:
`d7953d0695a725ae8ce67787c822bae069258f8e`.

## Scope and result

The validation runner copies `Statement.lean`, `ObligationTree.lean`,
`Proof.lean`, and `Validation.lean` into a fresh temporary module directory and
elaborates them with the existing pinned Lake environment. `Validation.lean`
does not import the proof or composition module: it independently reconstructs
the exact frozen proposition from `exists_seq_tendsto_sInf`, using an explicit
choice function and convergence transport.

The run passed the narrow kernel, axiom, marker, local provenance, frozen
registry, dependency pin, and dependency cleanliness checks. The proof,
conditional composition, and differential reconstruction each reported exactly
`propext`, `Classical.choice`, and `Quot.sound`. No network or dependency
mutation was used.

## Commands and exact results

```text
python3 Stage1_Instances/THM-M-1269/check_validation.py
  exit 0
  ok: exact statement, frozen composition, proof root, and independent local reconstruction elaborated
  ok: checked declarations report only propext, Classical.choice, and Quot.sound
  ok: placeholder/unsafe scan, proof provenance, frozen hashes, denominator, and clean pinned mathlib checks passed
  stale: the frozen pre-proof graph still reports root_closed=false with M1269-L-SINF as its cut
  blocked: cold empty-cache hermetic replay, complete TCB/SBOM closure, and distinct-runner independent verification

python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required

python3 scripts/stage1_target.py show THM-M-1269
  exit 0: rank 445, planned lifecycle, theorem_complete=false

git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD
  exit 0: 8a178386ffc0f5fef0b77738bb5449d50efeea95

git -C Formalizations/Lean/.lake/packages/mathlib status --short
  exit 0: empty output

(cd Formalizations/Lean && lake env lean --version)
  exit 0: Lean 4.29.0, commit 98dc76e3c0a9b856c9b98726b713fb04fab16740
```

## Fail-closed boundary

This is warm-cache, same-workspace provisional worker evidence. It is not the
cold empty-cache, offline, clean-snapshot replay required by section 10.6, and
the differential Lean module is not a distinct verifier identity or separately
provisioned runner under section 10.7. The frozen typed graph also predates the
proof receipt and still records an open root. Therefore the first failed gate
is `S56-10.6-HERMETIC-COLD-BUILD`; audit completion, theorem completion,
release, and master acceptance are all false.
