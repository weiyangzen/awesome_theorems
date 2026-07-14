# THM-M-1234 proof-phase recheck at current base

Item: `S56-M-1234-PROOF`

Recheck date: 2026-07-15 (Asia/Shanghai)

Base revision: `ed959a5a318a6244a0a9b53d335b24d0198860f7`

Base tree: `ad80b5a6c5620daa66871bb3bbb0109f03b62d90`

Worker automation clone: `slot25`.

The tracked owned path was clean at preflight. The only pre-existing worktree
entry was the automation-provided untracked `Formalizations/Lean/.lake`
symlink to the canonical pinned dependency cache. This packet is nonrelease
evidence.

## Verdict

`blocked`. No repo-local or pinned declaration proves the exact universal
`Stage1Rev56.THMM1234.Statement`, and this proof-only worker cannot repair the
frozen predecessor architecture. The item remains `[ ]`; lifecycle remains
`planned`; the root remains `[H1, M3, R3]`; and no proof receipt, semantic
obligation closure, graph change, or accepted debt change is added.

The existing Lean bodies are real and placeholder-free but do not close the
root:

- `root_of_construction_and_closure` is conditional on construction and
  equation/trace packages.
- `candidateConstructionPackage_from_initialData` uses constant-in-time
  initial fields. It inhabits the formal construction interface, but that
  interface consumes none of the frozen approximation, estimate, or
  compactness children, so it earns no closure for `M1234-A-STRUCTURE`.
- `initialCandidateFields_trace` proves only the trace of that constant
  candidate.
- `zero_data_solution` proves only the strict zero-data boundary case.

There is no sound encoding shortcut. `InitialData` is inhabited. Constant
initial fields do not in general satisfy the nonlinear weak momentum identity,
and the zero fields cannot satisfy the arbitrary initial pairing and
vorticity trace. The direct frozen root cut remains `M1234-A-STRUCTURE` plus
`M1234-E-CLOSURE`.

The frozen `EquationAndTraceClosurePackage` is also stronger than the usual
existence construction: it requires momentum and trace closure for every
structurally admissible `CandidateFields`, rather than for the particular
limit produced by the approximation argument. Correcting that quantification
or the child-consuming construction interface changes predecessor fingerprints
and requires a new registry version with an append-only delta; it is outside
this proof worker's authority.

## Failed Gate And Scheduler Action

The first expanded failed gate is `M1234-A-APPROX`: no checked,
placeholder-free construction of global smooth Euler approximants for every
frozen `InitialData` witness exists in the repository or pinned dependency
closure. Uniform estimates, nonlinear-compatible compactness, preservation of
the structural fields, linear and quadratic momentum passage, and the initial
trace remain open as well.

Six integrated proof-lane executions are visible in target history. The same
`M1234-A-APPROX` blocker is explicitly repeated in the latest five attempt or
recheck records, while the authoritative DAG still says `attempts: 0` and
`children: []`. Blueprint section 10.2 therefore requires the master/scheduler
to reconcile the attempt count and split or reopen the oversized work instead
of scheduling another identical proof-only retry. This worker did not edit the
DAG, generated checklist, or frozen registry.

Retry only after master acceptance of corrected child-consuming formal targets
and a registry delta, followed by local placeholder-free proofs of the analytic
children. An immutable exact compatible Lean 4 terminal body could instead be
pinned and checked for exact type, provenance, trust, and composition.

## Validation

All checks used the existing pinned environment. No `lake update`, `lake
build`, dependency clone/fetch, network access, or deliberate `.lake` mutation
was performed. The Lean replay copied the five owned modules to `/tmp`, placed
all generated objects and logs there, elaborated at trust level zero, and
removed the temporary directory. A post-run recheck reproduced the pre-run
dependency-cache metadata digest; this metadata comparison is not a content
digest.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | All 15 assurance groups and 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | All 1546 unique ordered targets at ranks 1 through 1546 passed. |
| `python3 scripts/stage1_target.py show THM-M-1234` | 0 | Rank 158; planned; L0/rework-required; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1234/check_obligation_tree.py` | 0 | 14 obligations and 28 typed edges passed; denominator `cfa0a02c...34c5d`; root open M3. |
| Isolated trust-zero `lake env` Lean replay below | 0 | All five modules elaborated. Printed proof declarations reported only `propext`, `Classical.choice`, and `Quot.sound`. |
| Prohibited-device scan over owned Lean files | 1 | Expected no-match exit; no `sorry`, `admit`, declared axiom, unsafe/opaque/extern injection, `sorryAx`, `implemented_by`, or `native_decide`. |
| Exact-topic search over every pinned package | 1 | Expected no-match exit for Yudovich, Yudovitch, incompressible Euler, and bounded vorticity. |
| `git diff --check` and `jq empty` | 0 | No whitespace errors; all owned JSON parsed. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion self-test manifest is absent. |

The isolated Lean recipe was:

```bash
set -euo pipefail
tmp=$(mktemp -d /tmp/thm-m-1234-proof-head-ed959a5a.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
cp Stage1_Instances/THM-M-1234/{Statement,AnchorAudit,ObligationTree,ConstructionProof,Proof}.lean "$tmp"/
lean=$(cd Formalizations/Lean && lake env which lean)
lean_path=$(cd Formalizations/Lean && lake env printenv LEAN_PATH)
cd "$tmp"
LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" timeout 600 "$lean" --trust=0 -t0 -o Statement.olean Statement.lean
LEAN_NUM_THREADS=1 LEAN_PATH=.:"$lean_path" timeout 600 "$lean" --trust=0 -t0 AnchorAudit.lean
LEAN_NUM_THREADS=1 LEAN_PATH=.:"$lean_path" timeout 600 "$lean" --trust=0 -t0 -o ObligationTree.olean ObligationTree.lean
LEAN_NUM_THREADS=1 LEAN_PATH=.:"$lean_path" timeout 600 "$lean" --trust=0 -t0 ConstructionProof.lean
LEAN_NUM_THREADS=1 LEAN_PATH=.:"$lean_path" timeout 600 "$lean" --trust=0 -t0 Proof.lean
```

The replay produced `Statement.olean` SHA-256
`1709e38a5b8cc96159b7042585666cb84536b4b3d9e26a63697992cd9820d308`.
The adjacent JSON binds this result to the exact sources, environment,
commands, and output hashes.

Because the assigned proof phase is not genuinely complete,
`.stage1-worker-selftest.json` is deliberately absent. This artifact is a
current-base blocker packet, not a proof receipt or state transition, and it
does not claim audit completion, theorem completion, validation, release, or
master acceptance.
