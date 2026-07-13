# THM-M-0918 scope map

## Preserved theorem family

- Target identity: `THM-M-0918`, named `Rogers-Ramanujan identities`.
- Repository attribution and date: Leonard Rogers/Srinivasa Ramanujan, 1894.
- Literal catalog gloss: `an identity of the partition function`.
- Conventional family: the first and second Rogers-Ramanujan identities, each having an analytic
  q-series/product form and a restricted-partition counting form.

The plural pair is the narrowest responsible family boundary. It is not yet a binder-complete
canonical statement. The repository does not select one member or authorize replacing the pair by
one convenient special case.

## Authoritative statement leads, not frozen claims

For complex `q` with `|q| < 1`, DLMF 17.2.49 and 17.2.50 display respectively:

```text
1 + sum_(n >= 1) q^(n^2) / ((1-q)(1-q^2)...(1-q^n))
  = product_(n >= 0) 1 / ((1-q^(5n+1))(1-q^(5n+4)))

1 + sum_(n >= 1) q^(n^2+n) / ((1-q)(1-q^2)...(1-q^n))
  = product_(n >= 0) 1 / ((1-q^(5n+2))(1-q^(5n+3))).
```

DLMF 26.10.13 and 26.10.14 give the corresponding partition-count forms: parts differing by at
least two versus parts congruent to `1` or `4` modulo five; and the same difference restriction
with every part at least two versus parts congruent to `2` or `3` modulo five. These displays are
scope locators only. The statement phase must admit one exact source and independently review the
full definitions and transports before freezing a proposition.

## Proposition-changing decisions

1. Whether the root is the first identity, second identity, conjunction of both, or a structured
   theorem family with separately identified roots.
2. Whether the canonical encoding is an analytic identity over `Complex`, a formal power-series
   coefficient identity, a partition-count equality for every `n : Nat`, or checked transports
   among these forms.
3. For the analytic form, the exact `q` domain, norm inequality, denominator nonvanishing,
   convergence notions, starting indices, and infinite sum/product conventions.
4. For the formal form, the coefficient ring, definitions of finite q-products and inverse
   factors, and justification that every inverse has unit constant coefficient.
5. For the combinatorial form, the representation of integer partitions, whether parts are stored
   increasingly or decreasingly, multiplicity behavior, and exact adjacent-difference predicate.
6. The residue predicate modulo five and the second identity's exclusion of part one, including
   whether these are encoded as positive parts or shifted natural indices.
7. Ordered quantifiers, coercions of cardinalities, equality codomain, names for the two identities,
   and the proof obligations connecting every alternate encoding.

These choices alter the proposition or its dependencies. None is silently resolved at intake.

## Boundary and degenerate cases

- `q = 0`, `q` on or outside the unit circle, and complex values where a chosen denominator or
  product convention needs explicit justification.
- Empty finite products, the `n = 0` series term, and whether the leading `1` is separated or
  expressed uniformly with a q-Pochhammer denominator.
- The empty partition of zero, one-part partitions, repeated equal parts, and partitions containing
  part one in the second identity.
- "Difference at least two" for partitions with fewer than two parts, and its dependence on the
  chosen order of parts.
- Residues represented by `1,4` or `2,3` modulo five, including the fact that partition parts are
  positive while Lean indices often begin at zero.

No case is excluded before an exact proposition is selected.

## Explicit exclusions

- `THM-M-0916` Euler's pentagonal-number theorem and `THM-M-0917` the generic partition-function
  item, even though their generating functions may become dependencies.
- `THM-M-0919` Gordon's generalization or `THM-M-0920` Andrews's partition theorem used as a
  replacement root without an exact checked specialization.
- Glaisher's theorem, Euler's odd/distinct partition identity, or a generic partition generating
  function used in place of the modulus-five difference-condition pair.
- A finite truncation, numerical coefficient check, asymptotic formula, or equality that assumes
  the desired identity as a premise.
- The catalog's `verified` label, DLMF formula availability, or a successful API probe used as
  human-source or kernel proof credit.

No canonical Lean target, expression fingerprint, checked alternate encoding, discovery protocol,
obligation registry, or proof state is frozen during intake.
