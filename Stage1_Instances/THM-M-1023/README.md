# THM-M-1023 theorem dossier

Lifecycle: `planned`. Intake, exact-statement, anchor-audit, and obligation-tree
artifacts are self-tested pending master acceptance. The exact statement
elaborates and the 17-node obligation denominator is frozen, but neither
Levy-Khinchin direction is proved. This dossier accepts no historical proof
credit and makes no claim of audit completion or theorem completion.

## Scope map

The repository metadata identifies the target as the Levy-Khinchin representation of infinitely divisible distributions. The intake interpretation is the classical real-line probability-measure theorem: a Borel probability measure on `R` is infinitely divisible exactly when its characteristic function admits Levy-Khinchin data. Both directions are in scope. Infinite divisibility is quantified over every integer `n >= 1` and uses convolution roots that are themselves probability measures.

The statement phase must freeze one normalization for the Fourier sign, Gaussian coefficient, truncation/compensation term, and Levy measure integrability condition. Those choices change the displayed drift parameter, so this dossier deliberately does not invent a formula and does not treat superficially different formulas as definitionally equal. Dirac measures, compound Poisson laws, and vanishing Gaussian or jump components remain in scope. The adjacent metadata target `THM-M-1024` is not substituted for or merged with this target.

No repository-local Lean declaration was found by the bounded intake search for the target name or standard English identifiers. This is a discovery result only, not proof that mathlib lacks a relevant API. A canonical Lean expression, minimal imports, normalized expression hash, checked transports, and mutation tests belong to the dependent statement node.

## Frozen proof architecture

The proof graph has two root-relevant terminal packages: the forward direction
constructs and uniquely identifies the Levy triplet from infinite divisibility;
the reverse direction scales valid triplet data and constructs probability
convolution roots. `ObligationTree.lean` checks that these two exact packages
compose into the frozen biconditional, without supplying either package.
`obligation-tree.md` records the typed route and node ledgers; the JSON registry
and graph bundle are the scope authority pending master acceptance.

The remaining workflow is `PROOF -> VALIDATION -> RELEASE`.

The minimal open root cut is `M1023-T-FORWARD` plus
`M1023-T-REVERSE`. Root debt remains `[H1, M3, R4]`.

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
