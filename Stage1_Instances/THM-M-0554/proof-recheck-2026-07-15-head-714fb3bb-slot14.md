# THM-M-0554 proof-phase recheck: blocked

Item: `S56-M-0554-PROOF`

Intent: `prove`

Recheck time: `2026-07-15T13:38:57+08:00`

Base revision: `714fb3bb6a070c2f659ece069f1a7219f9c045a0`

Base tree: `2c99a78c5fa247aebc885f31e6818fc029f17a60`

## Verdict

`blocked`. No source-faithful proof of the cohomological Atiyah-Hirzebruch
spectral sequence exists in the owned dossier or pinned dependency closure.
The current `Proof.lean` is placeholder-free and kernel-checks its conditional
field-by-field recomposition, but `statementOfBranchFamily` assumes the entire
E2, differential, convergence, and naturality family. It constructs none of
the required branches and cannot close a parent whose children remain open.

No proof receipt, frozen-node closure, composition certificate, accepted
receipt, or state transition is proposed. The root remains `M4`; its immediate
cut is:

- `M0554-X-GENCOH`: generalized-cohomology pair, excision, and wedge infrastructure;
- `M0554-C-EXACT-COUPLE`: the skeletal-filtration exact-couple construction;
- `M0554-C-E2-MODEL`: the cellular-cohomology E2 identification;
- `M0554-L-STRONG`: strong convergence for the finite skeletal filtration.

## First Failed Gate

Exact-statement fidelity and predecessor authority fail before proof credit is
possible. The selected theorem concerns a reduced generalized cohomology
theory and a genuine finite CW construction. The frozen Lean interface omits
reducedness; stores exactness, wedge, point, and CW conditions as selected
propositions without evidence; uses bare output propositions for coefficient
convention, strong convergence, and naturality; and represents the induced
filtration by the tautology `K.skeleton = K.skeleton`.

A scratch-only diagnostic constructed a zero spectral sequence and selected
the output propositions as `True`. Lean accepted the literal root at trust
level zero with no sorries. That term constructs no AHSS, cellular E2 model,
skeletal filtration, or strong-convergence proof. The scratch source, objects,
and logs were deleted and receive no proof credit: retaining or claiming this
term would be a fake result under the exact-statement and child-composition
gates.

The structured authorities are also not proof-ready. `instance.json` remains
`planned` with null canonical formal identity fields; `task-dag.json` is
unfrozen and marks proof `blocked_by_predecessors`; the obligation-tree item is
only provisional rather than master-accepted; and registry v1 uses planned
fingerprints for the substantive branches. A proof-only worker cannot rewrite
these predecessor authorities.

## Validation

The automation-provided `Formalizations/Lean/.lake` is an untracked symlink to
the canonical pinned cache. It was inspected and reused read-only. No Lake
update/build, dependency clone/fetch, checkout, network action, or `.lake`
mutation was performed.

The required `lake env lean` gate is unavailable in this worker: the pinned
`flt-regular` checkout has no valid `HEAD`, and a bounded probe timed out before
Lean started. This is recorded as a missing pinned artifact rather than
repaired. As the smallest available nonrelease diagnostic, the pinned Lean
4.29.0 binary was invoked directly with existing package object directories
in `LEAN_PATH`. All generated objects and logs were placed in `/tmp` and
removed. This fallback checks the current conditional declarations but does
not replace the required Lake validation or prove the AHSS.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0554` | 0 | Rank 106; lane `frontier_deep_formalization_debt`; lifecycle `planned`; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0554/check_obligation_tree.py` | 0 | 32 obligations and 91 typed edges passed; denominator `3c72072a...8048b`; root remains open at `M4` without a composition certificate. |
| `cd Formalizations/Lean && timeout 15 lake env lean --version` | 124 | Timed out before Lean started; empty output SHA-256 `e3b0c442...b855`; `flt-regular` has no valid `HEAD`. |
| Direct pinned Lean `--trust=0 -t0` replay of `Statement.lean`, `Proof.lean`, and `DifferentialProbe.lean` | 0 | Objects were 429072, 280728, and 15576 bytes; log SHA-256 values were `f1690fd1...d30`, `8cfbfe08...2a1`, and `30cba6d3...156`; all three conditional proof declarations were sorry-free and reported exactly `propext`, `Classical.choice`, and `Quot.sound`. |
| Scratch-only literal zero-witness diagnostic through the same fallback | 0 | Confirmed the statement defect; the term was sorry-free with the same three axioms. All scratch source, objects, and logs were removed, and no proof credit was assigned. |
| Pinned-package AHSS/generalized-cohomology/exact-couple/strong-convergence source scan | 1 | Expected no-match: no terminal proof candidate. |
| Prohibited-device scan over owned Lean sources | 1 | Expected no-match: no `sorry`, `admit`, `axiom`, `sorryAx`, bodyless `constant`/`opaque`, unsafe declaration, implementation override, external/oracle token. |
| `find Stage1_Instances/THM-M-0554 -maxdepth 1 -name '*.json' -print0 \| xargs -0 -n1 jq empty` | 0 | All top-level owned JSON artifacts, including this blocker record, parsed. |
| Scoped `jq -e` blocker assertions | 0 | Item/theorem identity, base revision/tree, blocked state, exact root cut, empty accepted receipts, and false proof/root/theorem/selftest flags matched. |
| `git diff --check` plus no-index whitespace checks for both new files | 0 | No whitespace diagnostic; the no-index commands returned expected content-difference status 1. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Self-test manifest absent because the proof phase is blocked. |

Pinned identities: Lean 4.29.0 commit `98dc76e3...16740`, Lean binary
SHA-256 `3e0d0d3...28bbf`, Lake `5.0.0-src+98dc76e`, manifest
SHA-256 `321626c8...2d81`, and mathlib revision `8a178386...ea95` with
tree `bdc39a31...1c2b`.

## Retry Condition

First publish and master-accept a source-faithful corrected statement,
reconcile instance/task/statement authority, and issue registry v2 with exact
branch fingerprints. Then construct and compose all four root-cut packages
without placeholders. Alternatively, pin an immutable compatible Lean 4 AHSS
proof and pass exact-type, provenance, trust, and composition checks. The
canonical pinned Lake artifact must also be restored so `lake env lean` can
run without fetching or mutation.

This is current-base blocker evidence only. It does not satisfy
`S56-M-0554-PROOF`, propose `[_]`, close any frozen obligation or root,
complete the audit or theorem, or authorize master acceptance. Because the
assigned proof phase is not genuinely self-tested as complete,
`.stage1-worker-selftest.json` remains absent.
