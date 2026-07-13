# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:554-559` supplies exactly the title `阿廷定理`, attribution to
Emil Artin, year 1931, gloss `关于诱导特征标的线性无关性` ("about the linear independence of
induced characters"), importance "high," and status `已验证`. Git history attributes all six
uncited lines to commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record contains no
bibliography, formula, domain, ordered binders, hypotheses, definitions, proof boundary, correction
history, reviewer, or formal artifact.

`Docs/Stage0_Blueprint.md:2163-2188` repeats the gloss while explicitly leaving the formal system,
foundation, exact definitions and premises, proof route, dependencies, alternate forms, axioms,
machine status, and artifact links open. The rev-5.6 manifest preserves `已验证` only as untrusted
metadata and resets the target to `L0 / rework_required`.

## Inspected modern source lead

Jean-Pierre Serre, *Linear Representations of Finite Groups*, translated by Leonard L. Scott,
Springer, 1977, DOI `10.1007/978-1-4684-9458-7`, Chapter 9, Section 9.2, Theorem 17 and its
corollary, printed page 70 (PDF page 78), was inspected in a temporary scan served by a university
course mirror at `https://www.math.tau.ac.il/~borovoi/courses/ReprFG/Hatzagot.pdf`. Theorem 17
fixes a finite group `G`,
a family `X` of subgroups, and the homomorphism

```text
Ind : direct_sum (H in X) R(H) -> R(G).
```

It proves the equivalence between (i) `G` being the union of the conjugates of the subgroups in
`X` and (ii) the cokernel of `Ind` being finite. Serre restates (ii) as: for each character `chi` of
`G`, there are virtual characters `chi_H` in `R(H)` and an integer `d >= 1` such that

```text
d * chi = sum (H in X) Ind_H^G (chi_H).
```

The immediate corollary says every character of `G` is a rational linear combination of characters
induced from characters of cyclic subgroups. The first proof establishes surjectivity after
complexification via injectivity of the adjoint restriction map. The result is therefore a
generation/spanning statement; it does not assert that the induced characters are linearly
independent. The observed scan SHA-256 is
`099bb953993bce35bcbdccd989140248e4db8dd066744a62830b7fe940627516`. The scan was not added
to the repository or accepted as immutable source evidence; the mirror was not identified as an
author or publisher host. Edition preservation, correction
audit, independent review, and catalog-to-source identity remain open, so this is `H1`, not `H0`.

## Historical source lead

Crossref metadata was inspected for Emil Artin, "Zur Theorie der L-Reihen mit allgemeinen
Gruppencharakteren," *Abhandlungen aus dem Mathematischen Seminar der Universitaet Hamburg* 8
(1931), 292-306, DOI `10.1007/BF02941010`. This matches the catalog's author and year and is a
plausible historical source for the standard induction theorem. The publisher page did not provide
an inspectable article body in this worker environment. No exact original theorem/page, notation
transport, translation, proof boundary, or correction history was located or credited.

## Clause crosswalk

| Catalog component | Inspected standard source | Prospective Lean surface | Intake assessment |
|---|---|---|---|
| "Artin theorem" | Serre Chapter 9, Theorem 17, Artin induction | future character-ring theorem | name and date fit a standard family, but catalog identity is unproved |
| "characters" | ordinary complex characters and virtual-character rings `R(H)`, `R(G)` | `FDRep.character` plus a future Grothendieck/character-ring model | character kind and representation ring absent from catalog |
| "induced" | sum of `Ind_H^G : R(H) -> R(G)` over a subgroup family | `Representation.ind` / `Rep.indFunctor` are representation-level anchors | subgroup inclusions, finite index, and character-ring functoriality open |
| "linear" | rational linear combination in the cyclic corollary | scalar extension of a virtual-character group | coefficient ring absent from catalog |
| "independence" | not asserted; Theorem 17 asserts finite cokernel, hence rational spanning | would require a `LinearIndependent` target and an exact indexed family | material contradiction with the inspected standard statement |
| author/year | Emil Artin / 1931 | provenance only | consistent with historical lead, insufficient to repair the gloss |

## Lean and substitution boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`:

- `Mathlib.RepresentationTheory.Character` defines `FDRep.character` and proves conjugacy
  invariance and orthogonality results;
- `Mathlib.RepresentationTheory.Induced` defines `Representation.ind`, `Rep.indFunctor`, and the
  induction-restriction adjunction;
- `Mathlib.LinearAlgebra.LinearIndependent.Basic` proves `linearIndependent_monoidHom`, explicitly
  documented as Dedekind's linear independence of characters.

These are adjacent interfaces only. No Artin finite-cokernel/rational-spanning theorem, virtual
character ring needed by Serre's statement, or exact induced-character independence declaration was
located in the bounded repo-local and pinned-mathlib search. The existing
`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_082.lean` is owned by `THM-M-0429`; it expressly
classifies the induction functor as infrastructure and says virtual characters and Brauer induction
remain missing. It supplies no proof credit here.

In particular, the following substitutions are forbidden:

- Artin induction/rational spanning for the catalog's literal independence claim;
- Dedekind linear independence of monoid homomorphisms for induced characters;
- irreducible-character orthogonality for independence of an unspecified induced family;
- representation induction or its adjunction for a theorem about the induced characters;
- Brauer induction, Artin L-function continuation, or any neighbor theorem.

## Statement retry gate

The statement phase may freeze a target only after an accountable source decision either corrects
the catalog gloss to a pinpoint Artin-induction proposition or identifies a genuine induced-
character linear-independence theorem. It must fix the exact group and finiteness assumptions,
subgroup family and duplicate/conjugacy convention, character and virtual-character definitions,
induction maps, coefficient ring, ordered binders, conclusion, degenerate cases, and all transports
to Lean. That decision needs immutable source preservation, an errata audit, and independent review.
