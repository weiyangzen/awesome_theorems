# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:10020-10025`, under ordinary differential equations, supplies
exactly the title `Liouville定理`, Joseph Liouville, 1838, the gloss `相空间体积守恒`,
importance "high," and status `已验证`. Git history places all six uncited lines in commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record contains no source title, equation,
definition, domain, binder, hypothesis, conclusion, proof boundary, correction, or formal artifact.

`Docs/Stage0_Blueprint.md:37398-37423` repeats the gloss while explicitly leaving the formal system,
foundation, exact definitions and premises, proof route, dependencies, equivalent formulations,
axioms, machine status, and artifact links open. The rev-5.6 manifest retains `已验证` only as
untrusted metadata and resets this target to `L0 / rework_required`.

## Duplicate repository records

`Docs/researches/math_theorems.md:11101-11106` independently records `THM-M-1520` as
`刘维尔定理`, Joseph Liouville, 1838, with the same gloss `相空间体积守恒` in mathematical
physics. `Docs/researches/physics_theorems.md:6839-6845` records the non-Stage1 mathematics item
`THM-P-0800` more explicitly as phase-space volume remaining invariant under Hamiltonian flow.

These records strongly identify the intended theorem family, but they do not decide whether the two
mathematics IDs are true duplicates, aliases with different source boundaries, or intentionally
different formulations. `THM-M-1520`'s existing canonical Lean statement and all its receipts belong
only to that target. Identity reconciliation and an approved source-root decision remain mandatory.

## Inspected modern source lead

David Tong, *Classical Dynamics*, University of Cambridge Part II Mathematical Tripos lecture notes,
Section 4.2, printed pages 88-90, was inspected from the author-hosted PDF linked by the author's
course page. The observed PDF had 1,093,743 bytes and SHA-256
`b65ba2b0399df6b02ca3850e5c69ee0255c3011a35664e80766349f521e43e80`; the tight inspected
Section 4.2 extract had SHA-256
`7b18b0386bde96a0babcc5add0883ae94c5dd40be9fe3a646a1143141d61819d`.

The section states that a region in phase space changes shape under time evolution but retains its
volume. Its displayed proof uses canonical coordinates `(q_i, p_i)`, the volume element
`dq_1 ... dq_n dp_1 ... dp_n`, Hamilton's equations, and the infinitesimal Jacobian; cancellation of
the mixed second derivatives gives determinant `1 + O(dt^2)` and hence constant volume. The following
discussion explicitly says the theorem holds for time-dependent Hamiltonians and need not imply
energy conservation, but the system must be Hamiltonian.

This authoritative modern exposition confirms the classical family and exposes needed assumptions.
It is not cited by the catalog, is not the 1838 primary source, and its informal finite-time step does
not by itself settle the exact regularity, local/global flow, measurable-set, or manifold statement
to formalize. The mutable remote PDF is a reproducible discovery lead, not admitted H0 evidence; no
complete genealogy, errata audit, immutable source packet, assumption-to-node map, or independent
review is claimed.

The existing `THM-M-1520` crosswalk also names V. I. Arnold, *Mathematical Methods of Classical
Mechanics*, second edition, Chapter 3, Section 16, as a bibliographic lead. That lead and its DOI are
not imported as accepted source evidence here because exact wording, page, assumptions, errata, and
target ownership have not been independently reviewed for `THM-M-1375`.

## Component crosswalk

| Catalog/source component | Prospective Lean surface | Intake assessment |
|---|---|---|
| phase space | canonical `R^n x R^n` or source-selected symplectic phase space | representation and dimension open |
| Hamiltonian evolution | `ContDiff` Hamiltonian plus integral curves or a `Flow` satisfying Hamilton's equations | regularity, time dependence, completeness, and sign convention open |
| volume | product Lebesgue `volume`, Liouville volume form, or induced measure | normalization and geometric-to-measure transport open |
| region evolves | image under a time map, with measurability/injectivity hypotheses | set class and local-domain behavior open |
| volume remains the same | determinant one, volume-form pullback, image-volume equality, or `MeasurePreserving` | exact root and implication directions open |
| infinitesimal Jacobian proof | mixed-partial cancellation and determinant evolution | source proof lead, not a checked finite-time proof |
| `已验证` | accepted source and kernel receipts would be required | no H or M credit |

## Lean discovery boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the discovery-only
probe elaborates generic gradient, smoothness, flow, volume, measure-preservation, and symplectic
matrix APIs. A bounded exact-topic search found no terminal declaration stating the Hamiltonian
Liouville volume theorem in pinned mathlib. Repository-local search found legacy file
`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_189.lean`, owned historically by `THM-M-1520`.
That file explicitly labels itself a statement boundary, supplies only generic/identity-model
wrappers and substrate, and sets its terminal-completion flags false. It is duplicate discovery
evidence, not an exact source-mapped theorem or proof for `THM-M-1375`. This is not the downstream
exhaustive external anchor audit and does not establish global absence.

Before leaving `H1`, accountable reviewers must select an immutable proposition and edition,
transcribe every incorporated definition, ordered binder, hypothesis and conclusion, audit proof
dependencies and corrections, reconcile duplicate ownership, and independently approve the mapping.
Only then may the statement phase freeze minimal imports, an elaborated expression and environment
fingerprint, checked transports, and the required statement mutations.
