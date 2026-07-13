# THM-M-1011 validation-phase evidence

Item: `S56-M-1011-VALIDATION`

Base revision: `e6c4d56e017f77b02752e6c1325f0298dfb7f4d4`

Base tree: `3aa71b6797c53e65f39bbac295dabcd2fff8e0a6`

Validation date: `2026-07-14` (`Asia/Shanghai`)

## Verdict

`self_tested_pending_master_acceptance`. A network-isolated trust-zero replay
freshly elaborates the exact statement, frozen conditional composition,
repo-local quotient proof, and a separately written exact-root quotient
reconstruction. Both exact roots are transitively sorry-free and report
exactly `propext`, `Classical.choice`, and `Quot.sound`.

The validation module imports neither `Proof` nor `ObligationTree`. It renames
and reconstructs the quotient transport directly from the frozen statement and
pinned mathlib. This is useful differential corroboration, but it uses the same
worker, checkout, Lean binary, warm dependency cache, route, and terminal
mathlib bodies. It is not the distinct signed verifier required by section
10.7 and supplies no additional mathematical proof credit.

## Authority Boundary

No obligation is accepted by this worker. The proof dependency is provisional
`[_]`, and the frozen typed graph predates the quotient proof: it still records
the direct-`T2Space` route, `root_closed=false`, and root `M5`. Validation does
not rewrite that architecture or instance state. The accepted vector therefore
remains the weaker `[H1, M5, R4]`, with `audit_complete=false` and
`theorem_complete=false`.

The first node gate failure is
`dependency.S56-M-1011-PROOF.master_acceptance`; quotient-route graph
reconciliation and `M1011-S-FOUNDATION` follow. The first release gate failure
is `S56-10.6-HERMETIC-COLD-BUILD`.

## Commands And Results

All commands ran inside the worker clone. No `lake update`, `lake build`,
dependency clone/fetch, network operation, or `.lake` mutation was performed.
The validation reuses the automation-provided canonical pinned `.lake` symlink
read-only.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and all 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1011` | 0 | rank 260, planned, legacy artifacts unaccepted, theorem incomplete |
| `env LEAN_NUM_THREADS=1 python3 Stage1_Instances/THM-M-1011/check_statement.py` | 0 | exact expression fingerprint and all four statement mutations passed |
| `env LEAN_NUM_THREADS=1 python3 Stage1_Instances/THM-M-1011/check_anchor_audit.py` | 0 | four candidates passed; the pre-proof direct forward anchor requires `T2Space` |
| `python3 Stage1_Instances/THM-M-1011/check_obligation_tree.py` | 0 | 14 obligations and 35 typed edges passed; frozen root remains open M5 |
| `python3 -I -B Stage1_Instances/THM-M-1011/check_validation.py` | 0 | network-isolated warm trust-zero replay, exact roots, sorry/axiom checks, selected provenance, receipt freshness, and fail-closed boundaries passed |
| `python3 -m json.tool` on the phase spec, receipt, and worker packet | 0 | all JSON parsed |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-m1011-pycache python3 -m py_compile Stage1_Instances/THM-M-1011/check_validation.py` | 0 | validator syntax compiled outside the repository tree |
| prohibited-mechanism scan over the four Lean sources | 1 | expected no-match result; no active placeholder, bodyless axiom, unsafe/oracle, native, opaque, or external mechanism |
| `git diff --check -- Stage1_Instances/THM-M-1011 .stage1-worker-selftest.json` | 0 | no whitespace errors |

`check_proof.py` was run before the validation worker packet was installed. It
is not rerun afterward because that predecessor checker conditionally requires
any root packet to identify `S56-M-1011-PROOF`; the validation checker directly
binds and replays its proof receipt and actual sources instead.

## Gate Decisions

| Gate | Decision | Evidence or failure |
|---|---|---|
| Exact kernel replay | provisional pass | Exact proof root and differential exact root elaborate under `--trust=0`. |
| Placeholder/unsafe boundary | pass | `assert_no_sorry`, printed sorry result, and comment-stripped scans pass. |
| Trust observation | provisional pass | Both exact roots use only the observed three classical/quotient axioms; no accepted foundation policy or complete TCB exists. |
| Selected provenance | provisional pass | Target, denominator, source, Git blob, olean, tool, pin, tree, cleanliness, and license hashes agree for the selected direct boundary. |
| Structured authority | fail closed | Proof is only `[_]`; frozen graph remains the unreconciled direct-`T2Space` route at M5. |
| Hermetic release | fail closed | Shared warm cache; no empty-cache cold build, offline restoration, deterministic release bundle, complete SBOM, or second platform. |
| Independent verification | fail closed | Same worker and cache; no distinct identity, clean provisioned runner, signature, or independent minimal verifier. |

This node-specific validation implementation is genuinely self-tested and may
be proposed as worker `[_]`. It is nonrelease evidence and grants no accepted
`M0-L`, `E0/E1`, `AUDIT-Z`, `THEOREM-Z`, release, or theorem-completion credit.
