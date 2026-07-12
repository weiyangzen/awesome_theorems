# Source-statement crosswalk

## Repository source record

The only repository-supplied record is at `Docs/researches/math_theorems.md:4755-4760` and was
introduced unchanged at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`:

| Catalog field | Received value | Statement consequence |
|---|---|---|
| title | `Nielsen不动点定理` | Names a theorem family, not a unique proposition. |
| attribution | Jakob Nielsen | Historical orientation only; no work, theorem, or page is cited. |
| date | 1921 | Does not select an edition or resolve the historical date convention. |
| statement | `不动点类的理论` | Names a subject; supplies no binders, assumptions, or conclusion. |
| importance | high | Scheduling metadata only. |
| formalization status | `已验证` | Explicitly untrusted; no human or machine proof credit. |

Stage0 at `Docs/Stage0_Blueprint.md:17557` projects the same gloss while leaving the formal
system, definitions/premises, proof route, dependencies, alternate statements, axioms, and
machine artifacts open. It cannot fill the missing proposition.

## Primary bibliographic leads

- J. Nielsen, *Uber die Minimalzahl der Fixpunkte bei den Abbildungstypen der Ringflachen*,
  *Mathematische Annalen* 82, 83-93, DOI `10.1007/BF01457977`. Crossref reports publication in
  March 1920; Springer also exposes volume/copyright metadata associated with 1921, and the
  Goettingen digitization catalogs the volume as 1921. This date discrepancy is recorded rather
  than silently normalized. The Goettingen range `PPN235181684_0082/LOG_0012` is a stable
  12-page scan. The article is a strong historical lead, but this intake has not admitted a
  theorem-level transcription, assumptions, proof boundary, or errata review from it.
- J. Nielsen, *Uber fixpunktfreie topologische Abbildungen geschlossener Flachen*,
  *Mathematische Annalen* 81, 94-96, DOI `10.1007/BF01563622` (Crossref: March 1920). This is a
  related primary lead, not automatically the catalog target.
- Bo Ju Jiang, *Lectures on Nielsen Fixed Point Theory*, Contemporary Mathematics 14, AMS, 1983,
  DOI `10.1090/conm/014`; Chapter I, "Fixed point classes and the Nielsen number," pages 4-23,
  DOI `10.1090/conm/014/01`. This is an authoritative secondary disambiguation lead, not a
  substitute for primary proof-source admission.

The citations and metadata are E5 discovery anchors only. No immutable text has yet received
independent statement/assumption/errata acceptance, so they establish neither H0 nor H1 for an
exact proposition.

## Phrase-to-statement map

| Received or candidate component | Required mathematical decision | Prospective Lean component | Intake result |
|---|---|---|---|
| fixed point | continuous self-map and fixed-point predicate | `ContinuousMap`, `Function.IsFixedPt`, `Function.fixedPoints` | adjacent API checked; target unresolved |
| fixed-point class | path/homotopy or lift/Reidemeister equivalence on fixed points | new equivalence relation, quotient/classes, and well-definedness | unresolved |
| class index | index domain, normalization, and invariance properties | integer-valued invariant with source hypotheses | unresolved |
| essential class | nonzero-index convention | predicate on class | unresolved |
| Nielsen number | finite count of essential classes and finiteness theorem | natural/finite-cardinal/cardinal-valued definition | unresolved |
| homotopy theory | exact kind and endpoints of homotopy | `ContinuousMap.Homotopic` is only generic substrate | unresolved |
| lower bound | scope of `N(f) <= #Fix(g)` and quantifier order over `g` | cardinality comparison plus class/index bridge | possible theorem family, not selected |
| minimum realization | hypotheses giving equality with the homotopy-class minimum | separate Wecken-type result | excluded as silent substitution |

There are therefore no ordered binders, hypotheses, exact conclusion, credited alternate
encoding, statement fingerprint, or formal proof body.

## Formal-source boundary

A bounded search of repo-local Lean and pinned mathlib at revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` found no relevant `Nielsen fixed`, `fixed point class`,
`Nielsen number`, or `Reidemeister class` declaration. The only Nielsen-named mathlib result is the
unrelated Nielsen-Schreier theorem. Mathlib's fixed-point and homotopy modules are discovery-only
substrate. This bounded result is not the dependency-ordered formal anchor audit.

## Human-source gate

To leave `H5`, the integration lane must admit one stable truth-valued target and an immutable
primary or authoritative source. An independent reviewer must approve the exact theorem/page,
incorporated definitions, every hypothesis, conclusion, proof boundary, dependent results,
translation, date/edition discrepancy, and correction/errata status, together with a row-level
source-to-mathematical-to-Lean map. Until then, the canonical statement and Lean target remain
null, and ordinary theorem-proof execution remains blocked.
