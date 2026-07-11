# S56-M-0387-PROOF worker evidence

Date: `2026-07-12`

Base revision: `6f186d1f0e8b92e3a37b1b5987787a8b954cd1a7`

Pinned environment:

- Lean: `4.29.0` (`98dc76e3c0a9b856c9b98726b713fb04fab16740`)
- mathlib: `8a178386ffc0f5fef0b77738bb5449d50efeea95`
- flt-regular: `56161b6eb5281fbfe9c38f2bcec0f429ebc11a27`

## Proof bodies admitted

`Proof.lean` rechecks five declarations against pinned source bodies: the exact
target transport, exponent three, exponent four, the regular-prime family, and
the conditional composition from all odd-prime exponents to the frozen root.
The last declaration consumes its premise explicitly. It is not an
unconditional proof of FLT.

The first unresolved gate is `M0387-WTW`: no placeholder-free proof of every
nonregular odd-prime exponent exists in the locally pinned closure. The audited
Imperial exact-root candidate remains ineligible because its pinned source has
a transitive `sorry`. Consequently the proof phase cannot truthfully close all
121 root-relevant obligations, the root remains `M2`, and theorem completion is
false. This worker nevertheless self-tested the concrete proof bodies it added;
master acceptance must preserve this open boundary.

## Commands and exact results

From the repository root:

```text
$ python3 Docs/tools/check_stage1_standard.py
check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)
exit 0

$ python3 scripts/stage1_target.py check
stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)
exit 0

$ python3 scripts/stage1_target.py show THM-M-0387
manifest entry found at execution_rank 1; baseline L0; rework_required true; theorem_complete false
exit 0

$ (cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0387/Statement.lean)
printed the elaborated FermatLastTheoremTarget declaration
exit 0

$ (cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0387/Proof.lean)
fermatLastTheoremTarget_iff_mathlib: [propext]
exponentThree: [propext, Classical.choice, Quot.sound]
exponentFour: [propext, Classical.choice, Quot.sound]
regularPrimeExponent: [propext, Classical.choice, Quot.sound]
target_of_odd_prime_exponents: [propext, Classical.choice, Quot.sound]
exit 0

$ rg -n '\b(sorry|admit|sorryAx)\b|(^|[^[:alnum:]_])axiom[[:space:]]' Stage1_Instances/THM-M-0387/Statement.lean Stage1_Instances/THM-M-0387/Proof.lean
no matches
exit 1 (the expected clean result for rg)

$ python3 Stage1_Instances/THM-M-0387/check_obligation_tree.py
PASS THM-M-0387 obligation tree: 132 obligations, 140 typed edges
registry denominator sha256: e934e59a6dfc78dda8ade1978b1b037c982ab8d1a9ca3d2e6c105b6f00b36643
root closure: open (M2); no proof or theorem completion claimed
exit 0
```

Source SHA-256 values during validation:

```text
5d7df0da0e5e44a1e136392332c035269f5c3f8b229ee8b5992c1a0a94fd05e5  Stage1_Instances/THM-M-0387/Statement.lean
3d3adf5b2a9683d46daf9d9b29b6bcce3d7cf51c5dcdb879c01bc84110ac8c4e  Stage1_Instances/THM-M-0387/Proof.lean
```
