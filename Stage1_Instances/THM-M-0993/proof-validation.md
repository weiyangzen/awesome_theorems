# THM-M-0993 proof-phase validation

Item: `S56-M-0993-PROOF`

## Implemented closure

`Proof.lean` proves the exact statement-phase finite-family product-form target.
It discharges the frozen leaves with pinned mathlib declarations:

| Obligation | Proof declaration | Terminal body |
|---|---|---|
| `M0993-L-SUM-INT` | `sum_integrable` | `iIndepFun.integrable_exp_mul_sum` |
| `M0993-L-MARKOV` | `exponential_markov` | `measure_ge_le_exp_mul_mgf` |
| `M0993-L-FACTOR` | `sum_mgf_factorization` | `iIndepFun.mgf_sum` plus definitional unfolding of `mgf` |
| `M0993-B-EMPTY` | `empty_family_boundary` | kernel-checked finite sum/product simplification |
| `M0993-T-ASSEMBLE`, `M0993-ROOT` | `chernoff_upper_tail` | local composition of the three leaves |

The proof target is checked textually against `Statement.lean` by
`check_proof.py`; no weakened or substituted proposition is used.

## Narrow validation record

Base revision: `d46cb092bbdc519f36ab9ad2a4e6c75e36fb8789`.
Proof source SHA-256:
`8a665a6407cbe71240ddfc8f311778328953194ae3097454edad35e851d7d042`.

All commands ran from the worker-clone root unless a command contains an
explicit `cd`. No dependency update, fetch, clone, or `.lake` mutation was
performed.

```text
$ python3 Docs/tools/check_stage1_standard.py
check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)
exit 0

$ python3 scripts/stage1_target.py check
stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)
exit 0

$ python3 Stage1_Instances/THM-M-0993/check_statement.py
statement_sha256: ecae1a493dd8be1ab742029ee934c64ecd0595761326dc1efadfa5fb2e590669; four mutations killed; mathlib 8a178386ffc0f5fef0b77738bb5449d50efeea95; Lean v4.29.0
exit 0

$ python3 Stage1_Instances/THM-M-0993/check_anchor_audit.py
check_anchor_audit: ok (exact pin, module hash, clauses, route, 4 candidates)
exit 0

$ python3 Stage1_Instances/THM-M-0993/check_obligation_tree.py
PASS THM-M-0993 obligation tree: 10 obligations, 21 typed edges
exit 0

$ python3 Stage1_Instances/THM-M-0993/check_proof.py
check_proof: ok (exact target, 5 proof declarations, no placeholders)
exit 0

$ cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0993/Proof.lean
sum_integrable: [propext, Classical.choice, Quot.sound]
exponential_markov: [propext, Classical.choice, Quot.sound]
sum_mgf_factorization: [propext, Classical.choice, Quot.sound]
empty_family_boundary: [propext, Classical.choice, Quot.sound]
chernoff_upper_tail: [propext, Classical.choice, Quot.sound]
exit 0

$ rg -n '\b(sorry|admit|axiom)\b' Stage1_Instances/THM-M-0993/Proof.lean
no matches
exit 1 (the expected ripgrep no-match status)

$ git diff --check -- Stage1_Instances/THM-M-0993
no output
exit 0
```

## Status boundary

This is self-tested proof-phase closure only. The later hermetic, freshness,
source/readability, independent validation, receipt, and release gates remain
outside this item. No theorem-completion or master-acceptance claim is made.
