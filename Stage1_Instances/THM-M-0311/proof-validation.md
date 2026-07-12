# THM-M-0311 proof-phase validation

Item: `S56-M-0311-PROOF`  
Base revision: `106084d7f6343f3046dfb9e108503edbcdc86191`  
Validation date: `2026-07-12` (`Asia/Shanghai`)

## Result

`Proof.lean` admits pinned mathlib's `MeasureTheory.Lp.instCompleteSpace` separately at the frozen
real and complex branch types, composes both bodies through the obligation-tree certificate, and
proves the exact `RieszFischerTarget`. All four declarations report precisely `propext`,
`Classical.choice`, and `Quot.sound`. There are no extra hypotheses, finite-measure restrictions,
alternate `Lp` encodings, placeholders, added axioms, or unsafe declarations.

The existing canonical pinned `.lake` artifacts were reused read-only. Temporary local oleans were
created outside the repository and removed. No Lake update/build, dependency clone/fetch, or
`.lake` mutation was performed.

## Commands and exact outcomes

| command | exit | outcome |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets with ranks 1 through 1546 passed |
| `python3 scripts/stage1_target.py show THM-M-0311` | 0 | rank 813, planned, L0/rework-required, theorem incomplete |
| isolated `lake env lean` elaboration of `Statement.lean`, `ObligationTree.lean`, then `Proof.lean` with `ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0` | 0 | exact root and both branch bodies elaborated; each axiom probe printed `[propext, Classical.choice, Quot.sound]` |
| `python3 Stage1_Instances/THM-M-0311/check_proof.py` | 0 | proof surface, hygiene, four input hashes, receipt, exact root, and disclosed axioms passed |
| `python3 Stage1_Instances/THM-M-0311/check_statement.py` | 0 | frozen exact expression, structural mutations, environment, and pin passed |
| `python3 Stage1_Instances/THM-M-0311/check_anchor_audit.py` | 0 | immutable candidate pin, exact wrapper, source body, and hygiene passed |
| `python3 Stage1_Instances/THM-M-0311/check_obligation_tree.py` | 0 | 17 frozen obligations and 33 typed edges passed; the immutable pre-proof boundary remains M3 |
| `python3 -m json.tool Stage1_Instances/THM-M-0311/proof-receipt.json` | 0 | receipt is valid JSON |
| placeholder scan over `Proof.lean` | 1 | expected no-match result for `sorry`, `admit`, `sorryAx`, added `axiom`, or `unsafe` declaration |
| `git diff --check -- Stage1_Instances/THM-M-0311 .stage1-worker-selftest.json` | 0 | no whitespace errors |

## Status boundary

The proof node is self-tested pending master acceptance. The earlier frozen architecture truthfully
retains its pre-proof M3 observation and is not rewritten. Proof-phase closure does not establish
H0/R0, hermetic or independent validation, audit completion, release, or theorem completion; those
remain downstream gates.
