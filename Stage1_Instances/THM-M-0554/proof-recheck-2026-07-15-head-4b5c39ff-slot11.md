# THM-M-0554 proof phase blocked at `4b5c39ff`

Item: `S56-M-0554-PROOF`

Recheck time: `2026-07-15T19:21:38+08:00`

Base revision: `4b5c39ffcc0e35a8509d4216af53c7cdeb190c7b`

Base tree: `e569e54769b7b5aab913ec248c533231658657f0`

## Verdict

`blocked`. No source-faithful Atiyah-Hirzebruch spectral-sequence proof body
exists in the repository or pinned dependency closure. The root stays
`[H3, M4, R4]`; no obligation, composition certificate, proof receipt, or
item state changes.

The first failed gate is
`S56-5.1-EXACT-TARGET-CONSISTENCY / M0554-S-DATA`. The frozen Lean output can
be inhabited without constructing the canonical mathematical AHSS. A fresh
temporary trust-zero probe constructed a zero spectral-sequence container,
defined `ordinaryCohomology` from that same zero page so its `E2` isomorphism
was reflexive, used an unrelated coefficient-zero object for all filtration
families, and selected `True` for the output propositions. Its exact literal
root declaration elaborated, was sorry-free, and reported only `propext`,
`Classical.choice`, and `Quot.sound`.

That term was deleted and receives no proof credit. It proves only that the
frozen encoding is too weak. It does not identify
`E2^{p,q}` with `H^p(X; E^q(pt))`, construct the skeletal filtration, prove
strong convergence, or establish naturality. Retaining it would be a fake
result and would bypass every required child in the frozen proof graph.

Specifically, reducedness is absent; `pointIsPoint`, `exactnessAxiom`,
`wedgeAxiomOrRepresentability`, `finiteCW`, `exhaustive`, and
`cellAttachments` are proposition-valued data rather than evidence;
`ordinaryCohomology` is unconstrained; `coefficientConvention`,
`strongConvergence`, and `naturalityInSpace` are output-selected propositions;
and `filtrationIsInducedBy` is only `K.skeleton = K.skeleton`.

The existing `Proof.lean` declarations remain valid placeholder-free
conditional composition bodies. `statementOfBranchFamily` assumes the full
`E2`, differential, convergence, and naturality family and therefore does not
construct a missing branch. It cannot close a parent while those required
children remain open.

The genuine mathematical root cut remains:

- `M0554-X-GENCOH`: generalized-cohomology pair, excision, and wedge infrastructure;
- `M0554-C-EXACT-COUPLE`: the skeletal-filtration exact-couple construction;
- `M0554-C-E2-MODEL`: the cellular-cohomology `E2` identification;
- `M0554-L-STRONG`: strong convergence for the finite skeletal filtration.

Pinned mathlib contains generic spectral-sequence and nearby CW/homology
substrate only. Its spectral-object module still documents the intended
`spectralSequence`, `homologyData`, and `spectralSequenceHomologyData`
constructors as `TODO`.

Predecessor authority independently blocks acceptance. The global obligation
tree is provisional `[_]`, `instance.json` remains `planned` with null formal
identity fields, and the local `task-dag.json` is unfrozen and marks `PROOF`
`blocked_by_predecessors`.

At worker start, this target already contained 41 prior tracked proof JSON/Markdown
pairs while scheduler authority still recorded zero attempts and no children.
Those files are not an authoritative tick ledger, but repeated unchanged
dispatch is far beyond the five-unresolved-tick split threshold. Integration
must reconcile the ledger and redirect execution to statement repair rather
than schedule the unchanged proof root again.

## Validation

