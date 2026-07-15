# THM-M-0554 proof phase blocked at `d71fe284`

Item: `S56-M-0554-PROOF`

Intent: `prove`

Recheck time: `2026-07-16T00:28:30+08:00`

Base revision: `d71fe284446b9f58daa00496a4e6530a42136324`

Base tree: `a73161e038e592f66fb80c29bf13672d58f60c64`

## Verdict

`blocked`. No source-faithful proof body for the cohomological
Atiyah-Hirzebruch spectral sequence exists in the owned dossier, the
repo-local Lean sources, or the pinned dependency closure. No proof receipt,
frozen-node closure, composition certificate, debt-vector change, or item
state transition is proposed. The root remains open at `M4`.

The first failed gate is exact-target fidelity (`S56-5.1` /
`M0554-S-DATA`). The canonical theorem requires a reduced generalized
cohomology theory, a genuine finite CW filtration, an `E2` identification with
`H^p(X; E^q(pt))`, and proved convergence and naturality. The frozen Lean
interface instead:

- omits reducedness;
- stores point, exactness, wedge, finite-CW, exhaustiveness, and cell-
  attachment requirements as proposition values without evidence;
- leaves `ordinaryCohomology` unrelated to `H^p(X; E^q(pt))`;
- lets the output choose bare propositions for coefficient convention,
  strong convergence, and naturality; and
- records the induced filtration only as `K.skeleton = K.skeleton`.

The literal proposition therefore admits a zero spectral-sequence/`True`
witness that constructs no AHSS. Retaining or crediting that witness would be
a fake result relative to the canonical claim and the frozen semantic
children, so this worker deliberately does not implement it.

`Proof.lean` contains genuine placeholder-free conditional composition:
`dataOfBranches`, `statementShapeOfBranches`, and
`statementOfBranchFamily` consume four explicit branch packages. The last
declaration assumes the complete E2, differential, convergence, and
naturality family; it constructs none of those branches and closes no frozen
obligation. `DifferentialProbe.lean` proves only the raw bidegree relation by
`rfl`. The typed graph requires `M0554-B-DIFFERENTIAL` to consume the open
`M0554-C-SPECTRAL` child, so the probe remains an uncomposed diagnostic.

The substantive root cut remains:

- `M0554-X-GENCOH`: generalized-cohomology pair, excision, and wedge
  infrastructure;
- `M0554-C-EXACT-COUPLE`: the skeletal-filtration exact-couple construction;
- `M0554-C-E2-MODEL`: the cellular-cohomology E2 identification; and
- `M0554-L-STRONG`: strong convergence for the finite skeletal filtration.

Predecessor authority independently prevents positive proof acceptance.
`S56-M-0554-OBLIGATION_TREE` is only provisional `[_]`, not master-accepted
`[x]`. The target `instance.json` remains `planned` with null canonical formal
identity fields, while `task-dag.json` is unfrozen and marks proof
`blocked_by_predecessors`. `statement.json` also names the nonexistent
`AtiyahHirzebruchConvergenceData`, so statement, instance, task, and registry
authority must be reconciled before proof work is dependency-legal.

Before this packet the unchanged root had 48 tracked proof-recheck
JSON/Markdown pairs, two proof-blocker JSON records, and one proof-progress
JSON record. Proof-relevant inputs did not change from the preceding slot13
recheck at `3a3be423`. This is far beyond the five-unresolved-tick split
threshold; the scheduler should not dispatch the unchanged proof root again.

## Fresh Validation

The automation-provided `Formalizations/Lean/.lake` symlink to the canonical
pinned artifacts was reused read-only. No `lake update`, `lake build`,
dependency clone/fetch, checkout, network action, or `.lake` mutation was
performed. Lean objects and logs were created under `/tmp` and removed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0554` | 0 | Rank 106; lane `frontier_deep_formalization_debt`; lifecycle `planned`; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0554/check_obligation_tree.py` | 0 | `PASS`: 32 obligations and 91 typed edges; denominator `3c72072a...8048b`; root remains open at `M4` without a composition certificate. |
| Isolated pinned `lake env`-resolved `lean --trust=0 -t0` replay | 0 | `Statement.lean`, `Proof.lean`, and `DifferentialProbe.lean` elaborated with Lean 4.29.0; object sizes were 429072, 280728, and 15576 bytes. Object SHA-256 values were `46d2fc1b...9ded`, `dc72a4c9...30c6`, and `a159b12b...fca9`; log SHA-256 values were `f1690fd1...d30`, `8cfbfe08...2a1`, and `30cba6d3...156`. |
| `#print axioms` and `#print sorries` emitted by `Proof.lean` | 0 | All three conditional declarations are sorry-free and depend on exactly `propext`, `Classical.choice`, and `Quot.sound`. |
| Pinned-package AHSS/generalized-cohomology/exact-couple/strong-convergence scan | 1 | Expected no-match result: no terminal proof candidate. |
| Scoped prohibited-device scan over owned Lean sources | 1 | Expected no-match result: no `sorry`, `admit`, `axiom`, `sorryAx`, unsafe/oracle device, or `native_decide`. |
| Mathlib spectral-object SHA-256 and `TODO` scan | 0 | SHA-256 `2ce62b9d...740aa`; `spectralSequence`, `homologyData`, and `spectralSequenceHomologyData` remain documented as `TODO`. |
| `git diff --quiet 3a3be423...HEAD --` over ten proof-relevant inputs | 0 | The statement, proof, diagnostic, and structured proof inputs are unchanged; the only target delta is the preceding slot13 blocker packet. |
| Lean/Lake, manifest, and dependency identity checks | 0 | Lean `4.29.0` commit `98dc76e...16740`; Lake `5.0.0-src+98dc76e`; manifest `321626c8...2d81`; mathlib revision `8a178386...ea95`, tree `bdc39a31...1c2b`, clean; `flt-regular` revision `56161b6e...1a27`, tree `32c9eace...893`, clean. |
| Packet JSON parse, fail-closed `jq` assertions, and all-owned-JSON parse | 0 | The packet and every top-level owned JSON artifact parse; identity, current base, blocked state, empty closure/receipt arrays, exact four-node cut, and false proof/root/audit/theorem/self-test flags agree. |
| Tracked and untracked `git diff --check` recipes | 0 | No whitespace diagnostic; each raw no-index command returned the expected content-difference status `1` with empty diagnostic output. |
| `test ! -e .stage1-worker-selftest.json` | 0 | The completion self-test manifest is absent because the assigned proof phase is blocked. |

The exact isolated Lean recipe, run from the repository root, was:

```bash
set -euo pipefail
repo=$PWD
target=$repo/Stage1_Instances/THM-M-0554
lean_root=$repo/Formalizations/Lean
tmp=$(mktemp -d /tmp/thm-m-0554-proof-d71fe284-slot13.XXXXXX)
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

## Retry Condition

Do not reschedule the unchanged proof root. First publish and master-accept a
source-faithful statement, reconcile instance/task/statement authority, and
issue obligation-registry version 2 with exact elaborated branch fingerprints.
Then implement and compose the four root-cut packages without placeholders.
Alternatively, pin an immutable, compatible, exact Lean 4 AHSS proof and pass
canonical mapping, provenance, trust, and composition gates.

This packet is fresh current-base blocker evidence only. It does not satisfy
`S56-M-0554-PROOF`, propose `[_]`, close an obligation or the root, complete
the audit or theorem, enter validation/release, or authorize master
acceptance. Because the assigned proof phase is not genuinely self-tested as
complete, `.stage1-worker-selftest.json` remains absent.
