# Source-statement crosswalk

Statement recheck base: `94009a6bebd743588e09c3b45bfbf18bf9b5c5e3` (2026-07-17).

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

## Statement-gate decision

No row above selects one exact root proposition. In particular, neither the repository metadata nor
an admitted immutable source resolves the base-field scope, Frobenius convention, extension
equivalence, classification boundary, inclusion reversal, tower functoriality, or degenerate cases.
The historical `S1_M_076.StatementShape` is therefore retained only as a candidate: it chooses some
of those fields, omits others, and cannot establish identity with the unresolved canonical claim.

Accordingly `statement.json` keeps the canonical human and Lean targets null. `Statement.lean`
checks only the pinned local-field/Galois/norm/open-subgroup API boundary and emits no target
declaration. The first failed gate is `S02-EXACT-TARGET.exact_source_statement_identity`; all four
required mutation classes remain honestly unrun until an exact target exists.
