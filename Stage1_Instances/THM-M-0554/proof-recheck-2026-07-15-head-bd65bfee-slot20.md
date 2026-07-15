# THM-M-0554 proof phase blocked at `bd65bfee` (slot 20)

Item: `S56-M-0554-PROOF`

Intent: `prove`

Recheck time: `2026-07-15T20:16:00+08:00`

Base revision: `bd65bfeeea414dd3cfe270a499dca2b9fd65e34c`

Base tree: `d78c646a63fe7e8004519c621319cbbef7adbb9c`

## Verdict

`blocked`. No source-faithful Atiyah-Hirzebruch spectral-sequence proof body
exists in the repository or pinned dependency closure. This attempt adds no
credited proof body, frozen-node closure, composition certificate, proof
receipt, debt-vector change, or item-state transition. The root remains
`[H3, M4, R4]`.

The first failed gate is `S56-5.1-EXACT-TARGET-CONSISTENCY /
M0554-S-DATA`. The literal Lean interface can be inhabited without
constructing the canonical mathematical AHSS. Reducedness is absent; the
theory and finite-CW requirements are stored as proposition values rather
than evidence; `ordinaryCohomology` is unrelated to `H^p(X; E^q(pt))`;
coefficient convention, strong convergence, and naturality are
output-selected propositions; and the filtration condition is the tautology
`K.skeleton = K.skeleton`.

A zero-page/`True` inhabitant would therefore be a fake result. It would not
construct the skeletal spectral sequence, identify its E2 page, prove strong
convergence, or establish naturality, and is deliberately neither retained
nor credited.

`Proof.lean` remains a genuine, placeholder-free conditional composition
harness. It assumes complete E2, differential, convergence, and naturality
packages, so it constructs none of the mathematical branches. The separate
`DifferentialProbe.lean` fact proves only the literal index relation by `rfl`.
Packaging that fact as a `DifferentialBranch` was tested during this attempt
and rejected before artifact creation: the frozen branch requires the open
`M0554-C-SPECTRAL` child, and section 6.7 forbids bypassing or silently
discarding a required child. The owned Lean sources were restored exactly;
`Proof.lean` retains SHA-256 `d6f81c98...cae1b`.

The genuine open root cut remains:

- `M0554-X-GENCOH`: generalized-cohomology pair, excision, and wedge infrastructure;
- `M0554-C-EXACT-COUPLE`: the skeletal-filtration exact-couple construction;
- `M0554-C-E2-MODEL`: the cellular-cohomology E2 identification;
- `M0554-L-STRONG`: strong convergence for the finite skeletal filtration.

Dependency authority independently blocks positive acceptance. The global
obligation-tree item is only provisional `[_]`; `instance.json` remains
`planned` with null canonical formal identity fields; and `task-dag.json` is
unfrozen and marks proof `blocked_by_predecessors`.

There are now 43 pre-existing tracked proof-attempt JSON records and 43
matching Markdown records for this target, while scheduler authority still
records zero attempts and no children. These files are not an authoritative
tick ledger, but the observed repeated dispatch exceeds the five-unresolved-
tick split threshold. The integration lane must reconcile the ledger and
redirect execution to statement/registry repair rather than schedule the
unchanged oversized proof root again.

## Validation

