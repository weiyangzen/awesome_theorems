# THM-M-1023 Intake Dossier

Lifecycle: `planned`. This dossier covers only `S56-M-1023-INTAKE`. It accepts no historical proof credit and makes no claim of exact Lean elaboration, audit completion, or theorem completion.

## Scope map

The repository metadata identifies the target as the Levy-Khinchin representation of infinitely divisible distributions. The intake interpretation is the classical real-line probability-measure theorem: a Borel probability measure on `R` is infinitely divisible exactly when its characteristic function admits Levy-Khinchin data. Both directions are in scope. Infinite divisibility is quantified over every integer `n >= 1` and uses convolution roots that are themselves probability measures.

The statement phase must freeze one normalization for the Fourier sign, Gaussian coefficient, truncation/compensation term, and Levy measure integrability condition. Those choices change the displayed drift parameter, so this dossier deliberately does not invent a formula and does not treat superficially different formulas as definitionally equal. Dirac measures, compound Poisson laws, and vanishing Gaussian or jump components remain in scope. The adjacent metadata target `THM-M-1024` is not substituted for or merged with this target.

No repository-local Lean declaration was found by the bounded intake search for the target name or standard English identifiers. This is a discovery result only, not proof that mathlib lacks a relevant API. A canonical Lean expression, minimal imports, normalized expression hash, checked transports, and mutation tests belong to the dependent statement node.

## Open task DAG

`S56-M-1023-STATEMENT` -> `ANCHOR_AUDIT` -> `OBLIGATION_TREE` -> `PROOF` -> `VALIDATION` -> `RELEASE`.

The first task must choose exact measure and convolution definitions, fix the Levy-Khinchin convention, elaborate the complete biconditional, and test the probability hypothesis, `n >= 1` scope, both implications, and degenerate components. No obligation registry or proof denominator is frozen by this intake.

## Intake validation

Base revision: `d6333f8365b25d4e77164d475fe735a47cf1e37d`. Commands were executed from the repository root on 2026-07-12.

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: ok; 15 assurance groups and 1546 uniform-L0 Lean 4 targets
python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required
python3 scripts/stage1_target.py show THM-M-1023
  exit 0: rank 499; planned; theorem_complete false
rg -n "无穷可分|infinitely divisible|InfinitelyDivisible|Infinite.*Divis" .
  exit 0: found only repository metadata/blueprint descriptions for this target; no Lean candidate was located
```

These checks validate membership, structural consistency, and the intake's bounded repository search. They do not validate a Lean statement or proof. JSON parsing, owned-path checks, and whitespace validation are included in the worker self-test; master acceptance remains outstanding.
