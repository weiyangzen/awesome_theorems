# THM-M-0605 proof phase: blocked at base f7b3c872

Item: `S56-M-0605-PROOF`

Intent: `prove`

Recorded: `2026-07-15T19:29:27+08:00`

Base revision: `f7b3c872ab727ab689486d74020c11dc5d99869f`

Base tree: `6c3dc9661349dd7774b23660eb9bde0212918c51`

Worker checkout: Stage1 rev-5.6 automation clone `slot49`

## Verdict

`blocked`. No placeholder-free Lean 4 proof body for the frozen target
`Stage1.THM_M_0605.ExoticSevenSphereExists` is present in the repository or
the pinned dependency closure. No proof body, composition certificate, or
obligation closure was added. The proof item stays `[ ]`, lifecycle stays
`planned`, the root vector stays `[H1, M4, R3]`, and audit completion, root
closure, validation, release, and theorem completion remain false.

The first failed gate is exact prerequisite statement fidelity. The frozen
`SmoothSevenManifold` requires `IsManifold (mathcal-R 7) omega`, an analytic
manifold structure. The human claim and actual pinned mathlib
`proof_wanted` marker instead require `IsManifold (mathcal-R 7) infinity`, a
smooth structure. The trust-zero regularity probe proves these orders are
unequal and checks only the analytic-to-smooth direction. The expected-
negative reverse probe cannot synthesize an analytic structure from a smooth
one. `AnchorAudit.lean` defines a local analytic `MathlibMarkerShape`, so its
equivalence is not a transport from the actual infinity-smooth marker. The
Python anchor checker omits this binder comparison; its successful exit does
not repair exact-statement fidelity.

A disposable trust-zero probe checked the valid one-way relation from the
frozen analytic target to the actual infinity-smooth marker shape, using
mathlib's analytic-to-smooth `IsManifold` instance. It used only `propext`,
`Classical.choice`, and `Quot.sound`. This implication cannot be reversed and
therefore supplies neither an exact equivalence nor root proof credit.

Independently, the mathematical proof body remains unavailable. The immediate
frozen root cut is `M0605-T-WITNESS`: a particular manifold, a homeomorphism
to the standard seven-sphere, and an `IsEmpty Diffeomorph` certificate. The
first missing construction is `M0605-C-BUNDLE`, the selected Milnor
3-sphere bundle over the 4-sphere with its clutching and characteristic data.
The total-space, homotopy-sphere, topological-identification, bounding-
manifold, smooth-obstruction, standard-comparison, nondiffeomorphism, and
witness packages downstream also remain open. The stronger frozen analytic
target additionally needs an analytic construction or a valid smooth-to-
analytic bridge.

The checked `exoticSevenSphereExists_of_witness` theorem is conditional
child-to-parent composition only: it consumes the complete witness and
constructs none of it. The standard sphere cannot be a shortcut because its
identity diffeomorphism contradicts the required `IsEmpty` certificate.
Assuming a missing witness component or returning only the composer would be
a placeholder or substituted theorem and was not done.

Pinned mathlib contains the nearby smooth signature only as
`proof_wanted exists_homeomorph_isEmpty_diffeomorph_sphere_seven`.
Batteries discards that declaration, and the trust-zero probe reports the
name as unknown. A scoped search across the repository, pinned mathlib, and
pinned Batteries found no retained Milnor-sphere, clutching, Eells-Kuiper,
Kervaire-Milnor, or equivalent construction package.

Since the preceding recheck at base `5544f999`, only that blocker packet was
integrated under this target. The statement, conditional composition,
anchor, regularity probes, frozen registry and graphs, validation
specifications, target manifest, toolchain, and dependency manifest are
byte-identical. Both blockers therefore persist at the current base.

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
| `python3 Stage1_Instances/THM-M-0605/check_anchor_audit.py` | 0 | The checker printed its exact-marker success message, but inspection and probes show that it omits the mismatched `IsManifold` binder; this is not exact-transport evidence. |
| `python3 Stage1_Instances/THM-M-0605/check_obligation_tree.py` | 0 | 19 obligations and 90 typed edges passed; denominator `c6e29bccc0135529afc98b27c38f6c5265449f1fd054602ec55fe9d9e5b6e5b7`; root remains open M4. |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0 at commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`; pinned mathlib is `8a178386ffc0f5fef0b77738bb5449d50efeea95`. |
| `cd Formalizations/Lean && lake env lean --trust=0 -t0 ../../Stage1_Instances/THM-M-0605/Statement.lean` | 0 | Frozen analytic target elaborated and printed its explicit expression with SHA-256 `b45c5a871dc9b5862356b1fd2540c8d770d8b4488230005303cc6b41f7b33469`. |
| Same command for `ObligationTree.lean` | 0 | Conditional composer elaborated; axioms were exactly `propext`, `Classical.choice`, and `Quot.sound`. |
| Same command for `AnchorAudit.lean` | 0 | Local analytic-shape equivalence elaborated and retained-marker rejection passed; it did not compare the actual smooth binder. |
| Same command for `probes/RegularityMismatch.lean` | 0 | Proved `omega` differs from `infinity`, analytic-to-smooth synthesis passed, and the discarded marker stayed unknown; axioms were `propext` and `Quot.sound`. |
| Same command for `probes/SmoothToAnalyticFails.lean` | 1 | Expected negative evidence: failed to synthesize analytic `IsManifold` from only an infinity-smooth instance. |
| Disposable trust-zero analytic-to-smooth packaging probe | 0 | The frozen target implies the actual infinity-smooth marker shape; axioms were `propext`, `Classical.choice`, and `Quot.sound`. The converse remains unavailable. |
| Same command for `probes/StandardSphereShortcut.lean` | 0 | The identity diffeomorphism rejected the standard-sphere shortcut; axioms were `propext`, `Classical.choice`, and `Quot.sound`. |
| Scoped Lean source search | 0 | Relevant hits were confined to the discarded marker, this dossier, THM-M-0578's duplicate statement/composer, and unrelated interfaces; no eligible terminal body was found. |
| Prohibited-device scan of checked target Lean files | 1 | Expected no-match exit: no `sorry`, `admit`, `sorryAx`, axiom declaration, unsafe declaration, or `native_decide` was found. |
| Proof-input whitelist diff from base `5544f999` | 0 | No canonical Lean source, frozen architecture input, diagnostic probe, dependency pin, target manifest, or validation specification changed. |
| `python3 -m json.tool`, `jq -e`, and `git diff --check` | 0 | Structured blocker syntax and fail-closed fields passed; no whitespace errors were found. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion manifest is absent because the assigned proof phase remains incomplete. |

## Retry condition

First reopen the statement and anchor phases. Freeze the infinity-smooth
target matching the human scope and actual marker, or justify the stronger
analytic target with a checked transport. Then implement the Milnor bundle
and every dependent topological and smooth-obstruction package without
placeholders, or integrate an immutable compatible proof-bearing declaration
for the exact corrected target. Rerun exact-type, trust, provenance, and
composition checks afterward.

This is current-base proof-phase blocker evidence, not a proof receipt. It
does not satisfy `S56-M-0605-PROOF`, repair or accept a prerequisite node,
promote scheduler state, close an obligation, or support audit or theorem
completion. Because the assigned phase is not genuinely complete,
`.stage1-worker-selftest.json` remains absent.
