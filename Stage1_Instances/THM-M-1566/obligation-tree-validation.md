# THM-M-1566 obligation-tree validation

Validated on 2026-07-12 in the worker clone at base revision
`3175b20b2d6ae989a526ad94ae0ff0d20df1bc58`. Lean used only the existing
pinned Lake environment. No dependency update, build, clone, or fetch ran.

| Command | Exit | Result |
|---|---:|---|
| `python3 Stage1_Instances/THM-M-1566/build_obligation_artifacts.py` | 0 | deterministically wrote 15 obligations and 40 typed edges; denominator `7ae15c07...3fe640` |
| `python3 Stage1_Instances/THM-M-1566/check_obligation_tree.py` | 0 | schema fields, frozen input hashes, denominators, reciprocal typed edges, root reachability, acyclicity, specs, and open-root boundary passed |
| `python3 Stage1_Instances/THM-M-1566/validate_obligation_tree.py` | 0 | exact statement source and conditional composition elaborated with no generated olean; axiom report was `[propext, Classical.choice, Quot.sound]` |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 targets consistent |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets and ranks consistent |
| `python3 scripts/stage1_target.py show THM-M-1566` | 0 | rank 182, planned lifecycle, theorem incomplete |
| forbidden-term scan of new Lean and Python sources | 1 | expected ripgrep no-match: no forbidden proof construct |
| `git diff --check -- Stage1_Instances/THM-M-1566 .stage1-worker-selftest.json` | 0 | no whitespace errors |

The first direct Lean attempt, `cd Formalizations/Lean && lake env lean
../../Stage1_Instances/THM-M-1566/ObligationTree.lean`, exited 1 because an
owned-path `Statement.olean` is deliberately absent from Lake's module search
path. The validator therefore concatenates the exact statement and tree source
in a temporary owned-path file, elaborates it with `lake env lean`, and deletes
the temporary file. This changes neither `.lake` nor the pinned sources.

## Boundary

This phase freezes the pre-status obligation universe and validates only the
conditional logical assembly. `M1566-T-EXISTENCE` and
`M1566-T-UNIQUENESS` are the minimal open root cut set and remain `M4`.
No human-source review, proof-body closure, release receipt, or theorem
completion is claimed. Master acceptance of this worker handoff remains
required.
