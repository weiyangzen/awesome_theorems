# Source-statement crosswalk

## Repository records

`Docs/researches/math_theorems.md:1864-1869` supplies exactly the title `麦克马伦定理`, Curtis
McMullen, 1994, the gloss `有理函数的Julia集`, importance "high", and status `已验证`. Git blame
attributes all six uncited lines to commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record
contains no bibliography, formula, theorem locator, assumptions, quantifiers, conclusion, or proof.

`Docs/Stage0_Blueprint.md:7166-7191` repeats the gloss while explicitly leaving the formal system,
logical foundation, background, exact definitions and premises, proof route, dependencies,
equivalent forms, axioms, machine status, and artifact links open. Its generic planning language
about a known closed result is not primary-source evidence. The rev-5.6 manifest retains
`已验证` only as `source_status_untrusted` and resets the target to `L0 / rework_required`.

The same corpus contains `McMullen定理` at lines 10481-10486 with the same other five fields. It is
separately eligible as `THM-M-1435` because the records have distinct literal titles. Its Stage0
projection is at lines 39023-39048. The duplicate establishes an intake collision; it supplies no
additional proposition and cannot be merged or credited by this worker.

## Bibliographic discovery boundary

Curtis T. McMullen's *Frontiers in Complex Dynamics*, *Bulletin of the American Mathematical
Society* 31 (1994), 155-172, DOI `10.1090/S0273-0979-1994-00519-1`, is preserved as arXiv version
`math/9410221v1`. The inspected 17-page PDF has SHA-256
`e8f777c2bda3133b0b30241702d447410826a892d507e12d8d68c9042d0a0b81`.

The paper surveys many conjectures and results about rational maps. It names theorems of Sullivan,
Douady-Hubbard, and Yoccoz as well as McMullen's work. Its Theorem 5.2 states that if
`f(z) = z^2 + c` is an infinitely renormalizable real quadratic polynomial, then its Julia set
carries no invariant line field; Corollary 5.3 concerns hyperbolicity of Mandelbrot-set interior
components meeting the real axis. This is credible ambiguity evidence, not target identity: the
catalog cites neither the paper nor a theorem locator or conclusion.

The survey cites `[Mc]` as McMullen's *Complex Dynamics and Renormalization*, then "to appear."
The identified Princeton University Press edition is dated 1995 and has DOI
`10.1515/9781400882557`. The catalog's 1994 date may refer to the survey, an announcement, or
another source, but it does not decide among them. Neither work receives H0 or statement credit at
intake.

## Component crosswalk

| Repository element | Mathematical component to freeze | Required Lean component | Intake assessment |
|---|---|---|---|
| `麦克马伦定理` | one theorem due to McMullen | immutable source, theorem/page locator, proof boundary, errata | name only; many candidates |
| Curtis McMullen / 1994 | historical attribution and date | source revision and reviewed bibliographic identity | credible leads; no selected source |
| "rational functions/maps" | sphere self-map, polynomial, polynomial-like map, or parameter family | exact map representation, degree, poles/infinity, iteration domain, hypotheses | object and class open |
| "Julia set" | one source-defined set and property | ambient type/topology, set predicate, normality/periodicity/measure definitions | definition and role open |
| unstated logical relation | definition, equality, implication, absence, density, rigidity, dimension, or connectivity | one exact `Prop` with ordered binders, hypotheses, and conclusion | no truth-valued conclusion |
| `已验证` | untrusted inventory label | accepted source review and kernel receipt would be required | no H or M credit |

## Duplicate and neighbor boundary

`THM-M-1435` is an apparent semantic duplicate but remains a separate manifest root. It cannot
lend this target its scope or credit, and this worker cannot change the target denominator.
Likewise, neighboring Yoccoz, Mandelbrot, Sullivan, Julia-set, renormalization, and Feigenbaum
targets own distinct subject labels. A corrected source crosswalk must explain rather than erase
those boundaries.

## Source gate

Before the target can leave `H5`, an accountable reviewer must approve a truth-valued correction,
preserve and hash an immutable primary edition, identify an exact theorem and every incorporated
definition, transcribe ordered binders and hypotheses, check translation, publication-date
provenance, corrections and errata, and map every conclusion clause and boundary case. A second
qualified reviewer must approve the mapping and the treatment of `THM-M-1435`. The corrected
proposition's H status must then be classified afresh; it cannot inherit `已验证`.

## Lean discovery boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, `IntakeProbe.lean`
checks complex numbers, one-point compactification, meromorphic predicates, function iteration,
periodic points, closure, and frontier. A bounded name search found no McMullen, Julia-set,
Mandelbrot, complex-dynamics, rational-dynamics, or Lattes target declaration in repo-local or
pinned mathlib Lean sources. The repository's legacy `S1_M_259.lean` instead identifies itself as
`THM-M-0504` and concerns Riemann-hypothesis consequences, so its numeric filename gives no target
credit here.

The canonical module, declaration or expression, elaborated-expression hash, checked transports,
and statement mutations remain null. The probe and bounded search are feasibility evidence only,
not a complete formal-candidate audit and not H0, M0, or readable-proof closure.
