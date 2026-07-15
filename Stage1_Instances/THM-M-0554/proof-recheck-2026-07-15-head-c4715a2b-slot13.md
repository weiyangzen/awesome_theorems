# THM-M-0554 proof phase blocked at `c4715a2b`

Item: `S56-M-0554-PROOF`

Recheck time: `2026-07-15T21:04:55+08:00`

Base revision: `c4715a2babbead02e04d70708c3ebc58c75a1942`

Base tree: `28cd40da86c57dea61aed02b4965f80699894bd3`

## Verdict

`blocked`. No source-faithful Atiyah-Hirzebruch spectral-sequence proof body
exists in the owned dossier or pinned dependency closure. No proof body,
frozen-node closure, composition certificate, proof receipt, debt-vector
change, or item-state transition is proposed. The root remains
`[H3, M4, R4]`.

The first failed gate is
`S56-5.1-EXACT-TARGET-CONSISTENCY / M0554-S-DATA`. The intended theorem is the
cohomological AHSS for a reduced generalized cohomology theory on a finite CW
complex. The frozen Lean interface omits reducedness; stores `pointIsPoint`,
exactness, wedge, finite-CW, exhaustiveness, and cell-attachment requirements
as proposition values without evidence; leaves `ordinaryCohomology`
unrelated to `H^p(X; E^q(pt))`; lets the output select bare propositions for
coefficient convention, strong convergence, and naturality; and records the
induced filtration only as the tautology `K.skeleton = K.skeleton`.

Consequently the literal Lean proposition admits a zero spectral-sequence and
`True` witness while constructing no mathematical AHSS. Prior disposable
trust-zero diagnostics establish that defect. Such a term would be a fake
result relative to the canonical claim and frozen semantic children, so it is
not retained or credited.

The existing `Proof.lean` declarations are genuine placeholder-free
conditional composition bodies. `statementOfBranchFamily`, however, assumes
the complete E2, differential, convergence, and naturality family. It
constructs none of those branches and cannot close a parent while its children
remain open. `DifferentialProbe.lean` proves only the literal bidegree relation
by `rfl`; registry v1 makes that branch a nonleaf requiring the open spectral-
sequence construction, so the probe receives no closure credit.

The substantive root cut remains:

- `M0554-X-GENCOH`: generalized-cohomology pair, excision, and wedge infrastructure;
- `M0554-C-EXACT-COUPLE`: the skeletal-filtration exact-couple construction;
- `M0554-C-E2-MODEL`: the cellular-cohomology E2 identification;
- `M0554-L-STRONG`: strong convergence for the finite skeletal filtration.

Pinned mathlib contains generic spectral-sequence, CW, and singular-homology
substrate only. Its spectral-object module still documents the intended
`spectralSequence`, `homologyData`, and `spectralSequenceHomologyData`
constructors as `TODO`. The current pinned-package scan found no terminal AHSS
body, and the ten proof-relevant inputs are byte-identical to the preceding
slot13 recheck at `88a5a5c6`.

Predecessor authority independently blocks positive acceptance. The blueprint
records `S56-M-0554-OBLIGATION_TREE` only as provisional `[_]`;
`instance.json` remains `planned` with null canonical-formal identity fields;
and `task-dag.json` is unfrozen and marks proof `blocked_by_predecessors`.

## Validation

