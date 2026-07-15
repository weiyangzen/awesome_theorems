# THM-M-1234 proof-phase recheck at `e89fe5cc` (slot23)

Item: `S56-M-1234-PROOF`

Date: `2026-07-15` (`Asia/Shanghai`)

Base revision: `e89fe5cc9f4b8de45e791d470b1e02e39ca0e734`

Base tree: `dc43d49d892d5f7eb05124c95f52f837b97734ba`

## Verdict

`blocked`. The exact universal declaration
`Stage1Rev56.THMM1234.Statement` still has no repo-local or pinned proof body.
This recheck adds no Lean proof body and closes no obligation. The proof item
remains `[ ]`, the lifecycle remains `planned`, and the root vector remains
`[H1, M3, R3] -> [H1, M3, R3]`. No proof, validation, release,
audit-completion, theorem-completion, or master-acceptance receipt is claimed.

The existing checked source cannot close the target:

- `root_of_construction_and_closure` consumes two packages rather than proving
  them;
- constant-in-time initial fields inhabit only the under-specified
  `CandidateConstructionPackage` and consume none of its frozen approximation,
  estimate, or compactness children;
- `zero_data_solution` proves only the strict zero-data boundary case; and
- `ClosurePackageDiagnostic.lean` shows that the frozen
  `EquationAndTraceClosurePackage` applies to every unrelated candidate.
  Applying it to zero fields forces arbitrary admissible initial velocity and
  vorticity test pairings to vanish.

No exact Yudovich, Yudovitch, incompressible-Euler, or bounded-vorticity
terminal theorem was found in the available pinned package sources. The legacy
`S1_M_158.lean` module records interfaces and explicit noncompletion, not a
terminal proof body.

Five bounded read-only GitHub repository metadata searches also found no new
exact candidate. Queries for `Yudovich theorem lean`, `Yudovitch lean`,
`Lean4 incompressible Euler`, and `Euler equations Lean theorem prover`
returned zero repositories. `vorticity lean4` returned only
`jcamlin/iDNS-Lean4-Mathlib4` and `Brsanch/sqg-lean-proofs`, both already
audited as non-exact. Unauthenticated GitHub code search returned HTTP 401, so
it provides no global absence evidence.

## Failed Gates And Retry

The first failed gate is the dependency gate:
`S56-M-1234-OBLIGATION_TREE` is worker-provisional `[_]`, not master-accepted
`[x]`. That predecessor is also not currently acceptable under rev-5.6:

- `typed-graphs.json` names `M1234-ROOT` as `root_node_id`, but no node has that
  ID; the root node is named `THM-M-1234-ROOT`.
- Every recipe in `validation-specs.json` is a shell-string `command` and omits
  the normative `cwd`, `argv`, `env_allowlist`, `timeout_seconds`,
  `expected_outputs`, `covered_obligation_ids`, and `covered_declarations`
  fields required by blueprint section 10.5.
- The frozen construction interface ignores its analytic children, while the
  closure interface is universally quantified over candidates unrelated to
  the construction.

Independently, the first expanded mathematical gap is `M1234-A-APPROX`: there
is no child-consuming, placeholder-free construction of global smooth Euler
approximants for every frozen `InitialData` witness. Uniform energy and
vorticity estimates, nonlinear-compatible compactness, structure preservation,
linear and quadratic momentum limit passage, and the one-sided initial trace
also remain open. The direct frozen root cut is `M1234-A-STRUCTURE` plus
`M1234-E-CLOSURE`.

Before this packet, the owned path contained eighteen structured proof-attempt,
blocker, or recheck JSON packets, while the authoritative proof item still
records `attempts: 0` and `children: []`. Blueprint section 10.2 requires a
split after five unresolved execution ticks. The master/scheduler must
reconcile that stale history instead of issuing another identical unsplit proof
task.

Retry after the master reopens and repairs the predecessor, publishes an
append-only registry version 2 with child-consuming construction targets and
closure tied to the specifically constructed candidate, and splits the
analytic leaves. An immutable exact compatible Lean 4 root theorem is an
alternative only after exact-type, provenance, trust, and composition checks.

## Validation

The automation-provided `.lake` symlink to the canonical pinned cache was
reused read-only. No `lake update`, `lake build`, dependency clone/fetch, or
`.lake` mutation was performed. Generated Lean objects and logs stayed in a
fresh `/tmp` directory and were removed. Network use was limited to the six
read-only GitHub API requests described above; it did not affect the pinned
Lean replay or dependency closure.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and all 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets at ranks 1 through 1546, all `L0/rework_required`, passed. |
| `python3 scripts/stage1_target.py show THM-M-1234` | 0 | Rank 158; planned; legacy artifacts unaccepted; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1234/check_obligation_tree.py` | 0 | 14 obligations and 28 typed edges passed; denominator `cfa0a02c68993c8b3eefc0edfe7d3d7bd20e2b58d140f47a1f5444a8ba734c5d`; root open at M3. This checker does not detect the root-ID or validation-recipe defects above. |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`. |
| `cd Formalizations/Lean && lake env which lean && lake env printenv LEAN_PATH` | 0 | Selected the pinned Lean binary and existing pinned build paths. |
| Isolated trust-zero replay below | 0 | All six owned modules elaborated. Printed declarations reported only `propext`, `Classical.choice`, and `Quot.sound`. |
| Prohibited-device scan over owned `*.lean` | 1 | Expected no-match exit: no `sorry`, `admit`, declared axiom, unsafe/opaque/extern escape, `sorryAx`, `implemented_by`, or `native_decide` was found. |
| Exact-topic scan over pinned package `*.lean` sources | 1 | Expected no-match exit: no exact-topic terminal candidate was found. |
| Five GitHub repository API searches | 0 | All returned HTTP 200; total counts were `0, 0, 0, 2, 0`. The two hits were already-audited non-exact projects. |
| GitHub code-search API request | 0 | Curl succeeded but the API returned HTTP 401 `Requires authentication`; no discovery or absence credit was assigned. |
| Structured predecessor conformance diagnostic | 0 | Confirmed `root_node_id=M1234-ROOT` is absent from `nodes[].node_id`; inspection confirmed all 14 recipes use shell-string commands and lack the required structured recipe fields. |

The successful narrow replay was:

```bash
set -euo pipefail
root=$PWD
tmp=$(mktemp -d /tmp/thm-m-1234-e89fe5cc-slot23.XXXXXX)
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

The external repository searches were executed with temporary response files:

```bash
curl -L --silent --show-error -H 'Accept: application/vnd.github+json' -o "$out" -w '%{http_code}' "$url"
```

The five repository URLs were
`https://api.github.com/search/repositories?q=Yudovich%20theorem%20lean&per_page=20`,
`https://api.github.com/search/repositories?q=Yudovitch%20lean&per_page=20`,
`https://api.github.com/search/repositories?q=Lean4%20incompressible%20Euler&per_page=20`,
`https://api.github.com/search/repositories?q=vorticity%20lean4&per_page=20`, and
`https://api.github.com/search/repositories?q=Euler%20equations%20Lean%20theorem%20prover&per_page=20`.
The unauthenticated code-search URL was
`https://api.github.com/search/code?q=Yudovich+language%3ALean&per_page=20`.
All temporary responses were deleted.

## Status Boundary

This target-scoped artifact is the required current-base blocker handoff, not a
proof receipt. It does not satisfy `S56-M-1234-PROOF`, propose `[_]`, change
task state, or support a later phase. Because the assigned universal proof
phase is not genuinely self-tested as complete, `.stage1-worker-selftest.json`
is deliberately absent.
