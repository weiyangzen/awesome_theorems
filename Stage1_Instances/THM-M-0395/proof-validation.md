# THM-M-0395 proof-phase validation

Item: `S56-M-0395-PROOF`

## Implemented bodies

`Proof.lean` supplies three genuine, premise-preserving finiteness transports:
finiteness pulls back through an injection, pulls back through the composed
base-change and Abel-Jacobi injections, and converts finiteness of the universal
point set to the canonical `Finite` conclusion. These bodies support the last
set-theoretic steps planned in `M0395-L3` and `M0395-T`.

They do not construct any arithmetic-geometric premise and therefore close no
frozen obligation on their own. In particular, there is no declaration of
`Stage1Rev56.THMM0395.Statement`; the root remains `M4`, and theorem completion
is false.

## Commands and exact results

Base revision: `c6c14c0add140b98175266dc6421066ea99c79b3`. Validation ran on
2026-07-12 Asia/Shanghai (`2026-07-11T19:33:36Z` UTC).

| command | exit | result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique ranks and targets passed |
| `python3 scripts/stage1_target.py show THM-M-0395` | 0 | rank 8, planned, L0/rework-required, theorem incomplete |
| `python3 Stage1_Instances/THM-M-0395/check_obligation_tree.py` | 0 | 17 obligations and 46 typed edges passed; root open M4 |
| `(cd Formalizations/Lean && bash ../../Stage1_Instances/THM-M-0395/check_proof.sh)` | 0 | statement and proof modules elaborated; all three declarations report only `propext`, `Classical.choice`, and `Quot.sound` |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| prohibited-token `rg` scan of `Proof.lean` | 1, expected empty | no `sorry`, `admit`, `axiom`, or `unsafe` match |
| `git diff --check -- Stage1_Instances/THM-M-0395` | 0 | no whitespace errors |

The check script removes its temporary `Statement.olean`. No `lake update`,
`lake build`, clone, fetch, network access, or `.lake` mutation was performed.

## Remaining cut set

`M0395-N`, `M0395-C`, `M0395-L1`, `M0395-X1`, `M0395-L2`, `M0395-L3`, and
`M0395-T` remain open, including their substantive children. Validation,
release, H0, R0, and theorem completion are unclaimed. This is a self-tested
partial proof-phase result pending master acceptance.
