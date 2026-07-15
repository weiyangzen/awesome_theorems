# THM-M-1063 validation-phase evidence

Item: `S56-M-1063-VALIDATION`. Base revision:
`be2be0dfe2f4f2cbdd35f1f2397e5a372d199eb9`; base tree:
`2d3961f99039c515141bdff4511470530d799581`.

## Verdict

`blocked`, with a self-tested negative validation packet proposed as `[_]`. The structured recipe
replays the exact statement, the identity-only open-root interface, the audited mathlib anchors,
and both partial proof declarations at Lean trust level zero. Each Lean process has a fresh
temporary working directory, a read-only host root, a cleared fixed environment, and an unshared
network namespace. The two proof declarations and two separately authored scalar probes all report
exactly `propext`, `Classical.choice`, and `Quot.sound`.

This does not validate Donsker's invariance principle. `Proof.lean` proves standardization and the
time-one scalar CLT only. The frozen registry has 29 machine-required obligations, every terminal
proof-body ID is null, and the graph closes no obligation. Continuous polygonal-path construction
and measurability, finite-dimensional convergence, finite-second-moment tightness, subsequential
limit identification, Brownian-law uniqueness, and final path-space composition remain absent.

## Commands and results

Commands ran in this worker clone on 2026-07-15 (`Asia/Shanghai`). No `lake update`, `lake build`,
dependency clone/fetch, checkout, or `.lake` mutation was performed.

| Command | Exit | Exact result summary |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1063` | 0 | rank 506; planned; theorem incomplete |
| `python3 -B Stage1_Instances/THM-M-1063/check_obligation_tree.py` | 0 | 31 obligations and 125 typed edges passed; denominator `a55c3e2...26a7703`; root open M4 |
| execute `validation-spec.json` `argv` without shell interpolation | 0 | network-isolated trust-zero replay and fail-closed kernel, trust, selected provenance, state, and packet checks passed |
| `python3 -m json.tool` over spec, receipt, blocker, and worker packet | 0 | all four structured artifacts parsed |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-m1063-validation-pycache python3 -m py_compile Stage1_Instances/THM-M-1063/check_validation.py` | 0 | checker syntax passed outside the repository |
| `git diff --check -- Stage1_Instances/THM-M-1063 .stage1-worker-selftest.json` | 0 | no whitespace diagnostics |

The target's root-project `lake env` is unavailable because the pre-existing canonical
`flt-regular/.git/HEAD` points to missing `refs/heads/.invalid`. The replay therefore uses the
installed pinned Lean 4.29.0 executable and explicit existing compiled paths, excluding
`flt-regular`. This is a network-isolated warm-cache run, not a cold hermetic release run.

## Gate decisions

| Gate | Decision | Evidence or failure |
|---|---|---|
| Narrow kernel replay | provisional pass | Exact statement, identity interface, anchors, and four scalar proof/probe declarations elaborate at trust zero with network denied. |
| Placeholder and observed trust boundary | provisional pass | Parser-aware source scan is clean; all four proof/probe axiom reports contain only the selected classical trio. This is not accepted transitive trust closure. |
| Selected provenance | provisional pass | Frozen local hashes, clean pinned mathlib revision/tree/origin/license, and three direct source/blob/olean triples agree. |
| Proof dependency and exact root | fail closed | Proof is only worker-provisional, closes zero frozen obligations, and has no Donsker root body. |
| Complete trust and provenance | fail closed | No complete declaration/import/TCB/compiler/plugin/SBOM/license-archive closure exists. |
| Hermetic reproduction | fail closed | Shared warm cache; no immutable clean checkout, empty-cache cold build, offline archive restoration, or deterministic release bundle. |
| Independent verification | fail closed | `Validation.lean` is a same-worker differential scalar probe in the same checkout and cache, not a distinct signed runner or independent minimal verifier. |
| Human and readable review | fail closed | No independently accepted H0 source crosswalk or R0 reconstruction exists. |

The first node gate is
`dependency.S56-M-1063-PROOF.master_acceptance_and_exact_root_closure`; the first theorem package
is `M1063-C-PATH / M1063-C-MEAS`; and the first release gate is
`S56-10.6-HERMETIC-COLD-EMPTY-CACHE-REPLAY`. The remaining root cut is `M1063-L-CLT`,
`M1063-L-MODULUS`, `M1063-L-ASCOLI`, `M1063-L-PROKHOROV`, `M1063-L-LAW-UNIQUE`, and
`M1063-T-API`.

The validation packet itself is genuinely replayed and self-tested, so the worker handoff proposes
only `[_]`. It grants no accepted receipt, frozen-obligation closure, M0, validation completion,
`AUDIT-Z`, `THEOREM-Z`, release, theorem completion, or master acceptance.
