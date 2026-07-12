# Exact-statement gate blocker

Item: `S56-M-1090-STATEMENT`  
Theorem: `THM-M-1090`  
Verdict: blocked, with no statement acceptance or theorem-completion claim

## Source identity failure

The complete target-specific mathematical record in
`Docs/researches/math_theorems.md` is the title "Markov process" (`马氏过程`), the attribution
Andrey Markov, the year 1906, and the gloss "Markov property" (`马尔可夫性质`).
`Docs/Stage0_Blueprint.md` repeats the gloss but explicitly leaves the exact definitions and
premises unspecified. Neither record gives a formula, a theorem or definition number, a page, a
process construction, or hypotheses from which a Markov property is to be concluded.

Consequently there is no source-identified proposition whose ordered binders can be preserved in
Lean. In particular, the record does not decide:

- discrete versus continuous time;
- ordinary deterministic-time versus strong stopping-time Markov behavior;
- homogeneous versus inhomogeneous transition laws;
- natural versus enlarged or completed filtration;
- conditional-expectation, regular-conditional-law, or conditional-independence encoding;
- pointwise versus almost-everywhere equality and its exceptional-set quantification;
- the state-space regularity needed for a regular conditional distribution;
- whether the item is a definition of a class of processes or a theorem deriving the property for
  a specified construction.

Each choice changes the proposition rather than merely its Lean presentation. Selecting any one of
them would therefore invent or substitute mathematics, contrary to the rev-5.6 exact-statement
gate. Assuming a Markov identity and projecting it would also turn the unidentified record into a
tautological wrapper, not formalize an identified theorem.

## Lean and mutation-test consequence

The pinned environment contains relevant substrate (`MeasureTheory.Filtration`, conditional
expectations and distributions, and probability kernels), as the existing `IntakeProbe.lean`
check confirms. A repository-local search did not identify a temporal Markov-process predicate
that could resolve the source ambiguity. `ProbabilityTheory.IsMarkovKernel` is instead the
probability-mass property of a kernel and is not a process's temporal Markov property.

Because there is no canonical expression, this phase cannot truthfully provide an expression hash,
environment fingerprint bound to that expression, checked alternate-form transports, or the four
required mutation fixtures. Mutation tests cannot distinguish a source-preserving target from a
source-changing mutation until the source fixes the target.

## Required unblock

An accountable source decision must supply an immutable edition and digest, exact page and
definition/theorem locator, and a full formula fixing all choices above. If the intended item is
only the definition of "Markov process," it must be reclassified as a definition target; if it is a
theorem, the source must identify the constructed process and hypotheses that entail the selected
Markov predicate. Only then can the dependent statement phase elaborate the exact target and run
the mandated mutation suite.

The first failed gate is canonical source-statement identity. The machine status remains `M4`, and
downstream anchor, obligation-tree, proof, validation, and release work remains dependency-blocked.

