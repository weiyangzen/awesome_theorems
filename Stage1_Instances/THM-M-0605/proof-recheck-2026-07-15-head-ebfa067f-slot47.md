# THM-M-0605 proof phase: blocked at base ebfa067f

Item: `S56-M-0605-PROOF`

Intent: `prove`

Recorded: `2026-07-15T21:14:06+08:00`

Base revision: `ebfa067f2385ca03cc0a0eeecf151993a994962c`

Base tree: `4d482bdb45ec4ff17c128d712608f7c7eea1ffc8`

Worker checkout: Stage1 rev-5.6 automation clone `slot47`

## Verdict

`blocked`. No placeholder-free Lean 4 body for
`Stage1.THM_M_0605.ExoticSevenSphereExists` exists in the repository or the
pinned dependency closure. This run added no proof body, closed obligation, or
composition certificate. The proof item stays `[ ]`, lifecycle stays
`planned`, the root vector stays `[H1, M4, R3]`, and audit and theorem
completion remain false.

The first failed gate is prerequisite statement fidelity. The frozen target
requires analytic `IsManifold (mathcal-R 7) omega`, while the human smooth
claim and the actual pinned mathlib marker use infinity-smooth regularity.
`AnchorAudit.lean` replaces the actual marker's binder with `omega` in its
local `MathlibMarkerShape`, so its equivalence is only a packaging equivalence
between two analytic shapes. It is not a transport from the cited source
marker. Trust-zero probes prove that the orders differ, synthesize only the
analytic-to-smooth direction, and fail in the smooth-to-analytic direction.
The statement and anchor phases therefore need correction or a checked
justification before this proof phase can close.

Independently, the required mathematical proof packages are absent. The
immediate root cut is `M0605-T-WITNESS`: one particular analytic seven-
manifold, a homeomorphism to the standard seven-sphere, and an `IsEmpty`
diffeomorphism certificate. The first missing construction is
`M0605-C-BUNDLE`, the selected Milnor 3-sphere bundle over the 4-sphere with
its clutching and characteristic data. Its total-space, homotopy-sphere,
topological-recognition, bounding-manifold, smooth-obstruction,
standard-comparison, nondiffeomorphism, and terminal witness packages are all
open. The stronger frozen target also requires an analytic construction or a
valid smooth-to-analytic bridge.

The checked theorem `exoticSevenSphereExists_of_witness` only composes a
complete witness already supplied as premises. It constructs none of the
three inputs. The standard sphere cannot be used as the witness because its
identity diffeomorphism contradicts the requested `IsEmpty` certificate.
Assuming any missing witness component, or returning the conditional
composer, would introduce a prohibited placeholder or substitute a weaker
theorem.

Pinned mathlib contains the nearby smooth signature only as source-only
`proof_wanted exists_homeomorph_isEmpty_diffeomorph_sphere_seven`.
Batteries elaborates that command using a temporary helper axiom inside
`withoutModifyingEnv` and then discards it. A direct trust-zero import probe
reports the name as unknown. Fresh scoped searches found no retained
Milnor-sphere, clutching, homotopy-sphere, Eells-Kuiper, Kervaire-Milnor, or
equivalent proof package in repository Lean sources or the 8,044 pinned
mathlib/Batteries Lean files. Mathlib's current bordism module additionally
states that bordisms and bordism groups remain future work.

Since the preceding evidence base `49a36d83`, only that base's blocker packet
was integrated under this target. The canonical Lean sources, diagnostic
probes, frozen registry and graphs, target manifest, toolchain, and dependency
pins did not change. Both blockers therefore persist at this base.

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
| `python3 Stage1_Instances/THM-M-0605/check_anchor_audit.py` | 0 | Its modeled marker/discard/M4 checks passed; source inspection shows that it does not compare the actual infinity-smooth binder. |
| `python3 Stage1_Instances/THM-M-0605/check_obligation_tree.py` | 0 | 19 obligations and 90 typed edges passed; denominator `c6e29bcc...b6e5b7`; root and witness remain open M4. |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release; Lake 5.0.0-src+98dc76e; mathlib is pinned at `8a178386ffc0f5fef0b77738bb5449d50efeea95`. |
| `cd Formalizations/Lean && LEAN_NUM_THREADS=1 timeout --foreground --kill-after=5s 240s lake env lean --trust=0 -t0 ../../Stage1_Instances/THM-M-0605/Statement.lean` | 0 | The frozen analytic target elaborated; output was 15,602 bytes with SHA-256 `b45c5a87...f7b33469`. |
| Same trust-zero command for `ObligationTree.lean` | 0 | Conditional assembly elaborated; axioms were exactly `propext`, `Classical.choice`, and `Quot.sound`. |
| Same trust-zero command for `AnchorAudit.lean` | 0 | The local analytic-shape equivalence elaborated; it did not compare the actual smooth marker binder. |
| Same trust-zero command for `probes/RegularityMismatch.lean` | 0 | Proved `omega != infinity`, synthesized analytic-to-smooth, and confirmed that the marker is not retained. |
| Same trust-zero command for `probes/AnalyticToSmoothMarker.lean` | 0 | The only valid implication elaborated; axioms were `propext`, `Classical.choice`, and `Quot.sound`. |
| Same trust-zero command for `probes/SmoothToAnalyticFails.lean` | 1 | Expected negative: failed to synthesize analytic `IsManifold` from only an infinity-smooth instance. |
| Same trust-zero command for `probes/StandardSphereShortcut.lean` | 0 | The identity diffeomorphism rejected the standard-sphere shortcut. |
| Disposable trust-zero import probe of the `proof_wanted` name | 1 | Expected negative: unknown identifier; disposable source SHA-256 `56696ce...fac7c6e3`. |
| Scoped pinned construction-package search | 1 | Expected no-match: no retained relevant construction package was found among 8,044 Lean files. |
| Prohibited-device scan of checked target Lean files | 1 | Expected no-match: no `sorry`, `admit`, `sorryAx`, axiom declaration, unsafe declaration, `implemented_by`, or `native_decide`. |
| `git diff --quiet 49a36d83..HEAD` over canonical proof inputs, pins, target manifest, registry, and graphs | 0 | No proof input, dependency pin, target contract, or frozen architecture changed. |
| `python3 -m json.tool` plus fail-closed `jq -e` assertions on the structured blocker | 0 | JSON syntax, item/base identity, blocked/open state, incomplete flags, empty accepted receipts, and changed paths passed. |
| `git diff --no-index --check /dev/null` for both new artifacts | 1 each | Expected content-difference status with zero whitespace diagnostics for both files. |
| `git diff --check; test ! -e .stage1-worker-selftest.json` | 0 | No tracked whitespace errors; the completion self-test is absent because the proof phase is incomplete. |

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
