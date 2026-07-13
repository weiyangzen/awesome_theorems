# Scope map

## Included family

The repository wording limits this target to the probabilistic Chebyshev inequality family:

- a random variable on a probability space;
- deviation from its expectation or mean;
- a two-sided tail probability bounded using variance or a second moment;
- a positive deviation threshold;
- a kernel-checked Lean 4 formulation once the exact source statement is approved.

The familiar prospective formula

`P({omega | r <= |X omega - E[X]|}) <= Var(X) / r^2`

for `r > 0` is a scope candidate, not the canonical statement. The source phase must establish
whether this is exactly the catalogue's intended form and how its probability-valued left side and
real-valued variance expression are encoded.

## Decisions required before the statement gate

An approved source and duplicate-target policy must settle:

- whether `THM-M-0282` and `THM-M-0992` are intentionally duplicate theorem instances, must be
  deduplicated, or are meant to have distinct statements;
- the sample-space universe and exact probability-measure encoding; the arbitrary finite-measure
  mathlib theorem is only a generalized formal candidate whose probability specialization would
  need a checked transport;
- real-valued variables versus a normed-space generalization;
- `MemLp X 2 P`, finite second moment, integrability plus measurability, or the weaker
  `AEStronglyMeasurable` extended-variance hypotheses;
- a closed event (`r <= |X - E[X]|`) versus a strict event, and `r : Real` versus a nonnegative
  threshold;
- the 1867 sum theorem's unstated mutual-independence premise, its omitted positive/nonzero domain
  for `alpha`, and the strict inside-interval versus closed-tail complement transport;
- real variance versus extended nonnegative variance, including all coercions and division rules;
- constant and zero-variance variables, empty or null spaces, and nonexistent or infinite moments;
- whether an equality case, sharpness statement, or standard-deviation normalization is part of
  the root rather than a later corollary.

Until those choices are source-backed and independently reviewed, the canonical statement,
ordered binders, hypotheses, conclusion, minimal imports, expression fingerprint, transports, and
statement mutations remain deliberately null or open.

## Explicit exclusions

- The deterministic Chebyshev sum inequality for similarly sorted finite sequences.
- Chebyshev polynomials, Chebyshev prime-counting functions, and approximation results carrying the
  same name.
- Markov's inequality alone, Cantelli's one-sided inequality, Hoeffding bounds, Chernoff bounds, or
  a weak-law theorem as substitutes for the two-sided variance bound.
- A fixed finite sample space, a bounded-variable special case, or a standard-normal example used
  as the unrestricted root.
- An arbitrary non-probability finite measure presented as the catalogue's expectation/probability
  semantics merely because the pinned mathlib declaration is generalized that way.
- A proposition assuming the desired probability inequality as a hypothesis or structure field.
- The duplicate `THM-M-0992` dossier, historical Stage1 wrapper, pinned candidate theorem, or
  untrusted `已验证` label used as inherited statement or proof credit.

## Neighbor boundary

`THM-M-0992` has the same title, attribution, year, and probability-tail gloss in a probability
category. Its current artifacts are discovery inputs only. The integration lane must resolve the
catalogue duplication without changing the authoritative target list in this worker task and
without broadening or substituting either theorem.
