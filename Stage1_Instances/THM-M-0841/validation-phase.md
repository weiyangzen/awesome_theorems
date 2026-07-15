# THM-M-0841 validation-phase evidence

Item: `S56-M-0841-VALIDATION`. Base revision:
`6bf9ee93a322e7d25cf9249226222095f95d1cff`; base tree:
`24acf86e69ab2e6fca9480c6269b6429874ba295`.

## Verdict

`no_state_change`, with a genuinely self-tested narrow packet proposed as `[_]`. The structured
recipe replays the exact statement, audited anchor probes, conditional obligation-tree composition,
all five partial proof declarations, and a separately written conditional root composition at Lean
trust level zero. Each Lean process runs with a fresh temporary writable directory, a read-only host
root, a cleared fixed environment, and an unshared network namespace.

This does not validate the Erdos-Stone theorem. Both `DenseBase` and `DenseStep` remain explicit
premises with no proof bodies. The exact complement transport body also does not reconcile its
frozen logical-decomposition children. The proof receipt is worker-provisional, no frozen
obligation is closed, and the target-local structured DAG remains all-open. The accepted root vector
therefore stays H1/M3/R4.

## Commands and results

Commands ran in this isolated worker clone on 2026-07-16 (`Asia/Shanghai`). No dependency update,
build, clone, fetch, checkout, or `.lake` mutation was performed.

| Command | Exit | Exact result summary |
|---|---:|---|
| `timeout 180 python3 Docs/tools/check_stage1_standard.py` | 1 | The aggregate validator fails closed because target-owned validation outputs make the checked-in read-only theorem-DAG inventory differ from fresh generation. The worker cannot regenerate that authority. |
| `python3 Docs/tools/check_stage1_theorem_dag_v2.py` before owned output creation | 0 | The 1546-node v2 graph, state snapshot, typed edges/hints/groups, order, and digest passed at preflight. A post-output rerun fails only on the expected stale generated evidence inventory; no graph or authority file is edited here. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required. |
| `python3 scripts/stage1_target.py show THM-M-0841` | 0 | Rank 1398; planned; L0/rework-required; theorem incomplete. |
| `/usr/bin/python3 -I -B Stage1_Instances/THM-M-0841/check_validation.py --probe` | 0 | Network-isolated trust-zero replay produced deterministic hashes and observed 6 roots, 16672 transitive constants, 653 modules, only the three expected axioms, no unexpected bodyless declaration, and no unsafe declaration. |
| Execute the `validation-spec.json` `argv` without shell interpolation | 0 | Frozen inputs, empty dependency context, partial kernel/trust observations, selected provenance, fail-closed decisions, receipt/blocker/spec, and worker packet agree. |
| `python3 -m json.tool` over the ledger, validation spec, receipt, blocker, and worker packet | 0 | All five structured artifacts parse. |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0841-validation-pycache python3 -m py_compile Stage1_Instances/THM-M-0841/check_validation.py` | 0 | Checker syntax passes outside the repository. |
| `git diff --check -- Stage1_Instances/THM-M-0841 .stage1-worker-selftest.json` | 0 | No whitespace diagnostics. |

The replay uses the installed pinned Lean 4.29.0 executable and existing compiled package paths
from the automation-provided canonical `.lake` symlink. Bubblewrap denies network and exposes the
host read-only except for the temporary directory. This is stronger than an ordinary warm replay,
but it remains shared-cache nonrelease evidence, not section 10.6 cold hermetic evidence.

## Gate decisions

| Gate | Decision | Evidence or failure |
|---|---|---|
| Dependency context | pass | The v2 node has no hard parent, ancestor, edge, hint, or shared group. The required schema-1.1 ledger records the exact graph and context digests with a fully empty audited closure. |
| Narrow kernel replay | provisional pass | Exact statement, anchors, conditional architecture, five partial bodies, and differential composition elaborate at trust zero with network denied. |
| Placeholder and observed trust boundary | provisional pass | Lean `assert_no_sorry`, `#print sorries`, parser-aware scanning, and the transitive constant walk agree; all six roots expose only `propext`, `Classical.choice`, and `Quot.sound`. This is observation, not accepted complete TCB closure. |
| Selected provenance | provisional pass | Frozen local hashes, clean pinned mathlib revision/tree/remote/license, and nine selected source/blob/olean triples agree. |
| Proof dependency and exact root | fail closed | `S56-M-0841-PROOF` is only `[_]`; `DenseBase` and `DenseStep` have no bodies. Conditional declarations do not prove their premises. |
| Frozen graph composition | fail closed | The direct `sparseFromDense` body does not consume the open frozen decomposition children, so zero canonical obligations receive closure credit. |
| Complete trust and provenance | fail closed | The primary-source PDF is unavailable here, and no complete source/declaration/import/object/compiler/bootstrap/plugin/TCB/SBOM/archive closure exists. |
| Hermetic reproduction | fail closed | Shared warm cache; no immutable clean checkout, empty-cache cold build, offline archive restoration, or deterministic release bundle. |
| Independent verification | fail closed | `rootFromDenseProducts` is same-worker corroboration in the same checkout, toolchain, and cache, not a distinct signed runner or independent minimal verifier. |
| Human and readable review | fail closed | No independently accepted H0 primary-source crosswalk or R0 reconstruction exists. |

The first node gate is `dependency.S56-M-0841-PROOF.master_acceptance`; the first mathematical gate
is the pair `M0841-B-R-TWO` and `M0841-B-R-GE-THREE`; and the first release gate is
`S56-10.6-HERMETIC-COLD-EMPTY-CACHE-REPLAY`. The frozen root cut also retains
`M0841-S-COMPLEMENT-TRANSPORT` pending graph reconciliation.

The packet itself is replayed and self-tested, so the handoff proposes only `[_]` for integration
review. It grants no accepted frozen obligation, exact root, M0, validation completion, `AUDIT-Z`,
`THEOREM-Z`, release, theorem completion, or master acceptance.
