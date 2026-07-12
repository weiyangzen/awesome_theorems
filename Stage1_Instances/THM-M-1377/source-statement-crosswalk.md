# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:10034-10039` supplies exactly the title `变分法`, attribution to
many mathematicians, the seventeenth century, the gloss `泛函极值的必要条件`, importance "high,"
and status `已验证`. Git history attributes all six uncited lines to repository commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The research document is a raw catalog source, not a
primary mathematical citation. It contains no bibliography, stable source ID, edition, theorem or
page locator, formula, definition, binder, hypothesis, conclusion, proof boundary, correction
history, reviewer, or formal artifact for this record.

`Docs/Stage0_Blueprint.md:37452-37477` repeats the gloss while explicitly leaving the formal system,
foundation, exact definitions and premises, proof process, dependencies, alternate forms, axioms,
machine status, and artifact links open. Its generic planning text about a known closed result is
not source evidence. The rev-5.6 manifest preserves `已验证` only as `source_status_untrusted` and
resets the target to `L0 / rework_required`.

## Literal crosswalk

| Catalog element | Necessary mathematical component | Prospective Lean component | Intake status |
|---|---|---|---|
| `变分法` | one theorem rather than the whole calculus-of-variations field | one exact `Prop` with ordered binders | result kind absent |
| "functional" | functional domain, codomain, scalar field, admissible class, and topology | typed spaces, functional, admissibility predicate, and typeclasses | all absent |
| "extrema" | local/global and min/max notion, comparison topology, interior or boundary status | `IsLocalMin`, `IsLocalMax`, constrained variants, or source-specific predicate | choice and scope absent |
| "necessary conditions" | derivative, first variation, differential equation, multiplier, boundary, or transversality conclusion | source-selected derivative/variation/operator expression | conclusion absent |
| admissible variations | regularity, constraints, endpoint/boundary conditions, and quantifier order | variation type, predicates, and ordered binders | absent |
| many mathematicians / seventeenth century | broad historical context | provenance metadata only | no accountable source |
| `已验证` | untrusted inventory field | accepted human proof and kernel receipt would be required | no H or M credit |

The noun phrase does not quantify over a functional or assert an implication. Treating a standard
textbook theorem as implicit would still require choosing materially different premises and
conclusions that the repository does not supply.

## Candidate-form boundary

Pinned mathlib's `Mathlib.Analysis.Calculus.LocalExtr.Basic` contains generic Fermat theorems such
as `IsLocalMin.hasFDerivAt_eq_zero`, `IsLocalMin.fderiv_eq_zero`, and
`IsLocalExtr.fderiv_eq_zero`. They express one plausible unconstrained real-normed-space reading:
a local extremum forces a Frechet derivative to vanish. The catalog does not select normed spaces,
Frechet differentiability, unconstrained interior extrema, or this conclusion, so these declarations
remain discovery-only APIs and are not an encoding, anchor, or proof of `THM-M-1377`.

An integral first-variation theorem additionally needs an interval or domain, integrand,
admissible paths or fields, endpoint or boundary data, regularity, differentiation-under-the-
integral conditions, and test variations. An Euler-Lagrange theorem further chooses a pointwise,
weak, or almost-everywhere differential conclusion. A multiplier theorem instead needs constraint
maps and a qualification. None is a mere alternate spelling of the generic Fermat interface, and
no checked transport among them is credited.

## Neighbor and substitution boundary

The next catalog record separately names Euler-Lagrange (`THM-M-1378`). The repository also assigns
distinct targets to variational PDE methods, the direct method, Tonelli existence, lower
semicontinuity, minimizing sequences, Maupertuis' principle, least action, and Lagrangian mechanics.
Those boundaries weigh against silently interpreting this record as any one neighboring target.
Legacy least-action files describe their own fixed-endpoint or Euler-Lagrange boundaries and do not
provide source provenance or proof credit here.

## Source gate

There is no theorem-bearing primary source selected by the repository. Before leaving `H5`, an
accountable target correction must select one stable truth-valued proposition; preserve an
immutable primary or authoritative edition; record theorem/section/page, every incorporated
definition, ordered binder, hypothesis, conclusion, proof boundary, and exceptional case; audit
errata; reconcile its relationship to neighboring targets and candidate forms; and obtain
independent source-to-statement approval.

`H5` here does not assert that the calculus of variations or its standard necessary-condition
theorems are false or mathematically open. It records that the repository phrase is not itself a
truth-valued target that a Lean kernel could check.

## Lean discovery boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the discovery-only probe
checks `IsLocalMin`, `IsLocalExtr`, `HasFDerivAt`, `fderiv`,
`IsLocalMin.hasFDerivAt_eq_zero`, and `IsLocalExtr.fderiv_eq_zero`. A bounded search found no
exact terminal calculus-of-variations, first-variation, or Euler-Lagrange declaration in pinned
mathlib. Repo-local references belong to other theorem dossiers or legacy planning surfaces. The
later dependency-ordered immutable formal-candidate audit remains open.

The canonical module, declaration or expression, expression and environment fingerprints, checked
alternate encodings, and statement mutations therefore remain null. No statement elaboration,
formal absence theorem, proof, audit completion, or theorem completion is claimed.
