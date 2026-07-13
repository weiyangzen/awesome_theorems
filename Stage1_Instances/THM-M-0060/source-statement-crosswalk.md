# THM-M-0060 source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:447-452` contains the complete catalog record:

- name: `史密斯标准形定理`;
- attribution: Henry John Stephen Smith;
- date: 1861;
- statement: `整数矩阵的等价标准形`;
- importance: high;
- formalization status: `已验证`.

All six lines originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. They include no
bibliography, displayed formula, dimensions, definition of equivalence, diagonal/divisibility
conditions, uniqueness clause, proof, or formal artifact. `Docs/Stage0_Blueprint.md:1753-1778`
repeats the gloss and explicitly leaves exact definitions and premises, proof route, equivalent
forms, axioms, logic dependencies, machine status, and artifact links open. Rev-5.6 therefore
resets the item to `L0 / rework_required`.

## Human-source lead

Henry John Stephen Smith, "XV. On systems of linear indeterminate equations and congruences,"
*Philosophical Transactions of the Royal Society of London* 151 (1861), pages 293-326,
DOI `10.1098/rstl.1861.0016`, is a primary historical lead matching the catalog author and year.
Crossref metadata and its supplied abstract were inspected on 2026-07-13. The abstract explicitly
introduces rectangular integral matrices, greatest minors, minor determinants, and matrix
relations used in systems of linear indeterminate equations.

This is not `H0`. The publisher PDF request returned HTTP 403 in this worker, so no immutable local
paper, exact theorem/page transcription, complete assumptions, proof-node map, correction/errata
audit, or independent review was admitted. The metadata response is a discovery record, not an
accepted proof source packet. These limitations support `H1` with an explicit open mapping list.

## Component crosswalk

| Catalog component | Candidate mathematical reading | Pinned Lean interface | Intake status |
|---|---|---|---|
| "integer matrix" | a rectangular `Matrix (Fin m) (Fin n) Int` | `Matrix`; `Matrix.toLin'` | dimensions/orientation not source-ratified |
| "equivalent" | invertible row/column changes or change of bases | `LinearMap.toMatrix`; bases and linear equivalences | relation not selected |
| "normal form" | rectangular diagonal entries, often with a divisibility chain and normalized associates | `Module.Basis.SmithNormalForm` | diagonal basis relation only; convention gap open |
| existence | every matrix admits such changes | `Submodule.exists_smith_normal_form_of_le`; `Submodule.smithNormalForm` | adjacent general-PID anchor; no root transport |
| uniqueness | invariant factors unique up to units or normalized signs | no credited declaration | catalog does not say whether included |
| Smith, 1861 | historical attribution | none | exact primary theorem/proof audit open |
| `已验证` | catalog status | none | no H/M/R credit |

## Pinned formal candidates

At mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, module
`Mathlib.LinearAlgebra.FreeModule.PID` defines `Module.Basis.SmithNormalForm`. Its fields are bases
for a module and submodule, an embedding between basis indices, coefficients, and the relation
`(bN i : M) = a i • bM (f i)`. The module overview says this equivalently represents an inclusion
or a linear map with the specified range by a diagonal matrix.

The same module proves `Submodule.exists_smith_normal_form_of_le` and constructs
`Submodule.smithNormalForm` under commutative-ring, domain, principal-ideal-ring, module, and finite
basis assumptions. `IntakeProbe.lean` authenticates these exact interfaces in the pinned
environment. The candidate is materially relevant and justifies `M3`, but it does not by itself
select the catalog proposition. In particular, the structure has no divisibility-chain,
associate-normalization, or uniqueness field, and no checked wrapper currently turns an arbitrary
rectangular integer matrix into this submodule-inclusion result and back.

`Mathlib.LinearAlgebra.Matrix.ToLin` supplies the matrix/linear-map interfaces needed for a possible
transport. `Mathlib.Algebra.Module.PID.equiv_free_prod_directSum` is a related PID module structure
theorem. Neither is credited as an exact root proof. A bounded repo-local and pinned-mathlib search
located no direct declaration whose checked type states the full left/right-unimodular integer
matrix theorem with a divisibility-normalized diagonal.

## Exactness gaps

The statement gate must admit a pinpoint source and fix matrix versus module scope, dimensions,
equivalence, diagonal shape, rank and zero conventions, divisibility, associate/sign normalization,
and existence versus uniqueness. It must then elaborate and fingerprint the exact Lean target,
check every matrix/module alternate encoding, and run all required mutation classes. The pinned
Smith APIs cannot close those gaps by name or proximity.
