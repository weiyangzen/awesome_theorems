# THM-M-1018 release decision handoff

## Exact verdict

`S56-M-1018-RELEASE` is **blocked**. Lifecycle remains `planned`, the accepted root vector remains
`[H2, M3, R4]`, and both `audit_complete` and `theorem_complete` are false. No receipt is accepted,
and this worker does not promote theorem or repository state.

The first workflow failure is `S56-10.2-DEPENDENCY-ACCEPTANCE`: validation is provisional `[_]`,
blocked, explicitly nonrelease, and not master-accepted. Independently, the first mathematical
failure is `M1018-L-DIRICHLET.kernel_closure`; its missing sine-integral evaluation and bounds leave
`M1018-T-ANALYTIC` as the exact open root cut.

## Evidence reconciliation

Fresh release-scoped replay elaborates the exact statement, conditional obligation composition, five
partial endpoint/Portmanteau/weak-limit bodies, and three validation probes at trust zero. Each
checked theorem reports only `propext`, `Classical.choice`, and `Quot.sound`; the owned Lean source
scan finds no placeholder, bodyless declaration, unsafe/oracle hook, native shortcut, or external
implementation. These are real but partial results. `conditionalCanonicalBridge` consumes the full
fixed-data inversion premise and is not a premise-free inhabitant of `LevyInversionTarget`.

The predecessor validation receipt remains useful historical evidence within its stated boundary,
but its advertised recipe is not replayable at integrated HEAD. The checker requires the deleted
predecessor `.stage1-worker-selftest.json`, hard-codes revision `718e166c`, and expects that worker's
old dirty change set. The exact recorded command now exits nonzero. The new `check_release.py`
therefore replays Lean directly from temporary source copies; it does not relabel the stale recipe as
a pass or modify the predecessor artifacts.

Primary-source fidelity remains `H2`: no stable edition, theorem/page, exact convention, assumptions,
errata, node crosswalk, or independent review supports `H0`. No independently reviewed structured
surface supports `R0`. Complete accepted provenance/foundation/TCB and supply-chain closure, an
immutable clean input, cold empty-cache build, offline restoration, independent signed runners, a
minimal independent verifier, protected release CI, and a deterministic evidence bundle are absent.

## Commands and exact results

All commands ran on 2026-07-15 from base revision
`3f555cfc0879cb7c42e83d6bcf7b9e3e09997e58`. The canonical pinned `.lake` artifacts were reused
without `lake update`, `lake build`, clone, fetch, or dependency mutation.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets at ranks 1 through 1546 passed. |
| `python3 scripts/stage1_target.py show THM-M-1018` | 0 | Rank 494; lifecycle `planned`; L0/rework-required; theorem incomplete. |
| `python3 -I -B Stage1_Instances/THM-M-1018/check_obligation_tree.py` | 0 | Frozen registry passed with 17 obligations and 34 typed edges; root open `M3`, cut `M1018-T-ANALYTIC`. |
| `bash Stage1_Instances/THM-M-1018/check_proof.sh` | 0 | Five partial bodies elaborated at trust zero with only the recorded axiom trio. |
| `python3 -I -B Stage1_Instances/THM-M-1018/check_validation.py` (before and after creating this release packet) | 1, 1 | Before the release packet existed, the checker failed on the removed predecessor self-test packet. With this release packet present, it failed its hard-coded predecessor-HEAD assertion. Its old-diff assertion is a third snapshot coupling. |
| `python3 -I -B Stage1_Instances/THM-M-1018/check_release.py` | 0 | Current hashes, target/DAG boundary, source hygiene, pinned dependency identity, network-isolated fresh Lean replay, and the exact blocked decisions agreed. |
| JSON parsing, Python syntax compilation outside the repository, scoped prohibited-device scan, and `git diff --check` | 0 | Structured artifacts parsed, checker compiled, no forbidden proof device was found, and scoped whitespace passed. |

This node is genuinely self-tested as a negative release reconciliation and proposes worker state
`[_]`. That worker state means the decision artifact exists and passed its narrow checker; it does
not mean release acceptance. `AUDIT-Z`, `THEOREM-Z`, theorem completion, release, and master
acceptance all remain false.
