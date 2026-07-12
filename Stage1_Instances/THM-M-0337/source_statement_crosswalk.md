# Source-statement crosswalk

| Source component | Repository evidence | Possible formal counterpart | Intake assessment |
|---|---|---|---|
| Name | `THM-M-0337`, `康内斯循环上同调` | A definition of cyclic cochains, cocycles, or cohomology groups | A mathematical theory or object name is not a proposition |
| Gloss | Stage0: `非交换几何的上同调` | A construction on an associative algebra | It does not identify the algebra category, coefficients, cochain convention, or a theorem |
| Type | Stage0 labels the entry `数学定理 / 命题` | A proposition-valued Lean expression | The label conflicts with the proposition-free content and cannot supply missing binders or a conclusion |
| Status | Stage0/manifest: `已验证`; the manifest explicitly marks it untrusted | No formal declaration follows from this label | No human- or machine-proof credit |
| Date and attribution | Stage0 says 1985 and Alain Connes | Historical subject metadata | No edition, theorem number, page, assumptions, or errata disposition |
| Claimed result | Absent | Definition, bicomplex equivalence, SBI exact sequence, Morita invariance, periodicity, or K-theory pairing | Selecting any one would broaden or substitute the target |

## Statement boundary

Several inequivalent theories are commonly discussed under this label: ordinary cyclic
cohomology, periodic cyclic cohomology, entire cyclic cohomology, and variants for topological or
bornological algebras. Even after choosing one, a theorem still needs a class of algebras, a base
ring or field, coefficient data, ordered assumptions, and a conclusion. The intake therefore does
not promote background definitions or a familiar theorem family into the canonical claim.

Before statement elaboration, an authoritative source amendment or reviewed scope decision must
provide all of:

1. one proposition, not merely the name or definition of a theory;
2. the precise cyclic theory and cochain convention;
3. the category of algebras, scalar and coefficient data, and all regularity or topology assumptions;
4. ordered quantifiers, hypotheses, conclusion, and excluded boundary cases;
5. a primary-source edition with theorem/page anchor, assumptions, and errata disposition.

Until then, source fidelity is `H5`, exact Lean encoding is `M4`, and there is no eligible proof
root. No primary-source theorem or external formalization candidate is asserted by this intake.
