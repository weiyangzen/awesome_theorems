# Source-statement crosswalk

## Repository record and provenance

`Docs/researches/math_theorems.md:2202-2207` supplies exactly the title `迹定理`, attribution
Sergei Sobolev, year 1936, gloss `Sobolev函数在边界上的限制`, importance `高`, and status
`已验证`. All six uncited lines originate at repository commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record contains no work, edition, theorem/page,
formula, definitions, assumptions, proof boundary, correction, erratum, or formal artifact.

`Docs/Stage0_Blueprint.md:8467-8492` projects the record as `THM-M-0307` while explicitly leaving
the formal system, exact definitions and premises, proof route, dependencies, equivalent forms,
axioms, machine status, and artifact links open. Its generated claim that a closed result is known
is not source evidence. Rev-5.6 therefore retains `已验证` only as untrusted metadata and resets the
target to `L0 / rework_required`.

The source corpus repeats the six-line block byte-for-byte at lines 9052-9057 in its PDE section.
Because the complete metadata signature is identical, the Stage0 generator retains only the first
record as `THM-M-0307`. This explains provenance duplication but supplies no second statement,
review, proof, or evidence packet.

## Literal crosswalk

| Repository component | Mathematical source detail required | Prospective Lean surface | Intake assessment |
|---|---|---|---|
| trace theorem | one exact theorem rather than a family name | a source-faithful `Prop` with ordered binders | root unidentified |
| Sobolev function | exact domain, order, exponent, weak-derivative model, values, and a.e. quotient | a concrete Sobolev construction and representative relation | absent |
| boundary | exact boundary notion, regularity, sigma algebra, and surface measure | a domain/boundary object and measure | absent |
| restriction | dense classical restriction, continuous extension, uniqueness, and agreement clause | an explicit trace map and checked dense-class bridge | absent |
| target and estimate | boundary space, smoothness loss, norm, constant dependencies, parameter range | a continuous linear map and exact bound, if source-selected | absent |
| extra strength | surjectivity, right inverse, kernel/zero-trace equality, or none | separately modeled conclusions and dependencies | absent |
| Sergei Sobolev, 1936 | pinpoint work, statement genealogy, translation, and corrections | source provenance only | catalog lead, not H0 |
| `已验证` | claimed formal status | kernel declaration plus accepted evidence would be required | explicitly rejected |

## Human-source status

No theorem-level primary or authoritative statement source is cited or accepted. The date and
attribution are bibliographic discovery leads only. This intake does not invent a 1936 title,
theorem number, page, translation, or modern formula and does not assign source credit based on
memory. The current `H5` classification applies to the underspecified catalog phrase, not to any
corrected source-selected trace theorem.

A modern exact-topic bibliographic lead is Zhonghai Ding, "A proof of the trace theorem of Sobolev
spaces on Lipschitz domains," *Proceedings of the American Mathematical Society* 124(2) (1996),
591-600, DOI `10.1090/S0002-9939-96-03132-2`. Crossref metadata confirms those bibliographic
fields, but this intake did not inspect or preserve the article's statement/proof text, map its
assumptions to the catalog, audit corrections, or obtain independent review. It also cannot
validate the catalog's Sobolev/1936 attribution. It is therefore a source-family lead only, not
`E4`, `H0`, or a selected canonical variant.

Before ordinary theorem execution or `H0`, accountable reviewers must preserve a lawful immutable
edition; identify an exact theorem, section and page; transcribe all incorporated definitions,
ordered binders, hypotheses, conclusion, parameter ranges, constants, and exceptional cases; map
the historical wording to any modern Sobolev, boundary, trace, and target-space conventions; audit
translation, corrections, and errata; reconcile the duplicated catalog provenance; and
independently approve the source-to-Lean crosswalk.

## Pinned Lean discovery boundary

At mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the narrow intake probe checks
`MeasureTheory.Lp`, `MeasureTheory.MemLp`, `Measure.restrict`, `ModelWithCorners.boundary`,
`ModelWithCorners.interior_union_boundary_eq_univ`, and
`MeasureTheory.eLpNorm_le_eLpNorm_fderiv_one`. These are, respectively, ambient `Lp`/measurability,
measure-restriction, manifold-boundary, and adjacent smooth Sobolev-inequality interfaces. None
constructs or proves a Sobolev trace map.

A bounded exact-topic search over pinned mathlib found no `TraceOperator`, `SobolevTrace`, or
Sobolev boundary-trace theorem. A legacy neighboring dossier also records the same missing local
terminal interface, but it is discovery input rather than evidence for this target. These bounded
observations are not an exhaustive downstream anchor audit and do not establish global absence.

The probe contains no target declaration or proof body. Consequently the canonical Lean module,
expression, elaborated-expression hash, environment fingerprint, alternate transports, statement
mutations, and proof provenance remain null or open, and the machine status stays `M4`.

## First blocker and retry condition

The first downstream blocker is exact source-statement identity. An approved source decision must
freeze every domain, boundary, measure, Sobolev, exponent, trace-space, map, estimate, additional
conclusion, binder, and degenerate-case choice in the scope map. Only then may the statement phase
write and elaborate an exact Lean expression, minimize imports, serialize its fingerprints, check
alternate encodings, and mutation-test hypotheses, domains, binder scope, and boundary cases.
