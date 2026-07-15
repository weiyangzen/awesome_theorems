# THM-M-0554 proof-phase recheck: blocked

Item: `S56-M-0554-PROOF`

Intent: `prove`

Recheck time: `2026-07-15T20:32:34+08:00`

Base revision: `a1ba351e42fd9eefe315119ef09c0b958358bb8e`

Base tree: `eed1b90627305460f9cee46277fc7c0cb235d1df`

## Verdict

`blocked`. The ten proof-relevant target inputs are byte-for-byte unchanged
from the preceding integrated recheck. The owned dossier and pinned dependency
closure still contain no source-faithful proof body for the cohomological
Atiyah-Hirzebruch spectral sequence.

`Proof.lean` is a genuine, placeholder-free conditional composition harness.
It assembles E2, differential, convergence, and naturality packages field by
field, but `statementOfBranchFamily` assumes the complete family of those
packages. It constructs none of the mathematical branches. Its checked
declarations therefore close no frozen obligation and receive no root proof
credit.

The immediate open root cut remains:

- `M0554-X-GENCOH`: generalized-cohomology pair, excision, and wedge infrastructure;
- `M0554-C-EXACT-COUPLE`: the skeletal-filtration exact-couple construction;
- `M0554-C-E2-MODEL`: the cellular-cohomology E2 identification;
- `M0554-L-STRONG`: strong convergence for the finite skeletal filtration.

No proof receipt, closure composition certificate, debt-vector change, or
item-state transition is proposed. The root remains `M4`.

## First Failed Gate

Exact-statement fidelity and dependency-legal predecessor authority fail
before positive proof credit. The selected mathematical claim requires a
reduced generalized cohomology theory and a genuine finite CW construction.
The frozen Lean interface omits reducedness; stores point, exactness, wedge,
finite-CW, exhaustiveness, and cell-attachment requirements as bare
proposition values rather than evidence; leaves `ordinaryCohomology`
unrelated to `H^p(X; E^q(pt))`; represents the induced filtration by the
tautology `K.skeleton = K.skeleton`; and lets the output select bare
propositions for coefficient convention, strong convergence, and naturality.

Those defects make the literal target inhabitable by a zero spectral-sequence
container and output-selected true propositions. Such a term constructs no
mathematical AHSS and consumes none of the four semantic root-cut packages.
It is deliberately neither retained nor credited because it would be a fake
or substituted result under the rev-5.6 statement-fidelity and composition
gates.

The structured authorities are also not proof-ready. `instance.json` remains
`planned` with null canonical formal identity fields. The local
`task-dag.json` is unfrozen and marks proof `blocked_by_predecessors`.
Registry v1 uses planned fingerprints for substantive branches, while the
global obligation-tree predecessor is only worker-provisional (`[_]`) rather
than master-accepted. A proof-only worker cannot repair those predecessor
authorities.

## Pinned Search

Pinned mathlib provides genuine generic spectral-sequence containers,
spectral-object interfaces, classical CW-complex skeleton/finiteness APIs,
and singular homology. A recursive search of the pinned packages found no
AHSS, generalized-cohomology, exact-couple, or strong-convergence terminal
declaration. No checked bridge composes the available substrate into the
frozen output. The pinned
`Mathlib/Algebra/Homology/SpectralObject/SpectralSequence.lean` source still
documents `spectralSequence`, `homologyData`, and
`spectralSequenceHomologyData` as `TODO`.

The only target-specific repo-local matches outside this dossier are the
legacy `S1_M_106.lean` interfaces and explicit blocker gates, not a terminal
proof body. `DifferentialProbe.lean` confirms by `rfl` only the literal
bidegree relation. It cannot close `M0554-B-DIFFERENTIAL`, whose required
child `M0554-C-SPECTRAL` remains open.

## Fresh Validation

