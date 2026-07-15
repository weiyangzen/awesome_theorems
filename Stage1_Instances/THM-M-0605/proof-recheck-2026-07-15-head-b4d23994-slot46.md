# THM-M-0605 proof phase: blocked at base b4d23994

Item: `S56-M-0605-PROOF`

Intent: `prove`

Recorded: `2026-07-15T20:05:01+08:00`

Base revision: `b4d239943a37f6c25c377bbfd85c0e1ec7f4acaa`

Base tree: `5f13e0e86bde3bcaaef38b979819490c648166e3`

Worker checkout: Stage1 rev-5.6 automation clone `slot46`

## Verdict

`blocked`. No placeholder-free Lean 4 body for the frozen proposition
`Stage1.THM_M_0605.ExoticSevenSphereExists` exists in the repository or the
pinned dependency closure. This run added no proof body, closed obligation, or
composition certificate. The proof item stays `[ ]`, the lifecycle stays
`planned`, the root vector stays `[H1, M4, R3]`, and the root, audit,
validation, release, and theorem-completion gates remain open.

The first failed gate is prerequisite statement fidelity. `Statement.lean`
requires `IsManifold (mathcal-R 7) omega`, which mathlib documents as an
analytic structure. The human claim and the actual pinned mathlib
`proof_wanted` marker require `IsManifold (mathcal-R 7) infinity`, a smooth
structure. `AnchorAudit.lean` substitutes `omega` in a locally defined marker
shape, so its equivalence does not compare with the actual source marker. The
trust-zero probes prove `omega != infinity`, synthesize only the valid
analytic-to-smooth direction, and fail as expected in the reverse direction.
The durable `AnalyticToSmoothMarker.lean` implication therefore diagnoses the
boundary but neither repairs exact statement identity nor proves existence.

Independently, the mathematical proof body is absent. The immediate frozen
root cut is `M0605-T-WITNESS`: a particular manifold, a homeomorphism to the
standard seven-sphere, and an `IsEmpty Diffeomorph` certificate. The first
missing package is `M0605-C-BUNDLE`, the selected Milnor 3-sphere bundle over
the 4-sphere with its clutching and characteristic data. Its total-space,
homotopy-sphere, topological-recognition, bounding-manifold,
smooth-obstruction, standard-comparison, nondiffeomorphism, and witness
packages are also open. The frozen analytic target additionally needs an
analytic construction or a valid smooth-to-analytic bridge.

The checked `exoticSevenSphereExists_of_witness` theorem is only conditional
child-to-parent composition: it consumes the complete witness and constructs
none of it. The standard sphere cannot be used as the witness because its
identity diffeomorphism contradicts the required `IsEmpty` certificate.
Assuming a missing witness component or returning the conditional composer
would be a prohibited placeholder or substituted theorem, so neither was done.

Pinned mathlib contains the nearby smooth signature only as
`proof_wanted exists_homeomorph_isEmpty_diffeomorph_sphere_seven`. Batteries
elaborates such markers with a temporary helper axiom inside
`withoutModifyingEnv` and then discards the environment change. A fresh direct
trust-zero import probe reports the identifier as unknown. A fresh scoped
search found no retained Milnor-sphere, clutching, homotopy-sphere,
Eells-Kuiper, Kervaire-Milnor, or equivalent construction package.

