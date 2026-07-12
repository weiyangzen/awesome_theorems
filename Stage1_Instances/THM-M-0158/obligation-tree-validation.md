# THM-M-0158 obligation-tree validation

Item: `S56-M-0158-OBLIGATION_TREE`. Base revision:
`4db87ed5646981780f2e885e21052d997afd1be7`.

Validation ran from the worker clone on 2026-07-12. The existing pinned Lake artifacts were reused;
no update, build, dependency clone, or fetch was run.

## Commands and results

| Command | Exit | Result |
|---|---:|---|
| `python3 Stage1_Instances/THM-M-0158/build_obligation_artifacts.py` | 0 | generated registry and seven typed graphs; denominator recorded below |
| `python3 Stage1_Instances/THM-M-0158/check_obligation_tree.py` | 0 | validated 15 obligations, hashes, node schema, reciprocal proof edges, graph adjacency, DAG reachability, hygiene, and open root boundary |
| `LEAN_PATH=$(cd Formalizations/Lean && lake env printenv LEAN_PATH) /home/sansha-2/.elan/toolchains/leanprover--lean4---v4.29.0/bin/lean -o Stage1_Instances/THM-M-0158/Statement.olean Stage1_Instances/THM-M-0158/Statement.lean` then `LEAN_PATH=Stage1_Instances/THM-M-0158:$(cd Formalizations/Lean && lake env printenv LEAN_PATH) /home/sansha-2/.elan/toolchains/leanprover--lean4---v4.29.0/bin/lean Stage1_Instances/THM-M-0158/ObligationTree.lean` | 0 | exact pinned Lean executable plus Lake-derived pinned dependency path elaborated the conditional composition; axiom report is `[propext, Classical.choice, Quot.sound]`; temporary `Statement.olean` removed |
| `lake env lean ../../Stage1_Instances/THM-M-0158/Statement.lean` (cwd `Formalizations/Lean`) | 0 | canonical statement still elaborates |
| `python3 ../../Stage1_Instances/THM-M-0158/check_statement.py` (cwd `Formalizations/Lean`) | 0 | canonical expression fingerprint unchanged and all four mutations distinguished |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0158` | 0 | rank 657, planned, theorem incomplete |
| `git diff --check -- Stage1_Instances/THM-M-0158` | 0 | no whitespace errors |

The frozen denominator SHA-256 is
`3011b75fc470fe84b58a07f7d7f4e31ca3e72e09730a17ff01480b3f1dc0a13c`. Validation gives
kernel evidence only for the conditional child-to-root composition, never for its explicit
derivation premise. There is no accepted receipt; master acceptance remains required.

An attempted `lake --dir Formalizations/Lean env lean ...` from the repository root exited 1 with
`no default toolchain configured`; it did not mutate dependencies. The successful composition check
therefore used the installed executable returned by `lake env which lean` and the dependency search
path returned by `lake env printenv LEAN_PATH`. The ordinary statement check still ran directly via
`lake env lean` from `Formalizations/Lean`.
