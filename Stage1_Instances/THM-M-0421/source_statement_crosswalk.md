# Source-statement crosswalk

| Claim component | Human source candidate | Lean candidate | Intake assessment |
|---|---|---|---|
| Finite-level reciprocity and norm kernel | J.-P. Serre, *Local Fields*, Graduate Texts in Mathematics 67, Springer, Chapter XIV (local class field theory) | Legacy `S1_M_076.LocalReciprocityData` is only a data shape | Primary monograph candidate identified; edition-specific theorem/page, hypotheses, convention, errata, and immutable digest remain open (`H1`) |
| Existence/classification by norm subgroups | Serre, *Local Fields*, Chapter XIV; also J. Neukirch, *Algebraic Number Theory*, Chapter V, local class field theory sections | Legacy `S1_M_076.StatementShape` is not a proof and is not accepted | Crosswalk must distinguish existence, injectivity up to `K`-isomorphism, and inclusion reversal |
| Base-field scope | Standard formulations cover nonarchimedean local fields, with presentation varying by source | `IsNonarchimedeanLocalField` exists in pinned mathlib | Source-specific characteristic assumptions have not been pinned |
| Reciprocity normalization | Uniformizer maps to a Frobenius element in the unramified case | No accepted declaration | Arithmetic/geometric Frobenius convention must be fixed before exact statement credit |
| Topological condition | Norm groups are open and of finite index | `OpenSubgroup` and `Subgroup.FiniteIndex` appear in the legacy discovery module | No node-specific elaboration or source alignment has yet been checked |
| Functoriality | Reciprocity is compatible with norm/restriction in towers | No accepted declaration | Decide whether functoriality is part of the root characterization or a required proof obligation |

The upstream research note supplies only the Chinese phrases “local class field theory” and
“abelian extensions of local fields,” plus an untrusted “verified” label. It is not enough for H0.
The cited books are discovery anchors, not accepted source receipts. A later source audit must pin
an edition, exact theorem locations, all assumptions and normalizations, errata status, and hashes.