All Lean checks reused the automation-provided read-only symlink to canonical
pinned Lake artifacts. No update, build, clone, fetch, checkout, network
action, or dependency mutation occurred. Generated objects and logs were
created under `/tmp` and removed. The untracked symlink makes this nonrelease
evidence.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0554` | 0 | Rank 106; lifecycle `planned`; baseline `L0/rework_required`; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0554/check_obligation_tree.py` | 0 | `PASS`: 32 obligations and 91 typed edges; denominator `3c72072a...8048b`; root remains open at `M4` with no composition certificate or proof closure. |
| Isolated `LAKE_NO_UPDATE=1 lake env` resolved `lean --trust=0 -t0` replay of `Statement.lean`, `Proof.lean`, and `DifferentialProbe.lean` | 0 | Objects were 429072, 280728, and 15576 bytes; log hashes were `f1690fd1...d30`, `8cfbfe08...2a1`, and `30cba6d3...156`. All conditional declarations were sorry-free and reported exactly `propext`, `Classical.choice`, and `Quot.sound`. |
| Prohibited-device scan over owned Lean sources | 1 | Expected no-match: no `sorry`, `admit`, bodyless declaration, `sorryAx`, unsafe/oracle device, or `native_decide` occurs. |
| Pinned-package AHSS/generalized-cohomology/exact-couple/strong-convergence scan | 1 | Expected no-match: no terminal proof candidate. |
| Equivalent repo-local scan outside this dossier and `.lake` | 0 | 159 source lines; target-specific hits are legacy interfaces and blocker gates, not a terminal body. |
| Lake-manifest package audit | 0 | All 11 package worktrees match their recorded revisions and are clean; mathlib is `8a178386...ea95`, tree `bdc39a31...1c2b`; flt-regular is `56161b6e...1a27`. |
| SHA-256 and `TODO` scan of mathlib's spectral-object source | 0 | SHA-256 `2ce62b9d...740aa`; `spectralSequence`, `homologyData`, and `spectralSequenceHomologyData` remain documented as `TODO`. |
| `git diff --quiet 8b931195...HEAD --` over ten proof-relevant inputs | 0 | No proof-relevant source or structured-input delta existed at worker start. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion self-test absent because the proof phase is blocked. |

The exact isolated Lean recipe, run from the repository root, was:

```bash
set -euo pipefail
repo=$PWD
target=$repo/Stage1_Instances/THM-M-0554
lean_root=$repo/Formalizations/Lean
tmp=$(mktemp -d /tmp/thm-m-0554-proof-bd65bfee-slot20.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
lean=$(cd "$lean_root" && LAKE_NO_UPDATE=1 lake env which lean)
base_path=$(cd "$lean_root" && LAKE_NO_UPDATE=1 lake env printenv LEAN_PATH)
cd "$target"
LEAN_NUM_THREADS=1 LEAN_PATH="$base_path" LAKE_NO_UPDATE=1 \
  timeout -k 5 300 "$lean" --trust=0 -t0 -R "$target" \
    -o "$tmp/Statement.olean" Statement.lean
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$base_path" LAKE_NO_UPDATE=1 \
  timeout -k 5 300 "$lean" --trust=0 -t0 -R "$target" \
    -o "$tmp/Proof.olean" Proof.lean
LEAN_NUM_THREADS=1 LEAN_PATH="$base_path" LAKE_NO_UPDATE=1 \
  timeout -k 5 300 "$lean" --trust=0 -t0 -R "$target" \
    -o "$tmp/DifferentialProbe.olean" DifferentialProbe.lean
```

Pinned environment: Lean `4.29.0` commit `98dc76e...16740`, Lake
`5.0.0-src+98dc76e`, Lean binary SHA-256 `3e0d0d3d...28bbf`, manifest
SHA-256 `321626c8...2d81`, and toolchain-file SHA-256
`651c8acc...5b1d2`.

## Retry Condition

Do not reschedule the unchanged proof root. Publish and master-accept a
source-faithful statement that encodes reducedness, inhabited theory/CW
hypotheses, actual ordinary-cohomology coefficients, filtration provenance,
strong convergence, and naturality. Reconcile instance/task/statement
authority, then issue obligation-registry version 2 with exact branch
fingerprints and smaller dependency-legal children. Alternatively, pin an
immutable exact compatible Lean 4 AHSS proof and pass canonical mapping,
provenance, trust, and composition gates.

This packet is durable blocker evidence only. It does not satisfy
`S56-M-0554-PROOF`, close an obligation or root, complete the audit or
theorem, or authorize validation, release, or master acceptance. Because the
assigned proof phase is incomplete, `.stage1-worker-selftest.json` remains
absent.
