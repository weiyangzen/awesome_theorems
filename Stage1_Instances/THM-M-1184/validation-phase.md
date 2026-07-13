# THM-M-1184 validation-phase result

Item: `S56-M-1184-VALIDATION`. Base revision:
`3bb4cb3ae15dff8b48c93242019edec3bf858e48`.

## Narrow validation

The structured recipe performs a trust-zero replay in a fresh temporary output
directory with the Lean subprocesses placed in a bubblewrap network namespace.
It re-elaborates the exact statement, checked conditional composition, all eight
proof-phase declarations, and `Validation.lean`'s separately written weak-duality
route. The differential module imports neither `Proof` nor `ObligationTree`.

Every printed declaration has exactly `propext`, `Classical.choice`, and
`Quot.sound` in its observed axiom set. The four local Lean modules pass a
comment-stripped prohibited-construct scan, and the differential declaration
passes `assert_no_sorry`. Statement, registry, graph, proof-receipt, toolchain,
mathlib revision/tree/remote, clean dependency worktree, and license hashes agree
with the recorded pins.

This validates only the existing weak branch and conditional composition. The
exact root is still `M2`: `kantorovichDuality_of_reverse` consumes an explicit
`ReverseDualityPackage`, and no body closes it. The reverse branch remains open
at `M1184-S-SEPARATION`, `M1184-C-POTENTIALS`, `M1184-L-GAP`,
`M1184-W-REVERSE`, and `M1184-T-STRONG`.

## Commands and results

All commands ran from the repository root on 2026-07-14 (Asia/Shanghai). The
pre-existing canonical `.lake` symlink was reused read-only. No `lake update`,
`lake build`, dependency clone/fetch, or `.lake` mutation was performed.

| Command | Exit | Exact result summary |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1184` | 0 | rank 169, lane `hard_mathlib_anchor_and_wrapper`, planned, theorem incomplete |
| `git status --short --untracked-files=all` | 0 | before edits, only the pre-existing untracked `Formalizations/Lean/.lake` symlink; nonrelease worktree |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | revision `3bb4cb3a...e48`, tree `8e911f5a...ddc` |
| `python3 -I -B Stage1_Instances/THM-M-1184/check_validation.py` | 0 | trust-zero network-isolated fresh-output replay passed for the exact statement, conditional composition, local weak branch, and same-worker differential weak branch; root remained M2 and release gates failed closed |
| `python3 Stage1_Instances/THM-M-1184/check_obligation_tree.py` | 0 | frozen 16-obligation, 43-edge typed architecture passed; root open M2 |
| `python3 Stage1_Instances/THM-M-1184/check_proof.py` | 0 | product coupling and weak-duality package closed provisionally; reverse package and root open |
| JSON parsing, Python syntax compilation to `/tmp`, scoped source scan, and `git diff --check` | 0 | new structured artifacts parsed, validator compiled, no prohibited construct matched, and whitespace checks passed |

## Gate decisions

| Gate | Decision | Evidence or failure |
|---|---|---|
| Exact kernel replay | provisional pass | The exact target, conditional composition, weak proof declarations, and differential weak package elaborate at `--trust=0` with fresh local oleans. |
| Placeholder and unsafe boundary | provisional pass | The source scan finds no `sorry`, `admit`, `sorryAx`, local `axiom`, `unsafe`, `opaque`, `extern`, `implemented_by`, or `native_decide`; the differential declaration also passes kernel `assert_no_sorry`. |
| Axiom observation | provisional pass | All checked declarations report exactly the selected classical trio. `M1184-S-FOUNDATION` remains M4, so no accepted foundation/TCB closure is inferred. |
| Direct local provenance | provisional pass | Content-addressed sources, receipt links, Lean/Lake binaries, pins, clean mathlib tree, remote, and license agree. `M1184-X-PROVENANCE` remains M4 because the full transitive declaration/import/artifact closure is not serialized or accepted. |
| Proof dependency and exact root | fail closed | The proof receipt is provisional, the reverse branch has no proof body, and the exact root remains M2. |
| Hermetic release replay | fail closed | The network-isolated Lean subprocesses still consume a shared warm `.lake`; there is no clean checkout, empty user/package/build caches, cold rebuild, complete SBOM/TCB, or offline archive restoration. |
| Independent verification | fail closed | The differential module ran under the same worker identity, checkout, and shared cache; there are no distinct signed attestations or independently provisioned verifier. |

The validation node is genuinely self-tested as an honest negative-root receipt.
It grants no accepted obligation state, `E0/E1`, root `M0-*`, `AUDIT-Z`,
`THEOREM-Z`, theorem completion, release, or master-acceptance credit.
