# THM-M-1234 proof-phase recheck at current base

Item: `S56-M-1234-PROOF`

Recheck date: 2026-07-16 (`Asia/Shanghai`)

Base revision: `cd9c0b0881ba3f56b9892820e7fbba665eb9efed`

Base tree: `00c421fc989812e85b6764775a1d009366148584`

Worker automation clone: `slot22`.

The tracked owned path was clean at preflight. The only pre-existing worktree
entry was the automation-provided untracked `Formalizations/Lean/.lake`
symlink to the canonical pinned dependency cache. This is nonrelease evidence.

## Verdict

`blocked`. No repo-local or pinned declaration proves the exact universal
`Stage1Rev56.THMM1234.Statement`. No proof body was added, the proof item stays
`[ ]`, lifecycle stays `planned`, the root stays `[H1, M3, R3]`, and neither
audit completion nor theorem completion is claimed.

The current Lean bodies are real and placeholder-free, but their boundaries
are strict:

- `root_of_construction_and_closure` is conditional on two package premises.
- `candidateConstructionPackage_from_initialData` uses constant-in-time initial
  fields. It proves the weak formal interface but consumes none of the frozen
  approximation, energy, or compactness children.
- `initialCandidateFields_trace` proves only the trace of that constant
  candidate.
- `zero_data_solution` proves only the strict zero-data boundary case.
- No declaration inhabits `EquationAndTraceClosurePackage` or `Statement`.

The frozen closure package is also over-quantified: it requires momentum and
trace closure for every structurally admissible `CandidateFields`, including
the zero fields unrelated to the initial data. The checked declarations in
`ClosurePackageDiagnostic.lean` show that this premise would force every
admissible initial velocity and vorticity test pairing to vanish. This is a
conditional architecture diagnostic, not a proof of inconsistency and not a
proof of the root.

## Failed Gates

The first workflow failure is the unfinished dependency:
`S56-M-1234-OBLIGATION_TREE` is only worker-provisional `[_]`, not
master-accepted `[x]`. Its artifacts are not acceptance-ready:

- `typed-graphs.json` sets `root_node_id` to `M1234-ROOT`, but the declared
  node ID is `THM-M-1234-ROOT`.
- All 14 validation recipes use shell-string `command` fields and omit the
  required structured `cwd`, `argv`, `env_allowlist`, `timeout_seconds`,
  `expected_outputs`, `covered_obligation_ids`, and `covered_declarations`.
- The checked construction interface does not consume its three analytic
  children, while the checked closure interface ranges over unrelated
  candidates. Repair changes frozen fingerprints and therefore needs a new
  registry version with an append-only delta.

Independently, the first substantive proof failure is `M1234-A-APPROX`: there
is no child-consuming, placeholder-free construction of smooth global Euler
approximants for every frozen `InitialData` witness in the repository or pinned
dependency closure. The direct root cut remains `M1234-A-STRUCTURE` plus
`M1234-E-CLOSURE`. Uniform estimates, nonlinear-compatible compactness,
linear and quadratic momentum passage, and initial trace remain open.

The legacy `S1_M_158.lean` file contains interfaces and audit scaffolding, not
a terminal proof. A scan of all 9,676 available pinned package Lean sources
found no Yudovich, Yudovitch, incompressible-Euler, or bounded-vorticity
terminal candidate. A bounded GitHub repository-metadata recheck returned no
repository for the three exact-topic queries and only the already rejected
Navier-Stokes and SQG repositories for `vorticity Lean4`. This is not an
exhaustive external nonexistence claim.

The owned path already contained 38 structured proof attempt/blocker/recheck
packets before this recheck, while the authoritative DAG still records
`attempts: 0` and `children: []`. Under blueprint section 10.2, the master must
stop identical proof-only rescheduling, reconcile the attempt history, and
split or reopen this oversized work.

## Retry Condition

First master-reopen the predecessor architecture and publish an accepted
registry delta with child-consuming construction targets, closure tied to the
specifically constructed candidate, a valid root reference, and node-specific
structured recipes. Then implement smooth approximation, uniform estimates,
nonlinear compactness, momentum-limit, and trace bodies as separate
placeholder-free leaves. Alternatively, pin an immutable exact compatible
Lean 4 terminal theorem and pass exact-type, provenance, trust, and composition
checks.

