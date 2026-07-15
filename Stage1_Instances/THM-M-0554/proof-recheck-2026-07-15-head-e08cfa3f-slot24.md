# THM-M-0554 proof-phase recheck: blocked

Item: `S56-M-0554-PROOF`

Intent: `prove`

Recheck time: `2026-07-15T12:19:17+08:00`

Base revision: `e08cfa3f7d7a37ef13682a7bac1e61f054d9522f`

Base tree: `002c1691169181f8d5a99919874237d131e9bd0d`

## Verdict

`blocked`. No genuine proof of the cohomological Atiyah-Hirzebruch spectral
sequence exists in the owned dossier or pinned dependency closure. The
current `Proof.lean` contains placeholder-free conditional recomposition, but
its root theorem assumes the entire E2, differential, convergence, and
naturality branch family. It therefore constructs none of the missing AHSS
branches and cannot close a parent whose required children remain open.

No proof receipt, frozen-node closure, composition certificate, or state
transition is proposed. The root remains `M4`, with this immediate cut:

- `M0554-X-GENCOH`: generalized-cohomology pair, excision, and wedge infrastructure;
- `M0554-C-EXACT-COUPLE`: the skeletal-filtration exact-couple construction;
- `M0554-C-E2-MODEL`: the cellular-cohomology E2 identification;
- `M0554-L-STRONG`: strong convergence for the finite skeletal filtration.

## First Failed Gate

Exact-statement fidelity and predecessor authority fail before positive proof
credit is possible. The selected human theorem requires a reduced generalized
cohomology theory and a genuine finite-CW construction. The frozen Lean
interface omits reducedness, stores its exactness/wedge/CW requirements as
unproved proposition-valued fields, chooses bare output propositions for
coefficient convention, strong convergence, and naturality, and represents
the induced filtration by the tautology `K.skeleton = K.skeleton`.

A fresh scratch-only diagnostic confirmed that the literal Lean proposition
is inhabited by a zero spectral sequence with zero page objects and
output-selected `True` propositions. The kernel accepts that term, but it
constructs no AHSS, provides no cellular E2 model or strong-convergence
argument, and closes none of the frozen semantic children. The diagnostic was
deleted and receives no proof credit: retaining it would be a fake result and
would violate the no-substitution and child-to-parent composition gates.

The structured authorities are also not proof-ready. `instance.json` remains
`planned` with null canonical formal identity fields; `task-dag.json` is
unfrozen and marks proof `blocked_by_predecessors`; the obligation-tree item is
only provisional rather than master-accepted; and registry v1 uses planned
fingerprints for the substantive branches. A proof-only worker cannot repair
these predecessor artifacts without broadening its assignment.

## Validation

The automation-provided `Formalizations/Lean/.lake` is an untracked symlink to
the canonical pinned cache and was not mutated. No Lake update/build,
dependency clone/fetch, or network operation was requested. The required root
`lake env lean` validation is presently unavailable: the shared
`flt-regular` checkout has `HEAD` pointing to the nonexistent local branch
`refs/heads/.invalid`, so Lake exits before launching Lean. This is recorded as
an environment blocker rather than repaired or fetched.

For the smallest available diagnostic, Lean 4.29.0 was invoked directly with
the existing pinned package object directories and toolchain library in
`LEAN_PATH`. All generated objects and logs lived under fresh `/tmp`
directories and were removed by traps. This nonrelease fallback validates only
the current conditional declarations and the statement-defect diagnostic; it
is not a substitute for the requested `lake env lean` gate.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0554` | 0 | Rank 106; lane `frontier_deep_formalization_debt`; lifecycle `planned`; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0554/check_obligation_tree.py` | 0 | 32 obligations and 91 typed edges passed; denominator `3c72072a...8048b`; root remains open at `M4` without a composition certificate. |
| `timeout 60 lake env lean --version` from `Formalizations/Lean` | 1 | Lake reported that `.lake/packages/flt-regular` could not resolve `HEAD`; log SHA-256 `d0b03389...9d7`, 242 bytes. |
| Direct pinned Lean `--trust=0 -t0` replay of `Statement.lean`, `Proof.lean`, and `DifferentialProbe.lean` | 0 | Objects were 429072, 280728, and 15576 bytes. Log hashes were `f1690fd1...d30`, `8cfbfe08...2a1`, and `30cba6d3...156`. The three conditional proof declarations were sorry-free and reported exactly `propext`, `Classical.choice`, and `Quot.sound`. |
| Scratch-only zero-witness diagnostic under the same direct pinned Lean fallback | 0 | The zero spectral sequence, fake data, and literal root term were sorry-free and reported exactly the same three axioms; log SHA-256 `29ddb8d5...1d3`, 376 bytes. The source and objects were deleted and are not credited. |
| Pinned-package search for AHSS/generalized-cohomology/exact-couple/strong-convergence Lean sources | 1 | Expected no-match: zero hits, empty-output SHA-256 `e3b0c442...b855`; no terminal proof candidate found. |
| Prohibited-device scan over owned Lean sources | 1 | Expected no-match: no `sorry`, `admit`, `axiom`, `sorryAx`, bodyless `constant`/`opaque`, unsafe declaration, implementation override, or oracle token. |
| `jq empty` over all top-level owned JSON files | 0 | Every structured target artifact parsed. |

Pinned identities: Lean 4.29.0 commit `98dc76e3...16740`, Lean binary
SHA-256 `3e0d0d3d...28bbf`, Lake 5.0.0-src+98dc76e, manifest SHA-256
`321626c8...2d81`, mathlib revision `8a178386...ea95` and tree
`bdc39a31...1c2b`. The owned target path was clean at start; only the
automation-provided `.lake` symlink was untracked.

## Retry Condition

First publish and master-accept a source-faithful corrected statement,
reconcile the instance/task/statement authorities, and issue registry v2 with
exact branch fingerprints. Then construct and compose all four root-cut
packages without placeholders. Alternatively, pin an immutable compatible
Lean 4 AHSS proof and pass exact-type, provenance, trust, and composition
checks. The canonical pinned Lake artifact must also be restored so the
required `lake env lean` replay can run without fetching or mutation.

This is current-base blocker evidence only. It does not satisfy
`S56-M-0554-PROOF`, propose `[_]`, close any frozen obligation or the root,
complete the audit or theorem, or authorize master acceptance. Because the
assigned proof phase is not genuinely self-tested as complete,
`.stage1-worker-selftest.json` remains absent.
