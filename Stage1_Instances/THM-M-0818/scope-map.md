# Scope map

## Preserved theorem family

The repository fixes the eponym, authors, year, and the subject "existence of a monotone
subsequence." The intended statement must remain inside this sequence-selection family. Intake does
not silently choose among the following materially different members:

1. **Sharp finite asymmetric form.** A sequence of `(r - 1) * (s - 1) + 1` suitably ordered,
   distinct values contains an increasing subsequence of length `r` or a decreasing subsequence of
   length `s`; `(r - 1) * (s - 1)` is sharp.
2. **Square specialization.** A sequence of `n^2 + 1` distinct comparable values contains an
   increasing or decreasing subsequence of length `n + 1`.
3. **Weak finite form with ties.** Equal values are admitted and assigned to one or both monotone
   alternatives. The bound and strictness conventions depend on the exact formulation.
4. **Infinitary form.** Every infinite sequence in an appropriate ordered domain has an infinite
   increasing or nonincreasing subsequence. Pinned mathlib exposes a relation-parametric version.

## Decisions required at statement freeze

1. Select a pinpoint primary passage and independently review the exact finite or infinite result.
2. Freeze the ordered parameters and off-by-one convention: lengths `r,s` versus `r+1,s+1`, and
   input length `(r-1)(s-1)+1` versus `r*s+1`.
3. Fix the value domain: real ordinates, natural numbers, a linear order, a partial order, or an
   arbitrary type with a transitive relation.
4. Specify whether input values must be distinct and whether the index selection is an embedding,
   a strictly increasing map, a finset of indices, or an explicit subsequence object.
5. Specify strict increasing/decreasing versus weak monotone/antitone behavior and the treatment of
   equal values. In mathlib's candidate, the first branch uses `r` and the second uses `not r`:
   choosing `<` gives strictly increasing or nonincreasing, while choosing `<=` gives nondecreasing
   or strictly decreasing. Thus one fixed relation does not directly encode weak/weak alternatives.
6. Resolve boundary cases such as zero or one requested length, empty and singleton inputs, repeated
   values, constant sequences, and non-total relations.
7. Freeze the exact transport, if any, between the original planar ordinate formulation, a finite
   sequence statement, the square specialization, and the pinned infinitary relation statement.
8. Select foundation, classical-choice, TCB, computation, and freshness profiles only after the
   exact target and minimal imports are known.

## Explicit exclusions

- The happy-ending convex-polygon existence theorem, although it is the main geometric problem of
  the same 1935 paper. It is not the catalog gloss "monotone subsequence."
- Ramsey's theorem, the graph theorem, and the distance or gradient selection results in the paper.
- The Erdos-Ginzburg-Ziv theorem, Erdos-Ko-Rado theorem, Erdos-Renyi results, and unrelated eponyms.
- A two-element comparable pair or generic well-quasi-order result substituted for the quantitative
  finite theorem.
- An infinite theorem substituted for a finite sharp theorem, or conversely, without a checked and
  source-approved relationship.
- A theorem restricted to a convenient domain, weakened length bound, assumed witness, or distinct
  input when the selected source permits ties.
- The catalog label `已验证`, a source URL, an elaborated `#check`, or a theorem comment treated as
  human-proof, kernel-closure, or theorem-completion evidence.

No canonical expression, statement fingerprint, checked alternate encoding, obligation registry,
discovery protocol, proof state, or completion claim is frozen at intake.
