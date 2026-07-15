# THM-M-0605 proof phase: blocked at base 031437b3

Item: `S56-M-0605-PROOF`

Intent: `prove`

Recorded: `2026-07-15T22:48:00+08:00`

Base revision: `031437b3091b838bb0200e432b96ced6b34104e2`

Base tree: `176564c09ede7e686005c8051df537617d84b7c5`

Worker checkout: Stage1 rev-5.6 automation clone `slot47`

## Verdict

`blocked`. No placeholder-free Lean 4 body for
`Stage1.THM_M_0605.ExoticSevenSphereExists` exists in the repository or the
pinned dependency closure. This run added no proof body, closed obligation, or
composition certificate. The proof item stays `[ ]`, lifecycle stays
`planned`, the root vector stays `[H1, M4, R3]`, and audit and theorem
completion remain false.

The first failed gate is prerequisite statement fidelity. The frozen target
requires analytic `IsManifold (mathcal-R 7) omega`, whereas the human smooth
claim and the actual pinned mathlib marker use infinity-smooth regularity.
`AnchorAudit.lean` replaces the marker's actual binder with `omega` in its
local `MathlibMarkerShape`, so its equivalence compares two analytic shapes;
it is not a transport from the cited source marker. Trust-zero probes prove
that the orders differ, synthesize only analytic-to-smooth regularity, and
fail in the smooth-to-analytic direction. The statement and anchor phases
must therefore be corrected or supplied with a checked justification before
this proof phase can close.

Independently, the required mathematics is absent. The immediate root cut is
`M0605-T-WITNESS`: one particular analytic seven-manifold, a homeomorphism to
the standard seven-sphere, and an `IsEmpty Diffeomorph` certificate. The first
missing construction is `M0605-C-BUNDLE`, the selected Milnor 3-sphere bundle
over the 4-sphere with its clutching and characteristic data. Its total-space,
homotopy-sphere, topological-recognition, bounding-manifold,
smooth-obstruction, standard-comparison, nondiffeomorphism, and terminal
witness packages are all open.

The checked theorem `exoticSevenSphereExists_of_witness` merely composes a
complete witness already supplied as premises. It constructs none of those
inputs. The standard sphere cannot be the witness because its identity
diffeomorphism contradicts the required `IsEmpty` certificate. Assuming a
missing component or returning the conditional composer would introduce a
prohibited placeholder or substitute a weaker theorem.

Pinned mathlib has the nearby infinity-smooth signature only as source-only
`proof_wanted exists_homeomorph_isEmpty_diffeomorph_sphere_seven`.
`proof_wanted` elaboration occurs under `withoutModifyingEnv`, so the name is
discarded. A trust-zero import probe reports it unknown. A current scoped
search found no retained Milnor-sphere, clutching, homotopy-sphere,
Eells-Kuiper, Kervaire-Milnor, or equivalent proof package in 9,676 pinned
package Lean files.

Since the preceding evidence base `feeafa8d`, the current base integrated only
that blocker packet under this target. The canonical Lean sources, probes,
frozen registry and graphs, target manifest, toolchain, and dependency pins
did not change. Both blockers therefore persist at this base.

## Validation

All commands ran in this worker clone. The automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts was reused
read-only. No `lake update`, `lake build`, dependency clone/fetch, network
request, or `.lake` mutation was performed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1,546 uniform-L0 Lean 4 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1,546 unique targets at ranks 1 through 1,546 passed. |
| `python3 scripts/stage1_target.py show THM-M-0605` | 0 | Rank 643; planned; L0/rework-required; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0605/check_anchor_audit.py` | 0 | Its modeled marker/discard/M4 checks passed; source inspection shows that it does not compare the actual infinity-smooth binder. |
| `python3 Stage1_Instances/THM-M-0605/check_obligation_tree.py` | 0 | 19 obligations and 90 typed edges passed; denominator `c6e29bcc...b6e5b7`; root and witness remain open M4. |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release; Lake 5.0.0-src+98dc76e; mathlib is pinned at `8a178386ffc0f5fef0b77738bb5449d50efeea95`. |
| Trust-zero `lake env lean` replay of `Statement.lean` | 0 | The frozen analytic target elaborated; output was 15,602 bytes with SHA-256 `b45c5a87...f7b33469`. |
| Same replay for `ObligationTree.lean` | 0 | Conditional assembly elaborated; output was 367 bytes with SHA-256 `77215ff9...c0c643`; axioms were exactly `propext`, `Classical.choice`, and `Quot.sound`. |
| Same replay for `AnchorAudit.lean` | 0 | The local analytic-shape equivalence elaborated; output was 184 bytes with SHA-256 `3f3bf748...1e90e`; it did not compare the actual infinity-smooth marker binder. |
| Same replay for `probes/RegularityMismatch.lean` | 0 | Proved `omega != infinity`, synthesized analytic-to-smooth, and confirmed that the marker is not retained; output was 169 bytes with SHA-256 `91ac80b1...ad91b7`. |
| Same replay for `probes/AnalyticToSmoothMarker.lean` | 0 | The only valid implication elaborated; output was 141 bytes with SHA-256 `0079117b...45c6e`; axioms were `propext`, `Classical.choice`, and `Quot.sound`. |
| Same replay for `probes/SmoothToAnalyticFails.lean` | 1 | Expected negative: failed to synthesize analytic `IsManifold` from only an infinity-smooth instance; output was 305 bytes with SHA-256 `dc77ce34...9ae43c8`. |
| Same replay for `probes/StandardSphereShortcut.lean` | 0 | The identity diffeomorphism rejected the standard-sphere shortcut; output was 137 bytes with SHA-256 `8e475abc...bbb72c`. |
| Scoped pinned construction-package search | 1 | Expected no-match: no retained relevant construction package was found among 9,676 pinned-package Lean files. |
| Prohibited-device scan of owned Lean files | 1 | Expected no-match: no `sorry`, `admit`, `sorryAx`, axiom declaration, unsafe declaration, `implemented_by`, or `native_decide`. |
| `git diff` from `feeafa8d` over canonical proof inputs, pins, target manifest, registry, and graphs | 0 | No proof input, dependency pin, target contract, or frozen architecture changed. |
| `python3 -m json.tool`, fail-closed `jq -e`, and new-file whitespace checks on this packet | 0 | JSON syntax, immutable-base identity, blocked/open state, false completion fields, empty receipt/closure lists, two changed paths, and whitespace passed. |
| `git diff --check; test ! -e .stage1-worker-selftest.json` | 0 | No whitespace errors; the completion self-test is absent because the proof phase remains incomplete. |

## Retry condition

First reopen statement and anchor phases: freeze the infinity-smooth target
matching the human claim and actual marker, or justify the stronger analytic
target with a checked equivalence. Then implement every frozen Milnor
construction and obstruction package without placeholders, or integrate an
immutable compatible proof-bearing declaration. Rerun exact-type, trust,
provenance, and composition checks afterward.

This current-base artifact is blocker evidence, not a proof receipt. It does
not satisfy `S56-M-0605-PROOF`, promote scheduler state, close an obligation,
or support validation, release, audit completion, or theorem completion.
Because the assigned phase is incomplete, `.stage1-worker-selftest.json`
remains absent.
