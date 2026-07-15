# THM-M-0605 proof phase: blocked at base 90a1d52c

Item: `S56-M-0605-PROOF`

Intent: `prove`

Recorded: `2026-07-15T19:44:06+08:00`

Base revision: `90a1d52c43113012c8aa0e2b110da02e58ce1724`

Base tree: `bc399f3ba59411f2a72d4f29d98eb85e7689b28c`

Worker checkout: Stage1 rev-5.6 automation clone `slot43`

## Verdict

`blocked`. No placeholder-free Lean 4 proof body for the frozen target
`Stage1.THM_M_0605.ExoticSevenSphereExists` exists in the repository or the
pinned dependency closure. No root-relevant proof body, composition
certificate, or obligation closure was added. The proof item stays `[ ]`, the
lifecycle stays `planned`, the root vector stays `[H1, M4, R3]`, and audit
completion, root closure, validation, release, and theorem completion remain
false.

The first failed gate is prerequisite statement fidelity. `Statement.lean`
requires `IsManifold (mathcal-R 7) omega`, which is an analytic manifold
structure. The human smooth claim and the actual pinned mathlib
`proof_wanted` marker instead use `IsManifold (mathcal-R 7) infinity`.
`RegularityMismatch.lean` proves that the two regularity orders differ and
checks only the analytic-to-smooth instance. The expected-negative
`SmoothToAnalyticFails.lean` cannot synthesize the converse. `AnchorAudit.lean`
defines a local marker shape with `omega`, so its equivalence does not transport
from the actual infinity-smooth marker; the Python checker's successful exit
does not compare or repair this binder.

`probes/AnalyticToSmoothMarker.lean` makes the exact one-way boundary durable:
the stronger frozen analytic shape implies the actual infinity-smooth marker
shape using mathlib's analytic-to-smooth `IsManifold` instance. It elaborates
at trust zero with only `propext`, `Classical.choice`, and `Quot.sound`. There
is no reverse instance, so this diagnostic theorem neither establishes exact
statement equivalence nor supplies root proof credit.

Independently, the mathematical proof body is unavailable. The immediate
frozen root cut is `M0605-T-WITNESS`: a particular manifold, a homeomorphism
to the standard seven-sphere, and an `IsEmpty Diffeomorph` certificate. The
first missing construction is `M0605-C-BUNDLE`, the selected Milnor
3-sphere bundle over the 4-sphere with its clutching and characteristic data.
Its total-space, homotopy-sphere, topological-identification,
bounding-manifold, smooth-obstruction, standard-comparison,
nondiffeomorphism, and witness packages remain open. The stronger analytic
target additionally needs an analytic construction or a valid
smooth-to-analytic bridge.

The checked `exoticSevenSphereExists_of_witness` theorem is conditional
child-to-parent composition only: it consumes the complete witness and
constructs none of it. The standard sphere cannot be a shortcut because its
identity diffeomorphism contradicts the required `IsEmpty` certificate.
Assuming a missing component or returning only the composer would be a
placeholder or substituted theorem and was not done.

Pinned mathlib contains the nearby smooth signature only as
`proof_wanted exists_homeomorph_isEmpty_diffeomorph_sphere_seven`.
Batteries discards it, a direct trust-zero import probe reports the name as
unknown, and the pinned construction-package search finds no retained
Milnor-sphere, clutching, homotopy-sphere, Eells-Kuiper, Kervaire-Milnor, or
equivalent package.

Since the preceding recheck at base `f7b3c872`, only that slot49 blocker pair
was integrated under this target. All canonical Lean sources, diagnostic
probes, frozen architecture, target manifest, toolchain, and dependency
manifest are byte-identical. Both blockers therefore persist at this base.

## Validation

All commands ran in this worker clone. The automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts was reused
read-only. No `lake update`, `lake build`, dependency clone/fetch, checkout
repair, network request, or dependency mutation was performed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets at ranks 1 through 1546 passed. |
| `python3 scripts/stage1_target.py show THM-M-0605` | 0 | Rank 643; planned; L0/rework-required; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0605/check_anchor_audit.py` | 0 | The checker printed success, but inspection and trust-zero probes show that it omits the mismatched `IsManifold` binder; this is not exact-transport evidence. |
| `python3 Stage1_Instances/THM-M-0605/check_obligation_tree.py` | 0 | 19 obligations and 90 typed edges passed; denominator `c6e29bccc0135529afc98b27c38f6c5265449f1fd054602ec55fe9d9e5b6e5b7`; root and witness remain open M4. |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0 at commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`; pinned mathlib is `8a178386ffc0f5fef0b77738bb5449d50efeea95`. |
| `cd Formalizations/Lean && lake env lean --trust=0 -t0 ../../Stage1_Instances/THM-M-0605/Statement.lean` | 0 | The frozen analytic target elaborated; printed output was 15,602 bytes with SHA-256 `b45c5a871dc9b5862356b1fd2540c8d770d8b4488230005303cc6b41f7b33469`. |
| Same command for `ObligationTree.lean` | 0 | The conditional composer elaborated; axioms were exactly `propext`, `Classical.choice`, and `Quot.sound`. |
| Same command for `AnchorAudit.lean` | 0 | The local analytic-shape equivalence elaborated and retained-marker rejection passed; it did not compare the actual smooth binder. |
| Same command for `probes/RegularityMismatch.lean` | 0 | Proved `omega != infinity`, checked analytic-to-smooth synthesis, and confirmed the discarded marker is unavailable. |
| Same command for `probes/SmoothToAnalyticFails.lean` | 1 | Expected negative: failed to synthesize analytic `IsManifold` from an infinity-smooth instance. |
| Same command for `probes/AnalyticToSmoothMarker.lean` | 0 | The one valid implication elaborated at trust zero; axioms were `propext`, `Classical.choice`, and `Quot.sound`. |
| Same command for `probes/StandardSphereShortcut.lean` | 0 | The identity diffeomorphism rejected the standard-sphere shortcut. |
| Direct trust-zero import probe of the `proof_wanted` name | 1 | Expected negative: `Unknown identifier exists_homeomorph_isEmpty_diffeomorph_sphere_seven`. |
| Scoped pinned construction-package search | 1 | Expected no-match: no retained clutching, homotopy-sphere, Milnor-sphere, Eells-Kuiper, or Kervaire-Milnor package was found. |
| Prohibited-device scan of checked target Lean files | 1 | Expected no-match: no `sorry`, `admit`, `sorryAx`, axiom declaration, unsafe declaration, or `native_decide` was found. |
| Proof-input whitelist diff from base `f7b3c872` | 0 | No canonical proof input or pin changed; the whole-target delta contains only the prior slot49 blocker pair. |

## Retry condition

First reopen the statement and anchor phases. Freeze the infinity-smooth
target matching the human scope and actual marker, or justify the stronger
analytic target with a checked equivalence. Then implement every frozen
Milnor construction and obstruction package without placeholders, or
integrate an immutable compatible proof-bearing declaration for the exact
corrected target. Rerun exact-type, trust, provenance, and composition checks.

This is current-base proof-phase blocker evidence, not a proof receipt. It
does not satisfy `S56-M-0605-PROOF`, repair or accept a prerequisite node,
promote scheduler state, close an obligation, or support audit or theorem
completion. Because the assigned phase is not genuinely complete,
`.stage1-worker-selftest.json` remains absent.
