# THM-M-0554 proof-phase recheck: blocked

Item: `S56-M-0554-PROOF`

Attempt: `2026-07-15T08:43:21+08:00`

Base revision: `8b9311952b6b4186c774d25758d16597a7c10a8b`

Base tree: `69a7cea0132f4b76e7324c2d5cc320dec94d2f10`

## Verdict

`blocked`. The current base now contains real, sorry-free conditional
composition bodies in `Proof.lean`, but it still contains no genuine
Atiyah-Hirzebruch spectral-sequence branch construction or proof of the
unconditioned root. No frozen obligation closes, the root remains `M4`, and
this recheck adds no proof receipt, state transition, or completion claim.

`dataOfBranches` consumes every field of explicit E2, differential,
convergence, and naturality packages. `statementShapeOfBranches` packages the
result, and `statementOfBranchFamily` derives the literal root only from a
premise supplying the complete branch family for every quantified input. This
is legitimate conditional recomposition, not an AHSS construction. Since all
four child branches remain open, rev-5.6 section 6.7 forbids parent closure.

The immediate root cut remains:

- `M0554-X-GENCOH`: generalized-cohomology pair, excision, and wedge infrastructure;
- `M0554-C-EXACT-COUPLE`: the skeletal-filtration exact-couple construction;
- `M0554-C-E2-MODEL`: the cellular-cohomology `E2` identification;
- `M0554-L-STRONG`: strong convergence for the finite skeletal filtration.

A fresh pinned-package search found no AHSS, generalized-cohomology,
exact-couple, or strong-convergence proof body. Mathlib supplies only the
generic spectral-sequence container and supporting topology. Its spectral-
object source still documents `spectralSequence`, `homologyData`, and
`spectralSequenceHomologyData` as `TODO`.

## First Failed Gate

Exact-statement fidelity fails before root proof credit is possible. The
canonical claim requires a reduced generalized cohomology theory and a genuine
finite-CW structure, but reducedness is absent from the frozen interface. The
theory fields `pointIsPoint`, `exactnessAxiom`, and
`wedgeAxiomOrRepresentability`, and the CW fields `finiteCW`, `exhaustive`, and
`cellAttachments`, store propositions rather than evidence. The output freely
chooses `coefficientConvention`, `strongConvergence`, and
`naturalityInSpace`, while `filtrationIsInducedBy` is merely
`K.skeleton = K.skeleton`.

Consequently the literal proposition admits a zero spectral-sequence and
`True` witness without constructing the mathematical AHSS. That candidate is
deliberately not retained or credited: it would be a fake result and closes
none of the frozen semantic children. The checked conditional composition in
`Proof.lean` avoids that exploit but necessarily leaves the missing branch
family as an explicit premise.

The dossier authorities are also unreconciled. The global obligation-tree
item is provisional (`[_]`), `instance.json` remains `planned` with null
canonical-formal identity fields, and the local intake DAG is unfrozen and
marks proof blocked by predecessors. In addition, `statement.json` refers to a
legacy convergence-data declaration rather than the owned
`Stage1.THM_M_0554.AtiyahHirzebruchData`. A proof-only worker cannot silently
repair those predecessor artifacts.

## Validation

All Lean commands reused the automation-provided symlink to the canonical
pinned `.lake` artifacts. No update, build, dependency clone/fetch, network
action, or `.lake` mutation was performed. Generated Lean output was placed in
a temporary directory and removed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0554` | 0 | Rank 106; lifecycle `planned`; baseline `L0/rework_required`; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0554/check_obligation_tree.py` | 0 | 32 obligations and 91 typed edges passed; denominator `3c72072a...8048b`; root remains M4 without a composition certificate. |
| Isolated pinned `lean --trust=0 -t0` replay of `Statement.lean`, then `Proof.lean` with temporary `LEAN_PATH` | 0 | Both files elaborated with Lean 4.29.0; temporary objects were 429072 and 280728 bytes. All three proof declarations reported exactly `propext`, `Classical.choice`, and `Quot.sound`, and all were sorry-free. Captured output was 888 bytes with SHA-256 `0f07d766...8758`. |
| Pinned-package AHSS/generalized-cohomology/exact-couple/convergence scan | 1 | Expected no-match result: no terminal proof candidate exists in the pinned package closure. |
| Prohibited-device scan over owned Lean files | 1 | Expected no-match result: no `sorry`, `admit`, `axiom`, `sorryAx`, bodyless `constant`/`opaque`, unsafe/oracle, or equivalent device. |
| Lean/Lake and mathlib revision/tree/status checks | 0 | Lean `4.29.0` commit `98dc76e...16740`; Lake `5.0.0-src+98dc76e`; mathlib `8a178386...ea95`, tree `bdc39a31...1c2b`, clean. |
| Spectral-object source hash and `TODO` scan | 0 | SHA-256 `2ce62b9d...740aa`; the intended spectral-sequence and homology-data constructors remain documented as `TODO`. |
| `git diff --quiet 4ba3f2fd..HEAD` over the eight canonical target inputs | 0 | Statement, registry, graph, validation, instance, and task inputs are unchanged across the `Proof.lean` integration. |
| `python3 -m json.tool` plus scoped `jq -e` assertions on the companion JSON | 0 | The packet parsed and its identity, blocked state, empty closure arrays, four-node root cut, and false completion flags agreed. |
| `git diff --check` plus no-index whitespace checks for both new artifacts | 0 | No whitespace diagnostic; each no-index command returned only the expected content-difference status 1. |
| `test ! -e .stage1-worker-selftest.json` | 0 | The self-test manifest is absent because the proof phase is blocked. |

The isolated Lean recipe, run from the repository root, was:

```bash
set -euo pipefail
repo=$PWD
target=$repo/Stage1_Instances/THM-M-0554
lean_root=$repo/Formalizations/Lean
tmp=$(mktemp -d /tmp/thm-m-0554-proof-slot22.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
lean=$(cd "$lean_root" && lake env which lean)
lean_path=$(cd "$lean_root" && lake env printenv LEAN_PATH)
cd "$target"
LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" timeout 300 "$lean" --trust=0 -t0 \
  -R "$target" -o "$tmp/Statement.olean" Statement.lean
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" timeout 300 "$lean" --trust=0 -t0 \
  -R "$target" -o "$tmp/Proof.olean" Proof.lean
```

## Retry Condition

First publish and master-accept a source-faithful corrected statement,
reconcile the instance, task, and statement projections, and issue obligation-
registry version 2 with exact branch fingerprints. Then construct and compose
the four root-cut packages without placeholders. An alternative is an
immutable compatible Lean 4 AHSS proof that can be pinned, exact-type
transported, and checked with complete provenance, trust, and composition
closure.

This packet is durable blocker evidence only. It does not satisfy
`S56-M-0554-PROOF`, close an obligation, complete the audit or theorem, or
authorize master acceptance. Because the assigned phase is not genuinely
self-tested as complete, `.stage1-worker-selftest.json` remains absent.
