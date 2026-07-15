# THM-M-1234 proof recheck at `6ee4e043` (slot17)

Item: `S56-M-1234-PROOF`

Intent: `prove`

Recorded: `2026-07-15T20:33:31+08:00`

Base revision: `6ee4e043011799c8a8d6f7f5a2b68dd5fb819679`

Base tree: `8e7811b64a8ad5298ec20aa3f40898f299dce655`

## Verdict

`blocked`. No placeholder-free body for the exact universal declaration
`Stage1Rev56.THMM1234.Statement` exists in the repository or the available
pinned dependency closure. The root remains `[H1, M3, R3]`; this packet does
not satisfy the proof item, propose `[_]`, or claim theorem completion.

The first failed gate is dependency legality. `S56-M-1234-OBLIGATION_TREE`
is worker-provisional `[_]`, not master-accepted `[x]`. Its typed graph names
`M1234-ROOT` as the root but has no node with that ID, all 14 validation
recipes omit required structured fields, and its proof interfaces do not
consume the frozen analytic children. In particular,
`CandidateConstructionPackage` is inhabited by constant-in-time initial
fields, while `EquationAndTraceClosurePackage` quantifies over every unrelated
`CandidateFields` witness.

Independently of that predecessor failure, the exact analytic root is open.
`Proof.lean` proves only the zero-data boundary case.
`ConstructionProof.lean` proves only the under-specified construction package
and a trace for one constant candidate. `ObligationTree.lean` composes the root
only after receiving both package proofs. `ClosurePackageDiagnostic.lean`
shows that the universally quantified closure package would force arbitrary
admissible initial velocity and vorticity test pairings to vanish when applied
to zero candidate fields; it does not prove that package or the root.

The legacy `Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_158.lean` contains
interfaces and audit records, not a terminal Yudovich proof. A search over all
9,042 available pinned package Lean sources found no Yudovich, incompressible
Euler, bounded-vorticity, or Biot-Savart terminal candidate. Closing the root
therefore requires a genuine global Euler approximation, uniform estimates,
nonlinear-compatible compactness, weak-momentum limit, and initial-trace
formalization, or an immutable exact compatible external theorem.

## Validation

All Lean checks reused the automation-provided canonical pinned `.lake`
artifacts read-only. No `lake update`, `lake build`, dependency clone/fetch,
network access, or `.lake` mutation occurred. Sources were copied to a fresh
temporary directory under `Formalizations/Lean`, checked with the Lake-selected
Lean binary at trust level zero, and removed. The pre-existing untracked
`.lake` symlink makes this nonrelease evidence.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets at ranks 1 through 1546, all `L0/rework_required`, passed. |
| `python3 scripts/stage1_target.py show THM-M-1234` | 0 | Rank 158; planned lifecycle; hard mathlib-anchor lane; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1234/check_obligation_tree.py` | 0 | 14 obligations and 28 typed edges passed; denominator `cfa0a02c68993c8b3eefc0edfe7d3d7bd20e2b58d140f47a1f5444a8ba734c5d`; root open at M3 and both analytic packages M4. The checker does not reject the typed-root or recipe defects. |
| Trust-zero isolated replay below | 0 | `Statement`, `AnchorAudit`, `ObligationTree`, `ConstructionProof`, `Proof`, and `ClosurePackageDiagnostic` elaborated. Printed declarations reported only `propext`, `Classical.choice`, and `Quot.sound`; two nonfatal `unnecessarySimpa` warnings appeared. |
| Prohibited-device scan over owned `*.lean` | 1 | Expected no-match exit: no `sorry`, `admit`, declared axiom, unsafe/opaque/extern escape, `sorryAx`, `implemented_by`, or `native_decide` was found. |
| Exact-topic scan over pinned package `*.lean` | 1 | Expected no-match exit over 9,042 files: no exact-topic candidate was found. |
| Structured predecessor diagnostic | 0 | `root_node_id=M1234-ROOT` is absent from `nodes[].node_id`; all 14 recipes lack required structured fields. |
| `jq empty Stage1_Instances/THM-M-1234/*.json` | 0 | Every pre-existing owned JSON artifact parsed before this packet was added. |

The successful narrow replay was:

```bash
set -euo pipefail
root=$PWD
tmp=$(mktemp -d "$root/Formalizations/Lean/.thm-m-1234-proof-6ee4e043-slot17.XXXXXX")
trap 'rm -rf "$tmp"' EXIT
cp Stage1_Instances/THM-M-1234/{Statement,AnchorAudit,ObligationTree,ConstructionProof,Proof,ClosurePackageDiagnostic}.lean "$tmp"/
lean=$(cd Formalizations/Lean && lake env which lean)
lean_path=$(cd Formalizations/Lean && lake env printenv LEAN_PATH)
export LEAN_NUM_THREADS=1
cd "$tmp"
LEAN_PATH="$lean_path" timeout --foreground 600 "$lean" --trust=0 -t0 -o Statement.olean Statement.lean
LEAN_PATH="$tmp:$lean_path" timeout --foreground 600 "$lean" --trust=0 -t0 AnchorAudit.lean
LEAN_PATH="$tmp:$lean_path" timeout --foreground 600 "$lean" --trust=0 -t0 -o ObligationTree.olean ObligationTree.lean
LEAN_PATH="$tmp:$lean_path" timeout --foreground 600 "$lean" --trust=0 -t0 ConstructionProof.lean
LEAN_PATH="$tmp:$lean_path" timeout --foreground 600 "$lean" --trust=0 -t0 Proof.lean
LEAN_PATH="$tmp:$lean_path" timeout --foreground 600 "$lean" --trust=0 -t0 ClosurePackageDiagnostic.lean
```

It produced `Statement.olean` SHA-256
`1709e38a5b8cc96159b7042585666cb84536b4b3d9e26a63697992cd9820d308`
and `ObligationTree.olean` SHA-256
`2521d53bc0b3ea2c9d0b7e7bcae9854ebe5081fc0cecd39a8a5fdfdf4324fc50`.

## Retry Condition

The master/scheduler must stop rescheduling this unchanged oversized node,
reconcile 33 integrated structured proof packets against the authoritative
attempt count of zero, and split the work as required after five unresolved
ticks. First reopen the predecessor and publish an append-only registry update
with child-consuming analytic interfaces, closure tied to the specifically
constructed candidate, a valid typed root, and node-specific structured
recipes. Then implement the approximation, energy, compactness, linear and
nonlinear limit, momentum, and trace leaves without placeholders. Pinning an
immutable exact Lean 4 theorem is an alternative only after exact-type,
provenance, trust, and composition checks.

Because the assigned universal proof phase is not genuinely self-tested as
complete, `.stage1-worker-selftest.json` is deliberately absent.