The automation-provided `Formalizations/Lean/.lake` symlink to canonical
pinned artifacts was reused read-only. `LAKE_NO_UPDATE=1` was set for Lake
environment queries. No Lake update/build, dependency clone/fetch, checkout,
network action, or `.lake` mutation was performed. Lean objects and logs were
isolated under `/tmp` and removed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0554` | 0 | Rank 106; lane `frontier_deep_formalization_debt`; lifecycle `planned`; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0554/check_obligation_tree.py` | 0 | `PASS THM-M-0554 obligation tree: 32 obligations, 91 typed edges`; denominator `3c72072a...8048b`; root remains open at `M4` with no composition certificate. |
| Isolated `LAKE_NO_UPDATE=1 lake env lean --trust=0 -t0` replay of `Statement.lean`, `Proof.lean`, and `DifferentialProbe.lean` | 0 | Lean 4.29.0 elaborated all three; objects were 429072, 280728, and 15576 bytes. Log SHA-256 values were `f1690fd1...d30`, `8cfbfe08...2a1`, and `30cba6d3...156`. The conditional proof declarations were sorry-free and reported exactly `propext`, `Classical.choice`, and `Quot.sound`. |
| Pinned-package AHSS/generalized-cohomology/exact-couple/strong-convergence `rg` scan | 1 | Expected no-match: no terminal proof candidate exists in the pinned packages. |
| Repo-local proof-candidate scan outside this dossier and `.lake` | 0 | Target-specific matches are legacy `S1_M_106.lean` interfaces and blocker gates, not a terminal AHSS proof body. |
| Prohibited-device scan over owned Lean sources | 1 | Expected no-match: no prohibited proof device occurs. |
| SHA-256 and TODO scan of the pinned spectral-object source | 0 | SHA-256 `2ce62b9d...740aa`; intended constructors remain documented as TODO. |
| `git diff --quiet 50db6284...HEAD --` over the ten proof-relevant inputs | 0 | All inputs are unchanged; intervening commits integrate blocker evidence only. |
| Lean/Lake and dependency identity checks | 0 | Lean `4.29.0` commit `98dc76e...16740`; Lake `5.0.0-src+98dc76e`; mathlib `8a178386...ea95`, tree `bdc39a31...1c2b`, clean; flt-regular `56161b6e...1a27`, tree `32c9eace...c893`, clean. |
| `find Stage1_Instances/THM-M-0554 -maxdepth 1 -name '*.json' -print0 \| xargs -0 -n1 jq empty` | 0 | Every top-level owned JSON artifact parsed after packet creation. |
| `python3 -m json.tool` plus scoped `jq -e` assertions on the companion JSON | 0 | The packet parsed; item/theorem/base identity, blocked state, exact root cut, empty closure/receipt arrays, and false completion/self-test flags agreed. |
| `git diff --check` plus normalized `git diff --no-index --check /dev/null <new-artifact>` checks | 0 | No whitespace diagnostic for the two new artifacts or tracked scoped diff. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Self-test manifest absent because the assigned proof phase is blocked. |

The isolated Lean recipe, run from the repository root, was:

```bash
set -euo pipefail
repo=$PWD
target=$repo/Stage1_Instances/THM-M-0554
lean_root=$repo/Formalizations/Lean
tmp=$(mktemp -d /tmp/thm-m-0554-slot16.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
cd "$lean_root"
LAKE_NO_UPDATE=1 timeout -k 5 60 lake env lean --version
lean=$(LAKE_NO_UPDATE=1 lake env which lean)
base_path=$(LAKE_NO_UPDATE=1 lake env printenv LEAN_PATH)
cd "$target"
LEAN_NUM_THREADS=1 LEAN_PATH="$base_path" timeout -k 5 300 \
  "$lean" --trust=0 -t0 -R "$target" -o "$tmp/Statement.olean" \
  Statement.lean
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$base_path" timeout -k 5 300 \
  "$lean" --trust=0 -t0 -R "$target" -o "$tmp/Proof.olean" \
  Proof.lean
LEAN_NUM_THREADS=1 LEAN_PATH="$base_path" timeout -k 5 300 \
  "$lean" --trust=0 -t0 -R "$target" \
  -o "$tmp/DifferentialProbe.olean" DifferentialProbe.lean
```

This warm pinned replay validates only the frozen statement, conditional
composition, and bidegree diagnostic. It supplies no evidence for the absent
AHSS construction branches or root.

## Retry Condition

First publish and master-accept a source-faithful statement, reconcile the
instance/task/statement authorities, and issue registry v2 with exact branch
fingerprints. Then implement and compose all four root-cut packages without
placeholders. Alternatively, pin an immutable compatible Lean 4 AHSS proof
and pass exact-type, provenance, trust, and composition gates.

Status boundary: this is durable current-base blocker evidence only. It does
not satisfy `S56-M-0554-PROOF`, close a frozen obligation or root, propose
`[_]`, complete the audit or theorem, enter validation/release, or authorize
master acceptance. Because the assigned proof phase is not genuinely
self-tested as complete, `.stage1-worker-selftest.json` remains absent.