Since the preceding recheck at base `90a1d52c`, the current base added only
`probes/AnalyticToSmoothMarker.lean` and the associated blocker pair under
this target. The canonical statement, conditional composer, anchor, other
diagnostic probes, frozen architecture, target manifest, toolchain, and
dependency manifest remain byte-identical. The new implication is diagnostic
only, so both hard blockers persist.

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
| `python3 Stage1_Instances/THM-M-0605/check_anchor_audit.py` | 0 | The checker printed success, but source inspection and trust-zero probes show that it omits the actual marker's mismatched regularity binder; this is not exact-transport evidence. |
| `python3 Stage1_Instances/THM-M-0605/check_obligation_tree.py` | 0 | 19 obligations and 90 typed edges passed; denominator `c6e29bccc0135529afc98b27c38f6c5265449f1fd054602ec55fe9d9e5b6e5b7`; root and witness remain open M4. |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0 at commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`; pinned mathlib is `8a178386ffc0f5fef0b77738bb5449d50efeea95`. |
| `cd Formalizations/Lean && LEAN_NUM_THREADS=1 timeout --foreground --kill-after=5s 240s lake env lean --trust=0 -t0 ../../Stage1_Instances/THM-M-0605/Statement.lean` | 0 | The frozen analytic target elaborated; printed output was 15,602 bytes with SHA-256 `b45c5a871dc9b5862356b1fd2540c8d770d8b4488230005303cc6b41f7b33469`. |
| Same command for `ObligationTree.lean` | 0 | The conditional composer elaborated; axioms were exactly `propext`, `Classical.choice`, and `Quot.sound`. |
| Same command for `AnchorAudit.lean` | 0 | The local analytic-shape equivalence elaborated; it did not compare the actual infinity-smooth binder. |
| Same command for `probes/RegularityMismatch.lean` | 0 | Proved `omega != infinity`, checked analytic-to-smooth synthesis, and confirmed the discarded marker is unavailable. |
| Same command for `probes/AnalyticToSmoothMarker.lean` | 0 | The only valid implication elaborated; axioms were `propext`, `Classical.choice`, and `Quot.sound`. |
| Same command for `probes/SmoothToAnalyticFails.lean` | 1 | Expected negative: failed to synthesize analytic `IsManifold` from an infinity-smooth instance. |
| Same command for `probes/StandardSphereShortcut.lean` | 0 | The identity diffeomorphism rejected the standard-sphere shortcut. |
| Disposable direct trust-zero import probe of the `proof_wanted` name | 1 | Expected negative: `Unknown identifier exists_homeomorph_isEmpty_diffeomorph_sphere_seven`. |
| Scoped pinned construction-package search | 1 | Expected no-match: no retained Milnor-sphere, clutching, homotopy-sphere, Eells-Kuiper, or Kervaire-Milnor package was found. |
| Prohibited-device scan of checked target Lean files | 1 | Expected no-match: no `sorry`, `admit`, `sorryAx`, axiom declaration, unsafe declaration, or `native_decide` was found. |
| Proof-input diff from base `90a1d52c` | 0 | Only the diagnostic `AnalyticToSmoothMarker.lean` was added; no canonical source, frozen architecture, target manifest, toolchain, or dependency pin changed. |
| `python3 -m json.tool` and `jq -e` on the structured blocker | 0 | JSON syntax and fail-closed item/base/verdict/state/completion fields passed. |
| `git diff --no-index --check /dev/null` on each new blocker artifact, accepting the ordinary difference exit only when diagnostics are empty | 0 | Both files had zero whitespace diagnostics. |
| `git diff --check; test ! -e .stage1-worker-selftest.json` | 0 | The tracked diff had no whitespace errors and the completion manifest is absent because the proof phase is incomplete. |

## Retry condition

First reopen the statement and anchor phases. Freeze the infinity-smooth target
matching the human claim and actual marker, or justify the stronger analytic
target with a checked equivalence. Then implement every frozen Milnor
construction and obstruction package without placeholders, or integrate an
immutable compatible proof-bearing declaration for the exact corrected target.
Rerun exact-type, trust, provenance, and composition checks afterward.

This is current-base proof-phase blocker evidence, not a proof receipt. It does
not satisfy `S56-M-0605-PROOF`, repair or accept a prerequisite node, promote
scheduler state, close an obligation, or support audit or theorem completion.
Because the assigned proof phase is not genuinely self-tested as complete,
`.stage1-worker-selftest.json` remains absent.
