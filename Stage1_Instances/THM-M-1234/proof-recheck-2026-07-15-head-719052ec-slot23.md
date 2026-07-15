# THM-M-1234 proof-phase blocker at `719052ec` (slot23)

Item: `S56-M-1234-PROOF`. Intent: `prove`. Recorded: 2026-07-15.

## Verdict

`blocked`; no state change. The exact target remains
`Stage1Rev56.THMM1234.Statement`, universally quantified over every admissible
whole-plane finite-energy velocity and bounded-vorticity curl. No repo-local or
pinned dependency declaration proves that proposition, and no exact immutable
external body is available to import.

The checked local bodies are truthful but insufficient:

- `root_of_construction_and_closure` only composes two explicit premises.
- `candidateConstructionPackage_from_initialData` supplies constant-in-time
  structural fields but consumes none of the frozen approximation, energy, or
  compactness children.
- `initialCandidateFields_trace` handles that one constant candidate.
- `zero_data_solution` proves only the zero-data boundary case.

The frozen direct cut is `M1234-A-STRUCTURE` plus `M1234-E-CLOSURE`; the first
expanded missing analytic body is `M1234-A-APPROX`. The remaining expansion is
`M1234-A-ENERGY`, `M1234-A-COMPACT`, `M1234-A-STRUCTURE`,
`M1234-E-LINEAR`, `M1234-E-NONLINEAR`, `M1234-E-TRACE`, and
`M1234-E-CLOSURE`.

## Dependency And Architecture Gate

The immediate dependency `S56-M-1234-OBLIGATION_TREE` is only worker-provisional
`[_]`, not master-accepted `[x]`. Its current artifacts also cannot support a
truthful proof receipt:

1. `typed-graphs.json` declares `root_node_id=M1234-ROOT`, but no
   `nodes[].node_id` has that value; the root entry uses
   `THM-M-1234-ROOT` instead.
2. All 14 validation recipes are shell-string `command` records and omit the
   structured `cwd`, `argv`, environment allowlist, timeout, expected outputs,
   covered obligation IDs, and covered declaration fields required by rev-5.6.
3. `CandidateConstructionPackage` is not child-consuming, while
   `EquationAndTraceClosurePackage` quantifies over every unrelated
   `CandidateFields`. The checked zero-candidate diagnostic shows that the
   latter premise would erase every admissible initial velocity and vorticity
   test pairing.

Changing those frozen interfaces is predecessor work and requires a new,
append-only registry version. This proof-only worker did not edit the registry,
graphs, validation specs, execution DAG, or generated checklist.

## Validation

The automation-provided untracked `.lake` symlink was reused read-only. No
`lake update`, `lake build`, clone, fetch, network access, or `.lake` mutation
was performed. All generated Lean objects and logs stayed in a fresh `/tmp`
directory and were removed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | All 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | All 1546 unique targets at ranks 1 through 1546 passed as L0/rework-required. |
| `python3 scripts/stage1_target.py show THM-M-1234` | 0 | Rank 158; planned; legacy artifacts unaccepted; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1234/check_obligation_tree.py` | 0 | 14 obligations and 28 typed edges passed; denominator `cfa0a02c68993c8b3eefc0edfe7d3d7bd20e2b58d140f47a1f5444a8ba734c5d`; root remains open at M3. The checker does not catch the conformance defects above. |
| Isolated trust-zero replay below | 0 | All six owned Lean modules elaborated with Lean 4.29.0; printed declarations use only `propext`, `Classical.choice`, and `Quot.sound`. |
| Prohibited-device scan over owned `*.lean` | 1 | Expected no-match exit: no `sorry`, `admit`, declared axiom, unsafe/opaque/extern escape, `sorryAx`, `implemented_by`, or `native_decide`. |
| Exact-topic scan over pinned package `*.lean` | 1 | Expected no-match exit: no Yudovich/Yudovitch, incompressible-Euler, or bounded-vorticity terminal candidate. |
| Structured predecessor diagnostic | 0 | Confirmed the missing root node ID and all 14 malformed recipes. |

The narrow Lean replay was:

```bash
set -euo pipefail
tmp=$(mktemp -d /tmp/thm-m-1234-719052ec-slot23.XXXXXX)
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

The replay produced `Statement.olean` SHA-256
`1709e38a5b8cc96159b7042585666cb84536b4b3d9e26a63697992cd9820d308`
and `ObligationTree.olean` SHA-256
`2521d53bc0b3ea2c9d0b7e7bcae9854ebe5081fc0cecd39a8a5fdfdf4324fc50`.

## Retry And Status Boundary

The scheduler/master must reconcile the repeated attempts, reopen the
predecessor, publish registry version 2 with child-consuming construction
targets and closure tied to the constructed candidate, correct the typed root
and structured recipes, and split the analytic work. The proof phase can then
implement approximation, uniform estimates, nonlinear-compatible compactness,
momentum limit passage, and trace bodies. An alternative is an immutable exact
compatible Lean 4 root theorem that passes exact-type, provenance, trust, and
composition checks.

This is a current-base blocker handoff, not a proof receipt. It does not satisfy
`S56-M-1234-PROOF`, propose `[_]`, establish audit/theorem completion, or
authorize validation, release, or master acceptance. Because the assigned
universal proof phase is not genuinely self-tested as complete,
`.stage1-worker-selftest.json` is deliberately absent.
