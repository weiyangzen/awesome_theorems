# Scope map

## Preserved catalog scope

- Target: `THM-M-0935`, `Dias da Silva-Hamidoune定理`, in combinatorics / enumerative
  combinatorics.
- Attribution and date: Dias da Silva / Hamidoune, 1994.
- Literal gloss: proof of the Erdos-Heilbronn conjecture.
- Lifecycle: `planned` from the uniform `L0 / rework_required` baseline.
- The catalog's `已验证` field is inventory metadata and supplies no source or machine credit.

The title, date, and gloss identify the restricted-sumset theorem family. They do not make the
general `h`-fold theorem and its `h = 2` corollary definitionally identical or choose which is this
target's canonical proposition.

## Candidate roots not credited

1. **General restricted `h`-fold theorem.** For a prime `p`, a finite set `A` in `F_p`, and an
   admissible natural `h`, let `h^A` contain sums of `h` pairwise distinct members of `A`. Then
   `|h^A| >= min(p, h * (|A| - h) + 1)`.
2. **Erdos-Heilbronn specialization.** For a prime `p` and a nonempty finite set `A` in `ZMod p`,
   the restricted self-sumset of unequal pairs has size at least `min(p, 2 * |A| - 3)`.
3. **Checked package.** The general theorem together with a formally checked `h = 2` transport to
   the catalog's conjecture wording.

These are candidate scope resolutions, not accepted statements. The primary article text and its
internal theorem locator have not been inspected, and secondary sources differ on whether the
admissible range includes `h = 0`.

## Proposition-changing decisions

The dependent statement phase must freeze all of the following from an immutable, independently
reviewed source passage:

- the general `h`-fold theorem, the `h = 2` conjecture specialization, or an explicit checked
  relationship between them;
- `F_p`, `ZMod p`, or another source-faithful cyclic-group representation, including a checked
  equivalence if more than one is credited;
- finite set versus finset presentation, decidable equality, and coercion conventions;
- the exact ordered binders for `p`, primality, `A`, `n = |A|`, and `h`;
- whether `A` must be nonempty independently of `h`, and whether `h` ranges over
  `0 <= h <= |A|` or `1 <= h <= |A|`;
- whether a restricted sum is the image of `A.powersetCard h` under finite sum, or an ordered tuple
  of pairwise-distinct members, plus the checked quotient/permutation transport;
- the exact natural-number arithmetic and parenthesization of
  `min p (h * (A.card - h) + 1)`, including the source-side side condition preventing truncated
  subtraction from changing the formula;
- whether `h = 2` is represented by two-element subsets or unequal ordered pairs, and the checked
  equality of their images in a commutative group; and
- every universe, typeclass, classical-choice, quotient, extensionality, and computation policy.

## Boundary cases

- `p = 0`, `p = 1`, and composite `p`; primality should exclude them but mutations must test it.
- `A = empty`, singleton `A`, and `A = univ`.
- `h = 0`, `h = 1`, `h = 2`, `h = |A|`, and `h > |A|`.
- `|A| < 2` in the `h = 2` formula, where natural subtraction can otherwise make a misleading
  totalized expression.
- equality at `h = |A|`, where the restricted sumset should be a singleton.
- the saturation branch where `h * (|A| - h) + 1 >= p`.
- repeated summands, different orderings of the same subset, and modularly equal sums from distinct
  subsets.
- the equivalence of `F_p` and `ZMod p`, and cardinal casts between finite types and naturals.

No case is excluded at intake because no canonical proposition has been selected.

## Explicit exclusions

- `THM-M-0934` (the Erdos-Heilbronn conjecture) silently merged with this proof-attribution target
  or sharing future receipts without an approved ownership and transport decision.
- `THM-M-0936` (Cauchy-Davenport), whose ordinary sumset has no pairwise-distinct restriction.
- the Alon-Nathanson-Ruzsa unequal-two-set extension, inverse restricted-sumset theorems, composite-
  modulus or arbitrary-group generalizations, weighted/linear variants, and signed subset sums.
- the paper's more general cyclic-subspace/Grassmann-derivative theorem used as the catalog root;
  it is potential proof architecture for the additive result, not an interchangeable conclusion.
- the unrestricted `Finset.subsetSum`, which unions sums over every subset cardinality.
- a premise or structure field that assumes the desired cardinality bound.
- finite examples, `native_decide`, random testing, an external solver, or an unchecked certificate
  used in place of the universal theorem.
- the untrusted catalog status, source metadata, bounded no-match search, or API probe treated as
  statement or proof evidence.

## Open gate

An independent additive-combinatorics reviewer must admit an immutable primary-source edition,
identify the exact theorem and all inherited definitions and assumptions, settle the general versus
`h = 2` ownership and endpoint conventions, inspect corrections or errata, and approve the
source-to-statement mapping. Only then may the statement phase elaborate and mutation-test the
matching Lean proposition.
