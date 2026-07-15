# THM-M-0554 proof-phase recheck: blocked

Item: `S56-M-0554-PROOF`

Intent: `prove`

Recheck time: `2026-07-15T15:45:31+08:00`

Base revision: `9d3f687e9bf0fe3120397744332e909472c52dfd`

Base tree: `558507d70ac5e5e38486f214a3e0ce7b33f7ae9b`

## Verdict

`blocked`. The ten proof-relevant target inputs are unchanged from the
preceding recheck. The owned dossier and pinned dependency closure still
contain no source-faithful proof of the cohomological Atiyah-Hirzebruch
spectral sequence.

`Proof.lean` remains a genuine, placeholder-free conditional composition
harness. It assembles all four output branches field by field and packages
them as the literal `Statement`, but `statementOfBranchFamily` assumes the
complete E2, differential, convergence, and naturality branch family. It
constructs none of those branches. Therefore it closes no frozen obligation
and receives no root proof credit.

The immediate open root cut remains:

- `M0554-X-GENCOH`: generalized-cohomology pair, excision, and wedge infrastructure;
- `M0554-C-EXACT-COUPLE`: the skeletal-filtration exact-couple construction;
- `M0554-C-E2-MODEL`: the cellular-cohomology E2 identification;
- `M0554-L-STRONG`: strong convergence for the finite skeletal filtration.

No proof receipt, closure composition certificate, debt change, or item-state
transition is proposed. The root remains `M4`.

## First Failed Gate

Exact-statement fidelity and dependency-legal predecessor authority fail
before positive proof credit. The selected mathematical claim requires a
reduced generalized cohomology theory and a genuine finite CW construction.
The frozen Lean interface omits reducedness; stores the point, exactness,
wedge, finite-CW, exhaustiveness, and cell-attachment requirements as
proposition values rather than evidence; leaves `ordinaryCohomology`
unrelated to `H^p(X; E^q(pt))`; represents the induced filtration by the
tautology `K.skeleton = K.skeleton`; and lets the output choose bare
propositions for coefficient convention, strong convergence, and naturality.

A disposable proof search confirms that these defects make the literal target
inhabitable using a zero spectral-sequence container, reflexive or zero-object
isomorphisms, and output-selected `True` propositions. That term constructs
no mathematical AHSS and consumes none of the four semantic root-cut
packages. It is deliberately neither retained nor credited because it would
be a fake or substituted result under the rev-5.6 statement-fidelity and
child-composition gates.

The structured authorities are also not proof-ready. `instance.json` remains
`planned` with null canonical formal identity fields. The local
`task-dag.json` is unfrozen and marks proof `blocked_by_predecessors`.
Registry v1 has planned fingerprints for substantive branches, while the
global obligation-tree predecessor is only worker-provisional rather than
master-accepted. This proof-only worker cannot repair those predecessor
authorities.

## Pinned Search

Pinned mathlib provides the generic `SpectralSequence` container,
`E2CohomologicalSpectralSequence`, CW skeleton APIs, and singular homology. A
recursive pinned-package search found no AHSS, generalized-cohomology,
exact-couple, or strong-convergence terminal theorem. Moreover,
`Mathlib/Algebra/Homology/SpectralObject/SpectralSequence.lean` still marks
the intended `spectralSequence`, `homologyData`, and
`spectralSequenceHomologyData` constructors as `TODO`.

`DifferentialProbe.lean` separately confirms by `rfl` that the literal
bidegree relation is inhabited. It does not close `M0554-B-DIFFERENTIAL`,
whose frozen registry child `M0554-C-SPECTRAL` is open, and it is not credited
as a composed proof.

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
| `python3 Stage1_Instances/THM-M-0554/check_obligation_tree.py` | 0 | `PASS THM-M-0554 obligation tree: 32 obligations, 91 typed edges`; denominator `3c72072a...8048b`; root remains open at `M4` with no composition certificate. |
| `timeout -k 2 60 lake env lean --version` from `Formalizations/Lean` | 0 | Lean 4.29.0 commit `98dc76e3...16740`; the required pinned environment is available. |
| Isolated `lake env lean --trust=0 -t0` replay of `Statement.lean`, `Proof.lean`, and `DifferentialProbe.lean` | 0 | Objects were 429072, 280728, and 15576 bytes. Log SHA-256 values were `f1690fd1...d30`, `8cfbfe08...2a1`, and `30cba6d3...156`. The three conditional proof declarations were sorry-free and reported exactly `propext`, `Classical.choice`, and `Quot.sound`. |
| Pinned-package AHSS/generalized-cohomology/exact-couple/strong-convergence `rg` scan | 1 | Expected no-match: no terminal proof candidate exists in the pinned packages. |
| Prohibited-device scan over owned Lean sources | 1 | Expected no-match: no `sorry`, `admit`, `axiom`, `sorryAx`, unsafe declaration, bodyless declaration, or equivalent escape. |
| SHA-256 and TODO scan of `Mathlib/Algebra/Homology/SpectralObject/SpectralSequence.lean` | 0 | SHA-256 `2ce62b9d...740aa`; intended constructors remain documented as TODO. |
| `git diff --quiet 80f0191c...HEAD --` over the ten proof-relevant inputs | 0 | Statement, proof, diagnostic, structured statement, audit, registry, graphs, validation specs, instance, and local DAG are unchanged; current HEAD adds blocker evidence only. |
| `python3 -m json.tool` plus scoped `jq -e` assertions on the companion JSON | 0 | The packet parsed; item/theorem/base identity, blocked state, exact root cut, empty closure/receipt arrays, and false completion/self-test flags agreed. |
| `find Stage1_Instances/THM-M-0554 -maxdepth 1 -name '*.json' -print0 \| xargs -0 -n1 jq empty` | 0 | Every top-level owned JSON artifact parsed. |
| `git diff --check` plus `git diff --no-index --check /dev/null` on both new artifacts | 0 | No whitespace diagnostic after normalizing the expected no-index content-difference statuses. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Self-test manifest absent because the assigned proof phase is blocked. |

The isolated Lean recipe, run from the repository root, was:

```bash
set -uo pipefail
repo=$PWD
target=$repo/Stage1_Instances/THM-M-0554
lean_root=$repo/Formalizations/Lean
tmp=$(mktemp -d /tmp/thm-m-0554-proof-9d3f687e-slot17.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
lean=$(cd "$lean_root" && lake env which lean)
lean_path=$(cd "$lean_root" && lake env printenv LEAN_PATH)
cd "$target"
LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" timeout 300 "$lean" --trust=0 -t0 \
  -R "$target" -o "$tmp/Statement.olean" Statement.lean
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" timeout 300 "$lean" --trust=0 -t0 \
  -R "$target" -o "$tmp/Proof.olean" Proof.lean
LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" timeout 300 "$lean" --trust=0 -t0 \
  -R "$target" -o "$tmp/DifferentialProbe.olean" DifferentialProbe.lean
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