The automation-provided `Formalizations/Lean/.lake` symlink to canonical
pinned artifacts was reused read-only. No `lake update`, `lake build`,
dependency clone/fetch, checkout, network action, or `.lake` mutation was
performed. Generated Lean objects and logs lived under `/tmp` and were removed
by a trap. The untracked symlink makes this nonrelease evidence.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0554` | 0 | Rank 106; lifecycle `planned`; baseline `L0/rework_required`; legacy artifacts unaccepted; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0554/check_obligation_tree.py` | 0 | `PASS`: 32 obligations and 91 typed edges; denominator `3c72072a...8048b`; root remains open at `M4` with no composition certificate or proof closure. |
| Isolated `LAKE_NO_UPDATE=1 lake env`-resolved `lean --trust=0 -t0` replay of `Statement.lean`, `Proof.lean`, and `DifferentialProbe.lean` | 0 | Objects were 429072, 280728, and 15576 bytes. Output hashes were `f1690fd1...d30`, `8cfbfe08...2a1`, and `30cba6d3...156`. The conditional proof declarations were sorry-free and reported exactly `propext`, `Classical.choice`, and `Quot.sound`. |
| Scoped prohibited-device scan over owned Lean sources | 1 | Expected no-match: no `sorry`, `admit`, `axiom`, `sorryAx`, bodyless `constant`/`opaque`, unsafe declaration, `implemented_by`, `extern`, or `native_decide` occurs. |
| Pinned-package AHSS/generalized-cohomology/exact-couple/strong-convergence scan | 1 | Expected no-match: no terminal proof candidate. |
| SHA-256 and `TODO` scan of mathlib's spectral-object source | 0 | SHA-256 `2ce62b9d...740aa`; the three intended constructors remain documented as `TODO`. |
| `git diff --quiet 88a5a5c6...HEAD --` over the ten proof-relevant inputs | 0 | No proof-relevant source or structured-input delta; intervening target changes add blocker evidence only. |
| `find Stage1_Instances/THM-M-0554 -maxdepth 1 -name '*.json' -print0 \| xargs -0 -n1 jq empty` | 0 | Every pre-existing top-level owned JSON artifact parsed. |
| Packet `python3 -m json.tool`, scoped `jq -e`, and all-owned-JSON parse checks | 0 | The current packet parses; identity, base, blocked state, false closure/completion flags, empty receipt arrays, and the exact four-node root cut agree. |
| `git diff --check` plus normalized no-index checks for both new artifacts | 0 | No whitespace diagnostic; each raw no-index command returned the expected content-difference status `1` with empty diagnostic output. |
| `test ! -e .stage1-worker-selftest.json` | 0 | The completion self-test manifest is absent because the assigned proof phase is blocked. |

The exact isolated Lean recipe, run from the repository root, was:

```bash
set -euo pipefail
repo=$PWD
target=$repo/Stage1_Instances/THM-M-0554
lean_root=$repo/Formalizations/Lean
tmp=$(mktemp -d /tmp/thm-m-0554-proof-c4715a2b-slot13.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
lean=$(cd "$lean_root" && LAKE_NO_UPDATE=1 lake env which lean)
base_path=$(cd "$lean_root" && LAKE_NO_UPDATE=1 lake env printenv LEAN_PATH)
cd "$target"
LEAN_NUM_THREADS=1 LEAN_PATH="$base_path" LAKE_NO_UPDATE=1 \
  timeout -k 5 300 "$lean" --trust=0 -t0 -R "$target" \
    -o "$tmp/Statement.olean" Statement.lean >"$tmp/statement.log" 2>&1
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$base_path" LAKE_NO_UPDATE=1 \
  timeout -k 5 300 "$lean" --trust=0 -t0 -R "$target" \
    -o "$tmp/Proof.olean" Proof.lean >"$tmp/proof.log" 2>&1
LEAN_NUM_THREADS=1 LEAN_PATH="$base_path" LAKE_NO_UPDATE=1 \
  timeout -k 5 300 "$lean" --trust=0 -t0 -R "$target" \
    -o "$tmp/DifferentialProbe.olean" DifferentialProbe.lean \
    >"$tmp/differential.log" 2>&1
```

Pinned identities: Lean 4.29.0 commit `98dc76e3...16740`, Lean binary
SHA-256 `3e0d0d3d...28bbf`, Lake `5.0.0-src+98dc76e`, manifest SHA-256
`321626c8...2d81`, mathlib revision `8a178386...ea95` and tree
`bdc39a31...1c2b`, and `flt-regular` revision `56161b6e...1a27` and tree
`32c9eace...c893`. Both dependency worktrees were clean.

## Retry Condition

Do not reschedule the unchanged proof root. First publish and master-accept a
source-faithful statement that encodes reducedness, inhabited theory/CW
hypotheses, actual ordinary-cohomology coefficients, filtration provenance,
convergence, and naturality. Reconcile instance/task/statement authority and
issue obligation-registry version 2 with exact branch fingerprints. Then
implement and compose the genuine four-package root cut. Alternatively, pin
an immutable exact compatible Lean 4 AHSS proof and pass canonical mapping,
provenance, trust, and composition gates.

This packet is current-base blocker evidence only. It does not satisfy
`S56-M-0554-PROOF`, propose `[_]`, close an obligation or the root, complete
the audit or theorem, enter validation/release, or authorize master
acceptance. Because the assigned proof phase is not genuinely self-tested as
complete, `.stage1-worker-selftest.json` remains absent.
