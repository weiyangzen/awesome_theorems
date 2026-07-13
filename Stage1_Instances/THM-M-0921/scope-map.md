# Scope map

## Preserved subject family

The intake preserves exactly the catalog family `Catalan numbers: counting in many combinatorial
problems`. A later statement phase may select one exact root or an explicitly approved multi-root
package only after an immutable source passage is mapped and independently reviewed. Candidate
components, none selected as the target at intake, include:

- a sequence `C_n`, defined recursively or by a source-fixed closed formula;
- equality between the recursive sequence and `binom(2n,n)/(n+1)`;
- a generating-function identity for `C(x) = sum C_n x^n`;
- the number of rooted binary trees with a specified node convention;
- the number of Dyck words or paths with a specified length or semilength convention;
- polygon triangulations, balanced parenthesizations, noncrossing structures, or another explicitly
  defined family; and
- checked transports between any definitions or encodings that an approved root relates.

## Decisions required at statement freeze

The statement phase must freeze all of the following from an approved source rather than from
familiar notation:

1. Whether the root is a sequence identity, recurrence, generating-function equation, one
   enumeration theorem, a theorem schema, or a finite package of separately rooted results.
2. The definition and codomain of `C_n`, including whether recursion, a quotient of binomial
   coefficients, or a generating function is primitive.
3. The index domain and quantifier order, especially whether `n = 0` is included.
4. For a cardinality claim, the exact finite object type, size statistic, labels, rooting,
   orientation, planarity, and equivalence relation.
5. Whether the conclusion is an equality in `Nat`, `Int`, `Rat`, formal power series, finite
   cardinality, or an asymptotic or bijective assertion.
6. For division formulas, whether division is natural-number Euclidean division, field division
   plus integrality, or a divisibility identity such as `(n+1) * C_n = binom(2n,n)`.
7. The complete source edition, theorem/exercise locator, proof boundary, corrections and errata,
   ordered binders, hypotheses, conclusion, foundation profile, and computation policy.

## Degenerate and boundary cases

Source review must explicitly dispose of `n = 0` and `n = 1`; the empty tree and empty Dyck word;
whether tree size means internal nodes, all nodes, edges, or leaves; whether path length is `n` or
`2n`; degenerate polygons; empty products and sums; natural-number division and its integrality
side condition; formal-power-series coefficient conventions; labelled versus unlabelled objects;
and quotienting by rotation, reflection, isomorphism, or no equivalence at all.

## Explicit exclusions

- `THM-M-0390` (Catalan's conjecture) and `THM-M-0391` (Mihailescu's theorem) concern consecutive
  perfect powers, not Catalan numbers. Their names, statements, and evidence do not transfer.
- `THM-M-0922` (Stirling numbers) and `THM-M-0923` (Bell numbers) are neighboring counting-
  sequence targets and remain separately owned.
- The recurrence, closed form, generating-series equation, and each combinatorial interpretation
  are distinct claims until checked transports and package composition are frozen.
- One binary-tree or Dyck-word count cannot establish the catalog's unbounded phrase "many
  combinatorial problems," and a prose list of interpretations is not a theorem schema.
- A definition of `catalan`, computed initial values, OEIS metadata, a numerical table, or an
  unchecked bijection supplies no proof of a source-selected root.
- Catalan's constant, Catalan's conjecture, Fermat-Catalan equations, Fuss-Catalan numbers, and
  Catalan objects from unrelated conventions cannot substitute for this target.
- The catalog's untrusted verified label and the intake API probe supply no human-source credit or
  proof credit for an unidentified root.

## Formal boundary

Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` defines `catalan : Nat ->
Nat` recursively. It proves the recurrence, the central-binomial quotient formula, the equivalent
divisibility identity, counts rooted binary trees by internal nodes, counts Dyck words by
semilength, and proves a formal-power-series equation. These are strong exact formal candidates for
several possible roots. They are not automatically a formalization of the catalog gloss, because
the gloss does not select any one of them or define a bounded package. Exact imports, a canonical
expression and fingerprint, checked source transport, mutations, exhaustive candidate audit, and
proof-body provenance belong to later phases.
