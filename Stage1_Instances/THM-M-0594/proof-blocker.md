# THM-M-0594 proof-phase blocker

Item: `S56-M-0594-PROOF`. Attempt date: 2026-07-12. Worker base
revision: `47d9662b1dbcf58d16808c52127e54b6fadb444c`.

## Verdict

The assigned proof phase is blocked and is not self-tested as complete. No
worker self-test receipt is issued.

The frozen root is the unrestricted existence theorem for every Hausdorff,
second-countable, boundaryless finite-dimensional smooth real manifold. The
only terminal proof in the pinned Lean closure is
`exists_embedding_euclidean_of_compact`, which has the additional typeclass
hypothesis `[CompactSpace M]`. `AnchorAudit.lean` checks this specialization
and its transport to `IsEmbedding`; it cannot discharge the unrestricted
root because the missing compactness instance cannot be derived from the
frozen assumptions.

At pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, the header of
`Mathlib/Geometry/Manifold/WhitneyEmbedding.lean` explicitly lists the
sigma-compact weak Whitney embedding theorem as future work. The theorem
requires a Sard/Hausdorff-dimension result not present in that module. The
frozen obligation registry therefore truthfully leaves the noncompact
exhaustion, global construction, properness, point-separation, and
topological bridge nodes open at M4, and leaves the root open at M3.

`ObligationTree.lean` contains a kernel-checked constructor from an already
supplied smooth embedding witness. This is composition evidence only: it
does not construct the witness and is not a proof of the root. Adding
compactness, restricting the theorem to compact manifolds, or treating this
conditional constructor as closure would broaden or substitute the assigned
theorem and is therefore rejected.

## Smallest real validation

The existing pinned Lake artifacts were used read-only. No Lake update,
build, fetch, clone, or dependency mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `15` assurance groups and `1546` uniform-L0 targets agree |
| `python3 scripts/stage1_target.py check` | 0 | `1546` unique targets, ranks `1..1546`, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0594` | 0 | Rank 255, planned, theorem incomplete |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0594/Statement.lean` | 0 | The exact unrestricted target elaborated |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0594/AnchorAudit.lean` | 0 | Compact specialization elaborated; axioms are `[propext, Classical.choice, Quot.sound]` |
| `cd Formalizations/Lean && lake env lean -R ../../Stage1_Instances/THM-M-0594 -o /tmp/THM-M-0594-Statement.olean ../../Stage1_Instances/THM-M-0594/Statement.lean`; then place that temporary object at `/tmp/m0594-leanpath/Statement.olean` and run `LEAN_PATH=/tmp/m0594-leanpath lake env lean -R ../../Stage1_Instances/THM-M-0594 ../../Stage1_Instances/THM-M-0594/ObligationTree.lean` | 0 | Conditional constructor elaborated; axioms are `[propext, Classical.choice, Quot.sound]` |
| `python3 Stage1_Instances/THM-M-0594/check_obligation_tree.py` | 0 | 16 obligations and 46 typed edges pass; root remains open M3 and noncompact construction/topological bridge remain M4 |
| `rg -n '\b(sorry|admit|axiom|proof_wanted)\b' Stage1_Instances/THM-M-0594/*.lean Formalizations/Lean/.lake/packages/mathlib/Mathlib/Geometry/Manifold/WhitneyEmbedding.lean` | 1 (expected) | No prohibited proof escape in the local Lean files or pinned terminal source |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95` |

## Unblocking condition

Proof execution can resume only after implementing the frozen noncompact
obligations in Lean, including the missing Sard/Hausdorff-dimension machinery
and checked child-to-parent composition, or after identifying an immutable,
license-compatible Lean 4 proof of the exact unrestricted target and bringing
it into the pinned repository-local validation closure. A compact-only result
does not satisfy this condition.

Status boundary: this record is actionable blocker evidence for the proof
phase. It makes no proof-phase acceptance, audit-completion, validation,
release, or theorem-completion claim.