All Lean checks reused the automation-provided read-only symlink to canonical
pinned Lake artifacts. No `lake update`, `lake build`, dependency clone/fetch,
network action, checkout, or `.lake` mutation occurred. Generated objects and
the rejected diagnostic source lived under `/tmp` and were removed by a trap.
The untracked symlink makes this nonrelease evidence.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0554` | 0 | Rank 106; lifecycle `planned`; baseline `L0/rework_required`; legacy artifacts unaccepted; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0554/check_obligation_tree.py` | 0 | `PASS`: 32 obligations and 91 typed edges; denominator `3c72072a...8048b`; root remains open at `M4` with no composition certificate or proof closure. |
| Isolated pinned `lean --trust=0 -t0` replay below | 0 | `Statement.lean`, `Proof.lean`, `DifferentialProbe.lean`, and the temporary defect probe elaborated. Existing and temporary declarations were sorry-free and reported exactly `propext`, `Classical.choice`, and `Quot.sound`. |
| Scoped prohibited-declaration scan | 1 | Expected no-match: no placeholder, bodyless declaration, unsafe declaration, `implemented_by`, or `extern` occurs; axiom output contains no `sorryAx`. |
| Pinned-package AHSS/generalized-cohomology/exact-couple/convergence scan | 1 | Expected no-match: zero matching source lines and no terminal proof candidate. |
| Equivalent repo-local scan outside this dossier and `.lake` | 0 | 159 lines, SHA-256 `f3fcfa5d...f303`; target-specific hits are legacy interfaces and blocker gates, not a terminal body. |
| Lean/Lake and manifest package audit | 0 | Lean `4.29.0` commit `98dc76e...16740`; Lake `5.0.0-src+98dc76e`; all 11 package worktrees clean at recorded revisions; mathlib `8a178386...ea95`, tree `bdc39a31...1c2b`. |
| SHA-256 and `TODO` scan of mathlib spectral-object source | 0 | SHA-256 `2ce62b9d...740aa`; all three intended constructors remain documented as `TODO`. |
| `git diff --quiet 8b931195...HEAD --` over ten proof-relevant inputs | 0 | No proof-relevant source or structured-input delta. |

The isolated Lean recipe, run from the repository root, was:

```bash
set -euo pipefail
repo=$PWD
target=$repo/Stage1_Instances/THM-M-0554
lean_root=$repo/Formalizations/Lean
tmp=$(mktemp -d /tmp/thm-m-0554-slot11-4b5c39ff.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
lean=$(cd "$lean_root" && lake env which lean)
lean_path=$(cd "$lean_root" && lake env printenv LEAN_PATH)
cp "$target/Statement.lean" "$target/Proof.lean" \
  "$target/DifferentialProbe.lean" "$tmp/"
# StatementDefectProbe.lean was generated only in $tmp and was deleted.
cd "$tmp"
LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" timeout --foreground 300 \
  "$lean" --trust=0 -t0 -o Statement.olean Statement.lean
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" timeout --foreground 300 \
  "$lean" --trust=0 -t0 -o Proof.olean Proof.lean
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" timeout --foreground 300 \
  "$lean" --trust=0 -t0 -o DifferentialProbe.olean DifferentialProbe.lean
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" timeout --foreground 300 \
  "$lean" --trust=0 -t0 -o StatementDefectProbe.olean \
  StatementDefectProbe.lean
```

The important evidence digests are:

- `Statement.olean`: `46d2fc1b505a12e1f1004ee3411f771f972e6c8393cd5e6e35843dc103ef9ded`;
- existing proof output: `8cfbfe08991a8a319a2a3a003e890b38e0c094dcf5971f158f65b3cb54c172a1`;
- discarded defect-probe source: `ea70d45d883bcd6fc3444df94df37acce2e22b7b6652d62708689ac66c0bb4be`;
- defect-probe output: `57e8b80df878a620d9e5a28259e920a57e5dae0b7f10701bfedb2f6e3981e73c`.

## Retry Condition

Do not reschedule the unchanged proof root. Publish and master-accept a
source-faithful statement that encodes reducedness, inhabited theory/CW
hypotheses, actual ordinary cohomology coefficients, filtration provenance,
convergence, and naturality. Reconcile instance/task/statement authority and
issue obligation-registry version 2 with exact branch fingerprints. Then
implement the genuine four-package root cut. Alternatively, pin an immutable
exact compatible Lean 4 AHSS proof and pass canonical mapping, provenance,
trust, and composition gates.

This packet is blocker evidence only. It does not satisfy
`S56-M-0554-PROOF`, close an obligation, complete the audit or theorem, or
authorize validation, release, or master acceptance. Because the proof phase
is incomplete, `.stage1-worker-selftest.json` remains absent.
