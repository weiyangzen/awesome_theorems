# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:6861-6866` supplies exactly:

| Catalog field | Verbatim value | Intake interpretation |
|---|---|---|
| title | `Kemperman定理` | named theorem family, but no theorem locator |
| attribution | `Johannes Kemperman` | matches the 1960 primary-paper author |
| time | `1960` | matches the primary-paper year |
| statement | `阿贝尔群上子集和的结构` | vague structural gloss, identical to the Kneser entry |
| importance | `高` | metadata only |
| formalization status | `已验证` | explicitly untrusted under rev-5.6 |

All six lines originate in repository commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. Their exact extract has SHA-256
`b5fe7a0d82ecd5c25b408c0e9edfa1156cd1c6bb5a3311a99d08c6b6a51a5324`. The record has no
citation, formula, definition chain, assumptions, conclusion, proof boundary, errata, or formal
declaration.

The stable-ID history has a material trap. Before Stage0 deduplication, this record was
`THM-M-0966`; commit `c61be3c80710c07c5f7626e3404e51f40ecb39a6` renumbered it to current
`THM-M-0939`. Provenance must bind the current ID to the title, attribution, year, and gloss rather
than relying on a pre-dedup ID alone.

`Docs/Stage0_Blueprint.md:25606-25631` repeats the fields and explicitly leaves the formal system,
foundation, definitions and premises, proof route, dependencies, alternate forms, axioms, machine
status, and artifact links open. Its current exact projection extract has SHA-256
`b356a5532860f107c8b08fae1a80ff931e81a8e1be4488f36591ac2c427e3387`.

## Primary bibliographic candidate

J. H. B. Kemperman, *On small sumsets in an abelian group*, *Acta Mathematica* 103 (1960),
pages 63-88, DOI `10.1007/BF02546525`, is the exact-author, exact-year, exact-topic primary
bibliographic candidate. Publisher and bibliographic metadata identify the paper, and both modern
sources below cite it as the original Kemperman structure theorem.

This intake does not claim a theorem-level inspection of a lawful complete primary edition. In
particular, it has not mapped the original paper's Theorem 5.1 and incorporated definitions against
every modern premise and conclusion, inspected a complete correction/errata history, or obtained
independent review. The primary lead therefore supports candidate identity, not `H0` or a canonical
statement.

## Inspected modern complete-proof candidate

Tomas Boothby, Matt DeVos, and Amanda Montejano, *A New Proof of Kemperman's Theorem*,
arXiv:`1301.0095v2` [math.CO], 16 March 2013, was inspected in its 20-page v2 form. The observed
PDF has SHA-256 `641f3122cdce22d2358ed8f079c9e1d909f92d2ab53e62c64971f256663f38e8`.

The paper defines sumsets and stabilizers; pair deficiency and criticality; trivial, pure, and
superpairs; finite/cofinite trios and trio deficiency; maximality and similarity; pure and impure
beats and chords; and continuations. Theorem 4.5 then states that every maximal nontrivial critical
trio in `G_1` has a finite chain `Upsilon_1,...,Upsilon_m` in strictly descending subgroups
`G_1 > ... > G_m`, with every nonterminal member an impure beat or chord continuing to the next,
and the terminal member a pure beat or chord. Sections 5-8 supply its proof. The introduction
expressly says that this trio formulation differs from earlier pair statements and adopts Lev's
top-down perspective.

This is a precise recursive root candidate with a complete proof, not the admitted canonical root.
Its pair/trio equivalence, finiteness/cofiniteness conventions, full definition dependencies,
original-source correspondence, and any version/correction questions remain to be audited and
independently reviewed.

## Inspected modern pair variant

Vsevolod F. Lev, *Critical pairs in abelian groups and Kemperman's structure theorem*,
arXiv:`math/0508179v2` [math.NT], 3 February 2006, later *International Journal of Number Theory*
2(3) (2006), 379-396, was inspected in v2. The observed text extract has SHA-256
`b752fd7dec9a3ab78d96570e719cd678d509831ea790338b50863261852167fd`.

