# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:163-168` gives the Chinese title
`哈塞-闵可夫斯基定理`, attributes it to Helmut Hasse and Hermann Minkowski, dates it 1924, and
states only `二次型的局部-整体原理` ("local-global principle for quadratic forms"). The same
six-line record is duplicated at lines 3089-3094. Git history places both uncited records in commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`.

`Docs/Stage0_Blueprint.md:663-687` repeats the gloss and explicitly leaves exact definitions and
premises, proof route, dependencies, equivalent formulations, axiom policy, and machine artifact
open. The rev-5.6 manifest retains `已验证` only as untrusted source metadata and resets the item
to `L0 / rework_required`.

The catalog contains no bibliography, theorem/page locator, base field, dimension or regularity
condition, place convention, local-solubility definition, ordered binders, conclusion direction,
proof boundary, errata record, or reviewer. Its wording therefore identifies a theorem family but
does not itself freeze a stable proposition.

## Primary-source leads

Crossref metadata confirms Helmut Hasse, *Darstellbarkeit von Zahlen durch quadratische Formen in
einem beliebigen algebraischen Zahlkoerper*, *Journal fuer die reine und angewandte Mathematik*,
issue 153 (1924), pages 113-130, DOI `10.1515/crll.1924.153.113`. The publisher's full text was not
accessible to this worker, and no primary text was admitted or inspected. The article is a strong
historical number-field lead, not an accepted statement crosswalk.

Crossref also confirms H. Minkowski, *Ueber die Bedingungen, unter welchen zwei quadratische
Formen mit rationalen Coefficienten in einander rational transformirt werden koennen*, the same
journal, issue 106 (1890), pages 5-26, DOI `10.1515/crll.1890.106.5`. Its title indicates a
rational-equivalence formulation, not automatically the exact number-field isotropy proposition.
It is a historical precursor lead only.

Neither record supplies an immutable primary edition in this dossier, a pinpoint theorem within
the cited pages, a full definition/assumption/conclusion map, translation provenance, errata audit,
or independent source review. No `H0` claim follows from the bibliographic match.

## Component crosswalk

| Catalog component | Material interpretations | Prospective Lean surface | Intake assessment |
|---|---|---|---|
| quadratic forms | coordinate polynomial, `QuadraticForm`, or regular quadratic space | carrier, scalar field, module, dimension, `QuadraticForm` | representation and regularity open |
| local | finite places only or all finite and infinite completions | `NumberField.FinitePlace`, `NumberField.InfinitePlace`, scalar completion | place family absent |
| global | rational field, arbitrary number field, or global field | `[Field K] [NumberField K]` or another selected structure | domain absent |
| principle | isotropy, scalar representation, form equivalence, or classification | nonzero-zero predicate, representation predicate, `Equivalent`, invariants | conclusion family ambiguous |
| local-to-global | hard implication or one side of an equivalence | implication from all local predicates to global predicate | direction absent |
| global-to-local | functorial scalar extension | base-change transport of a nonzero zero | likely easy direction, not catalog-explicit |
| nontrivial zero | zero vector excluded; degeneracy convention separate | `exists x, x != 0 and Q x = 0` | witness rule absent |
| `verified` | untrusted inventory label | no declaration or proof body | explicitly rejected as evidence |

## Lean and duplicate-scope boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the bounded exact-topic
search found quadratic-form and number-field completion substrate but no declaration named for the
Hasse-Minkowski theorem. `IntakeProbe.lean` checks only that selected substrate interfaces
elaborate.

Repo-local `Stage1_Instances/THM-M-0423/Statement.lean` and
`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_067.lean` contain a candidate coordinate-free
isotropy statement and supporting definitions. Both explicitly withhold the hard theorem proof.
They belong to `THM-M-0423`, are legacy/discovery inputs for this target, and confer neither exact
statement identity nor proof credit. Their overlap with `THM-M-0020` requires a later reviewed
duplicate/scope decision.

## Required source admission

The statement phase must preserve one lawful complete source edition, select its exact result and
proof boundary, transcribe all incorporated definitions, ordered binders, hypotheses, conclusion,
and boundary cases, reconcile the Hasse and Minkowski formulations, audit translations and errata,
and obtain independent review. Only then may the same claim be frozen, elaborated, fingerprinted,
transported, and mutation-tested in Lean.
