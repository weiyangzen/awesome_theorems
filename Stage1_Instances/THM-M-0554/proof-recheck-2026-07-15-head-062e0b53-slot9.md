# THM-M-0554 proof-phase recheck: blocked

Item: `S56-M-0554-PROOF`

Intent: `prove`

Recheck time: `2026-07-15T18:34:33+08:00`

Base revision: `062e0b530c644c6d9c62556518568dd91a7374cd`

Base tree: `0879a3d554dc3011e1c5b513107c330547ea185c`

## Verdict

`blocked`. The ten proof-relevant target inputs are byte-for-byte unchanged
from the preceding integrated recheck. Neither the owned dossier nor the
pinned dependency closure contains a source-faithful proof body for the
cohomological Atiyah-Hirzebruch spectral sequence.

`Proof.lean` is a real, placeholder-free conditional composition harness. It
assembles E2, differential, convergence, and naturality packages field by
field, but `statementOfBranchFamily` assumes the complete family and
constructs none of those mathematical branches. It closes no frozen
obligation and receives no proof credit.

The immediate open root cut remains:

- `M0554-X-GENCOH`: generalized-cohomology pair, excision, and wedge infrastructure;
- `M0554-C-EXACT-COUPLE`: the skeletal-filtration exact-couple construction;
- `M0554-C-E2-MODEL`: the cellular-cohomology E2 identification;
- `M0554-L-STRONG`: strong convergence for the finite skeletal filtration.

No proof receipt, composition certificate, debt-vector change, or item-state
transition is proposed. The root remains `M4`.

## First Failed Gate

Exact-statement fidelity and dependency-legal predecessor authority fail
before positive proof credit. The selected mathematical claim requires a
reduced generalized cohomology theory and a genuine finite CW construction.
The frozen Lean interface omits reducedness; stores point, exactness, wedge,
finite-CW, exhaustiveness, and cell-attachment requirements as bare `Prop`
fields; leaves `ordinaryCohomology` unrelated to `H^p(X; E^q(pt))`; represents
the induced filtration by the tautology `K.skeleton = K.skeleton`; and lets
the output select bare propositions for coefficient convention, strong
convergence, and naturality.

These defects make the literal target inhabitable by a zero spectral-sequence
container and output-selected true propositions. Such a term constructs no
mathematical AHSS and consumes none of the four semantic root-cut packages.
Retaining or crediting it would be a fake or substituted result under the
rev-5.6 statement-fidelity and composition gates.

The structured authorities are also not proof-ready. `instance.json` remains
`planned` with null canonical formal identity fields. The local
`task-dag.json` is unfrozen and marks proof `blocked_by_predecessors`.
Registry v1 uses planned fingerprints for substantive branches, while the
global obligation-tree predecessor is worker-provisional (`[_]`) rather than
master-accepted. A proof-only worker cannot repair those predecessor phases.

## Pinned Search

Pinned mathlib supplies generic spectral-sequence containers, spectral-object
interfaces, CW skeleton APIs, and singular homology. A recursive search found
no AHSS, generalized-cohomology, exact-couple, or strong-convergence terminal
declaration. The pinned
`Mathlib/Algebra/Homology/SpectralObject/SpectralSequence.lean` source still
documents `spectralSequence`, `homologyData`, and
`spectralSequenceHomologyData` as `TODO`.

The only target-specific repo-local matches outside this dossier are the
legacy `S1_M_106.lean` interfaces and explicit blocker gates, not a terminal
proof body. `DifferentialProbe.lean` proves by `rfl` only the literal bidegree
relation. It cannot close `M0554-B-DIFFERENTIAL`, whose required child
`M0554-C-SPECTRAL` remains open.

## Fresh Validation

The automation-provided `Formalizations/Lean/.lake` symlink to canonical
pinned artifacts was reused read-only. No Lake update/build, dependency
clone/fetch, checkout, network action, or `.lake` mutation was performed.
Lean objects and logs were isolated under `/tmp` and removed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0554` | 0 | Rank 106; lane `frontier_deep_formalization_debt`; lifecycle `planned`; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0554/check_obligation_tree.py` | 0 | `PASS THM-M-0554 obligation tree: 32 obligations, 91 typed edges`; denominator `3c72072a...8048b`; root remains open at `M4`. |
| `LAKE_NO_UPDATE=1 timeout -k 5 60 lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e...16740`. |
| Isolated `LAKE_NO_UPDATE=1 lake env lean --trust=0 -t0` replay of `Statement.lean`, `Proof.lean`, and `DifferentialProbe.lean` | 0 | All elaborated; objects were 429072, 280728, and 15576 bytes. Log SHA-256 values were `f1690fd1...d30`, `8cfbfe08...72a1`, and `30cba6d3...156`. Conditional declarations were sorry-free and reported exactly `propext`, `Classical.choice`, and `Quot.sound`. |
| Pinned-package AHSS/generalized-cohomology/exact-couple/strong-convergence `rg` scan | 1 | Expected no-match: empty output SHA-256 `e3b0c442...b855`; no terminal proof candidate exists. |
| Repo-local proof-candidate scan outside this dossier and `.lake` | 0 | Output SHA-256 `74eb1264...bf6`; target-specific matches are legacy `S1_M_106.lean` interfaces and blocker gates. |
| Prohibited-device scan over owned Lean sources | 1 | Expected no-match: empty output SHA-256 `e3b0c442...b855`; no prohibited proof device was found. |
| SHA-256 and TODO scan of the pinned spectral-object source | 0 | SHA-256 `2ce62b9d...740aa`; intended constructors remain documented as TODO. |
| `git diff --quiet 310be814...HEAD --` over the ten proof-relevant inputs | 0 | All proof-relevant target inputs are unchanged. |
| Lean/Lake and dependency identity checks | 0 | Lean `4.29.0`; Lake `5.0.0-src+98dc76e`; mathlib `8a178386...ea95`, tree `bdc39a31...1c2b`, clean; flt-regular `56161b6e...1a27`, clean. |

The isolated Lean recipe, run from the repository root, was:

```bash
set -euo pipefail
repo=$PWD
target=$repo/Stage1_Instances/THM-M-0554
lean_root=$repo/Formalizations/Lean
tmp=$(mktemp -d /tmp/thm-m-0554-proof-062e0b53-slot9.XXXXXX)
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

First publish and master-accept a source-faithful statement, reconcile the
instance/task/statement authorities, and issue registry v2 with exact branch
fingerprints. Then implement and compose all four root-cut packages without
placeholders. Alternatively, pin an immutable compatible Lean 4 AHSS proof
and pass exact-type, provenance, trust, and composition gates.

Status boundary: this is fresh durable blocker evidence only. It does not
satisfy `S56-M-0554-PROOF`, close a frozen obligation or root, propose `[_]`,
complete the audit or theorem, enter validation/release, or authorize master
acceptance. Because the assigned proof phase is not genuinely self-tested as
complete, `.stage1-worker-selftest.json` remains absent.