## Validation

All Lean checks used the existing pinned environment. No `lake update`, `lake
build`, dependency clone/fetch, or `.lake` mutation was run. The replay copied
the six owned modules to `/tmp`, generated all objects and logs there, checked
them with Lean 4.29.0 at trust level zero, and removed the temporary directory.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | All 15 assurance groups and 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | All 1546 unique ordered targets passed. |
| `python3 scripts/stage1_target.py show THM-M-1234` | 0 | Rank 158; planned; L0/rework-required; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1234/check_obligation_tree.py` | 0 | 14 obligations and 28 typed edges passed; denominator `cfa0a02c...34c5d`; root open M3. This checker does not enforce the malformed node reference or structured-recipe contract. |
| Isolated trust-zero Lean replay below | 0 | All six modules elaborated. The printed local declarations report only `propext`, `Classical.choice`, and `Quot.sound`. `Statement.olean` SHA-256 is `1709e38a5b8cc96159b7042585666cb84536b4b3d9e26a63697992cd9820d308`. |
| Prohibited-device scan over owned Lean files | 1 | Expected no-match exit: no `sorry`, `admit`, declared axiom, unsafe/opaque/extern injection, `sorryAx`, `implemented_by`, or `native_decide`. |
| Exact-topic scan over 9,676 pinned package Lean sources | 1 | Expected no-match exit: no exact-topic candidate was found. |
| Structured predecessor diagnostics | 1, 1 | Expected fail-closed results: dangling `root_node_id`; all 14 recipes fail the normative structured-field predicate. |
| Bounded GitHub repository-metadata queries | 0 | Exact-topic totals were zero; `vorticity Lean4` returned only the two previously rejected non-exact repositories. |
| `jq empty Stage1_Instances/THM-M-1234/*.json` | 0 | All pre-existing owned JSON artifacts parsed before this handoff. |
| Blocker JSON invariant check and `git diff --check` | 0 | The new handoff parses, records no completion, and has no whitespace errors. |
| `test ! -e .stage1-worker-selftest.json` | 0 | The completion manifest is absent because the proof phase is blocked. |

The isolated Lean recipe was:

```bash
set -euo pipefail
tmp=$(mktemp -d /tmp/thm-m-1234-proof-head-cd9c0b08.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
cp Stage1_Instances/THM-M-1234/{Statement,AnchorAudit,ObligationTree,ConstructionProof,ClosurePackageDiagnostic,Proof}.lean "$tmp"/
lean=$(cd Formalizations/Lean && lake env which lean)
lean_path=$(cd Formalizations/Lean && lake env printenv LEAN_PATH)
cd "$tmp"
LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" timeout 600 "$lean" --trust=0 -t0 -o Statement.olean Statement.lean
LEAN_NUM_THREADS=1 LEAN_PATH=.:"$lean_path" timeout 600 "$lean" --trust=0 -t0 AnchorAudit.lean
LEAN_NUM_THREADS=1 LEAN_PATH=.:"$lean_path" timeout 600 "$lean" --trust=0 -t0 -o ObligationTree.olean ObligationTree.lean
LEAN_NUM_THREADS=1 LEAN_PATH=.:"$lean_path" timeout 600 "$lean" --trust=0 -t0 ConstructionProof.lean
LEAN_NUM_THREADS=1 LEAN_PATH=.:"$lean_path" timeout 600 "$lean" --trust=0 -t0 ClosurePackageDiagnostic.lean
LEAN_NUM_THREADS=1 LEAN_PATH=.:"$lean_path" timeout 600 "$lean" --trust=0 -t0 Proof.lean
```

Because the assigned proof phase is not genuinely complete,
`.stage1-worker-selftest.json` is deliberately absent. This blocker packet is
not a proof receipt, does not satisfy `S56-M-1234-PROOF`, and supports no
provisional or accepted state, audit completion, theorem completion,
validation, release, or master acceptance.
