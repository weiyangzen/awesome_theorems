# THM-M-1234 proof-phase recheck at `557b928b` (slot31)

Item: `S56-M-1234-PROOF`

Recheck date: `2026-07-15` (`Asia/Shanghai`)

Base revision: `557b928b377b386864527c9fb4831d45857837aa`

Base tree: `e677879a6eb4cb9d6795ba1bd78726af06ab9465`

Worker automation clone: `slot31`.

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
and zero fields cannot satisfy the arbitrary initial pairing and vorticity
trace. The direct frozen root cut remains `M1234-A-STRUCTURE` plus
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

Nine pre-existing structured proof-attempt/blocker packets are visible in the
owned target history before this recheck, and the same analytic blocker is
explicitly repeated across the recent records. The authoritative DAG still
says `attempts: 0` and `children: []`. Blueprint section 10.2 therefore
requires the master/scheduler to reconcile the attempt count and split or
reopen the oversized work instead of scheduling another identical proof-only
retry. This worker did not edit the DAG, generated checklist, or frozen
registry.

Retry only after master acceptance of corrected child-consuming formal targets
and a registry delta, followed by local placeholder-free proofs of the analytic
children. An immutable exact compatible Lean 4 terminal body could instead be
pinned and checked for exact type, provenance, trust, and composition.

## Validation

All checks used the existing pinned environment. No `lake update`, `lake
build`, dependency clone/fetch, network access, or `.lake` mutation was
performed. The Lean replay copied the five owned modules to `/tmp`, placed all
generated objects and logs there, elaborated at trust level zero, and removed
the temporary directory.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and all 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required. |
| `python3 scripts/stage1_target.py show THM-M-1234` | 0 | Rank 158; planned; L0/rework-required; legacy artifacts unaccepted; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1234/check_obligation_tree.py` | 0 | 14 obligations and 28 typed edges passed; denominator `cfa0a02c...34c5d`; root open at M3. |
| Isolated trust-zero `lake env` Lean replay below | 0 | All five modules elaborated; printed proof declarations reported only `propext`, `Classical.choice`, and `Quot.sound`. |
| Token-anchored prohibited-device scan over owned `*.lean` files | 1 | Expected no-match exit; no prohibited construct was found. |
| Exact-topic search over pinned package sources | 1 | Expected no-match exit for Yudovich, Yudovitch, incompressible Euler, and bounded vorticity. |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`; tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b`. |
| `python3 -m json.tool Stage1_Instances/THM-M-1234/proof-recheck-2026-07-15-head-557b928b-slot31.json >/dev/null` | 0 | The paired structured blocker packet parsed as JSON. |
| `git diff --check -- Stage1_Instances/THM-M-1234 .stage1-worker-selftest.json` | 0 | No whitespace errors. |
| `git diff --no-index --check /dev/null Stage1_Instances/THM-M-1234/proof-recheck-2026-07-15-head-557b928b-slot31.md` | 1 | Expected new-file diff exit with no whitespace diagnostics. |
| `git diff --no-index --check /dev/null Stage1_Instances/THM-M-1234/proof-recheck-2026-07-15-head-557b928b-slot31.json` | 1 | Expected new-file diff exit with no whitespace diagnostics. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion self-test manifest remains absent because the proof phase is incomplete. |

The successful narrow Lean replay was:

```bash
set -euo pipefail
tmp=$(mktemp -d /tmp/thm-m-1234-proof-head-557b928b-slot31.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
cp Stage1_Instances/THM-M-1234/{Statement,AnchorAudit,ObligationTree,ConstructionProof,Proof}.lean "$tmp"/
lean=$(cd Formalizations/Lean && lake env which lean)
lean_path=$(cd Formalizations/Lean && lake env printenv LEAN_PATH)
export LEAN_NUM_THREADS=1
cd "$tmp"
LEAN_PATH="$lean_path" timeout 600 "$lean" --trust=0 -t0 -o Statement.olean Statement.lean
LEAN_PATH=".:$lean_path" timeout 600 "$lean" --trust=0 -t0 AnchorAudit.lean
LEAN_PATH=".:$lean_path" timeout 600 "$lean" --trust=0 -t0 -o ObligationTree.olean ObligationTree.lean
LEAN_PATH=".:$lean_path" timeout 600 "$lean" --trust=0 -t0 ConstructionProof.lean
LEAN_PATH=".:$lean_path" timeout 600 "$lean" --trust=0 -t0 Proof.lean
```

The replay produced `Statement.olean` SHA-256
`1709e38a5b8cc96159b7042585666cb84536b4b3d9e26a63697992cd9820d308`.
The paired JSON packet binds the source, environment, and output hashes.

## Status Boundary

This is current-base nonrelease blocker evidence, not a proof receipt. It does
not satisfy `S56-M-1234-PROOF`, change task state, or claim audit completion,
theorem completion, validation, release, or master acceptance.
`accepted_receipt_ids=[]`. Because the assigned universal proof phase is not
genuinely complete, `.stage1-worker-selftest.json` is deliberately absent.
