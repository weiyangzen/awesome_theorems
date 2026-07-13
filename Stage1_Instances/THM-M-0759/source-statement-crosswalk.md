# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:5591-5596` supplies exactly the title `自动机理论`,
collective attribution, the twentieth century, the gloss `有限自动机的理论`, high importance,
and status `已验证`. Git blame attributes all six uncited lines to repository commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record contains no formula, source, definition,
binder, premise, conclusion, proof boundary, correction history, or formal artifact.

`Docs/Stage0_Blueprint.md:20731-20756` repeats the gloss and explicitly leaves the formal system,
foundation, exact definitions and premises, proof route, dependencies, equivalent statements,
axioms, machine status, and artifact links open. Its generated planning language is not source
evidence. The rev-5.6 manifest retains `已验证` only as `source_status_untrusted` and resets the
target to `L0 / rework_required`.

## Survey and bibliography boundary

The separate repository survey `Docs/researches/cs_theorems.md:224-239` lists Kleene equivalence,
NFA/DFA equivalence, the regular-language pumping lemma, Myhill-Nerode, DFA minimization,
regular-language closure and decision properties, and further results as separate rows. This is
positive evidence that "finite automata theory" does not identify one of them, or their
conjunction, as this target's root.

That survey's bibliography names Sipser's *Introduction to the Theory of Computation* (2012) and
Hopcroft, Motwani, and Ullman's *Introduction to Automata Theory, Languages, and Computation*
(2006), but it does not connect either book, edition, theorem, or page to `THM-M-0759`. They are
general bibliographic leads only. No immutable primary or authoritative source statement, proof
boundary, errata disposition, or independent source review was accepted at intake.

## Component crosswalk

| Repository element | Mathematical decision required | Prospective Lean component | Intake assessment |
|---|---|---|---|
| `自动机理论` | select one theorem rather than a field | one exact canonical `Prop` | topic label only; root open |
| `有限` | specify which carriers must be finite | `Fintype` or an explicit finite-set condition | not stated |
| `自动机` | select DFA, NFA, epsilon-NFA, or another model | exact structure and transition semantics | model open |
| words and languages | fix alphabet, word representation, membership, and language equality | commonly `List alpha` and `Language alpha` | absent from the catalog |
| `理论` | identify a conclusion such as equivalence, characterization, closure, pumping, minimization, or decidability | an exact proposition and checked constructions | no conclusion supplied |
| collective attribution / twentieth century | identify a source and theorem history | immutable source identity and pinpoint locators | not actionable attribution |
| `已验证` | untrusted inventory label | no proof object | explicitly rejected as evidence |

## Candidate readings and conflicts

A correctness theorem for a single machine, DFA/NFA language equivalence, Kleene equivalence,
Myhill-Nerode, a pumping lemma, closure of regular languages, minimal-automaton uniqueness, and a
decision-procedure theorem have different binders, hypotheses, conclusions, constructions, and
proofs. Some are separately owned by neighboring Stage1 targets. Choosing one because pinned
mathlib happens to expose it would be a broadened or substituted theorem, not a source crosswalk.

## Lean intake boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the discovery-only
probe checks one candidate family: finite-word `Language`, `DFA`, `NFA`, `epsilon-NFA`, acceptance and evaluation, regularity and
closure, DFA/NFA and epsilon-NFA/NFA translations, pumping, regular-expression semantics, and the
left-quotient Myhill-Nerode characterization. These are multiple adjacent results, not a unique
source-mapped root. In particular, the DFA/NFA/epsilon-NFA structures permit infinite state types,
while their documentation requires `Fintype` for true finite automata. The regular-expression
module explicitly leaves its equivalence with DFA/NFA as future work.

No canonical target, expression fingerprint, proof body, trust closure, or machine-proof credit
follows from the API checks. The bounded repo-local and pinned search is discovery evidence only;
the dependency-ordered anchor audit remains open.

## Required target decision and source correction

The worker proposes redirecting this H5 subject label to one independently approved exact
finite-automata theorem, or having the master split or reject it if no faithful single root exists.
Ordinary proof execution is blocked until the integration lane accepts that target decision.

Before statement work, an accountable reviewer must approve one exact theorem and immutable
edition, pinpoint the statement, incorporated definitions, assumptions, proof boundary, and
corrections, reconcile it with the umbrella catalog wording and neighboring targets, and obtain an
independent crosswalk review. The correction must freeze the model, finiteness conventions,
alphabet, state space, words, transition and acceptance semantics, ordered binders, every
hypothesis, exact conclusion, and boundary cases. Until then the catalog wording is provisionally
`H5`, while machine and readability states remain `M4` and `R4`.
