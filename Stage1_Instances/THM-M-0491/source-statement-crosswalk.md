# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:3602-3607` supplies exactly the title `梅纳德定理`, attribution to
James Maynard, the year 2013, the gloss `素数间隙的上界改进` ("improvement of the upper bound on
prime gaps"), importance `high`, and status `已验证`. Git history places all six uncited lines in
commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record contains no bibliography, theorem
locator, numeral, formula, definitions, binders, assumptions, conditionality, proof boundary,
correction history, reviewer, or formal artifact.

`Docs/Stage0_Blueprint.md:13460-13485` repeats the gloss while explicitly leaving the formal system,
foundation, exact definitions and premises, proof process, dependencies, alternate forms, axioms,
machine status, and artifact links open. The rev-5.6 manifest preserves `已验证` only as untrusted
metadata and resets the target to `L0 / rework_required`.

## Inspected primary source lead

James Maynard, *Small gaps between primes*, *Annals of Mathematics* 181 (2015), issue 1,
pages 383-413, DOI `10.4007/annals.2015.181.1.7`, is the matching primary source. The official
journal page and paper were inspected on 2026-07-13. The observed journal PDF had 528,115 bytes and
SHA-256 `3c24d010f00d1212418351b6f6baed9c94251a3ce958c36f56ebbc450ade9349`.

The paper originated as arXiv `1311.4600v1`, submitted 2013-11-19. The observed v1 source archive
had SHA-256 `f22c7cf10b89d3b97d521f98da460c0519743eae6b6c2a92797d862e23218067`.
The current v3, dated 2019-10-28 and described as correcting typos, had observed source-archive
SHA-256 `b9b9113d1fa1abb4781d1b4b93b3da80c01a10fbee1166ddc654f003c900a2df`.
The journal edition is the preferred statement lead; v1 explains the catalog's 2013 date but is not
an unqualified final-edition pin.

The paper's notation section fixes `N = {1, 2, ...}` and makes `p_n` the nth prime. Thus source
`m in N` means `m >= 1`, and source `p_1 = 2` corresponds to Lean's zero-indexed
`Nat.nth Nat.Prime 0`. A later statement must implement and check this index transport; it may not
quantify over Lean `m = 0` as though that were a source case.

The source is a strong `H1` lead, not `H0`: the repository does not cite it or select one of its
results, complete definition/assumption/proof-boundary and correction mapping has not been accepted,
the observed mutable copies were not preserved as an immutable repository source packet, and no
independent reviewer has approved the catalog-to-source identity.

## Candidate theorem crosswalk

| Source result | Exact source-level conclusion | Why the catalog could mean it | Intake boundary |
|---|---|---|---|
| Theorem 1.1, p. 384 | for `m` a positive integer, `liminf_n (p_(n+m)-p_n) << m^3 exp(4m)` | general improvement for arbitrarily many primes in bounded intervals | `m`, indexing, liminf, and the absolute implied constant must be encoded exactly |
| Theorem 1.2, p. 385 | a positive proportion (depending on `m`) of `m`-subsets of any sufficiently large finite set produce infinitely many simultaneous primes | another headline output of the new sieve method | finite-set, density, asymptotic, and infinitude conventions are absent from the catalog |
| Theorem 1.3, p. 385 | unconditionally `liminf_n (p_(n+1)-p_n) <= 600` | most direct numerical improvement over the Zhang/Polymath bounds discussed immediately before it | likely contextual lead, but no `600` or theorem number occurs in the catalog |
| Theorem 1.4, pp. 385-386 | under the paper's full level-of-distribution hypothesis, adjacent liminf is at most 12 and two-step liminf at most 600 | conditional improved upper bounds in the same paper | premise and two conclusions cannot be omitted or selectively made unconditional |
| Propositions 4.2-4.3, pp. 388-390 | a level-of-distribution and variational sieve criterion yields infinitely many prime-rich translates and explicit bounds for `M_5`, `M_105`, and large `k` | proof engine behind Theorems 1.1, 1.3, and 1.4 | method-level statement with substantially more definitions and hypotheses; not selected by the gloss |

## Component crosswalk

| Catalog component | Source component | Prospective Lean surface | Intake assessment |
|---|---|---|---|
| James Maynard / 2013 | arXiv v1 origin of *Small gaps between primes* | provenance metadata only | strong identity lead; final edition and corrections still matter |
| prime gaps | `p_(n+m)-p_n` for the increasing prime sequence | `Nat.nth Nat.Prime`, subtraction/cast choice, ordered indexing | exact `m` and codomain open |
| upper-bound improvement | Theorems 1.1, 1.3, 1.4 and their consequences | liminf or an equivalent infinitely-often predicate | result and equivalence not selected |
| unconditional improvement | Theorem 1.3's bound 600 and Theorem 1.1's general bound | exact constants and quantifiers | candidate only |
| conditional improvement | Theorem 1.4 under Elliott-Halberstam/level of distribution | explicit analytic premise plus paired conclusions | candidate only; cannot be weakened |
| `已验证` | untrusted inventory label | source review and kernel receipt would be required | no H or M credit |

## Revision and correction boundary

The headline Theorems 1.1-1.4 occur already in v1 and persist in the journal edition, but the proof
text was corrected. For example, v1's derivation of Theorem 1.3 says `M_105 > 2` even though its
stated Proposition 4.3 and the journal proof use the needed `M_105 > 4`; v2 also corrected a
counting denominator in the Theorem 1.2 proof. A future source packet must pin the admitted edition,
compare announced corrections and errata, and map every incorporated definition, premise,
transition, computation, and conclusion. The catalog year alone cannot choose an edition.

## Lean discovery boundary

Pinned mathlib provides `Nat.nth`, `Nat.prime_nth_prime`, `Nat.primeCounting`,
`Nat.tendsto_primeCounting`, the one-dimensional `BoundingSieve` and `SelbergSieve` interfaces,
`BoundingSieve.siftedSum_le_mainSum_errSum_of_upperMoebius`, and von Mangoldt definitions. These
are useful substrate or neighboring results. They neither define Maynard's multidimensional sieve
criterion nor state any of the candidate root conclusions.

A bounded search of repository-local Lean and pinned mathlib for Maynard, small/bounded prime gaps,
or a matching nth-prime liminf theorem found no exact target declaration. The only pinned mathlib
mention of Maynard concerns the unrelated Duffin-Schaeffer theorem and explicitly says that result
is not formalized there. This scoped search is not the downstream immutable anchor audit and is not
a claim that no external formalization exists.

## Source gate

Before leaving `H1`, accountable reviewers must preserve and hash an approved source edition,
select exactly one result and proof boundary, map its prime indexing, definitions, ordered binders,
hypotheses, constants, asymptotics, conclusion, and boundary cases, reconcile v1 with later
corrections, justify the boundary with Zhang and open prime-gap conjectures, and independently
approve fidelity to `THM-M-0491`. Only then may the statement phase freeze minimal imports, an
elaborated Lean expression and environment fingerprint, checked alternate encodings, and the four
required statement mutations.
