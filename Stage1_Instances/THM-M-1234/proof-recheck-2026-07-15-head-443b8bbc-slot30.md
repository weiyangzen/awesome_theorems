# THM-M-1234 proof-phase recheck at `443b8bbc` (slot30)

Item: `S56-M-1234-PROOF`

Date: `2026-07-15` (`Asia/Shanghai`)

Base revision: `443b8bbc23bf35a1e7a4bb7b3183073f76bbee2b`.

Base tree: `c5771c47c12b80aba613e6d844570f83b39ded6d`.

## Verdict

`blocked`. The exact universal declaration
`Stage1Rev56.THMM1234.Statement` still has no repo-local or pinned proof body.
This attempt adds no proof body and closes no obligation. The proof phase
remains `[ ]`, lifecycle remains `planned`, and the root vector stays
`[H1, M3, R3] -> [H1, M3, R3]`. No proof receipt, audit-completion,
theorem-completion, validation, release, or master-acceptance claim is made.

The existing checked source provides conditional root assembly, a
constant-in-time structural candidate and its trace, and the strict zero-data
solution. None proves the canonical statement for arbitrary `InitialData`.
The diagnostic module also confirms an architecture defect in frozen registry
version 1: `EquationAndTraceClosurePackage` quantifies over every structurally
admissible candidate. Applying it to unrelated zero fields forces arbitrary
admissible initial velocity and vorticity test pairings to vanish. Meanwhile,
`CandidateConstructionPackage` does not consume its approximation, estimate,
or compactness children. These interfaces cannot certify the intended analytic
composition.

## Failed Gate And Retry Condition

The immediate dependency gate is unfinished:
`S56-M-1234-OBLIGATION_TREE` is worker-provisional `[_]`, not master-accepted
`[x]`. Independently, the first expanded mathematical gap is
`M1234-A-APPROX`: no child-consuming placeholder-free construction of global
smooth Euler approximants for every frozen `InitialData` witness exists in the
repository or pinned dependency closure. Uniform energy and bounded-vorticity
estimates, nonlinear-compatible compactness, structure preservation, passage
of the linear and quadratic momentum terms, and initial trace remain open.

The direct frozen root cut remains `M1234-A-STRUCTURE` plus
`M1234-E-CLOSURE`. Reopen after the master publishes and accepts registry
version 2 with child-consuming construction targets and closure tied to the
specifically constructed candidate, then splits and schedules the analytic
leaves. A direct exact proof of `Statement`, or an immutable compatible
external terminal body, is an alternative only after exact-type, provenance,
trust, and composition checks.

Twelve structured proof-attempt/blocker packets predate this attempt, but the
authoritative proof item still records `attempts: 0` and `children: []`.
Blueprint section 10.2 requires the master/scheduler to reconcile this stale
state and split the oversized item after five unresolved ticks. This worker did
not edit the DAG, generated blueprint, or frozen predecessor artifacts.

## Validation

All checks reused existing pinned artifacts read-only. No `lake update`, `lake
build`, dependency clone/fetch, network access, or deliberate `.lake` mutation
was performed. Generated Lean objects and logs stayed in `/tmp` and were
removed. The automation-provided untracked `.lake` symlink makes this
nonrelease evidence.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and all 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required`. |
| `python3 scripts/stage1_target.py show THM-M-1234` | 0 | Rank 158; planned; legacy artifacts unaccepted; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1234/check_obligation_tree.py` | 0 | 14 obligations and 28 typed edges passed; denominator `cfa0a02c68993c8b3eefc0edfe7d3d7bd20e2b58d140f47a1f5444a8ba734c5d`; root open at M3. |
| `cd Formalizations/Lean && lake env which lean` | 1 | The canonical cache's `flt-regular` checkout has `HEAD -> refs/heads/.invalid` and Lake could not resolve `HEAD`. The missing/corrupt pinned artifact was recorded rather than fetched or repaired. |
| Isolated trust-zero Lean replay below | 0 | All six owned modules elaborated with the pinned Lean 4.29 binary and existing compiled package paths; printed declarations reported only `propext`, `Classical.choice`, and `Quot.sound`. |
| Prohibited-device scan over owned `*.lean` | 1 | Expected no-match exit with empty output: no `sorry`, `admit`, axiom declaration, unsafe/opaque/extern escape, `sorryAx`, `implemented_by`, or `native_decide` was found. |
| Exact-topic scan over pinned package `*.lean` | 1 | Expected no-match exit with empty output: no Yudovich/Yudovitch, incompressible-Euler, or bounded-vorticity theorem was found. |
| `jq empty Stage1_Instances/THM-M-1234/*.json` | 0 | All owned structured JSON artifacts parsed. |

Because `lake env` was blocked by the corrupt `flt-regular` checkout, the
narrow replay used the exact toolchain binary named by `lean-toolchain` and
assembled `LEAN_PATH` solely from existing package build directories:

```bash
set -euo pipefail
root=$PWD
tmp=$(mktemp -d /tmp/thm-m-1234-proof-head-443b8bbc-slot30.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
cp Stage1_Instances/THM-M-1234/{Statement,AnchorAudit,ObligationTree,ConstructionProof,Proof,ClosurePackageDiagnostic}.lean "$tmp"/
lean=$(ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 elan which lean)
lean_path=$(find "$root/Formalizations/Lean/.lake/packages" \
  -path '*/.lake/build/lib/lean' -type d | sort | paste -sd: -)
export LEAN_NUM_THREADS=1
cd "$tmp"
LEAN_PATH="$lean_path" timeout 600 "$lean" --trust=0 -t0 -o Statement.olean Statement.lean
LEAN_PATH=".:$lean_path" timeout 600 "$lean" --trust=0 -t0 AnchorAudit.lean
LEAN_PATH=".:$lean_path" timeout 600 "$lean" --trust=0 -t0 -o ObligationTree.olean ObligationTree.lean
LEAN_PATH=".:$lean_path" timeout 600 "$lean" --trust=0 -t0 ConstructionProof.lean
LEAN_PATH=".:$lean_path" timeout 600 "$lean" --trust=0 -t0 Proof.lean
LEAN_PATH=".:$lean_path" timeout 600 "$lean" --trust=0 -t0 ClosurePackageDiagnostic.lean
```

Lean was version `4.29.0`, commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`; its binary SHA-256 was
`3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf`.
The sorted `LEAN_PATH` string SHA-256 was
`dcb0f520971d8af4041b3c13d7b5f7148cbfc17cc76c478ed72db719bef9c333`.
`Statement.olean` hashed
`1709e38a5b8cc96159b7042585666cb84536b4b3d9e26a63697992cd9820d308`;
`ObligationTree.olean` hashed
`2521d53bc0b3ea2c9d0b7e7bcae9854ebe5081fc0cecd39a8a5fdfdf4324fc50`.
The paired JSON packet binds all source, environment, object, and output hashes.

## Status Boundary

This current-base nonrelease packet records a repeated dependency,
architecture, and analytic blocker. It does not satisfy
`S56-M-1234-PROOF`, propose `[_]`, or support audit or theorem completion.
Because the assigned universal proof phase is not genuinely self-tested as
complete, `.stage1-worker-selftest.json` is deliberately absent.
