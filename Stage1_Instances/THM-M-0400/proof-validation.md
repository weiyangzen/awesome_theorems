# THM-M-0400 proof-phase validation

Item: `S56-M-0400-PROOF`

## Implemented bodies

`Proof.lean` supplies three genuine elementary lemmas from the frozen proof
route: each coordinate norm is bounded by `integerHeight`, every nonzero
integer vector has height at least one, and `rationalVector` preserves
nonzeroness. These bodies implement the height/nonzero encoding part of
`M0400-S-BOUNDARY`; they neither assume nor conceal the Subspace Theorem.

The deep coefficient-field, source-convention transport, auxiliary-object,
nonvanishing, gap, subspace-extraction, finite-cover, and terminal-composition
obligations remain open. Therefore no declaration of the canonical
`Stage1Rev56.THMM0400.Statement` theorem is made, no frozen obligation is
marked closed, the root remains `M3`, and theorem completion is false.

## Commands and exact results

Base revision: `15a5351889f1657f452569fe630c9e39edb81877`.
Validation ran on 2026-07-12 Asia/Shanghai (`2026-07-11T19:43:19Z` UTC).

| command | exit | result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique ranks and targets passed |
| `python3 scripts/stage1_target.py show THM-M-0400` | 0 | rank 13, planned, L0/rework-required, theorem incomplete |
| `python3 Stage1_Instances/THM-M-0400/check_obligation_tree.py` | 0 | 13 obligations, 36 typed edges, registry `54e7cf55a13703dbbe9da4759bb2feea896ff9e8e2c16efe0a6be1af68127a72` passed |
| `(cd Formalizations/Lean && bash ../../Stage1_Instances/THM-M-0400/check_proof.sh)` | 0 | statement and proof elaborated; all three declarations report only `propext`, `Classical.choice`, and `Quot.sound` |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| prohibited-token `rg` scan of `Proof.lean` | 1, expected empty | no `sorry`, `admit`, `axiom`, or `unsafe` match |
| `git diff --check -- Stage1_Instances/THM-M-0400` | 0 | no whitespace errors |

The check script removes its temporary `Statement.olean`. No `lake update`,
`lake build`, clone, fetch, network access, or `.lake` mutation was performed.
The pre-existing untracked `.lake` symlink is outside this item's owned path.

## Remaining boundary

This is a self-tested partial proof-phase result pending master acceptance. It
does not claim validation, release, H0, R0, audit completion, or theorem
completion. The retry condition for root proof work is a pinned formal proof of
the central Subspace-Theorem engine or a full local implementation of its open
obligations, followed by exact composition and the later trust gates.
