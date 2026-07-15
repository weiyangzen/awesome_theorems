# THM-M-0605 proof phase: blocked at base 255c85c9

Item: `S56-M-0605-PROOF`

Intent: `prove`

Recorded: `2026-07-15T18:42:11+08:00`

Base revision: `255c85c9e88403358cd081cd624f3b90eb808654`

Base tree: `5165028b1b2e17baadaf6a4936b14b7b5fd8c9ed`

Worker checkout: Stage1 rev-5.6 automation clone `slot52`

## Verdict

`blocked`. No placeholder-free Lean 4 proof body for the frozen target
`Stage1.THM_M_0605.ExoticSevenSphereExists` is present in the repository or
the pinned dependency closure. No proof body or obligation closure was added.
The proof item stays `[ ]`, lifecycle stays `planned`, the root vector stays
`[H1, M4, R3]`, and audit completion, root closure, validation, release, and
theorem completion remain false.

The first failed gate precedes proof implementation. The frozen
`SmoothSevenManifold` requires `IsManifold (mathcal-R 7) omega`, which is an
analytic manifold structure. The actual pinned mathlib `proof_wanted` marker
and the dossier's stated smooth scope require
`IsManifold (mathcal-R 7) infinity`. The checked regularity probe proves these
orders unequal and verifies only the analytic-to-smooth direction. The
expected-negative reverse probe cannot synthesize an analytic structure from
a smooth one. `AnchorAudit.lean` proves an equivalence to a locally rewritten
analytic marker shape, not to the actual smooth marker. Its Python checker
does not inspect this binder mismatch, so its successful exit is not exact
source-transport evidence.

Independently, the proof-body blocker remains. The immediate frozen root cut
is `M0605-T-WITNESS`: a particular manifold, a homeomorphism to the standard
seven-sphere, and an `IsEmpty Diffeomorph` certificate. The first unavailable
construction is `M0605-C-BUNDLE`, the selected Milnor 3-sphere bundle over the
4-sphere with its clutching and characteristic data. The downstream
total-space, homotopy-sphere, topological-identification, bounding-manifold,
smooth-obstruction, standard-comparison, nondiffeomorphism, and witness
packages also remain open. The stronger frozen analytic target additionally
needs an analytic construction or a justified smooth-to-analytic transport.

The checked theorem `exoticSevenSphereExists_of_witness` is conditional
child-to-parent composition only: it consumes the complete witness and
constructs none of it. The standard sphere is not a shortcut because its
identity diffeomorphism contradicts the required `IsEmpty` certificate.
Assuming any missing component or returning only the conditional composer
would be a placeholder or a substituted theorem and was not done.

Pinned mathlib contains the nearby smooth signature only as
`proof_wanted exists_homeomorph_isEmpty_diffeomorph_sphere_seven`.
Batteries elaborates such a marker with a temporary helper axiom inside
`withoutModifyingEnv` and discards it. The trust-zero import probe reports the
name as unknown. Scoped searches found no retained Milnor-sphere, clutching,
homotopy-sphere, Eells-Kuiper, Kervaire-Milnor, or equivalent proof package.

Since the preceding slot52 recheck at base `62a4768e`, only proof-blocker
packets were integrated under this target. The canonical Lean sources,
regularity probes, frozen architecture inputs, target manifest, toolchain,
and dependency manifest remain byte-identical. Both blockers therefore
persist at the current base.

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
| `python3 Stage1_Instances/THM-M-0605/check_anchor_audit.py` | 0 | The validator reported an exact marker, but source inspection and the trust-zero probes show it omits the mismatched `IsManifold` binder; this is not exact-transport evidence. |
| `python3 Stage1_Instances/THM-M-0605/check_obligation_tree.py` | 0 | 19 obligations and 90 typed edges passed; denominator `c6e29bccc0135529afc98b27c38f6c5265449f1fd054602ec55fe9d9e5b6e5b7`; root remains open M4. |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0 at commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`; pinned mathlib is `8a178386ffc0f5fef0b77738bb5449d50efeea95`. |
| `cd Formalizations/Lean && lake env lean --trust=0 -t0 ../../Stage1_Instances/THM-M-0605/Statement.lean` | 0 | Frozen analytic target elaborated and printed; its frozen printed-expression SHA-256 is `b45c5a871dc9b5862356b1fd2540c8d770d8b4488230005303cc6b41f7b33469`. |
| Same command for `ObligationTree.lean` | 0 | Conditional composer elaborated; axioms were exactly `propext`, `Classical.choice`, and `Quot.sound`. |
| Same command for `AnchorAudit.lean` | 0 | Local analytic-shape equivalence elaborated and the retained-marker rejection passed; it did not compare the actual smooth binder. |
| Same command for `probes/RegularityMismatch.lean` | 0 | Proved omega differs from infinity, analytic-to-smooth synthesis passed, and the discarded marker remained unknown; axioms were `propext` and `Quot.sound`. |
| Same command for `probes/SmoothToAnalyticFails.lean` | 1 | Expected negative evidence: failed to synthesize analytic `IsManifold` from only an infinity-smooth instance. |
| Same command for `probes/StandardSphereShortcut.lean` | 0 | The identity diffeomorphism rejected the standard-sphere shortcut; axioms were `propext`, `Classical.choice`, and `Quot.sound`. |
| Scoped retained-body/construction search | 0 | Hits were confined to discarded markers, this dossier, THM-M-0578's duplicate statement/composer, and metadata probes; no eligible proof body or required construction package was found. |
| Prohibited-device scan of checked Lean files | 1 | Expected no-match exit: no `sorry`, `admit`, `sorryAx`, axiom declaration, unsafe declaration, or equivalent proof escape was found. |
| Scoped diff from base `255c85c9` before this packet | 0 | No target proof source, frozen architecture input, dependency pin, generated checklist, scheduler state, or target manifest had changed. |

## Retry condition

First reopen the statement and anchor phases. Deliberately freeze the
infinity-smooth target matching the human scope and source marker, or justify
the stronger analytic target with a real checked transport. Then implement
the Milnor bundle and all dependent topological and smooth-obstruction
packages without placeholders, or integrate an immutable compatible
proof-bearing declaration for the exact corrected target. Rerun exact-type,
trust, provenance, and composition checks afterward.

This is current-base proof-phase blocker evidence, not a proof receipt. It
does not satisfy `S56-M-0605-PROOF`, repair or accept a prerequisite node,
promote scheduler state, close an obligation, or support audit or theorem
completion. Because the assigned phase is not genuinely complete,
`.stage1-worker-selftest.json` remains absent.
