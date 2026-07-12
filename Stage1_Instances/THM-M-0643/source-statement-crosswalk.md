# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:4762-4767` supplies exactly the title `Wecken定理`, attribution
to Franz Wecken, year 1942, gloss `不动点类的Nielsen数`, importance "high," and status
`已验证`. The record was introduced at commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. It contains no citation, definitions, domains,
ordered binders, hypotheses, conclusion, proof boundary, correction history, or formal artifact.

`Docs/Stage0_Blueprint.md:17584-17609` repeats that gloss while explicitly leaving the formal
system, foundation, exact definitions and premises, proof route, dependencies, equivalent forms,
axioms, machine status, and artifact links open. The rev-5.6 manifest retains `已验证` only as
untrusted metadata and resets the target to `L0 / rework_required`.

## Primary bibliographic leads

Publisher/Crossref metadata identifies a three-paper primary series by Franz Wecken:

- *Fixpunktklassen. I*, *Mathematische Annalen* 117 (1940), 659-671,
  DOI `10.1007/BF01450034`.
- *Fixpunktklassen. Teil II. Homotopieinvarianten der Fixpunkttheorie*,
  *Mathematische Annalen* 118 (1941 publisher metadata; commonly cited 1942), 216-234,
  DOI `10.1007/BF01487362`.
- *Fixpunktklassen. Teil III. Mindestzahlen von Fixpunkten*,
  *Mathematische Annalen* 118 (1941 publisher metadata; commonly cited 1942), 544-577,
  DOI `10.1007/BF01487386`.

The first paper's deposited references explicitly discuss inequalities between a minimum
fixed-point count and an algebraic/Nielsen-type count for earlier special polyhedra. The later
papers cite the first as their preliminary terminology. This makes the series a credible primary
lead for the catalog family, but metadata and reference snippets do not identify the exact final
theorem passage or all its assumptions. The catalog's 1942 date also differs from the publisher's
1940/1941 print metadata. No date is silently normalized, and no theorem text, translation,
erratum disposition, or independent source review is accepted here.
Part III is the direct minimum-fixed-point source lead. Publisher metadata for it says that Part I
supplies frequently used notation and that Part II is not used there; the paywalled body was not
available for an exact `Satz` and page transcription.

An inspected modern disambiguation lead is Ulrich Koschorke, *Minimum numbers and Wecken theorems
in topological coincidence theory. I*, arXiv `1305.1664v1` (2013-05-07). Printed page 20 states
that, for fixed points of a self-map `f` of `M`, the relevant coincidence Nielsen invariants reduce
to the classical `N(f)` and attributes `N(f) = MF(f)` for dimension `m >= 3` to Wecken. Printed
page 6 gives a later classification for closed connected manifolds, excluding negative-Euler-
characteristic surfaces. The inspected PDF has SHA-256
`59e1975bd1f991eec8e9dc4e3c54bf8c801c1a92ad08ae6821d497974592cb57`.
This confirms the minimum/equality interpretation and the material dimension boundary, but it is
not the primary proof and cannot silently replace the original theorem with the modern all-closed-
manifold classification.

## Component crosswalk

| Catalog or candidate component | Required source decision | Prospective Lean surface | Intake result |
|---|---|---|---|
| fixed point | topological space and continuous self-map | `ContinuousMap`, `Function.IsFixedPt`, `Function.fixedPoints` | generic APIs checked; domain open |
| fixed-point class | path/homotopy or lift/Reidemeister equivalence | future relation/quotient plus well-definedness | absent from catalog and pinned API search |
| class index and essentiality | index normalization and nonzero criterion | future integer-valued invariant | unresolved |
| Nielsen number | finite count of essential classes | future natural, finite-cardinal, or cardinal value | gloss names it but does not define it |
| homotopy lower bound | quantification over representatives `g` and fixed-set count | `ContinuousMap.Homotopic` plus cardinality bridge | prerequisite/candidate, not the realization theorem |
| minimum/realization | source hypotheses under which a representative attains `N(f)` | existential representative or checked equality | likely Wecken family, exact proposition open |
| `已验证` | untrusted inventory label | no proposition or proof object | no H or M credit |

## Formal-source boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the discovery probe
checks fixed-point predicates, closedness of fixed-point sets, continuous maps, and ordinary and
relative homotopy. A bounded search of repo-local Lean and pinned mathlib found no relevant
`Wecken`, `Nielsen fixed`, `fixed point class`, `Nielsen number`, or `Reidemeister class`
declaration. Generic interfaces do not select a source statement or supply a proof. This is a
bounded intake observation, not a global absence claim or the dependency-ordered anchor audit.

## Gate to exact statement

Before leaving `H1`, accountable reviewers must admit an immutable primary or authoritative source
and identify one exact theorem passage; transcribe every incorporated definition, ordered binder,
hypothesis, conclusion, dimension and boundary condition; reconcile the 1940/1941/1942 dating and
the Nielsen-versus-Wecken target boundary; audit corrections; and independently approve the map.
Only then may the statement phase choose minimal imports, elaborate an exact Lean expression,
serialize its fingerprint, check alternate transports, and run the required statement mutations.
