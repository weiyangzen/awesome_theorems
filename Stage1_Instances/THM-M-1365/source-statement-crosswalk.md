# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md:9950-9955` supplies exactly the title `Smale马蹄`, Stephen Smale,
the year 1967, the gloss `混沌的几何模型`, importance "high," and status `已验证`. The same six
lines are duplicated at `10229-10234`. Git history attributes both uncited records to repository
commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. Neither occurrence contains a definition, formula,
binder, hypothesis, conclusion, bibliography, edition, theorem/page locator, proof boundary,
correction record, or formal artifact.

The repository separately catalogs physics records `THM-P-0778`, whose gloss says a horseshoe map
produces chaotic dynamics, and `THM-P-0786`, whose gloss explicitly says the horseshoe map is
topologically conjugate to the shift map. Those records show that the repository distinguishes the
broad chaos gloss from an explicit conjugacy gloss; they are separate targets and cannot supply
statement identity or proof credit here.

`Docs/Stage0_Blueprint.md:37128-37153` repeats the gloss while leaving the proof system, logical
foundation, background, exact definitions and premises, proof process, dependencies, equivalent
formulations, axioms, machine status, and artifact links open. The rev-5.6 manifest retains
`已验证` only as untrusted source metadata and resets this target to `L0 / rework_required`.

## Inspected primary discovery source

Stephen Smale, *Differentiable Dynamical Systems*, **Bulletin of the American Mathematical
Society** 73(6), 1967, pages 747-817, DOI
`10.1090/S0002-9904-1967-11798-1`, is a plausible primary source matching the catalog attribution
and year. The AMS-hosted scan was inspected outside the repository; the observed 7,390,130-byte
PDF had SHA-256 `759e0601e50ceebc812c4a4c67e5b9ed59534848c6d342a2e2cf56871db19551`.

Section 1.5, printed pages 769-775, defines the full shift on a finite alphabet and describes the
folded-square construction. It then presents distinct results: shift periodic points (5.1), the
two-strip invariant-set conjugacy (5.3), perturbation stability (5.4), a global sphere extension,
and the transverse-homoclinic-point theorem (5.5). The text calls the Figure 1 construction the
"horseshoe," but the catalog does not cite the article or identify which result or conjunction is
intended by "geometric model of chaos."

The scan and extracted text of Proposition (5.3) also appear to alternate between the invariant-set
symbol and an omega-like symbol in the conjugacy clause after defining the former. Intake does not
silently normalize that potential print/OCR ambiguity. The precursor `[115]` and a reliable
typeset/transcribed source must be compared before exact wording is frozen.

This inspection discriminates candidate statements; it is not an H0 source admission. A future
source audit must preserve an approved immutable edition, transcribe the selected result and every
incorporated definition and hypothesis, check the cited precursor `[115]`, corrections and errata,
map premises to formal binders, and obtain independent review.

## Component crosswalk

| Repository element | Mathematical alternatives | Prospective Lean surface | Intake assessment |
|---|---|---|---|
| "Smale horseshoe" | explicit two-strip planar construction; perturbation-stable class; global sphere example; homoclinic-point consequence | future map, square/strips, maximal invariant set, and exact assumptions | construction/theorem family only |
| "geometric model" | folded image of a square with horizontal contraction and vertical expansion | geometric predicates, affine/cone estimates, intersection components, iterates | dimensions, constants, and boundary rules absent |
| "chaos" | full-shift conjugacy; dense/infinite periodic points; entropy; sensitivity; indecomposability | an exact source-selected dynamical conclusion | not a defined predicate or conclusion |
| invariant set | all forward/backward iterates remaining in the square; nonwandering component; Cantor set | indexed intersection or orbit-stay predicate plus compactness/invariance | object and iterate convention absent |
| symbolic coding | one- or two-sided shift, full shift or subshift, semiconjugacy or conjugacy | sequence space, shift map, coding map, homeomorphism, `Function.Semiconj` | alphabet, direction, and strength absent |
| Stephen Smale / 1967 | historical attribution and plausible paper | provenance metadata only | source lead corroborated, target not selected |
| `已验证` | untrusted inventory label | no Lean declaration or proof object | explicitly rejected as evidence |

## Proposition boundaries

Proposition (5.3), perturbation Proposition (5.4), the global sphere construction, and homoclinic
Theorem (5.5) are not equivalent statement packages. The full-shift periodic-point result (5.1) is
a consequence ingredient, not the geometric construction. A two-symbol full shift also differs
from an arbitrary finite alphabet, a subshift of finite type, and a one-sided shift. Intake cannot
fill the missing ordered binders, hypotheses, conclusion, or Lean expression by choosing one of
these from memory.

The separately scheduled symbolic-dynamics, shift-map, topological-entropy, hyperbolic-dynamics,
and Markov-partition targets are scope neighbors, not sources of shared proof credit.

## Lean boundary and retry requirement

The pinned probe elaborates `Stream'`, `Stream'.tail`, `Function.Semiconj`,
`Function.Semiconj.iterate_right`, `Function.Semiconj.mapsTo_periodicPts`,
`Function.IsPeriodicPt`, and `Homeomorph`. These generic interfaces could support a later symbolic
coding, but they define no horseshoe map, strip geometry, invariant Cantor set, hyperbolicity, or
source-selected conjugacy. A bounded local search found no exact named horseshoe declaration; that
is not the required immutable external anchor audit and does not prove global absence.

Before statement closure, accountable reviewers must select one immutable, pinpointed source
proposition; preserve all incorporated definitions, ordered binders, geometric and regularity
assumptions, conclusion, proof boundary, and correction status; decide every candidate and neighbor
boundary; and independently approve the mapping. Only then may the Lean statement gate freeze
minimal imports, an elaborated expression, checked transports, and removed-hypothesis,
changed-domain, binder-scope, and boundary mutations.
