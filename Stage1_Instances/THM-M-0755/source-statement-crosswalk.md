# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md:5563-5568` is the complete source-corpus record. It gives the
Chinese title `解析层次`, Stephen Kleene, 1955, the gloss `解析集合的层次`, importance `高`, and
formalization label `已验证`. It was introduced in repository commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. That commit is repository provenance, not an edition
of a mathematical source.

`Docs/Stage0_Blueprint.md:20623-20648` repeats the record while explicitly leaving definitions and
premises, proof route, dependency graph, equivalent formulations, axioms, machine status, and
artifact links open. The rev-5.6 manifest deliberately preserves `已验证` only as
`source_status_untrusted`. Nothing in these records identifies a truth-valued proposition, a
primary theorem/page, or a Lean declaration.

## Source leads, not accepted H evidence

The Spring 2024 archived edition of Walter Dean and Alberto Naibo, *Recursive Functions*, Stanford
Encyclopedia of Philosophy, section 3.6.2, is an authoritative secondary orientation source. It
defines the lightface analytical hierarchy in second-order arithmetic and states Theorem 3.13,
attributed to Kleene 1955a: for every `n >= 1`, a `Pi^1_n`-definable subset of natural numbers
exists that is not `Sigma^1_n`-definable and belongs to neither class at any lower level; its
complement gives the dual witness. This makes hierarchy strictness a well-motivated statement
candidate, but a secondary source cannot choose the repository's missing root or establish H0.

The same source identifies these primary leads:

- S. C. Kleene, "Arithmetical Predicates and Function Quantifiers", *Transactions of the American
  Mathematical Society* 79(2) (1955), 312-340,
  DOI `10.1090/S0002-9947-1955-0070594-4`;
- S. C. Kleene, "Hierarchies of Number-Theoretic Predicates", *Bulletin of the American
  Mathematical Society* 61(3) (1955), Crossref pages 193-213,
  DOI `10.1090/S0002-9904-1955-09896-3`.
- S. C. Kleene, "On the Forms of the Predicates in the Theory of Constructive Ordinals (Second
  Paper)", *American Journal of Mathematics* 77(3) (1955), 405-428,
  DOI `10.2307/2372632`.

Crossref metadata confirms the first two bibliographic records. The primary texts were not preserved and
audited in this intake: AMS retrieval returned HTTP 403, and no theorem/page/assumption/proof/
errata crosswalk or independent review was completed. The SEP bibliography gives pages 193-214 for
the survey, disagreeing with Crossref's 193-213; even the pagination needs source-audit
reconciliation. The leads therefore remain E5 discovery metadata here, not E4/H0 evidence.

## Crosswalk

| Repository phrase | Possible mathematical component | Prospective Lean surface | Intake status |
|---|---|---|---|
| `解析集合` / analytical sets | relations definable in the standard model of second-order arithmetic | coded two-sorted/function-quantifier syntax, semantics, and extensional set predicates | leading lightface reading; absent from repository source and pinned API |
| `层次` / hierarchy | alternating `Sigma^1_n`, `Pi^1_n`, and intersection `Delta^1_n` classes | indexed formula/definability predicates with checked base and successor clauses | no such hierarchy located in pinned mathlib |
| hierarchy theorem | strictness and separating witnesses at every positive level | quantified existence/nondefinability theorem plus complement/lower-level transports | secondary Theorem 3.13 candidate only |
| normal form | alternating set/function quantifiers over an arithmetical matrix | syntax normalization and satisfaction preservation | different candidate conclusion |
| analytical set, boldface reading | continuous image of a Polish space | `MeasureTheory.AnalyticSet` | pinned API exists but is not a source match by itself |
| effective tree coding | computable trees and well-foundedness at the first projective level | `Descriptive.tree` plus missing effective/well-foundedness/reduction infrastructure | generic tree carrier only |
| Stephen Kleene / 1955 | historical locator | immutable primary edition, theorem/page, assumptions, proof nodes, and errata | bibliographic leads found; pinpoint audit open |
| `已验证` | untrusted inventory label | no Lean proposition or proof object | explicitly rejected as evidence |

## Lean and status boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the intake probe checks
`PrimrecPred`, `ComputablePred`, `REPred`, generic first-order prenex-form interfaces, powersets of
natural numbers, generic descriptive trees, and the boldface `MeasureTheory.AnalyticSet` predicate.
A bounded search of the pinned
`Mathlib/Computability`, `Mathlib/Logic`, `Mathlib/ModelTheory`, `Mathlib/SetTheory/Descriptive`, and
relevant measure-theory sources found no obvious analytical/projective hierarchy, lightface,
second-order-arithmetic hierarchy, or `Sigma^1_n`/`Pi^1_n` framework. This is a reproducible local
observation, not the later immutable anchor audit and not proof that no external formalization
exists.

The first downstream blocker is source selection: an independent reviewer must inspect an
immutable primary text, select and justify the exact proposition represented by this catalog entry,
and record edition, theorem/page, definitions, assumptions, conclusion, proof boundary, and errata.
Only then may the statement phase freeze binders, domains, encodings, foundation profile, minimal
imports, an elaborated expression hash, alternate transports, and mutation tests. Until then the
catalog target is provisionally `[H5, M4, R4]`; no H0, formal statement, or proof credit is claimed.
