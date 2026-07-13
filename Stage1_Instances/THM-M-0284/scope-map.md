# Scope map

## Received claim

`Docs/researches/math_theorems.md` supplies the title `柯尔莫哥洛夫零一律`, the attribution Andrey
Kolmogorov, the year 1933, and the gloss `尾事件的零一性质`. This identifies the Kolmogorov tail
zero-one theorem family. It is not an exact proposition and supplies no citation, definition chain,
ordered binders, hypotheses, boundary cases, or formal declaration.

## Candidate classical boundary

A standard formulation starts with an independent sequence of random variables or sigma-algebras.
The tail sigma-algebra consists of events unchanged by discarding any finite initial segment. Every
event measurable in that tail sigma-algebra then has probability zero or one. This paragraph is a
scope guide only, not the frozen canonical claim.

The statement phase must select from an immutable source and freeze:

- independent random variables, their generated sigma-algebras, or an independent sequence of
  sub-sigma-algebras as the primitive input;
- a natural-number sequence or a more general directed index order, and the `atTop` versus reverse
  indexing convention used to describe the tail;
- the ambient measurable space and whether each component sigma-algebra must lie below a named
  ambient structure;
- an ordinary probability measure, a finite measure, a Markov-kernel version, or another exact
  source-specified measure model;
- the tail sigma-algebra definition, event measurability predicate, and equality of any alternate
  intersection-of-future-sigma-algebras encoding;
- the conclusion as `mu t = 0 or mu t = 1`, membership in `{0, 1}`, or another checked equivalent;
- all universes, typeclasses, quantifier order, implicit binders, and zero/trivial/empty cases.

## Pinned Lean candidate boundary

At mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, module
`Mathlib.Probability.Independence.ZeroOne` provides
`ProbabilityTheory.measure_zero_or_one_of_measurableSet_limsup_atTop`. Its surface quantifies over
a measurable carrier, an index type with `SemilatticeSup`, `NoMaxOrder`, and `Nonempty`, a sequence
of sub-sigma-algebras `s`, an ambient sigma-algebra `m0`, and a measure `mu`. From `s n <= m0`,
`iIndep s mu`, and measurability of `t` in `Filter.limsup s Filter.atTop`, it concludes
`mu t = 0 or mu t = 1`.

The same pinned module contains kernel, `atBot`, conditional, abstract-filter, tail
self-independence, and self-independent-event variants. The ordinary `atTop` declaration is an
exact-topic formal candidate, hence provisional `M3`; it is not silently made the target and
receives no proof credit at intake.

## Explicit exclusions

- Hewitt-Savage's finite-permutation law (`THM-M-1008`), Borel-Cantelli (`THM-M-0285`), the
  Kolmogorov three-series theorem (`THM-M-1007`), and martingale optional stopping.
- An arbitrary self-independent event lemma without the tail-sigma-algebra derivation.
- A kernel or conditional variant substituted for an ordinary-measure source, or conversely.
- A finite-coordinate, trivial-event, or assumed-zero-or-one special case used as the root.
- A structure that stores tail measurability or the desired conclusion as unearned data.
- The untrusted catalog status, a theorem-name match, documentation index, or API probe used as
  accepted source or proof evidence.

The legacy file `Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_284.lean` belongs to
`THM-M-1004` (optional stopping), not this target. Its slot number confers no identity or evidence.

## Downstream boundary

The next phase must approve and independently review an exact source proposition, then freeze and
mutation-test one minimally imported Lean expression and any checked transports. Formal anchor
audit, obligation construction, and proof credit remain later phases.
