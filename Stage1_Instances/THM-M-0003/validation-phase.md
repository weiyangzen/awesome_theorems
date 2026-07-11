# S56-M-0003-VALIDATION worker evidence

Date: `2026-07-12`. Base revision: `20ad05958a693d2ca2006867b6235dc8616d9220`.

The validation recipes re-elaborate the exact frozen proposition and two proof routes in a temporary
output directory: the direct pinned mathlib wrapper and the frozen four-segment composition. Both
close in the Lean kernel. The scoped declarations report only `propext`, `Classical.choice`, and
`Quot.sound`. The local proof source contains no `sorry`, `admit`, `sorryAx`, new `axiom`, `unsafe`
declaration, or oracle boundary.

Provenance is pinned to mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`
and tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b`. Its snake-lemma source and olean hashes
match the proof receipt, and the dependency worktree is clean. This supports a provisional `M0-W`
proposal for the exact root. It does not update the earlier obligation-tree snapshot, whose `M1`
classification truthfully records its pre-proof phase boundary.

Release gates fail closed. This worker clone uses the canonical warm `.lake` symlink, not an empty
independently provisioned cache. The host rejects `unshare --net`, so enforced network denial was
not available, although all imports resolved locally. There is no distinct verifier identity,
checkout, runner, or non-shared writable dependency cache. Axiom-policy and transitive-TCB
acceptance, `H0`, `R0`, and master acceptance also remain open. Therefore this receipt is not
release-grade `E0/E1` evidence and does not claim theorem completion.

## Commands and results

| Command | Exit | Exact result summary |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique ranks; all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0003` | 0 | rank 98; planned; theorem incomplete |
| `env -i PATH="$PATH" HOME="$HOME" LANG=C.UTF-8 LC_ALL=C.UTF-8 TZ=UTC bash ../../Stage1_Instances/THM-M-0003/check_proof.sh` from `Formalizations/Lean` | 0 | exact root and composition elaborated; declared axiom sets emitted; output SHA-256 `8f716392...f1e9` |
| `python3 Stage1_Instances/THM-M-0003/check_statement.py` | 0 | exact expression hash `11326894...a40`; four mutations killed |
| `python3 Stage1_Instances/THM-M-0003/check_obligation_tree.py` | 0 | 19 obligations and 52 typed edges structurally pass |
| `python3 Stage1_Instances/THM-M-0003/check_proof.py` | 0 | receipt hashes, terminal bodies, declarations, and hygiene pass |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --porcelain` | 0 | no output; pinned dependency worktree clean |
| `unshare --net true` | 1 | host denied creation of a network namespace; hermetic network gate remains failed |
| `python3 Stage1_Instances/THM-M-0003/check_validation.py` | 0 | receipt inputs and fail-closed root/release decisions agree |

First failed release gate: `trust.accepted_axiom_policy`. The exact root is kernel-closed, but
hermetic, independent, source, readability, and acceptance gates remain open.
