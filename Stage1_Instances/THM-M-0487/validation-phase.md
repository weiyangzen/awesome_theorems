# THM-M-0487 validation-phase handoff

Item: `S56-M-0487-VALIDATION`

Base revision: `9d50d838c8132b2aaf005a4863baeb5385e52a97`

Base tree: `ef268baf236c1fe55806a57847c7f78ed6587b9d`

## Verdict Boundary

This is a self-tested, provisional blocked validation handoff. A network-isolated, read-only-host
recipe rebuilt fresh outputs for the exact statement, the frozen conditional compositions, the two
proof-phase finite-count interfaces, and a trust-only `Validation.lean` probe. Both partial proof
declarations are sorry-free and report exactly `propext`, `Classical.choice`, and `Quot.sound`.
Selected direct mathlib source, blob, compiled-object, origin, license, dependency, and tool hashes
also agree with the pinned environment.

The exact weak Goldbach root does not have a proof body. The partial count equivalence proves no
positivity theorem. `M0487-T-ANALYTIC` and `M0487-T-FINITE-UPPER` remain the minimal open proof cut,
so the root remains `[H1, M3, R3]`, accepted closure remains empty, and both
`audit_complete=false` and `theorem_complete=false` are mandatory.

## Commands And Results

No `lake update`, `lake build`, dependency clone/fetch, network request, or `.lake` mutation was
performed. The canonical pinned `.lake` symlink was reused read-only. All new Lean outputs were
written beneath a private `/tmp` and removed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0487` | 0 | rank 1366, planned, legacy artifacts unaccepted, theorem incomplete |
| the exact `argv` array in `validation-spec.json` | 0 | bubblewrap denied network and mounted the host read-only; pinned `lake env lean --trust=0` rebuilt the exact statement, seven conditional compositions, the two partial interfaces, and the trust probe from fresh temporary outputs |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-m0487-validation-pycache python3 -m py_compile Stage1_Instances/THM-M-0487/check_validation.py` | 0 | validator compiled without writing generated files in the owned path |
| `python3 -m json.tool` on the spec, receipt, blocker, and worker packet | 0 | all four JSON artifacts parsed |
| scoped prohibited-device scan over the four checked Lean modules | 1 | expected no-match exit; no `sorry`, `admit`, `sorryAx`, bodyless declaration, unsafe/opaque declaration, native proof escape, or external implementation exists |
| `git diff --check -- Stage1_Instances/THM-M-0487 .stage1-worker-selftest.json` | 0 | no whitespace errors |

## Failed Gates

The first phase gate is the incomplete proof dependency. Its integrated receipt truthfully binds
the current proof inputs but closes zero frozen obligations and supplies no root body. The older
proof and 54 obligation-tree checker recipes are snapshot-bound to their former base/DAG state, so
they now fail freshness; this validator replays their underlying Lean declarations but does not
misreport those old recipes as freshly passing.

The network-isolated recipe is stronger than an ordinary warm run, but it still reuses the shared
canonical dependency cache. It is not the new-checkout, cold empty-cache, offline archive replay
required by section 10.6. The trust probe also runs in this worker and cache, so it is not the
distinct signed verifier or independently implemented minimal verifier required by section 10.7.
Complete transitive provenance/TCB, supply-chain restoration, source H0, readable R0, deterministic
bundling, release reconciliation, and master acceptance remain open.

## Retry Condition

Implement or pin/import placeholder-free bodies for both open range packages, including admitted
finite data, certificates, and a kernel-sound replay; compose and master-accept the exact root; and
refresh the structured recipes. Release then additionally requires complete trust/provenance, a
cold empty-cache offline replay, and distinct signed independent verification.
