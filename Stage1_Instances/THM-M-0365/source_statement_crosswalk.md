# Source-statement crosswalk

| Claim component | Repository or source anchor | Lean candidate | Intake assessment |
|---|---|---|---|
| Name | `Docs/researches/math_theorems.md`: "Tb theorem" | none | Names a theorem family, not a unique proposition |
| Repository wording | "singular integrals under nondegeneracy conditions" | none | Does not define "nondegeneracy," the operator, hypotheses, or conclusion |
| Attribution and date | Guy David / Jean-Lin Journe; 1985 | none | Metadata only; likely incomplete attribution and no pinpoint result |
| Historical discovery lead | G. David, J.-L. Journe, S. Semmes, *Operateurs de Calderon-Zygmund, fonctions para-accretives et interpolation*, Revista Matematica Iberoamericana 1 (1985), no. 4, pp. 1-56 | none | Plausible primary source family; edition hash, exact theorem/page, assumptions, and errata are not audited |
| Ambient domain | Not supplied | none | Euclidean versus spaces-of-homogeneous-type and homogeneous versus non-homogeneous settings remain open |
| Operator and kernel | Only "singular integrals" is supplied | none | Kernel size/smoothness, truncation, adjoint, weak boundedness, and initial domain remain unknown |
| Testing data | The name `Tb` suggests data involving `b` | none | One `b`, a dual pair, para-accretive data, or local test systems cannot be chosen from the name alone |
| Hypotheses | Described only as "nondegeneracy conditions" | none | Accretivity, para-accretivity, cancellation/BMO testing, and quantitative constants are not interchangeable |
| Conclusion | No mapping property or estimate is written | none | `L2` boundedness is a likely family-level conclusion but cannot be frozen as the repository root yet |
| Formal status | Manifest field `source_status_untrusted` is `已验证` | none | The label is discovery metadata, not human-source or kernel evidence |

The same short wording is projected into `Docs/Stage0_Blueprint.md`; that entry explicitly leaves
precise definitions, assumptions, proof path, equivalent formulations, axioms, and machine status
unfilled. It therefore adds no exact statement information.

The letter `b` alone is not a specification. Published results under the Tb name differ in whether
they use one or two testing functions, global or cube-local testing, accretive or para-accretive
data, doubling or non-doubling measures, and scalar or operator-valued kernels. A valid source
selection must bind an immutable primary source to its theorem/page, transcribe the exact ordered
quantifiers and constant dependencies, map every hypothesis, and record corrections or errata.
Only then can the statement phase choose a Lean expression and mutation-test its domains,
hypotheses, adjoint/testing conditions, and conclusion.

No `H0`, exact-statement, formal-anchor, or machine-closure claim is made.
