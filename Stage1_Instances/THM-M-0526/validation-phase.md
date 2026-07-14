# THM-M-0526 validation-phase result

Item: `S56-M-0526-VALIDATION`. Base revision:
`c470319c4a07f669317557ea705f6546605ac4da`.

## Narrow validation

The structured recipe re-elaborates the exact frozen target in `Statement.lean`, both conditional
composition certificates in `ObligationTree.lean`, all three partial proof declarations in
`Proof.lean`, and two separately written reconstructions in `Validation.lean`. Every Lean process
runs through the pinned `lake env lean --trust=0 -t0` in a fresh temporary output directory with a
fixed locale, timezone, and thread count. Bubblewrap clears the environment, makes `/tmp` private,
and denies network access to Python orchestration and every child process. The differential module
imports neither `Proof` nor `ObligationTree`.

Every checked declaration uses no axiom outside `propext`, `Classical.choice`, and `Quot.sound`.
The four local Lean files pass a nested-comment-aware scan for placeholders, bodyless declarations,
unsafe code, and oracle devices; both differential declarations also pass `assert_no_sorry`.
Current source hashes and the clean pinned mathlib revision, tree, origin, license, and selected
source/olean hashes agree with the receipt.

This is intentionally a negative-root validation. The proof predecessor is only provisional, and
its local bodies cover square commutativity and path subdivision, not the universal-property lift
or uniqueness packages. `SVK-CHANGE-BASEPATH` and six other members of the root cut remain open.
The root stays `[H2, M4, R4]`, `audit_complete=false`, and `theorem_complete=false`.

## Commands and results

Commands ran from the repository root on 2026-07-15 (Asia/Shanghai). The automation-provided
canonical `.lake` symlink was reused without mutation. No `lake update`, `lake build`, dependency
clone, or dependency fetch was run.

| Command | Exit | Exact result summary |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0526` | 0 | rank 583, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |
| `git status --short --untracked-files=all` | 0 | before edits, only the pre-existing untracked `Formalizations/Lean/.lake` symlink; nonrelease worktree |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | revision `c470319c...c4da`, tree `680bb215...4aa` |
| execute the `validation-spec.json` argv without shell interpolation; capture combined stdout/stderr | 0 | network-isolated trust-zero narrow replay passed; exact root, release hermeticity, and independent gates remained fail-closed |

The validation runner's exact summary is:

```text
PASS THM-M-0526 network-isolated trust-zero replay of the exact frozen target
PASS conditional composition, three partial declarations, and two differential reconstructions use only the observed classical axiom subset
PASS frozen hashes, placeholder scan, and selected pinned mathlib source/olean provenance
OPEN SVK-CHANGE-BASEPATH and six other root-cut obligations; exact root, release hermeticity, and distinct-runner verification fail closed
```

## Gate decisions

| Gate | Decision | Evidence or failure |
|---|---|---|
| Narrow kernel replay | provisional pass | Fresh local oleans elaborate the exact target and every claimed conditional, partial, or differential declaration at trust level zero. |
| Placeholder and unsafe boundary | provisional pass | No prohibited source device occurs; both differential declarations are kernel-reported sorry-free. |
| Axiom observation | provisional pass | Every checked declaration uses only the observed classical trio. This is not an accepted complete foundation/TCB closure. |
| Selected direct provenance | provisional pass | Current inputs are hash-bound; the pinned mathlib revision/tree/origin/license and selected source/olean artifacts agree. Full transitive provenance remains open. |
| Proof dependency and exact root | fail closed | The predecessor is not master accepted; lift existence, generation, and uniqueness branches remain open, so no exact root body exists. |
| Human-source and readability | fail closed | H2/R4, complete primary-source fidelity, readable reconstruction, and independent H0/R0 reviews remain open. |
| Hermetic release replay | fail closed | The run reused shared warm artifacts, not a clean checkout with empty caches, cold rebuild, offline restoration, and complete SBOM/TCB archive. |
| Independent verification | fail closed | The differential module shares this worker, checkout, toolchain, and cache; no distinct signed verifier or independently provisioned runner exists. |

The validation node is self-tested only as an honest, nonrelease blocked receipt. It grants no
accepted obligation state, exact root closure, `M0-*`, `E0/E1`, `AUDIT-Z`, `THEOREM-Z`, release,
theorem completion, or master acceptance.
