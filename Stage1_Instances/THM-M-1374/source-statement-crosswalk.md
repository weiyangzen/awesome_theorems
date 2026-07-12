# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:10013-10018` supplies exactly the title `Noether定理`, Emmy
Noether, 1918, the gloss `对称性与守恒量`, importance `高`, and status `已验证`. Git blame places all
six uncited fields in commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`.

`Docs/Stage0_Blueprint.md:37371-37396` repeats those fields while leaving the target formal system,
logical foundation, exact definitions and premises, proof process, dependencies, equivalent forms,
axioms, choice/classical-logic use, machine-checked status, and artifact links open. The rev-5.6
manifest preserves `已验证` only as untrusted metadata and resets the target to
`L0 / rework_required`.

The catalog therefore contains no bibliography, theorem or page locator, variational functional,
group action, regularity, ordered binders, hypotheses, conclusion, incorporated definitions, proof
boundary, translation provenance, correction record, or reviewer. The phrase `symmetries and
conserved quantities` is a relation between concepts, not a stable proposition.

## Historical primary-text lead

Emmy Noether, *Invariante Variationsprobleme*, *Nachrichten von der Gesellschaft der
Wissenschaften zu Goettingen, Mathematisch-Physikalische Klasse* (1918), pages 235-257, is the
historical source family indicated by the catalog attribution and year. M. A. Tavel's English
translation, originally published in *Transport Theory and Statistical Physics* 1(3) (1971), was
inspected through arXiv `physics/0503066v3`, "Invariant Variation Problems." The observed 14-page
PDF has SHA-256 `b9f73c19db726b7fd427a38fb786a4a0e7653472abd56d3a042e3b0255ac07d5`.

Section 1, translated pages 1-3, defines finite continuous groups with `rho` essential parameters,
infinite continuous groups depending on `rho` arbitrary functions and their derivatives,
variational integrals, and Lagrange expressions. It then states:

- Theorem I: invariance under a finite continuous group gives `rho` linearly independent
  combinations of Lagrange expressions that are divergences; its converse is subject to the
  source's exception and integrability/group-property qualifications. In one dimension, imposing
  the Lagrange equations gives first integrals, while in several dimensions it gives conservation
  laws.
- Theorem II: invariance under an infinite continuous group whose arbitrary functions occur through
  order `sigma` gives `rho` identities among Lagrange expressions and their derivatives through
  that order, and conversely subject to source-noted qualifications.

This source shows why the catalog gloss is underdetermined: it does not select Theorem I or II,
direct or converse direction, one- or multidimensional setting, or any later specialization. The
translation's arXiv record notes corrigenda, but no complete original/translation reconciliation,
errata admission, line-by-line definition and assumption map, lawful repository source capture, or
independent review has been completed. The inspected file is a discovery input, not accepted `H0`
evidence.

## Component crosswalk

| Catalog component | Material interpretations in the source family | Prospective Lean surface | Intake assessment |
|---|---|---|---|
| symmetry | finite group with essential parameters; infinite group depending on arbitrary functions; infinitesimal or integrated action; exact or divergence invariance | group/action or local action, generators, transformations on independent and dependent variables or jets | all choices absent |
| variational problem | one- or multi-integral, dependent fields and derivatives of source-selected order, boundary conditions | action functional or density, jet/derivative data, variations, integration and boundary predicates | not mentioned by catalog |
| Lagrange expressions | Euler-Lagrange expressions before imposing equations of motion | source-selected Euler-Lagrange operator and regularity hypotheses | definition and order absent |
| conserved quantity | first integral in one dimension, divergence-free current in several dimensions, charge after additional integration and boundary assumptions | derivative-zero, `Function.IsConstant`, divergence-zero, or conserved integral/charge | carrier and conservation notion absent |
| direct theorem | invariance implies divergence relations or differential identities | implication from checked invariance to checked identity | not selected |
| converse | divergence relations or identities imply invariance under source conditions | reverse implication with integrability/effectiveness side conditions | not selected |
| finite versus infinite group | first theorem versus second theorem, with different outputs | finite parameters versus arbitrary-function/gauge data | not selected |
| correspondence | may mean two directions, an association modulo trivial terms, or only an informal slogan | `Iff`, paired implications, quotient/equivalence, or a construction | catalog wording does not say `correspondence`; duplicate target does |
| 1918 | historical publication year | provenance only | no edition or locator supplied |
| `已验证` | inventory label | no declaration or proof body | explicitly rejected as evidence |

## Duplicate target and legacy artifact

The repository separately owns `THM-M-1515`, `诺特定理`, under mathematical physics. Its source
record at `Docs/researches/math_theorems.md:11066-11071` says `对称性与守恒量的对应`, which is
similar but not identical to the present gloss. The target manifest gives it legacy slot
`S1-M-184`; `THM-M-1374` has no legacy slot.

`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_184.lean` is discovery input for that distinct
target. Its prose says finite-dimensional, but its formal binders specify only a real normed-space
Lagrangian, a flow, an infinitesimal generator, momentum, and an opaque Euler-Lagrange predicate;
they do not include a `FiniteDimensional` typeclass. Its `NoetherHypotheses` includes
`NoetherCurrentDerivativeFormula`, which already assumes that every Euler-Lagrange trajectory has
zero derivative of the proposed charge; the general conclusion is then obtained from that assumed
bridge. It also proves a concrete zero-Lagrangian special case. The file explicitly states that no
terminal Noether proof is claimed and records `not_repo_local_closed`.

Thus the artifact neither selects the canonical meaning of `THM-M-1374` nor proves a general
source-mapped Noether theorem. Reusing it would substitute another target and would hide the main
bridge inside a hypothesis.

## Required source admission

The statement phase must preserve and hash a lawful complete source edition, select a precisely
delimited theorem and directions, transcribe every incorporated definition, ordered binder,
hypothesis, exception, and conclusion, map the proof boundary, reconcile original and translated
wording and corrections, and obtain independent review. It must explicitly decide finite versus
infinite symmetry, mechanics versus fields, exact versus quasi-invariance, off-shell identities
versus on-shell conservation, boundary terms, current equivalence, and converse scope. It must then
freeze and mutation-test the same exact Lean expression.

Until that happens, the canonical mathematical and Lean targets remain null. The source
classification is `H5` because the catalog record is not a stable truth-valued proposition; the
machine classification is `M4` because no usable source-identical formal target has been located;
and readability is `R4` because no source-faithful proof reconstruction can attach to an unfrozen
root.
