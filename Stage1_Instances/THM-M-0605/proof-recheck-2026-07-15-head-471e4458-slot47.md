# THM-M-0605 proof phase: blocked at base 471e4458

Item: `S56-M-0605-PROOF`

Intent: `prove`

Recorded: `2026-07-15T20:16:20+08:00`

Base revision: `471e4458269351ee096972776c478d019941b679`

Base tree: `e30e1cefce39148420ccc4525b726d57f58ee94b`

Worker checkout: Stage1 rev-5.6 automation clone `slot47`

## Verdict

`blocked`. No placeholder-free Lean 4 body for
`Stage1.THM_M_0605.ExoticSevenSphereExists` exists in the repository or the
pinned dependency closure. This run added no proof body, closed obligation, or
composition certificate. The proof item stays `[ ]`, lifecycle stays
`planned`, the root vector stays `[H1, M4, R3]`, and audit and theorem
completion remain false.

The first failed gate is prerequisite statement fidelity. The frozen target
requires analytic `IsManifold (mathcal-R 7) omega`, while both the stated
smooth claim and pinned mathlib marker use infinity-smooth regularity.
`AnchorAudit.lean` changes that binder to `omega` in a local marker shape, so
its equivalence is not a transport from the actual marker. Trust-zero probes
prove the orders differ and confirm that only analytic-to-smooth synthesis is
available; the reverse check fails. The statement and anchor phases must be
reopened before this proof phase can close.

Independently, all mathematical witness bodies are absent. The immediate root
cut is `M0605-T-WITNESS`: a particular seven-manifold, a homeomorphism to the
standard seven-sphere, and an `IsEmpty Diffeomorph` certificate. The first
missing package is `M0605-C-BUNDLE`, the selected Milnor 3-sphere bundle over
the 4-sphere with clutching and characteristic data. Its total-space,
homotopy-sphere, topological-recognition, bounding-manifold,
smooth-obstruction, standard-comparison, nondiffeomorphism, and witness
packages are also open. The analytic target additionally needs an analytic
construction or valid smooth-to-analytic bridge.

The checked `exoticSevenSphereExists_of_witness` theorem only composes a
complete witness; it constructs none of its inputs. The standard sphere is
not a witness because its identity diffeomorphism contradicts the required
`IsEmpty` certificate. Returning the conditional composer or assuming a
missing witness component would weaken the target or introduce a placeholder.

Pinned mathlib has the nearby smooth signature only as source-only
`proof_wanted exists_homeomorph_isEmpty_diffeomorph_sphere_seven`. Batteries
elaborates it under `withoutModifyingEnv`, then discards it; a direct import
probe reports the name as unknown. The scoped pinned search found no retained
Milnor-sphere, clutching, homotopy-sphere, Eells-Kuiper, Kervaire-Milnor, or
equivalent construction package.

Since the preceding base `b4d23994`, only its blocker packet was integrated
under this target. Canonical Lean sources, frozen registry and graphs, target
manifest, toolchain, and dependency pins are unchanged, so both blockers
persist.

## Validation

All commands ran in this worker clone. The automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts was reused
read-only. No `lake update`, `lake build`, dependency clone/fetch, network
request, or `.lake` mutation was performed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets at ranks 1 through 1546 passed. |
| `python3 scripts/stage1_target.py show THM-M-0605` | 0 | Rank 643; planned; L0/rework-required; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0605/check_anchor_audit.py` | 0 | The checker reported its modeled marker/discard/M4 checks passed, but it does not compare the actual infinity-smooth binder. |
| `python3 Stage1_Instances/THM-M-0605/check_obligation_tree.py` | 0 | 19 obligations and 90 typed edges passed; denominator `c6e29bccc0135529afc98b27c38f6c5265449f1fd054602ec55fe9d9e5b6e5b7`; root and witness remain open M4. |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0 at commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`; mathlib is `8a178386ffc0f5fef0b77738bb5449d50efeea95`. |
| `cd Formalizations/Lean && LEAN_NUM_THREADS=1 timeout --foreground --kill-after=5s 240s lake env lean --trust=0 -t0 ../../Stage1_Instances/THM-M-0605/Statement.lean` | 0 | The frozen analytic target elaborated; output was 15,602 bytes with SHA-256 `b45c5a871dc9b5862356b1fd2540c8d770d8b4488230005303cc6b41f7b33469`. |
| Same trust-zero command for `ObligationTree.lean` | 0 | The conditional composer elaborated; axioms were exactly `propext`, `Classical.choice`, and `Quot.sound`. |
| Same trust-zero command for `AnchorAudit.lean` | 0 | The local analytic-shape equivalence elaborated; it did not compare the actual infinity-smooth binder. |
| Same trust-zero command for `probes/RegularityMismatch.lean` | 0 | Proved `omega != infinity`, synthesized analytic-to-smooth, and confirmed the marker is not retained. |
| Same trust-zero command for `probes/AnalyticToSmoothMarker.lean` | 0 | The only valid implication elaborated with axioms `propext`, `Classical.choice`, and `Quot.sound`. |
| Same trust-zero command for `probes/SmoothToAnalyticFails.lean` | 1 | Expected negative: failed to synthesize analytic `IsManifold` from only an infinity-smooth instance. |
| Same trust-zero command for `probes/StandardSphereShortcut.lean` | 0 | The identity diffeomorphism rejected the standard-sphere shortcut. |
| Disposable trust-zero import probe of the `proof_wanted` name | 1 | Expected negative: unknown identifier. |
| Scoped pinned construction-package search | 1 | Expected no-match: no retained relevant construction package was found. |
| Prohibited-device scan of checked target Lean files | 1 | Expected no-match: no `sorry`, `admit`, `sorryAx`, axiom declaration, unsafe declaration, or `native_decide`. |
| Scoped diff from base `b4d23994` | 0 | Only the preceding blocker packet was added; no proof input or pin changed. |
| `python3 -m json.tool` plus fail-closed `jq -e` assertions on the structured blocker | 0 | JSON syntax, item/base identity, blocked/open state, incomplete flags, empty accepted receipts, and changed paths passed. |
| `git diff --no-index --check /dev/null` for both new artifacts | 0 | Both artifacts had zero whitespace diagnostics; the ordinary content-difference exit was handled explicitly. |
| `git diff --check; test ! -e .stage1-worker-selftest.json` | 0 | No tracked whitespace errors; completion self-test is absent because the proof phase is incomplete. |

## Retry condition

First reopen statement and anchor phases: freeze the infinity-smooth target
matching the claim and source marker, or justify the stronger analytic target
with a checked equivalence. Then implement all frozen Milnor construction and
obstruction packages without placeholders, or integrate an immutable
compatible proof-bearing declaration. Rerun exact-type, trust, provenance,
and composition checks afterward.

This current-base artifact is blocker evidence, not a proof receipt. It does
not satisfy `S56-M-0605-PROOF`, promote scheduler state, close an obligation,
or support validation, release, audit completion, or theorem completion.
Because the assigned phase is incomplete, `.stage1-worker-selftest.json`
remains absent.
