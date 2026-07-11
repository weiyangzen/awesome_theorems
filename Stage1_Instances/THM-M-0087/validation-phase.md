# THM-M-0087 validation-phase result

Item: `S56-M-0087-VALIDATION`. Base revision:
`b0f46ce08e1b6a797d65cf735b0ccf96bd57ddcb`.

The validation phase independently re-elaborates the frozen Gabriel-Popescu
statement, its four-package child-to-root composition, and the direct exact-root
wrapper in a fresh temporary output directory. All checked local and terminal
declarations report only `propext`, `Classical.choice`, and `Quot.sound`. The
three Lean modules contain no `sorry`, `admit`, `sorryAx`, local `axiom`, or
`unsafe` declaration.

Provenance is pinned to clean mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` and tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The terminal Gabriel-Popescu source
and compiled artifact hashes agree with the proof receipt. This supports a
provisional `M0-W` proposal for the exact root, pending master acceptance and
the trust policy gate.

## Commands and results

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique ranks; all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0087` | 0 | rank 133; planned; theorem incomplete |
| `env -i PATH="$PATH" HOME="$HOME" LANG=C.UTF-8 LC_ALL=C.UTF-8 TZ=UTC bash ../../Stage1_Instances/THM-M-0087/check_proof.sh` from `Formalizations/Lean` | 0 | exact statement, frozen composition, four proof packages, direct root wrapper, and terminal declarations checked |
| `python3 Stage1_Instances/THM-M-0087/check_anchor_audit.py` | 0 | six exact anchors and clean pinned mathlib revision passed |
| `python3 Stage1_Instances/THM-M-0087/check_obligation_tree.py` | 0 | 17 obligations and 33 typed edges passed |
| `python3 Stage1_Instances/THM-M-0087/check_proof.py` | 0 | proof declarations, source hashes, and hygiene passed |
| `python3 Stage1_Instances/THM-M-0087/check_validation.py` | 0 | independent hash, pin, provenance, hygiene, kernel, and fail-closed decisions passed |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --porcelain` | 0 | no output; pinned dependency worktree clean |
| `unshare --net true` | 1 | host denied a network namespace; enforced network isolation unavailable |
| `git diff --check -- Stage1_Instances/THM-M-0087 .stage1-worker-selftest.json` | 0 | no whitespace errors |

No update, build, clone, fetch, or other dependency mutation was performed.
Temporary `.olean` files were removed with the temporary directory.

## Gate boundary

This was a warm-cache replay using the canonical shared `.lake` symlink, not a
cold empty-cache build or offline restoration. The observed axioms do not yet
have an accepted theorem-specific foundation policy or complete transitive TCB
inventory. A distinct runner, second attestation, independently implemented
minimal verifier, `H0`, `R0`, `AUDIT-Z`, and master acceptance are absent.
Consequently `theorem_complete=false`; no release or independent-validation
claim is made.
