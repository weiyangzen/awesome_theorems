# THM-M-0554 proof-phase recheck: blocked

Item: `S56-M-0554-PROOF`

Intent: `prove`

Recheck time: `2026-07-15T08:56:29+08:00` through
`2026-07-15T08:56:36+08:00`

Base revision: `f94e9d38903a8428e13b050f044d57ef76fc65ed`

Base tree: `3aa6f6cbea0f08da6762c671d71e89e864f21cd1`

## Verdict

`blocked`. No exact Atiyah-Hirzebruch spectral-sequence proof body exists in
the pinned dependency closure, and this proof-only worker cannot truthfully
manufacture one from the frozen target. The root remains `M4`; no frozen
obligation closes and no composition certificate or proof receipt is claimed.

The existing `Proof.lean` contains real, placeholder-free conditional
composition bodies:

- `Stage1.THM_M_0554.Proof.dataOfBranches` consumes the four branch packages
  field by field and returns `AtiyahHirzebruchData`;
- `Stage1.THM_M_0554.Proof.statementShapeOfBranches` packages that data as the
  literal `StatementShape`;
- `Stage1.THM_M_0554.Proof.statementOfBranchFamily` quantifies the binders and
  returns the literal `Statement`.

These declarations elaborate at trust level zero and are sorry-free, but the
last theorem retains the complete family of E2, differential, convergence,
and naturality packages as an explicit premise. They therefore implement only
conditional child-to-parent assembly and cannot close a parent whose required
children remain open. The frozen registry also gives those composition nodes
planned rather than elaborated fingerprints.

The immediate root cut is unchanged:

- `M0554-X-GENCOH`: generalized-cohomology pair, excision, and wedge infrastructure;
- `M0554-C-EXACT-COUPLE`: the skeletal-filtration exact-couple construction;
- `M0554-C-E2-MODEL`: the cellular-cohomology E2 identification;
- `M0554-L-STRONG`: strong convergence for the finite skeletal filtration.

Pinned mathlib supplies the generic spectral-sequence container, CW-complex
substrate, and singular homology only. A fresh scan of every pinned package
found no AHSS, generalized-cohomology, exact-couple, or strong-convergence
terminal body. Mathlib's spectral-object source still describes the intended
`spectralSequence`, `homologyData`, and `spectralSequenceHomologyData`
constructors as `TODO`.

## First Failed Gate

Exact-statement fidelity fails before positive root proof credit. The intended
claim is the cohomological AHSS for a reduced generalized cohomology theory on
a finite CW complex. The frozen interface does not encode reducedness, and
stores `pointIsPoint`, `exactnessAxiom`, `wedgeAxiomOrRepresentability`,
`finiteCW`, `exhaustive`, and `cellAttachments` as proposition-valued data
without proofs. The output selects bare propositions for
`coefficientConvention`, `strongConvergence`, and `naturalityInSpace`, while
`filtrationIsInducedBy` is only `K.skeleton = K.skeleton`.

As earlier checked blocker evidence records, a zero spectral-sequence and
output-selected `True` fields can therefore inhabit the literal target. That
term constructs no mathematical AHSS, closes none of the four root-cut
packages, and would be a fake result under the exact-statement and
child-to-parent gates. It was neither retained nor credited here.

Predecessor authority is independently open. The global obligation-tree item
is only worker-provisional (`[_]`), `instance.json` still has null canonical
module/expression/fingerprint/environment fields with
`open_statement_phase`, and the local `task-dag.json` is unfrozen with proof
blocked by predecessors. This proof-only packet does not rewrite those
authorities.

## Validation

All Lean commands reused the automation-provided symlink to the canonical
pinned Lake artifacts. No update, build, dependency clone/fetch, network
operation, or `.lake` mutation ran. Lean objects and logs were written to a
fresh temporary directory and removed by a trap.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0554` | 0 | Rank 106; lane `frontier_deep_formalization_debt`; lifecycle `planned`; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0554/check_obligation_tree.py` | 0 | 32 obligations and 91 typed edges passed; denominator `3c72072a...8048b`; root remains open at `M4`, with no composition certificate or proof closure credited. |
| Isolated pinned `lean --trust=0 -t0` recipe below | 0 | `Statement.lean` and `Proof.lean` elaborated with Lean 4.29.0; temporary objects were 429072 and 280728 bytes. |
| `#print axioms` for all three conditional proof declarations | 0 | Each reported exactly `propext`, `Classical.choice`, and `Quot.sound`. |
| `#print sorries` for all three conditional proof declarations | 0 | Each reported `Declarations are sorry-free!`. |
| `rg` AHSS/generalized-cohomology/exact-couple/strong-convergence query over `Formalizations/Lean/.lake/packages` | 1 | Expected no-match result: no pinned terminal proof candidate. |
| Prohibited-device scan over owned Lean sources | 1 | Expected no-match result: no `sorry`, `admit`, `sorryAx`, bodyless declaration, `unsafe`, oracle, or equivalent escape. |
| `jq empty Stage1_Instances/THM-M-0554/*.json` | 0 | Every pre-existing owned JSON artifact parsed. |
| `git diff --check -- Stage1_Instances/THM-M-0554 .stage1-worker-selftest.json` | 0 | No tracked-diff whitespace diagnostics. |
| `test ! -e .stage1-worker-selftest.json` | 0 | The completion manifest is absent because this proof phase is blocked. |

The isolated Lean recipe, run from the repository root, was:

```bash
set -uo pipefail
repo=$PWD
target=$repo/Stage1_Instances/THM-M-0554
lean_root=$repo/Formalizations/Lean
tmp=$(mktemp -d /tmp/thm-m-0554-proof-f94e9d38-slot17.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
lean=$(cd "$lean_root" && lake env which lean)
lean_path=$(cd "$lean_root" && lake env printenv LEAN_PATH)
cd "$target"
LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" timeout 300 "$lean" --trust=0 -t0 \
  -R "$target" -o "$tmp/Statement.olean" Statement.lean \
  > "$tmp/statement.log" 2>&1
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" timeout 300 "$lean" --trust=0 -t0 \
  -R "$target" -o "$tmp/Proof.olean" Proof.lean \
  > "$tmp/proof.log" 2>&1
```

Both commands exited `0`. The statement log was 482 bytes with SHA-256
`f1690fd11232bafbe452f7a63a140204ae23ca3a0f90e0126f4b22dacfd54d30`.
The proof log was 406 bytes with SHA-256
`8cfbfe08991a8a319a2a3a003e890b38e0c094dcf5971f158f65b3cb54c172a1`.

## Retry Condition

First publish and master-accept a source-faithful statement, reconcile the
instance/task/statement authorities, and issue obligation-registry version 2
with exact branch fingerprints. Then construct and compose all four root-cut
packages without placeholders. Alternatively, pin an immutable compatible
Lean 4 AHSS proof and pass exact-type, provenance, trust, and composition
checks.

This is durable current-base blocker evidence only. It does not satisfy
`S56-M-0554-PROOF`, propose `[_]`, close an obligation, complete the audit or
theorem, or authorize master acceptance. Because the assigned phase is not
genuinely self-tested as complete, `.stage1-worker-selftest.json` remains
absent.
