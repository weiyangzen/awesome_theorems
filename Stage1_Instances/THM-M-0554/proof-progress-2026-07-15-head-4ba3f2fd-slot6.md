# THM-M-0554 proof progress at `4ba3f2fd` (slot 6)

Item: `S56-M-0554-PROOF`

Attempt: `2026-07-15T08:28:41+08:00`

Base revision: `4ba3f2fd1e609b5958f24e0415eef9300da16924`

Base tree: `6abc1f64758c17a59dad8c80ac44f238983dc720`

## Verdict

`blocked`, with kernel-checked partial composition progress. `Proof.lean` now
defines four disjoint branch packages matching every field of the literal
`AtiyahHirzebruchData` output and checks their field-for-field recomposition,
`Nonempty` packaging, and conditional abstraction to the exact frozen
`Statement`.

The branch family is an explicit premise. No branch is asserted, no AHSS is
constructed, and no frozen obligation or root is claimed closed. This is not
a proof-phase self-test and no worker self-test manifest is emitted.

The proof bodies provisionally implement only the conditional composition
route associated with:

- `M0554-B-RECOMPOSE`: all four branch packages are consumed without dropping
  an output field;
- `M0554-T-DATA`: the fields are assembled into one exact data record;
- `M0554-T-INHABIT`: that record is packaged as the frozen `StatementShape`;
- `M0554-T-ROOT`: a family of such packages yields the exact literal root.

These nodes remain open because every required child branch remains open and
the predecessor obligation registry is only provisional. The accepted state,
root vector, and exact four-node root cut are unchanged.

## Remaining blocker

The first failed gate is still exact-statement fidelity. The selected human
claim requires a reduced generalized cohomology theory and a genuine finite
CW structure. The frozen Lean interface instead stores `pointIsPoint`,
`exactnessAxiom`, `wedgeAxiomOrRepresentability`, `finiteCW`, `exhaustive`, and
`cellAttachments` as unevidenced proposition-valued fields. Its output chooses
bare propositions for `coefficientConvention`, `strongConvergence`, and
`naturalityInSpace`, and its filtration field is the tautology
`K.skeleton = K.skeleton`.

Consequently a zero spectral-sequence and output-selected `True` propositions
inhabit the literal target without constructing the mathematical AHSS. That
diagnostic term is deliberately not retained or credited. `Proof.lean`
instead leaves all substantive branch data as premises, so it cannot exploit
the defect to manufacture a completion result.

The immediate root cut remains:

- `M0554-X-GENCOH`: generalized-cohomology pair, excision, and wedge infrastructure;
- `M0554-C-EXACT-COUPLE`: the skeletal-filtration exact-couple construction;
- `M0554-C-E2-MODEL`: the cellular-cohomology `E2` identification;
- `M0554-L-STRONG`: strong convergence for the finite skeletal filtration.

Pinned mathlib supplies generic spectral-sequence, CW-complex, and singular-
homology substrate only. No pinned terminal AHSS body was found, and mathlib's
spectral-object source still documents its intended constructors as `TODO`.
The local `DifferentialProbe.lean` remains an uncomposed diagnostic because it
does not consume the required `M0554-C-SPECTRAL` child.

Predecessor authority is also unresolved: the global obligation-tree item is
`[_]`, `instance.json` still has null canonical-formal identity fields, and
the local `task-dag.json` is unfrozen with proof blocked by predecessors. This
proof-only packet does not rewrite any of those authorities.

## Validation

All Lean checks reused the automation-provided symlink to the canonical pinned
Lake artifacts. No update, build, dependency clone/fetch, network action, or
`.lake` mutation was performed. Lean output was written to a temporary
directory and removed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0554` | 0 | Rank 106; lifecycle `planned`; baseline `L0/rework_required`; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0554/check_obligation_tree.py` | 0 | 32 obligations and 91 typed edges passed; denominator `3c72072a...8048b`; root remains `M4` with no composition certificate or proof closure. |
| Isolated pinned `lean --trust=0 -t0` recipe below | 0 | `Statement.lean` and `Proof.lean` elaborated with Lean 4.29.0; temporary objects were 429072 and 280728 bytes. |
| `#print axioms` for the three proof declarations | 0 | Each reported exactly `propext`, `Classical.choice`, and `Quot.sound`. |
| `#print sorries` for the three proof declarations | 0 | Each reported `Declarations are sorry-free!`. |
| Pinned-package AHSS/generalized-cohomology/exact-couple/convergence scan | 1 | Expected no-match result: no terminal proof candidate in the pinned package closure. |
| Prohibited-device scan over owned Lean files | 1 | Expected no-match result: no `sorry`, `admit`, `axiom`, `sorryAx`, unsafe/oracle, or equivalent device. |
| Lean/Lake and mathlib revision/tree/status checks | 0 | Lean `4.29.0` commit `98dc76e...16740`; Lake `5.0.0-src+98dc76e`; mathlib `8a178386...ea95`, tree `bdc39a31...1c2b`, clean. |

The isolated Lean recipe, run from the repository root, was:

```bash
set -euo pipefail
repo=$PWD
target=$repo/Stage1_Instances/THM-M-0554
lean_root=$repo/Formalizations/Lean
tmp=$(mktemp -d /tmp/thm-m-0554-proof-progress.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
lean=$(cd "$lean_root" && lake env which lean)
lean_path=$(cd "$lean_root" && lake env printenv LEAN_PATH)
cd "$target"
LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" timeout 300 "$lean" --trust=0 -t0 \
  -R "$target" -o "$tmp/Statement.olean" Statement.lean
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" timeout 300 "$lean" --trust=0 -t0 \
  -R "$target" -o "$tmp/Proof.olean" Proof.lean
```

## Retry condition

First publish and master-accept a source-faithful corrected statement,
reconcile the instance/task/statement authorities, and issue obligation-
registry version 2 with exact elaborated branch fingerprints. Then construct
and compose the four root-cut packages without placeholders. Alternatively,
pin an immutable compatible Lean 4 AHSS proof and pass exact-type, provenance,
trust, and composition checks.

This packet preserves real partial proof bodies but does not satisfy
`S56-M-0554-PROOF`, propose `[_]`, close an obligation, complete the audit or
theorem, or authorize master acceptance. `.stage1-worker-selftest.json`
remains absent.
