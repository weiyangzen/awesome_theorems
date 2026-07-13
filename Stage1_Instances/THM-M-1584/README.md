# THM-M-1584 rev-5.6 intake

`THM-M-1584` is the discrete-mathematics catalog item `Chaitin不可计算数` (`Chaitin
uncomputable number`). The repository attributes it to Gregory Chaitin, dates it to 1975, and
supplies only the gloss `Omega数的不可计算性` (`uncomputability of Omega numbers`) plus an
untrusted `verified` label. It supplies no source citation, machine model, definition of Omega,
quantifiers, hypotheses, conclusion, or formal artifact.

## Intake result

This dossier creates a fail-closed `planned` instance. The standard theorem family is recognizable:
after choosing a universal prefix-free or self-delimiting machine `U`, its halting probability is
the sum of `2^(-length p)` over halting programs `p`, and the resulting real is noncomputable.
That description is a scope discriminator, not the canonical statement.

The catalog does not say whether the root is for every universal prefix-free machine, one fixed
machine, or the family of Chaitin Omega reals. It also does not fix the program alphabet and
measure, universality convention, prefix-free domain, convergence and real encoding, definition of
computable real, or whether randomness and incompleteness consequences belong to the root.
Choosing any familiar formulation now would invent or substitute missing mathematics.

## Source and formal boundary

Two exact 1975 Chaitin publications are credible source leads: *Randomness and Mathematical Proof*
and *A Theory of Program Size Formally Identical to Information Theory*. Bibliographic metadata was
verified, but no complete primary text, pinpoint Omega definition/theorem, premise map, correction
audit, or independent source review was admitted. The catalog's 1975 date therefore identifies a
historical source family, not an `H0` statement.

`IntakeProbe.lean` elaborates adjacent pinned partial-recursive code, halting undecidability,
uniquely-decodable-code, and Kraft-McMillan APIs. A bounded exact-topic search found no Chaitin
Omega, halting-probability, prefix-free-machine, or algorithmic-randomness declaration in pinned
mathlib or repository-local Lean. This is intake discovery, not a downstream anchor audit or a
global absence claim.

The canonical mathematical and Lean targets remain null. The provisional vector is
`[H1, M4, R4]`: a standard theorem family and credible primary leads exist, but the exact source
statement is not mapped; no usable exact formal artifact is credited; and no source-faithful
readable proof can attach to an unfrozen root. All six downstream tasks remain open. No accepted
execution state, audit completion, theorem completion, or master acceptance is claimed.
