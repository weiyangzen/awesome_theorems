# THM-M-0605 proof phase: blocked at base 9bce865a

Item: `S56-M-0605-PROOF`

Intent: `prove`

Recorded: `2026-07-15T13:53:14+08:00`

Base revision: `9bce865a14bcc270344ea909d6936c6ea22aa1c2`

Base tree: `523a9471aac257c4cf54acceee07172fab22f5b4`

Worker checkout: Stage1 rev-5.6 worker automation clone `slot63`

## Verdict

`blocked`. No placeholder-free Lean 4 proof body for the exact target
`Stage1.THM_M_0605.ExoticSevenSphereExists` is present in the repository or
the pinned dependency closure. No proof body or obligation closure was added.
The proof item stays `[ ]`, the lifecycle stays `planned`, the root vector
stays `[H1, M4, R3]`, and audit completion, root closure, validation, release,
and theorem completion remain false.

The immediate frozen root cut is `M0605-T-WITNESS`: a smooth
seven-manifold, a homeomorphism to the standard seven-sphere, and an
`IsEmpty Diffeomorph` certificate. The first unavailable construction is
`M0605-C-BUNDLE`, the selected Milnor 3-sphere bundle over the 4-sphere with
its clutching and characteristic data. The downstream total-space,
homotopy-sphere, topological-identification, bounding-manifold,
smooth-obstruction, standard-comparison, nondiffeomorphism, and witness
packages also remain open.

The checked theorem `exoticSevenSphereExists_of_witness` is only the frozen
child-to-parent composition: it consumes the complete witness package and
constructs none of it. The anchor theorem transports only the exact statement
shape. A fresh trust-zero probe rejects the standard-sphere shortcut:
`Diffeomorph.refl` inhabits the standard sphere's self-diffeomorphism type, so
that type cannot be `IsEmpty`. Providing a different atlas together with the
emptiness certificate is precisely the missing exotic-smooth-structure
theorem. Assuming a witness component or returning only the conditional
composer would be a placeholder or substituted theorem and was not done.

Pinned mathlib contains the matching signature only as
`proof_wanted exists_homeomorph_isEmpty_diffeomorph_sphere_seven` in
`Mathlib.Geometry.Manifold.PoincareConjecture`. Batteries elaborates this
command inside `withoutModifyingEnv`; the temporary helper axiom is discarded.
The trust-zero probe reports the name as unknown. Scoped searches found no
retained proof-bearing Milnor-sphere, clutching, homotopy-sphere,
Eells-Kuiper, Kervaire-Milnor, or equivalent declaration. Mathlib's bordism
module explicitly leaves actual bordisms and bordism groups as future work,
so it cannot supply the frozen smooth-obstruction branch.

Since the preceding recheck at base `57d8d017`, only that blocker packet was
added under this target. The statement, conditional composition, registry,
typed graphs, audit, validation specifications, target manifest, toolchain,
and dependency manifest are byte-identical. Their hashes are bound in the
paired JSON record, so the mathematical blocker persists at this base.

## Validation

All commands ran in this worker clone. The automation-provided untracked
`Formalizations/Lean/.lake` symlink was treated as read-only. No `lake update`,
`lake build`, dependency clone/fetch, checkout repair, network request, or
dependency mutation was performed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets at ranks 1 through 1546 passed. |
| `python3 scripts/stage1_target.py show THM-M-0605` | 0 | Rank 643; planned; L0/rework-required; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0605/check_anchor_audit.py` | 0 | Exact marker, dependency pins, discard semantics, and the M4 boundary passed. |
| `python3 Stage1_Instances/THM-M-0605/check_obligation_tree.py` | 0 | 19 obligations and 90 typed edges passed; denominator `c6e29bccc0135529afc98b27c38f6c5265449f1fd054602ec55fe9d9e5b6e5b7`; root remains open M4. |
| `cd Formalizations/Lean && lake env lean --trust=0 -t0 ../../Stage1_Instances/THM-M-0605/Statement.lean` | 1 | Failed before Lean because the shared manifest-pinned `flt-regular` checkout cannot resolve `HEAD`; no repair or fetch was attempted. |
| direct pinned-Lean trust-zero replay | 0 | `Statement.lean`, `ObligationTree.lean`, and `AnchorAudit.lean` elaborated from existing read-only artifacts; statement output was 15602 bytes and composer axioms were exactly `propext`, `Classical.choice`, and `Quot.sound`. This is narrow nonrelease fallback evidence. |
| trust-zero standard-sphere/name probe | 0 | `Diffeomorph.refl` refuted emptiness for the standard witness with only the three expected axioms; the discarded marker was unknown. |
| scoped retained-body search | 0 | 31 hits in 11 relevant Lean files were duplicate or conditional statements, metadata/audit material, or the discarded marker; no eligible terminal body was found. |
| pinned construction-package search | 1 | Expected no-match exit: no retained clutching, homotopy-sphere, Milnor-sphere, Eells-Kuiper, or Kervaire-Milnor package was found. |
| pinned nondiffeomorphism-signature search | 0 | The only matching signatures were the discarded exotic-seven-sphere and exotic-R4 `proof_wanted` targets. |
| prohibited-device scan of the checked Lean surface | 1 | Expected no-match exit: no `sorry`, `admit`, `sorryAx`, bodyless declaration, unsafe theorem, or equivalent proof device was found. |
| scoped diff from base `57d8d017` | 0 | No proof input, pin, or target-manifest input changed; only the preceding blocker packet was added under this target. |

The direct fallback copied the three checked files to a fresh `mktemp`
directory, assembled `LEAN_PATH` from existing root/package
`.lake/build/lib/lean` directories, and ran the pinned Lean 4.29.0 executable
(SHA-256
`3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf`)
with `LEAN_NUM_THREADS=1`, a 600-second timeout, `--trust=0`, `-t0`, and `-R`.
The disposable directory was removed after the replay.

The successful loophole/name probe imported the same pinned Poincare module
and used this disposable source under the same trust-zero recipe:

```lean
theorem standardSphereSelfDiffeomorphNotEmpty : ¬ IsEmpty
    (sphere (0 : EuclideanSpace ℝ (Fin (7 + 1))) 1
      ≃ₘ⟮𝓘(ℝ, EuclideanSpace ℝ (Fin 7)),
        𝓘(ℝ, EuclideanSpace ℝ (Fin 7))⟯
      sphere (0 : EuclideanSpace ℝ (Fin (7 + 1))) 1) := by
  intro h
  exact h.false
    (Diffeomorph.refl 𝓘(ℝ, EuclideanSpace ℝ (Fin 7))
      (sphere (0 : EuclideanSpace ℝ (Fin (7 + 1))) 1) ∞)

#print axioms standardSphereSelfDiffeomorphNotEmpty
#check_failure exists_homeomorph_isEmpty_diffeomorph_sphere_seven
```

## Retry condition

Provide placeholder-free implementations of the frozen Milnor bundle and all
dependent topological and smooth-obstruction packages. Alternatively,
integrate an immutable compatible Lean 4 proof-bearing declaration of the
exact target with complete dependency and license evidence. The cache-owning
lane must also restore the already manifest-pinned `flt-regular` checkout
before the prescribed `lake env` checks can replay.

This is current-base blocker evidence, not a proof receipt. It does not
satisfy `S56-M-0605-PROOF`, promote scheduler state, close an obligation, or
support audit or theorem completion. Because the assigned phase is not
genuinely self-tested as complete, `.stage1-worker-selftest.json` remains
absent.
