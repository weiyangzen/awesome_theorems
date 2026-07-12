# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md` records only:

- title: `布劳尔群定理`;
- attribution: Richard Brauer;
- year: 1932;
- gloss: `域上中心单代数的分类`;
- importance: high;
- untrusted formalization label: `已验证`.

All six lines originate in repository commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. `Docs/Stage0_Blueprint.md` repeats this metadata while
leaving the definitions, premises, proof route, equivalent statements, axioms, machine status, and
artifact links open. The generated Stage0 projection is not an independent mathematical source.

## Historical leads

Crossref metadata identifies the following possible primary-source leads:

- Richard Brauer, "Ueber Systeme hyperkomplexer Zahlen," *Mathematische Zeitschrift* 30
  (1929), 79-107, DOI `10.1007/BF01187754`.
- R. Brauer, E. Noether, and H. Hasse, "Beweis eines Hauptsatzes in der Theorie der Algebren,"
  *Journal fuer die reine und angewandte Mathematik* 167 (1932), 399-404, DOI
  `10.1515/crll.1932.167.399`.

Only bibliographic metadata was inspected at intake. No immutable article scan, exact theorem or
page passage, incorporated definition, premise map, proof boundary, correction, translation, or
independent source review is accepted. The catalogue attributes the item only to Brauer, while the
1932 metadata lists three authors; this unresolved genealogy is another reason not to infer the
root from date alone.

## Clause crosswalk

| Repository phrase or candidate clause | Mathematical data that must be fixed | Pinned Lean candidate | Intake status |
|---|---|---|---|
| "over a field" | arbitrary field, characteristic and universe policy | `{K : Type u} [Field K]` | API available; exact binder scope open |
| "central simple algebra" | associative unital `K`-algebra, centrality, simplicity, finite dimensionality | `CSA.{u,v} K` | strong bundled candidate; source identity open |
| stable classification | positive matrix sizes and stabilized algebra equivalence | `IsBrauerEquivalent A B` | relation definition and equivalence lemmas available |
| equivalence classes | quotient carrier and equality/representative relationship | `Brauer.CSA_Setoid K`, `BrauerGroup K` | carrier definition available; not a full theorem |
| abelian group theorem | tensor-product closure and congruence, unit, inverse, associative and commutative laws | no completed API in `BrauerGroup.Defs`; its TODO names this gap | materially stronger candidate root; open |
| division representative | matrix-over-division-algebra existence and uniqueness at class level | Wedderburn-Artin family candidates outside the minimal probe | supporting/alternate family; no root credit |
| Morita classification | both directions between stable matrix and categorical module equivalence | TODO in `BrauerGroup.Defs` | open bridge, not silently included |
| arithmetic/cohomological classification | explicitly selected invariant and field hypotheses | no candidate selected | excluded unless a source selects it |

## Formal discovery candidates

The intake probe checks the pinned mathlib declarations named above and prints the axiom reports of
the transitivity and equivalence witnesses. This confirms only that the definitions and relation
infrastructure elaborate in the pinned environment.

The separate `THM-M-0424` legacy file
`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_078.lean` contains quotient wrappers, a
Wedderburn-Artin wrapper, and interfaces for which it supplies no inhabitant for missing
Brauer-group data. It explicitly
describes the quotient and normal-form results as a partial boundary. Because it belongs to another
target and predates this intake, it supplies discovery context only: no accepted statement,
obligation, receipt, or proof credit transfers to `THM-M-0037`.

## First failed source gate

`H0` fails at source identity and pinpoint mapping. There is no reviewed immutable source passage
from which to determine the root conclusion, assumptions, definitions, chronology, proof boundary,
or errata status. Consequently there is also no checked source-to-Lean identity or transport. The
provisional `H1` records real leads and a constrained theorem family, not source fidelity.
