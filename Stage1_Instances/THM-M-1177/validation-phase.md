# THM-M-1177 validation-phase result

Item: `S56-M-1177-VALIDATION`. Base revision:
`ffea62ba1a7c0b0f84d70fd07f87d3eef57fe330`.

## Narrow validation

The structured recipe performs a trust-zero replay in a fresh temporary output
directory, with every Lean subprocess placed in a bubblewrap network namespace.
It re-elaborates the exact statement, the checked conditional composition, all
eight proof-phase declarations, and `Validation.lean`'s separately written
nonpositive-maximum route. The differential module imports neither `Proof` nor
`ObligationTree`.

Every printed declaration has exactly `propext`, `Classical.choice`, and
`Quot.sound` in its observed axiom set. The four local Lean modules pass a
comment-stripped prohibited-construct scan, and the differential declaration
passes `assert_no_sorry`. Statement, registry, graph, proof-receipt, toolchain,
mathlib revision/tree/origin, clean dependency worktree, and license hashes
agree with the recorded pins.

This validates only the existing degenerate branch and conditional
composition. The proof predecessor is still provisional. The authoritative
frozen graph therefore remains `M4` with cut
`{M1177-B-DEGENERATE, M1177-T-POSITIVE}`. If the proof receipt is later
master-accepted, the proposed state is only `M2` with `M1177-T-POSITIVE` open.
The conditional theorem `abpTarget_of_positiveMaximumPackage` consumes that
package explicitly; it is not a proof of the exact ABP root.

## Commands and results

Commands ran from the repository root on 2026-07-14 (Asia/Shanghai). The
pre-existing canonical `.lake` symlink was reused read-only. No `lake update`,
`lake build`, dependency clone/fetch, or `.lake` mutation was performed.

| Command | Exit | Exact result summary |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1177` | 0 | rank 377, lane `hard_mathlib_anchor_and_wrapper`, planned, theorem incomplete |
| `git status --short --untracked-files=all` | 0 | before edits, only the pre-existing untracked `Formalizations/Lean/.lake` symlink; nonrelease worktree |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | revision `ffea62ba...330`, tree `4662e08d...cb` |
| `python3 -I -B Stage1_Instances/THM-M-1177/check_validation.py` | 0 | trust-zero network-isolated fresh-output replay passed for the exact statement, conditional composition, local degenerate branch, and same-worker differential branch; accepted root remained M4 and release gates failed closed |
| `python3 Stage1_Instances/THM-M-1177/check_obligation_tree.py` | 0 | frozen 21-obligation, 69-edge architecture passed; accepted root open M4 |
| `python3 Stage1_Instances/THM-M-1177/check_proof.py` | 0 | degenerate package closed provisionally; positive-maximum package and exact root open |
| JSON parsing, Python syntax compilation to `/tmp`, scoped source scan, and `git diff --check` | 0 | structured artifacts parsed, validator compiled, no prohibited construct matched, and whitespace checks passed |

## Gate decisions

| Gate | Decision | Evidence or failure |
|---|---|---|
| Exact kernel replay | provisional pass | The exact target, conditional composition, proof declarations, and differential degenerate package elaborate at `--trust=0` with fresh local oleans. |
| Placeholder and unsafe boundary | provisional pass | No `sorry`, `admit`, `sorryAx`, local `axiom`, `unsafe`, `opaque`, `extern`, `implemented_by`, or `native_decide`; the differential declaration also passes kernel `assert_no_sorry`. |
| Axiom observation | provisional pass | All checked declarations report exactly the selected classical trio. `M1177-S-FOUNDATION` and `M1177-X-TCB` remain M4, so no accepted foundation/TCB closure is inferred. |
| Direct local provenance | provisional pass | Content-addressed sources, receipt links, Lean/Lake/bubblewrap identities, clean pinned mathlib revision/tree/origin, and license agree. Full transitive body/import/artifact provenance remains open. |
| Proof dependency and exact root | fail closed | The proof receipt is unaccepted and the positive-maximum package has no proof body; the exact root is open. |
| Hermetic release replay | fail closed | The network-isolated Lean subprocesses still consume a shared warm `.lake`; there is no clean checkout, empty caches, cold rebuild, complete SBOM/TCB archive, or offline restoration. |
| Independent verification | fail closed | The differential module ran under the same worker identity, checkout, toolchain, and shared cache; there are no distinct signed attestations or independently provisioned verifier. |

No canonical statement, proof body, obligation, graph, or accepted-state artifact
was changed. The small `check_proof.py` adjustment only permits a dependency
validator to coexist with the later validation-phase root handoff manifest.

The validation node is genuinely self-tested as an honest negative-root receipt.
It grants no accepted obligation state, `E0/E1`, root `M0-*`, `AUDIT-Z`,
`THEOREM-Z`, theorem completion, release, or master-acceptance credit.
