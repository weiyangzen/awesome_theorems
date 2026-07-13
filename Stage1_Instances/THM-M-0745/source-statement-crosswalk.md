# Source-statement crosswalk

## Repository source record

The only claim-bearing repository record is `Docs/researches/math_theorems.md:5493-5498`, introduced
in commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`:

| Catalog field | Received value | Statement consequence |
|---|---|---|
| title | `递归枚举集` | Names recursively enumerable sets, not a theorem about them. |
| attribution | many mathematicians | Does not identify a source, definition, or proof. |
| time | twentieth century | Does not select a work or edition. |
| statement | `递归可枚举集的性质` | Supplies no property, binders, assumptions, or conclusion. |
| importance | high | Scheduling metadata only. |
| formalization status | `已验证` | Explicitly untrusted; supplies no human or machine proof credit. |

The generated Stage0 projection at `Docs/Stage0_Blueprint.md:20353-20378` repeats the gloss while
marking the formal system, exact definitions and premises, proof route, dependencies, alternate
forms, axioms, machine state, and artifact links as pending. It does not enrich the statement.

The catalog is a secondary compilation and gives no bibliography for this entry. No primary source
edition, theorem/page locator, incorporated definition, proof boundary, correction or errata check,
translation, or independent reviewer has been supplied or accepted. The received record is E5
intake provenance, not H0 or H1 evidence for an exact proposition.

## Phrase-to-statement map

| Received or candidate component | Required source decision | Prospective Lean surface | Intake result |
|---|---|---|---|
| recursively enumerable | domain, range, semidecision, recognizer, or another equivalent definition | `REPred`, `Partrec`, or a future checked encoding | unresolved; no definition selected |
| set | `Set Nat`, `Nat -> Prop`, positive integers, program codes, or another carrier | predicate/set representation plus encoding instances | unresolved |
| properties | one exact implication, equivalence, closure, example, or classification result | no canonical expression | no result selected |
| partial-function domain | exact partial-recursive model and equality convention | `REPred`, `Partrec.dom_re` | pinned definition/characterization candidate only |
| decidable implies r.e. | decidability and coding hypotheses | `ComputablePred.to_re` | candidate consequence only |
| r.e. and co-r.e. iff decidable | complement and `DecidablePred` conventions | `ComputablePred.computable_iff_re_compl_re` | distinct Post-style characterization only |
| halting set is r.e. | evaluator, code type, and input parameter | `ComputablePred.halting_problem_re` | example owned near `THM-M-0741`, not this root |
| `已验证` | evidence and exact checked declaration | no proof object | no H or M credit |

There are consequently no ordered binders, hypotheses, exact conclusion, credited alternate
encoding, statement fingerprint, canonical obligation, or proof body.

## Bibliographic and formal leads

Pinned mathlib's bibliography contains Robert I. Soare, *Recursively enumerable sets and degrees*,
Springer-Verlag, 1987, ISBN `3-540-15299-7`, DOI `10.1007/978-3-662-02460-7`. The broad reference is
cited by `Mathlib.Computability.Reduce`, but no theorem or page is tied to this catalog item. It is
a topic-level bibliographic lead only, not a pinpoint primary proof source or H0/H1 crosswalk.

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, a bounded inspection of
`Mathlib.Computability.Halting` found `REPred`, `REPred.of_eq`, `Partrec.dom_re`,
`ComputablePred.to_re`, `ComputablePred.computable_iff_re_compl_re`,
`ComputablePred.halting_problem_re`, and `ComputablePred.halting_problem_not_re`. The declarations
cover definitions, transports, a decidability characterization, and examples with materially
different statements. Their diversity confirms rather than resolves the catalog ambiguity.

This bounded intake inspection is not the dependency-ordered anchor audit and makes no exhaustive
absence claim. The probe authenticates names and types only; no candidate is source-mapped or
credited to the target.

## Human-source gate

To leave `H5`, an accountable reviewer must approve a stable truth-valued target and an immutable
primary or authoritative source. The crosswalk must then bind its exact theorem and incorporated
definitions, every assumption and conclusion, proof and dependency boundaries, corrections and
errata, translation, and each source component to the mathematical and Lean encodings. Until that
happens, ordinary statement and theorem-proof execution remains blocked.
