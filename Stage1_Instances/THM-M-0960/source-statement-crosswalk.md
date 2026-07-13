# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:7008-7013` supplies exactly the title
`Ellenberg-Gijswijt定理`, attribution to Jordan Ellenberg and Dion Gijswijt, the year 2017, the
gloss `cap集的上界` ("an upper bound for cap sets"), importance "high," and status `已验证`. Git
history attributes all six uncited lines to commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record contains no formula, definition,
ordered binders, hypotheses, conclusion, theorem locator, proof boundary, correction history,
reviewer, or formal artifact.

`Docs/Stage0_Blueprint.md:26173-26198` repeats the gloss while explicitly leaving the formal
system, foundation, exact definitions and premises, proof route, dependencies, alternate forms,
axioms, machine state, and artifact links open. The rev-5.6 manifest preserves `已验证` only as
untrusted metadata and resets the target to `L0 / rework_required`.

## Inspected primary source lead

The publisher-hosted article Jordan S. Ellenberg and Dion Gijswijt, *On large subsets of F_q^n
with no three-term arithmetic progression*, *Annals of Mathematics* 185 (2017), issue 1,
pages 339-343, DOI `10.4007/annals.2017.185.1.8`, was inspected on 2026-07-13. Its observed PDF
SHA-256 is `9c54de6e297f0ac678c640def09b3ac8ab960aca05f4059d44e95c9e38b43c8c`.

- Theorem 4, printed page 341, assumes a finite field `F_q`; coefficients `alpha`, `beta`, and
  `gamma`, not all zero, with sum zero; and a subset `A` of `F_q^n` for which the corresponding
  equation has only diagonal solutions in `A^3`. It concludes
  `|A| <= 3 m_((q-1)n/3)`, using the preceding definition of `m_d` as the number of monomials with
  total degree at most `d` and each variable exponent at most `q - 1`.
- Corollary 5, printed page 342, states that a subset `A` of `(Z/3Z)^n` containing no three-term
  arithmetic progression satisfies `|A| = o(2.756^n)`.
- The surrounding prose also derives a qualitative `c^n` bound with `c < q` and discusses the
  result for odd primes.

The arXiv v1 manuscript `1605.09223v1`, dated 2016-05-30, was inspected separately and has observed
PDF SHA-256 `3cd77ddab97f046121ef684d68cea9d175b438363ee60b2abe1faa0db05f116b`.
It is not silently treated as the publication. The manuscript's setup gives the degree range
`[0, 2n]` rather than `[0, (q - 1)n]`; its Proposition 2 remark says `n > 2m_(d/2)` rather than the
correct cardinal condition `|A| > 2m_(d/2)`; and it calls rank-one summands "rank 1" where the
publication says "rank at most 1." Its Theorem 4 states `gamma != 0`, whereas the publisher version
uses the symmetric "not all zero" hypothesis and begins the proof by relabeling so that
`gamma != 0`. The manuscript also calls the optimized cutoff an integer despite substituting a
possibly nonintegral value, while the publication consistently permits real `d`, and the
large-deviation computation changes from the lower tail to its symmetric upper tail. These
differences require an edition and correction decision before any source-identical target is frozen.

A bounded publisher audit on 2026-07-13 found no article-page erratum link; publisher searches for
the authors plus "erratum" returned no result; issue 185(1) lists an unrelated erratum as its next
article; and the Crossref record exposed no update relation. This supports only the statement "no
publisher-listed erratum was located in the recorded search," not a certified absence of errata.

This is a strong `H1` primary proof lead, not `H0`: the catalog does not cite or select the article's
Theorem 4 or Corollary 5, no independent reviewer has approved the mapping, and an official errata
and correction audit has not been accepted.

## Clause crosswalk

| Catalog component | Published source surface | Prospective Lean surface | Intake assessment |
|---|---|---|---|
| `cap集` | progression-free subset of `(Z/3Z)^n` in Corollary 5 | `Set (Fin n -> ZMod 3)` or a checked equivalent plus `ThreeAPFree` | ambient encoding probed; exact definition and binder open |
| `上界` | exact monomial-count bound in Theorem 4 | `Nat.card`/`Finset.card` inequality with a defined bounded monomial count | candidate only; cutoff and cardinality representation open |
| `上界` | asymptotic `o(2.756^n)` in Corollary 5 | a maximum-cap-cardinality sequence, quantified family, or equivalent epsilon/threshold formulation | the printed corollary is conventional shorthand; its exact Lean binder is open, and 2.756 is a convenient decimal above the derived algebraic constant |
| Ellenberg-Gijswijt | general finite-field polynomial-method theorem | finite fields, vector powers, coefficients, diagonal-solution predicate | stronger/general source surface; catalog ownership unresolved |
| 2017 | Annals publication year | publisher edition and immutable source identity | bibliographically aligned; version delta still relevant |
| `已验证` | untrusted inventory label | accepted source review and kernel receipt would be required | no H0 or M credit |

## Pinned Lean boundary

Pinned mathlib supplies `ThreeAPFree`, `ZMod`, finite function spaces, and cardinality APIs. It also
supplies `roth_3ap_theorem`, a qualitative density theorem for finite abelian groups. That theorem
does not state the polynomial-method monomial bound or the `2.756^n` cap-set estimate. A bounded
search of repo-local Lean and pinned mathlib found no Ellenberg, Gijswijt, cap-set, slice-rank, or
exponential-bound declaration. `IntakeProbe.lean` authenticates only the prospective object model.

These observations are intake discovery, not the downstream immutable formal-anchor audit, a
global absence claim, or a proof.

## Source gate

Before leaving `H1`, accountable reviewers must select and preserve the approved source edition,
audit publication/manuscript changes and official errata, select the exact root proposition, map
every incorporated definition, binder, hypothesis, conclusion, and boundary case, and independently
approve fidelity to the catalog target. Only then may the statement phase freeze minimal imports,
the elaborated expression and environment fingerprints, checked alternate encodings, and the
required removed-hypothesis, changed-domain, binder-scope, and boundary-case mutations.
