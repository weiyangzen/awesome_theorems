# THM-M-1061 validation-phase result

Item `S56-M-1061-VALIDATION` was replayed against base revision
`4ba3f2fd1e609b5958f24e0415eef9300da16924` on 2026-07-15. The result is a
truthful negative-root validation: the exact statement and all thirteen local
partial proof declarations elaborate at trust level zero, but no declaration
proves the premise-free Varadhan root.

## Scoped result

`check_validation.sh` copies the five Lean inputs to a fresh directory under
`/tmp`, resolves the pinned Lean executable and constructs `LEAN_PATH` from the
existing manifest-named compiled package directories, and runs every Lean
process inside `bubblewrap --unshare-net` with
a read-only root, fixed locale/timezone, and one writable temporary directory.
The exact statement, conditional root transport, proof bodies, seven anchor
probes, and two separately written partial probes elaborate. Every checked
proof, transport, and differential declaration reports exactly `propext`,
`Classical.choice`, and `Quot.sound`.

The separately written probes recheck only the open-set LDP projection and the
conditional liminf/limsup merge. They import neither `Proof` nor
`ObligationTree`, but they run in this worker and use the same kernel and cache;
they are not the distinct independent verifier required by rev-5.6 section
10.7.

## Gate decisions

| Gate | Decision | Evidence or failure |
|---|---|---|
| Exact statement and mutations | pass | Expression SHA-256 `681a5c8f...32119`; all four frozen mutations differ. |
| Narrow kernel replay | pass, nonrelease | Statement, conditional transport, 13 proof declarations, anchors, and 2 differential probes elaborate with `--trust=0`. |
| Placeholder/unsafe policy | pass | Comment-stripped sources and Lean output contain no forbidden placeholder, bodyless declaration, unsafe/oracle mechanism, or `sorryAx`. |
| Axiom observation | pass, provisional | Parsed reports are exactly `propext`, `Classical.choice`, and `Quot.sound`. |
| Selected provenance | pass, bounded | Source/blob/olean hashes for five relevant pinned mathlib files, mathlib revision/tree/remote/license, and tool identities agree. |
| Proof dependency acceptance | fail closed | `S56-M-1061-PROOF` remains worker-provisional `[_]`; no master receipt accepts it. |
| Exact root kernel closure | fail closed | Lower localization, compact cover/core, tail, lower/upper analytic terminals, and a premise-free root body remain absent. |
| Complete foundation/TCB/provenance | fail closed | Selected hashes and observed axioms are not a full transitive declaration/import/bootstrap/compiler/SBOM closure. |
| Hermetic release replay | fail closed | The network-isolated run reused the automation-provided shared warm `.lake`; it was not a clean empty-cache cold build or offline archive restoration. |
| Independent verification | fail closed | No distinct signed identity, independently provisioned runner/cache, second attestation, or independent minimal release verifier exists. |

The root vector remains `H1/M3/R3`; `audit_complete=false` and
`theorem_complete=false`. No frozen obligation receives accepted closure.

## Commands

All commands ran from the worker repository root. This worker issued no `lake
update` or `lake build` command. During a superseded failed rerun, however,
`lake env printenv LEAN_PATH` encountered a missing canonical `flt-regular`
artifact and Lake attempted and later completed its pinned clone in the shared
canonical `.lake`. That failed run is excluded from the evidence above. The
final runner no longer invokes Lake for discovery and omits `flt-regular` from
the target-specific `LEAN_PATH`; the shared-cache side effect is disclosed as
invalid worker evidence rather than credited.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets in ranks 1 through 1546 passed |
| `python3 scripts/stage1_target.py show THM-M-1061` | 0 | rank 504, planned, L0/rework-required, theorem incomplete |
| `python3 -I -B Stage1_Instances/THM-M-1061/check_validation.py` | 0 | narrow replay and truthful fail-closed decisions passed |
| `python3 Stage1_Instances/THM-M-1061/check_statement.py` | 0 | exact expression fingerprint and four mutations passed |
| `python3 Stage1_Instances/THM-M-1061/check_anchor_audit.py` | 0 | bounded M4 audit and pinned mathlib revision passed |
| `python3 Stage1_Instances/THM-M-1061/check_obligation_tree.py` | 0 | 15 obligations, 49 typed edges, open M3 root passed |
| `python3 Stage1_Instances/THM-M-1061/check_proof.py` | 0 | partial bodies, hashes, axiom reports, and open-root boundary passed |
| `python3 -m json.tool Stage1_Instances/THM-M-1061/validation-spec.json >/dev/null` | 0 | valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-1061/validation-receipt.json >/dev/null` | 0 | valid JSON |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-m1061-pycache python3 -m py_compile Stage1_Instances/THM-M-1061/check_validation.py` | 0 | validator syntax passed outside the repository |
| `git diff --check -- Stage1_Instances/THM-M-1061 .stage1-worker-selftest.json` | 0 | no whitespace errors |

First failed node gate: `dependency.S56-M-1061-PROOF.master_acceptance`.
First failed theorem gate: `M1061-L-LOWER-LOCAL`. The remaining root cut is
`M1061-L-LOWER-LOCAL`, `M1061-T-LOWER`, `M1061-C-COMPACT-COVER`,
`M1061-L-CORE-UPPER`, `M1061-L-TAIL-UPPER`, and `M1061-T-UPPER`.
The frozen pre-proof architecture projects this same open subtree through its
coarser cut `{M1061-T-LIMIT-MERGE}`; the six-node list is the proof receipt's
post-implementation analytic cut and does not rewrite that frozen graph.

Status boundary: provisional worker self-test of the validation phase only. It
is not an accepted receipt, M0/E0/E1, H0/R0, `AUDIT-Z`, `THEOREM-Z`, release,
theorem completion, or master acceptance.
