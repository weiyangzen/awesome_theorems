# Scope map

## Preserved catalog scope

The repository fixes only target `THM-M-1583`, the label `algorithmic information theory`, the
attribution Solomonoff/Kolmogorov/Chaitin, the period 1960s, and the gloss `the algorithmic theory
of information`. Intake preserves that subject and historical attribution. It does not silently
turn a field description into a quantified theorem.

## Candidate roots not credited

- An invariance theorem saying that complexities induced by two universal description systems
  differ by at most an additive constant.
- A counting or incompressibility theorem saying that most fixed-length strings have no much
  shorter descriptions.
- Uncomputability, upper semicomputability, or failure of lower semicomputability for a specified
  plain or prefix-free complexity.
- A coding theorem relating prefix complexity, universal a priori probability, or algorithmic
  probability up to a convention-dependent additive or multiplicative constant.
- A Martin-Lof randomness characterization by prefix complexity.
- A convergence or dominance theorem for Solomonoff induction under a specified computable
  environment class.
- An incompleteness theorem or a theorem about Chaitin's halting probability.

No candidate is selected, conjoined, asserted, or credited at intake.

## Proposition-changing decisions

An approved target correction must freeze all of the following:

- one exact theorem and immutable source result rather than the whole field;
- finite binary strings, natural numbers, infinite sequences, measures, semimeasures, formal
  theories, or another precise object domain, including all encodings and universes;
- plain, prefix-free, monotone, process, conditional, time-bounded, or another complexity notion;
- the reference machine model, acceptable programs, input/output convention, pairing or auxiliary
  input convention, universality or optimality property, and how program length is measured;
- whether the result is machine-relative or invariant, and the dependency and quantifier scope of
  every additive or multiplicative constant;
- computable, partial computable, enumerable, upper semicomputable, lower semicomputable, or
  oracle-relative predicates and their representations;
- a finite counting measure, fair-coin measure, computable measure, universal semimeasure, or
  another probability object, including normalization and logarithm base;
- the exact conclusion: equality, inequality, bounded difference, existence, noncomputability,
  asymptotic statement, convergence, randomness equivalence, or incompleteness bound;
- ordered binders, hypotheses, excluded cases, foundation and computation policies, proof boundary,
  and checked transports for alternate encodings.

Each choice changes the proposition. This list is a resolution ledger, not a canonical claim.

## Degenerate and boundary cases

The statement phase must decide at least empty strings and programs; machines with empty domain,
non-prefix-free domain, no universality witness, or nonunique outputs; undefined computations;
zero-length descriptions; condition equal to the described object; singleton alphabets; empty and
finite sample spaces; zero probabilities and logarithms of zero; additive constants below zero or
with hidden machine dependence; strict versus non-strict length bounds; finite versus infinite
objects; oracle-free versus relative complexity; and existential versus fixed reference machines.

No case is excluded at intake. A structure or hypothesis that stores the desired optimality,
complexity bound, randomness equivalence, convergence, uncomputability, or incompleteness
conclusion as input data is circular.

## Neighbor and substitution exclusions

- `THM-M-1582` owns the separate `Kolmogorov complexity` catalog record. Its minimal-description
  gloss cannot silently become this field-wide target.
- `THM-M-1584` owns `Chaitin's uncomputable number`. A theorem about Omega cannot stand for all of
  algorithmic information theory.
- `Docs/researches/cs_theorems.md:647` is a separate computer-science Kolmogorov-complexity record
  whose gloss says `foundation of algorithmic information theory`; it transfers no identity or
  proof credit.
- The adjacent computer-science incompressibility record is a specific counting/result family, not
  this umbrella field.
- The invariance theorem, coding theorem, Levin-Schnorr theorem, Chaitin incompleteness, Berry
  paradox, halting problem, and Kleene recursion theorem are not interchangeable roots.
- Generic computability, Goedel-numbering, unique-decodability, or Kraft-McMillan APIs are
  substrate, not an algorithmic-information root theorem.
- A custom definition designed so that the desired result holds by reflexivity or by projecting a
  stored field is not a source-faithful formalization.
- Finite experiments, compression benchmarks, sampled programs, numerical probability estimates,
  and the untrusted `verified` label supply no theorem proof.

## Formal boundary

Pinned mathlib exposes codes and evaluation for partial recursive functions, computability of code
evaluation, finite uniquely decodable word sets, and the Kraft-McMillan inequality. The probe
authenticates only these adjacent interfaces. It does not expose a located definition of plain or
prefix-free Kolmogorov complexity, an optimal prefix-free universal machine, universal semimeasure,
Martin-Lof randomness, Solomonoff prior, or Chaitin Omega, and it states no target theorem.

No canonical Lean target, minimal import claim, expression fingerprint, checked transport,
mutation suite, obligation registry, discovery-protocol freeze, or proof body is credited at intake.
