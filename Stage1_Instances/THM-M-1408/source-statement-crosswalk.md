# Source-statement crosswalk

## Repository authority

`Docs/researches/math_theorems.md` records `Ornstein同构定理`, Donald Ornstein, 1970, and only
`Bernoulli系统的分类` ("classification of Bernoulli systems"). `Docs/Stage0_Blueprint.md` repeats
that slogan and explicitly leaves exact definitions and premises, proof path, equivalent forms,
axioms, machine status, and artifact links open. The rev-5.6 manifest retains `已验证` solely as
`source_status_untrusted`.

A physics-corpus record says `相同熵的伯努利系统同构` ("Bernoulli systems with the same entropy are
isomorphic"), but that record belongs to the separate Stage0 target `THM-P-0889`. It corroborates a
likely historical reading; it is not the statement authority for `THM-M-1408`.

## Primary-source candidate

Crossref bibliographic metadata identify Donald Ornstein, *Bernoulli shifts with the same entropy
are isomorphic*, **Advances in Mathematics** 4(3) (1970), 337-352, DOI
`10.1016/0001-8708(70)90029-0`. The title is a strong discovery anchor for the intended theorem
family. It is not an `H0` packet: no immutable article text has been preserved here, no exact
definition/theorem/page passage has been transcribed, the ordered assumptions and proof boundary
have not been checked, errata have not been audited, and no independent source reviewer has
approved the mapping. The broad page range is bibliographic metadata, not a pinpoint theorem
locator.

The existence of a separate 1970 paper concerning infinite-entropy Bernoulli shifts further makes
the entropy domain a material source decision. The statement phase must inspect the chosen source,
not infer an unrestricted theorem from the first paper's title.

## Crosswalk

| Source phrase | Mathematical component to freeze | Required Lean component | Intake status |
|---|---|---|---|
| Bernoulli system/shift | alphabet or base probability space, product path space, product measure, and shift | `Measure.infinitePi`, measurable coordinate shift, and proof that it preserves the product measure | nearby substrate probed; exact model open |
| "same entropy" | exact Shannon or Kolmogorov-Sinai entropy, codomain, logarithm convention, and finiteness | finite/countable entropy sum plus a checked bridge to dynamical entropy | absent as a target interface; `Real.negMulLog` is scalar substrate only |
| "isomorphic" | measurable equivalence modulo null sets, measure preservation, inverse laws, and shift intertwining | a source-faithful a.e. dynamical-isomorphism structure or quotient representation | `MeasurableEquiv` and `MeasurePreserving` exist; exact a.e. interface open |
| classification | equal entropy implies isomorphism, or iff after a separate converse | ordered binders and exact implication/iff proposition | direction not supplied by repository slogan |
| Bernoulli systems | finite/countable alphabets, one/two-sided shifts, standardness and support hypotheses | exact types, universes, instances, and boundary predicates | unresolved |
| `已验证` | untrusted inventory metadata | no Lean declaration or proof component | explicitly rejected as evidence |

## Lean boundary

The pinned environment is Lean 4.29.0 at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740` with mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. The bounded intake probe checks infinite product
measure, coordinate measure preservation, measurable equivalences and their inverse preservation,
and scalar entropy primitives. A scoped name search found no Ornstein theorem, Bernoulli-shift
declaration, or measure-theoretic/Kolmogorov-Sinai entropy interface in pinned mathlib. The latter
negative result is bounded intake evidence, not an exhaustive external anchor audit.

Before `H0`, a source reviewer must approve an immutable edition, pinpoint definitions and theorem
passage, every premise/transition/conclusion mapping, corrections and errata. Before statement
credit, a formal reviewer must approve the exact elaborated Lean target and checked transports for
every credited alternate encoding. Until both happen, the root remains `H1/M4` and no proof claim is
legal.

