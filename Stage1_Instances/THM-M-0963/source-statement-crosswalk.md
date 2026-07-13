# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:7029-7034` supplies exactly the theorem name,
Ray-Chaudhuri/Wilson attribution, year 1975, the gloss `L-相交族的上界` ("upper bound for
an L-intersecting family"), importance "high," and status `已验证`. Git history places all
six uncited lines in commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record omits
the ground set, uniformity, definition and cardinality of `L`, parameter range, family
representation, ordered binders, exact bound, source locator, proof boundary, corrections,
and formal artifact.

`Docs/Stage0_Blueprint.md:26254-26278` repeats the gloss and explicitly leaves precise
definitions and premises, proof route, dependencies, alternate formulations, axioms, machine
state, and artifact links open. The rev-5.6 manifest retains `已验证` only as untrusted
metadata and resets the target to `L0 / rework_required`.

## Primary-source lead

D. K. Ray-Chaudhuri and R. M. Wilson, *On t-designs*, *Osaka Journal of Mathematics* 12
(1975), no. 3, 737-744, ISSN `0030-6126`. zbMATH Open record `0342.05018` confirms the
authors, title, journal, volume, year, pages, subject classification, and that an open version
exists. Project Euclid's discovered legacy locator is `euclid.ojm/1200769162`, though direct
requests were intercepted by its access-control page and therefore did not authenticate article
content in this run. Later papers consistently cite the publication as the source of the
eponymous bound.

The publisher and Osaka repository endpoints were unreachable or access-blocked from this
worker environment, so the primary pages were not inspected and no primary PDF hash is
claimed. The exact theorem number, wording, incorporated definitions, proof clauses, errata,
and relationship between the paper's t-design results and the commonly quoted L-intersection
corollary therefore remain open. This is a bibliographic lead supporting `H1`, not an `H0`
source packet.

## Immutable secondary restatements

- G. Hegedus, *A generalization of the Erdos-Ko-Rado Theorem*,
  arXiv:`1512.05531v2`, Theorem 1.6, PDF SHA-256
  `5476cb136628400030a75699b0e93e2f9855c57024304f8ac74c5db2c86f9452`.
- A. Barg and O. Musin, *Bounds on sets with few distances*, arXiv:`0905.2423v2`,
  Theorem 7 and reference [22], PDF SHA-256
  `b6423e0a3372fcb096559a01d38416203d9841d86788b860ee2e422660a680a0`.
- R. Mathew, T. K. Mishra, R. Ray, and S. Srivastava, *Modular and fractional
  L-intersecting families of vector spaces*, arXiv:`2004.04937v2`, introduction and
  reference list, PDF
  SHA-256 `b98ced16c18304392900eb56f5d44e98b2b8a5fa601296b39485bf9ae9b9707d`.

The first source states the full candidate binder shape; the second independently gives the
same `choose n s` bound; the third defines L-intersection and notes the all-`s`-subsets tight
example. None is the primary 1975 proof or an independent H0 review.

## Component crosswalk

| Catalog/secondary component | Candidate mathematical meaning | Prospective Lean surface | Intake assessment |
|---|---|---|---|
| finite ground set `[n]` | a set with exactly `n` points | `Fin n` | direct candidate encoding; abstract-type transport open |
| `L`, `|L| = s` | `s` permitted nonnegative intersection cardinalities | `L : Finset Nat`, `L.card = s` | set/list and exact/at-most conventions open |
| `k`-uniform family | every member is a `k`-subset of `[n]` | `F : Finset (Finset (Fin n))` plus `forall A in F, A.card = k` | no-duplicate finite-family model; source transport open |
| L-intersecting | distinct `A, B` in `F` satisfy `card (A inter B) in L` | `(F : Set _).Pairwise (fun A B => (A inter B).card in L)` | self-pair is deliberately excluded; exact encoding not frozen |
| `0 < s <= k <= n` | candidate parameter range | natural-number inequalities | primary endpoint audit open |
| upper bound | number of distinct family members is at most `choose n s` | `F.card <= n.choose s` | candidate conclusion, not accepted root |
| tightness | all `s`-subsets with `k=s`, `L={0,...,s-1}` meet the bound | `Finset.powersetCard` candidate witness | not part of the upper-bound declaration unless sourced |
| `已验证` | untrusted inventory label | no proposition or proof object | no H or M credit |

## Pinned Lean boundary

At mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`,
`Mathlib.Data.Finset.Powerset` provides `Finset.powersetCard`,
`Finset.card_powersetCard`, `Finset.card_le_card`, finite-set intersection, and
`Nat.choose`; imported pairwise infrastructure provides `Set.Pairwise`. A bounded lexical
search over pinned mathlib and repository-local Lean found no Ray-Chaudhuri-Wilson or
L-intersecting declaration under the recorded terms. This is discovery-only evidence, not an
exhaustive downstream anchor audit or a claim of global absence.

`IntakeProbe.lean` checks those interfaces and elaborates the candidate proposition shape.
It declares no theorem and supplies no proof. Before leaving `H1`, reviewers must inspect an
immutable primary edition, select the exact source passage, map every definition, binder,
premise, conclusion, boundary case and correction, and independently approve the crosswalk.
Only the later statement phase may freeze minimal imports, a canonical Lean expression and
environment fingerprint, checked transports, and the required statement mutations.
