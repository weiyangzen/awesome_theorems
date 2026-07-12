# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md` gives the title, Richard Karp, 1972, and only the gloss
`经典的NP完全问题` ("classic NP-complete problems"). `Docs/Stage0_Blueprint.md` repeats that
metadata and leaves exact definitions, assumptions, proof path, axioms, and machine artifact open.
The manifest deliberately carries `已验证` only as `source_status_untrusted`; it has no proof or
statement authority.

## Primary source anchor

Richard M. Karp, "Reducibility among Combinatorial Problems", in Raymond E. Miller and James W.
Thatcher (eds.), *Complexity of Computer Computations*, Plenum Press, 1972, pp. 85-103,
DOI `10.1007/978-1-4684-2001-2_9`.

The chapter defines a language-recognition problem, polynomial algorithms, the class `P`, a class
`NP`, polynomial reducibility, and `(polynomial) complete` languages. Its central displayed theorem
states: "All the problems on the following list are complete." The ensuing sections define the
listed problems and give a reduction scheme and individual reductions. This identifies the intended
collective claim and rules out reading the repository title as a single-problem theorem.

This is an `H1` locator, not `H0`: the exact list, every source definition and side condition, the
page-level proof crosswalk, and errata have not yet been independently reviewed. Crossref confirms
the bibliographic pages and DOI. A publicly hosted scan was inspected for intake discovery but is
not vendored or treated as an immutable accepted evidence object.

## Crosswalk

| Source/repository component | Mathematical role | Required Lean component | Intake status |
|---|---|---|---|
| "problems on the following list" | exact finite theorem inventory | fixed index type/list plus bijection to 21 source entries | included; transcription/review open |
| language-recognition problem | decision predicate over finite encodings | `Language` or a checked equivalent predicate encoding | nearby API probed; exact encoding open |
| `P` and `NP` | deterministic/nondeterministic polynomial resource bounds | machine model, acceptance semantics, input length, polynomial bound | absent from pinned mathlib search; formal interface open |
| polynomial reducibility | polynomial-time instance translation preserving answers | reduction function, correctness iff, totality, and time/size bound | `ManyOneReducible` is computable-only and insufficient |
| complete | source completeness predicate and class membership | explicit completeness structure/proposition | formal definition open |
| reduction scheme | shared proof architecture | typed reduction graph and composition certificates | obligation-tree work, not intake credit |
| individual problem definitions | Boolean, graph, set, arithmetic, routing, packing, covering, assignment, sequencing predicates | concrete finite datatypes and predicates | exact 21-way mapping open |

## Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the bounded
`IntakeProbe.lean` imports the formal-language and computable-reduction modules and representative
finite-graph APIs. These provide useful encoding ingredients. In particular, mathlib's
`ManyOneReducible` requires a computable translator, not a polynomial-time one, so it cannot be the
canonical reduction relation without an additional checked resource bound. No repo-local theorem
for the collective Karp result was found by the bounded name search; that observation is only an
intake boundary and does not replace the later immutable anchor audit.

Before H0, an independent reviewer must verify the stable edition, displayed theorem, exact list and
counting convention, every problem definition and assumption, reduction premises, proof pages, and
known errata, and approve a row-by-row source-to-Lean map.

