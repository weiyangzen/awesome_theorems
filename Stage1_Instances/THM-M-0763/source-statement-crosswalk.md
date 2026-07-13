# Source-statement crosswalk

## Repository record and provenance

`Docs/researches/math_theorems.md:5619-5624` supplies exactly the title `乔姆斯基层次`, attribution
Noam Chomsky, year 1956, gloss `形式语言的分类`, importance `高`, and status `已验证`. All six
uncited lines originate at repository commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record contains no work, edition, theorem/page,
formula, definitions, ordered binders, assumptions, conclusion, proof boundary, correction,
erratum, reviewer, or formal artifact.

`Docs/Stage0_Blueprint.md:20839-20864` projects that record as `THM-M-0763` while explicitly leaving
the formal system, precise definitions and premises, proof route, dependencies, equivalent forms,
axioms, machine status, and artifact links open. Its generic claim that a closed result is known is
not source evidence. Rev-5.6 therefore retains `已验证` only as untrusted metadata and resets the
target to `L0 / rework_required`.

The independent computer-science inventory row at `Docs/researches/cs_theorems.md:260` calls the
topic `Chomsky层级` and says `形式语言的四层层级`; Stage0 projects it as `THM-C-0151`. That record is
outside rev-5.6 and has no accepted duplicate-identity decision. It confirms that a four-level
reading is plausible, but cannot supply this target's source statement or evidence.

## Literal crosswalk

| Repository component | Mathematical detail required | Prospective Lean surface | Intake assessment |
|---|---|---|---|
| formal languages | alphabet, finiteness, words, empty word, and language equality | `Language T = Set (List T)` or a checked alternate | adjacent API exists; exact domain absent |
| classification | exact truth-valued conclusion and its quantifier order | one binder-complete `Prop` | absent |
| hierarchy | grammar classes, inclusion directions, strictness, and witnesses | predicates for every class plus implications/nonimplications | no variant selected |
| grammar types | exact type-0/1/2/3 production restrictions and derivation semantics | source-faithful grammar structures and generated languages | only context-free substrate exists locally |
| machine characterizations | exact automata, acceptance, effectiveness, and transports | DFA/PDA/LBA/TM definitions and checked equivalences | optional candidate, not catalog content |
| Noam Chomsky, 1956 | exact work, statement genealogy, terminology, assumptions, and corrections | source provenance only | historical lead, not H0 |
| `已验证` | claimed proof/formal status | accepted source or kernel evidence would be required | explicitly rejected |

## Inspected 1956 primary-source lead

Noam Chomsky, "Three Models for the Description of Language," *IRE Transactions on Information
Theory* 2(3) (September 1956), 113-124, DOI `10.1109/TIT.1956.1056813`, was inspected from an
author-hosted scan. Crossref confirms the bibliographic fields. In the journal pagination, page 114
defines languages and finite-state languages; pages 116-117 define phrase-structure grammars,
derivations, derivable languages, and terminal strings; page 118 gives Theorem (27), whose proof
continues on page 119:

1. Every finite-state language is terminal, but not conversely.
2. Every derivable language is terminal, but not conversely.
3. There are derivable nonfinite-state languages and finite-state nonderivable languages.

This is a concrete classification result and a strong historical source lead. It is not the modern
four-type hierarchy: it compares three differently named classes and includes incomparability
between finite-state and derivable languages. The catalog does not say whether this historical
theorem or a later four-level formulation is intended. The scan was inspected only for intake
disambiguation; its temporary copy is not a repository artifact, no corrections or translation
were audited, and no independent reviewer accepted a source-to-target mapping. It supplies no H0
or canonical-statement credit.

Noam Chomsky, "On Certain Formal Properties of Grammars," *Information and Control* 2(2) (June
1959), 137-167, DOI `10.1016/S0019-9958(59)90362-6`, is a likely modern hierarchy source lead.
Crossref confirms those bibliographic fields, but no immutable full statement/proof text, pinpoint
theorem, incorporated definitions, correction record, or independent mapping was obtained. It is
therefore bibliographic discovery only.

## Pinned Lean discovery boundary

At mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the narrow intake probe checks
`Language`, `Language.IsRegular`, `ContextFreeRule`, `ContextFreeGrammar`,
`ContextFreeGrammar.language`, `ContextFreeGrammar.mem_language_iff`,
`Language.IsContextFree`, `ComputablePred`, and `REPred`. These provide
formal-language, regular-language, context-free, decidability, and recursive-enumerability
substrate only. They do not define or prove an identified Chomsky-hierarchy root.

A bounded exact-topic search over repo-local Lean and pinned mathlib found no `Chomsky` occurrence,
context-sensitive or unrestricted grammar hierarchy, or type-0/type-1 classification declaration.
This observation is intake discovery only, not an exhaustive downstream anchor audit or a global
absence proof. In particular, `Language.IsRegular` and `Language.IsContextFree` being available does
not itself prove their inclusion or strictness.

## First downstream blocker

The first downstream blocker is exact source-statement identity. Accountable reviewers must select
or correct one truth-valued proposition; preserve a lawful immutable source edition; identify exact
definition/theorem/page locators; map every incorporated definition, binder, hypothesis, conclusion,
proof boundary, correction, and boundary case; reconcile `THM-C-0151`; and independently approve
the source choice. Only then may the statement phase elaborate an exact Lean expression, minimize
imports, serialize its fingerprints, check alternate encodings, and mutation-test hypotheses,
domains, binder scope, and boundary cases.
