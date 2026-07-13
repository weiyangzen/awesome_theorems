# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:6826-6831` gives exactly the name
`Erdős-Heilbronn猜想`, attribution Paul Erdos/Hans Heilbronn, year 1964, gloss
`子集和的大小下界`, high importance, and status `已验证`. Git history places all six uncited lines
in commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. It supplies no formula, ambient group,
prime hypothesis, definition of restricted addition, quantifiers, boundary convention, citation,
proof, or formal artifact.

`Docs/Stage0_Blueprint.md:25471-25496` repeats the gloss while explicitly leaving exact definitions
and premises, proof route, dependencies, equivalent forms, axioms, machine state, and artifact links
open. Its generic closed-result prose is planning metadata. The rev-5.6 manifest keeps `已验证` only
as `source_status_untrusted` and resets the target to `L0 / rework_required`.

## Inspected secondary discriminator

S. M. Jayasuriya, S. D. Reich, and J. P. Wheeler, *On the inverse Erdos-Heilbronn problem for
restricted set addition in finite groups*, arXiv:`1210.6509v2` (4 October 2013), was inspected from
the immutable version URL `https://arxiv.org/pdf/1210.6509v2`. The observed 198290-byte PDF has
SHA-256 `fb3e54b877a46c4bd3677f50061d2cb39de1a88aec48a7c6e4a019918135b26c`.

On PDF page 3, Section 2.2 and Theorem 2.2 describe the two-set restricted-sum result: for prime
`p` and nonempty `A, B` in `Z/pZ`, the set of `a + b` with `a != b` has cardinality at least the
minimum of `p` and `|A| + |B| - 3`. The following paragraph says Dias da Silva and Hamidoune first
proved the `A = B` case in 1994 and Alon, Nathanson, and Ruzsa proved the general case in 1995;
Remark 2.3 calls the `A = B` case the Dias da Silva-Hamidoune theorem. The same page says the
conjecture was stated at a 1963 conference and did **not** appear in the 1964 Erdos-Heilbronn paper.

This survey is a useful family discriminator and source-search map, not a primary H0 source. It
does not select what the sparse catalog intended, and it has no independent source-review receipt.

## Bibliographic leads

Crossref metadata identifies P. Erdos and Hans Heilbronn, *On the addition of residue classes mod
p*, *Acta Arithmetica* 9(2) (1964), 149-159, DOI `10.4064/aa-9-2-149-159`. This fixes a
bibliographic identity only. In light of the inspected survey, it must not be cited as if it
contained the conjecture without primary-page inspection.

Crossref also identifies J. A. Dias da Silva and Y. O. Hamidoune, *Cyclic Spaces for Grassmann
Derivatives and Additive Theory*, *Bulletin of the London Mathematical Society* 26(2) (1994),
140-146, DOI `10.1112/blms/26.2.140`. It is a primary proof lead for the `A = B` case, but its
theorem text, incorporated definitions, assumptions, proof boundary, corrections, and errata have
not been admitted or independently reviewed here. Its target-level ownership also overlaps the
separate `THM-M-0935` record and must be resolved before statement selection.

The survey further points to the 1963 conference proceedings and Erdos's 1971 problem list for the
initial/formal statement, and to the 1995/1996 Alon-Nathanson-Ruzsa papers for the general proof.
These are bibliography leads reconstructed from a secondary source, not inspected primary records.

## Component crosswalk

| Catalog/source component | Candidate mathematical meaning | Pinned Lean surface | Intake assessment |
|---|---|---|---|
| `子集和` | sums of all subsets of one finite set | `Finset.subsetSum` | literal vocabulary candidate, but a different construction from restricted pair sums |
| restricted sum | sums `a + b` with `a != b` | product/filter/image or an eventual dedicated definition | no dedicated pinned interface located; encoding not frozen |
| one-set case | `A` paired with itself | one finite set plus restricted self-sum | conventional conjecture/proof specialization only |
| two-set case | `A` paired with `B` and ambient-element inequality | two finite sets plus restricted binary image | later general theorem; catalog does not select it |
| modulus | prime cyclic group `Z/pZ` | `ZMod p` and `Nat.Prime p` | strong conventional candidate, absent from catalog gloss |
| lower bound | minimum of modulus size and a cardinal expression | `Nat.min`, integer casts, or side-conditioned natural subtraction | arithmetic and small-cardinality convention open |
| unrestricted neighbor | all sums `A + B` | `ZMod.cauchy_davenport` | checked neighboring theorem, not a restricted-sum proof |
| `已验证` | untrusted inventory status | accepted exact-target kernel receipt | no source or proof credit |

## Pinned Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, module
`Mathlib.Combinatorics.Additive.SubsetSum` defines `Finset.subsetSum` as the image of the powerset
under finite summation. Module `Mathlib.Combinatorics.Additive.CauchyDavenport` declares
`ZMod.cauchy_davenport` for the unrestricted pointwise sum of two nonempty finsets modulo a prime.
`IntakeProbe.lean` elaborates these declarations and generic product/filter/image vocabulary.

A bounded case-insensitive search of repository Lean and pinned mathlib for Erdos-Heilbronn, Dias
da Silva, and restricted-sumset names found no obvious exact declaration. That is an intake search
result, not a global absence claim or the downstream immutable anchor audit. The available APIs
neither choose the source proposition nor prove it, so the machine status is `M4`.

## Admission boundary

Before the statement phase can close, accountable reviewers must admit an immutable primary
statement, select the one-set/two-set/`h`-fold boundary, map every binder, premise, definition,
conclusion, historical/proof-source role, and small-cardinality case, audit corrections and errata,
and approve the target's relationship to `THM-M-0935`. The selected claim must then elaborate with
minimal pinned imports, receive expression/environment fingerprints, compile every credited
transport, and survive the required statement mutations.

This crosswalk supports provisional `H1` only. It freezes source leads, ambiguities, and exclusions;
it does not freeze a canonical proposition or accept `H0`, `M0`, `R0`, audit completion, theorem
completion, or master acceptance.