Lev's Theorem C explicitly cites Kemperman [K60, Theorem 5.1]. It takes finite nonempty subsets
`A,B` of a nontrivial abelian group. It characterizes simultaneous satisfaction of
`|A+B| <= |A|+|B|-1` and the condition "the period of `A+B` is zero or `mu(A,B)=1`" by the
existence of nonempty residual subsets `A_0,B_0` and a nonzero subgroup `H`: the residual pair is
elementary within `H`-cosets; the remainders are unions of `H`-cosets; the quotient images have
sumset size `|Abar|+|Bbar|-1`; and the distinguished quotient sum has a unique representation.
Lev separately defines four elementary-pair types and the representation count `mu`.

This formulation is especially close to the cited original theorem, but it is not interchangeable
with Theorem 4.5 without a reviewed equivalence map. Its use of the small-sumset inequality plus
Kemperman's additional condition must also not be weakened to the inequality alone.

## Phrase-to-proposition crosswalk

| Repository phrase | Source component | Prospective Lean component | Intake result |
|---|---|---|---|
| abelian group | arbitrary additive abelian `G` in both modern candidates | `AddCommGroup G`, plus explicit finiteness on sets/subgroups where required | candidate domain identified; exact root open |
| subset sum | `A+B = {a+b}` and representation counts | pointwise `Set`/`Finset` addition with checked coercion/cardinality bridges | representation decision open |
| structure | residual elementary pair plus quotient recursion, or beat/chord continuation chain | an inductive classification predicate with checked pair/trio equivalence | candidate structures identified; none frozen |
| Kemperman theorem | original K60 Theorem 5.1 as presented by Lev; modern recursive Theorem 4.5 | one exact proposition or reviewed equivalent package | root selection pending |
| 1960 | primary-paper publication year | immutable source metadata | identity match only |
| verified | catalog status | no proposition or proof term | rejected as H/M evidence |

## Neighbor theorem crosswalk

| Theorem | What it supplies | Why it is not the target |
|---|---|---|
| Cauchy-Davenport | lower bound `min(p, |A|+|B|-1)` in a prime cyclic group | direct bound in a special ambient group, no general structural classification |
| Vosper | classifies prime-cyclic critical pairs by exceptional/full cases and common-difference progressions | special case of the arbitrary-abelian classification |
| Kneser | stabilizer/period-sensitive cardinality formula or inequality for finite sumsets | reduction and numerical structure, not the complete critical-pair recursion |
| Kemperman-Scherk | lower bound using minimum representation multiplicity `mu(A,B)` | distinct theorem despite overlapping attribution and notation |

## Pinned Lean boundary

The intake probe authenticates pinned `cauchy_davenport_minOrder_add`,
`ZMod.cauchy_davenport`, and additive-action stabilizer declarations. These are adjacent expression
tools only. The bounded intake inspection found no named Kemperman structure theorem, critical-
pair/trio API, elementary-pair classification, beat/chord continuation system, or pair/trio bridge
in repo-local Lean or pinned mathlib. This is discovery-only evidence, not the later precommitted
anchor audit and not a universal absence claim.

No canonical Lean statement, formal module, expression hash, environment fingerprint, or proof
body is credited. The provisional root remains `[H1, M4, R4]`.

## Source gate

Before statement acceptance, accountable reviewers must preserve one lawful immutable primary
edition; locate the exact original theorem and incorporated definitions; inspect corrections and
errata; select the original pair form, Lev variant, Boothby-DeVos-Montejano trio form, or an
explicit equivalent package; map every binder, definition, hypothesis, conclusion, boundary case,
and proof dependency; prove or source-approve every pair/trio and normalization transport; and
independently approve the crosswalk. Until then the canonical mathematical and Lean statements
remain null, and no proof or completion claim follows from the inspected sources.
