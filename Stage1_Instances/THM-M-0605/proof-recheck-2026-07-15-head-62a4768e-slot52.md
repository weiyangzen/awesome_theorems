# THM-M-0605 proof phase: blocked at base 62a4768e

Item: `S56-M-0605-PROOF`

Intent: `prove`

Recorded: `2026-07-15T18:30:00+08:00`

Base revision: `62a4768eab1bedaed6d970d504e1788c021f47a9`

Base tree: `fc154c2bea683094c1a662e67edba530547f5270`

Worker checkout: Stage1 rev-5.6 automation clone `slot52`

## Verdict

`blocked`. No placeholder-free Lean 4 proof body for the frozen target
`Stage1.THM_M_0605.ExoticSevenSphereExists` is present in the repository or
the pinned dependency closure. No proof body or obligation closure was added.
The proof item stays `[ ]`, lifecycle stays `planned`, the root vector stays
`[H1, M4, R3]`, and audit completion, root closure, validation, release, and
theorem completion remain false.

The first failed gate is prerequisite exact-statement and anchor fidelity.
The frozen `SmoothSevenManifold` requires `IsManifold (mathcal-R 7) omega`,
which mathlib uses for analytic manifolds. The actual pinned mathlib
`proof_wanted` marker and the dossier's stated smooth scope require
`IsManifold (mathcal-R 7) infinity`. The new trust-zero
`probes/RegularityMismatch.lean` proves the regularity orders unequal and
checks analytic-to-smooth synthesis. The expected-negative
`probes/SmoothToAnalyticFails.lean` confirms that a smooth instance does not
synthesize the analytic field. `AnchorAudit.lean` instead compares the target
to a locally rewritten analytic shape, not the actual smooth marker.

Independently, the proof-body blocker remains. The immediate frozen root cut
is `M0605-T-WITNESS`: a particular manifold, a homeomorphism to the standard
seven-sphere, and an `IsEmpty Diffeomorph` certificate. The first unavailable
construction is `M0605-C-BUNDLE`, the selected Milnor 3-sphere bundle over the
4-sphere with its clutching and characteristic data. The downstream
total-space, homotopy-sphere, topological-identification, bounding-manifold,
smooth-obstruction, standard-comparison, nondiffeomorphism, and witness
packages also remain open. The stronger analytic target additionally needs an
analytic construction or a justified smooth-to-analytic transport.

The checked theorem `exoticSevenSphereExists_of_witness` is conditional
child-to-parent composition only: it consumes the complete witness and
constructs none of it. The new trust-zero
`probes/StandardSphereShortcut.lean` also proves that the standard sphere has
an infinity-smooth identity diffeomorphism and therefore cannot satisfy the
required `IsEmpty` certificate. Assuming any missing component or returning
only the conditional composer would be a placeholder or substituted theorem
and was not done.

Pinned mathlib contains the nearby smooth signature only as
`proof_wanted exists_homeomorph_isEmpty_diffeomorph_sphere_seven`.
`proof_wanted` discards its temporary declaration, and the retained-name probe
reports `Unknown identifier`. Scoped searches found no retained Milnor-sphere,
clutching, homotopy-sphere, Eells-Kuiper, Kervaire-Milnor, or equivalent proof
package. Since the preceding mismatch-aware packet at base `8400eb33`, the
canonical Lean sources, frozen architecture inputs, manifest, toolchain, and
dependency manifest are byte-identical. Only that earlier blocker packet was
integrated under this target, so both blockers persist.

## Validation

All commands ran in this worker clone. The automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts was reused
read-only. No `lake update`, `lake build`, dependency clone/fetch, checkout
repair, network request, or dependency mutation was performed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets at ranks 1 through 1546 passed. |
| `python3 scripts/stage1_target.py show THM-M-0605` | 0 | Rank 643; planned; L0/rework-required; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0605/check_anchor_audit.py` | 0 | The validator reported an exact marker, but it does not compare the source marker's mismatched `IsManifold` binder; this pass is not exact-transport evidence. |
| `python3 Stage1_Instances/THM-M-0605/check_obligation_tree.py` | 0 | 19 obligations and 90 typed edges passed; denominator `c6e29bccc0135529afc98b27c38f6c5265449f1fd054602ec55fe9d9e5b6e5b7`; root remains open M4. |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | Lean 4.29.0 at commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`; Lake 5.0.0. |
| `cd Formalizations/Lean && lake env lean --trust=0 -t0 ../../Stage1_Instances/THM-M-0605/Statement.lean` | 0 | Frozen analytic target elaborated; output was 15,602 bytes with SHA-256 `b45c5a871dc9b5862356b1fd2540c8d770d8b4488230005303cc6b41f7b33469`. |
| Same command for `ObligationTree.lean` | 0 | Conditional composer elaborated; axioms were exactly `propext`, `Classical.choice`, and `Quot.sound`. |
| Same command for `AnchorAudit.lean` | 0 | Local analytic-shape transport elaborated and discarded-name check passed; it did not compare to the actual infinity-smooth marker binder. |
| Same command for `probes/RegularityMismatch.lean` | 0 | Proved omega differs from infinity; analytic-to-smooth synthesis passed; retained mathlib marker remained unknown. Axioms were `propext` and `Quot.sound`. |
| Same command for `probes/SmoothToAnalyticFails.lean` | 1 | Expected negative evidence: failed to synthesize `IsManifold (mathcal-R 7) omega M` from only the infinity-smooth instance. |
| Same command for `probes/StandardSphereShortcut.lean` | 0 | The identity diffeomorphism rejected the standard-sphere shortcut; axioms were exactly `propext`, `Classical.choice`, and `Quot.sound`. |
| Scoped retained-body and construction-package searches | 0 | Hits were confined to discarded markers, this dossier, a duplicate statement/composer, and metadata probes; no eligible terminal body or required construction package was found. |
| Prohibited-device scan of checked Lean files | 0 | No `sorry`, `admit`, `sorryAx`, `native_decide`, `implemented_by`, axiom declaration, unsafe declaration, or equivalent proof escape was found. |
| `git diff --name-status 8400eb33..HEAD` on target proof inputs, target manifest, toolchain, and dependency manifest | 0 | Only the preceding slot40 blocker packet was added; all canonical proof inputs and pins are byte-identical. |

## Retry condition

First reopen the statement and anchor phases. Deliberately freeze the
infinity-smooth target matching the human scope and source marker, or justify
the stronger analytic target with a checked transport. Then implement the
Milnor bundle and all dependent topological and smooth-obstruction packages
without placeholders, or integrate an immutable compatible proof-bearing
declaration for the exact corrected target. Rerun exact-type, trust,
provenance, and composition checks afterward.

This is current-base proof-phase blocker evidence, not a proof receipt. It does
not satisfy `S56-M-0605-PROOF`, repair or accept a prerequisite node, promote
scheduler state, close an obligation, or support theorem completion. Because
the assigned phase is not genuinely self-tested as complete,
`.stage1-worker-selftest.json` remains absent.
