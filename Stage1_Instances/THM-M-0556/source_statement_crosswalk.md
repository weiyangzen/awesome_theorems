# Source-statement crosswalk

The repository source record says only `纤维化的谱序列` ("the spectral
sequence of a fibration"). The table maps that wording to historically relevant
primary sources without treating a citation as an exact-statement audit.

| Claim component | Human source anchor | Lean target at intake | Assessment |
|---|---|---|---|
| Spectral sequence associated to a fibre space | J.-P. Serre, *Homologie singuliere des espaces fibres. Applications*, Annals of Mathematics 54 (1951), 425-505 | None selected | Primary historical source identified; theorem/page, hypotheses, notation, and errata require direct edition audit |
| General filtered-complex spectral-sequence method underlying the construction | J. Leray, *L'anneau spectral et l'anneau filtre d'homologie d'un espace localement compact et d'une application continue*, Journal de mathematiques pures et appliquees 29 (1950), 1-139 | Future construction node only | Genealogical source, not evidence that its general theorem is identical to the fibration claim |
| Early page | Common modern homological form has fibre homology with a base local system; a constant-coefficient tensor formula needs extra hypotheses | Unselected expression | The generated phrase omits coefficients, monodromy, indexing, and hypotheses; no formula is frozen |
| Abutment | A filtration of total-space homology/cohomology under stated convergence conditions | Unselected expression | Target and convergence semantics are absent from the source phrase |
| Naturality and products | Standard extensions/refinements in modern treatments | Not in the frozen root | Must not be inserted into the root without a source decision |

This crosswalk deliberately does not conflate the Leray spectral sequence of a
general map, the Serre spectral sequence of a fibration, and any one modern
Leray-Serre convention. The statement phase must select a primary-source-backed
formulation and then freeze all ordered binders, universes, hypotheses,
differentials, page conventions, and convergence data before searching for
proof closure.

Source locators for discovery, not immutable evidence receipts:

- Serre bibliographic record: Ann. of Math. (2), volume 54 (1951), pages 425-505.
- Leray bibliographic record: J. Math. Pures Appl. (9), volume 29 (1950), pages 1-139.

No `H0` claim is made. `H1` records that a classical proof source is identified
while exact statement/premise mapping, edition hashes, translation issues,
errata/corrections, and independent review remain outstanding.
