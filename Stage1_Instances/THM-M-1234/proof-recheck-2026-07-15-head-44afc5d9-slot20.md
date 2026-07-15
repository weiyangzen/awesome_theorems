# THM-M-1234 proof recheck at `44afc5d9` (slot20)

Item: `S56-M-1234-PROOF`

Intent: `prove`

Recorded: `2026-07-15T21:07:25+08:00`

Base revision: `44afc5d93ff24855c0f4cc5ae48f4b6be094a08e`

Base tree: `4fbba127c10efa3d76cb99767630cf3034a84ada`

## Verdict

`blocked`. The exact universal declaration
`Stage1Rev56.THMM1234.Statement` still has no repo-local or pinned proof body.
The root remains `[H1, M3, R3]`; this packet does not satisfy the proof item,
propose `[_]`, or claim theorem completion.

The first failed gate is dependency legality. The assigned proof item depends
on `S56-M-1234-OBLIGATION_TREE`, but that predecessor remains
worker-provisional `[_]`, not master-accepted `[x]`. It is also not ready for
acceptance: `typed-graphs.json` refers to a nonexistent root node ID, all 14
validation recipes omit the required structured recipe fields, and the
construction/composition interface does not consume its frozen analytic
children.

Independently, the exact analytic proof is absent. `Proof.lean` closes only the
zero-data boundary case. `ConstructionProof.lean` inhabits the under-specified
construction interface with constant initial fields and proves their trace.
`ObligationTree.lean` derives the root only after receiving an
`EquationAndTraceClosurePackage`; no declaration proves that package or the
root. `ClosurePackageDiagnostic.lean` shows why this is not a sound shortcut:
the package ranges over every unrelated candidate, so applying it to zero
fields forces arbitrary admissible initial velocity and vorticity test
pairings to vanish. The diagnostic is conditional and does not prove package
inconsistency or the root.

The legacy `Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_158.lean` contains
interfaces and noncompletion audits, not a terminal proof. A source scan over
the available pinned packages found no Yudovich, Yudovitch, incompressible
Euler, bounded-vorticity, or Biot-Savart terminal candidate. The direct open
root cut remains `M1234-A-STRUCTURE` plus `M1234-E-CLOSURE`; its expanded
analytic work includes approximation, uniform estimates, nonlinear-compatible
compactness, structure preservation, momentum-limit passage, and the initial
trace.

## Validation

All checks reused the automation-provided canonical pinned `.lake` artifacts
read-only. No `lake update`, `lake build`, dependency clone/fetch, network
access, or `.lake` mutation occurred. Lean sources and generated objects were
confined to a fresh `/tmp` directory and removed. The pre-existing untracked
`.lake` symlink makes this nonrelease evidence.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and all 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets at ranks 1 through 1546, all `L0/rework_required`, passed. |
| `python3 scripts/stage1_target.py show THM-M-1234` | 0 | Rank 158; planned lifecycle; legacy artifacts unaccepted; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1234/check_obligation_tree.py` | 0 | 14 obligations and 28 typed edges passed; denominator `cfa0a02c68993c8b3eefc0edfe7d3d7bd20e2b58d140f47a1f5444a8ba734c5d`; root open at M3. This checker does not reject the root-ID or recipe defects. |
| Isolated trust-zero replay below | 0 | All six modules elaborated. Printed declarations reported only `propext`, `Classical.choice`, and `Quot.sound`; two nonfatal `unnecessarySimpa` warnings appeared. |
| Prohibited-device scan over owned `*.lean` | 1 | Expected no-match exit: no `sorry`, `admit`, declared axiom, unsafe/opaque/extern escape, `sorryAx`, `implemented_by`, or `native_decide` was found. |
| Exact-topic scan over pinned package `*.lean` sources | 1 | Expected no-match exit over 9,676 files; no exact-topic candidate was found. |
| Structured predecessor diagnostic | 0 | `root_node_id=M1234-ROOT` is absent from `nodes[].node_id`; all 14 recipes lack `cwd`, `argv`, `env_allowlist`, `timeout_seconds`, `expected_outputs`, `covered_obligation_ids`, and `covered_declarations`. |
| `python3 -m json.tool Stage1_Instances/THM-M-1234/proof-recheck-2026-07-15-head-44afc5d9-slot20.json >/dev/null` | 0 | The structured blocker packet parsed as JSON. |
| `jq empty Stage1_Instances/THM-M-1234/*.json` | 0 | Every owned JSON artifact parsed. |
| `git diff --check -- Stage1_Instances/THM-M-1234 .stage1-worker-selftest.json` | 0 | No tracked whitespace errors. |
| New-file `git diff --no-index --check` for this JSON and Markdown pair | 1 each | Expected new-file diff exits with no whitespace diagnostics. |
| `test ! -e .stage1-worker-selftest.json` | 0 | The completion self-test manifest remains absent because the proof phase is incomplete. |

The successful narrow replay was:

```bash
set -euo pipefail
tmp=$(mktemp -d /tmp/thm-m-1234-44afc5d9-slot20.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
cp Stage1_Instances/THM-M-1234/{Statement,AnchorAudit,ObligationTree,ConstructionProof,Proof,ClosurePackageDiagnostic}.lean "$tmp"/
lean=$(cd Formalizations/Lean && lake env which lean)
lean_path=$(cd Formalizations/Lean && lake env printenv LEAN_PATH)
export LEAN_NUM_THREADS=1
cd "$tmp"
LEAN_PATH="$lean_path" timeout --foreground 600 "$lean" --trust=0 -t0 -o Statement.olean Statement.lean
LEAN_PATH=".:$lean_path" timeout --foreground 600 "$lean" --trust=0 -t0 AnchorAudit.lean
LEAN_PATH=".:$lean_path" timeout --foreground 600 "$lean" --trust=0 -t0 -o ObligationTree.olean ObligationTree.lean
LEAN_PATH=".:$lean_path" timeout --foreground 600 "$lean" --trust=0 -t0 ConstructionProof.lean
LEAN_PATH=".:$lean_path" timeout --foreground 600 "$lean" --trust=0 -t0 Proof.lean
LEAN_PATH=".:$lean_path" timeout --foreground 600 "$lean" --trust=0 -t0 ClosurePackageDiagnostic.lean
```

It produced `Statement.olean` SHA-256
`1709e38a5b8cc96159b7042585666cb84536b4b3d9e26a63697992cd9820d308`
and `ObligationTree.olean` SHA-256
`2521d53bc0b3ea2c9d0b7e7bcae9854ebe5081fc0cecd39a8a5fdfdf4324fc50`.

## Retry Condition

The master/scheduler must stop identical proof-only rescheduling, reconcile 34
integrated structured proof packets against the authoritative attempt count of
zero, and split the item as required after five unresolved execution ticks.
First reopen the predecessor and publish an append-only registry update with
child-consuming analytic targets, closure tied to the candidate actually
constructed, a valid typed root reference, and node-specific structured
recipes. Then implement the analytic leaves without placeholders. An immutable
exact compatible Lean 4 root theorem is an alternative only after exact-type,
provenance, trust, and composition checks.

Because the universal proof phase is not genuinely self-tested as complete,
`.stage1-worker-selftest.json` is deliberately absent.
