# THM-M-0257 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the catalog item
`阿尔福斯-贝尔斯定理` (Ahlfors-Bers theorem). The repository attributes it to Lars Ahlfors and
Lipman Bers, dates it to 1960, and supplies only the gloss `泰希米勒空间的复结构` (the complex
structure of Teichmuller space). The `已验证` label is untrusted metadata under rev-5.6 and gives
no source or Lean proof credit.

The name, authors, date, and gloss identify a historically established theorem family but not one
binder-complete proposition. The joint 1960 Ahlfors-Bers paper *Riemann's Mapping Theorem for
Variable Metrics* is a strong bibliographic lead. However, modern usage applies the theorem name
both to existence and uniqueness of normalized solutions of the Beltrami equation and to their
holomorphic dependence on the coefficient. The literal complex-structure gloss also points toward
same-era results of Ahlfors and Bers about finite-type Teichmuller spaces, complex-analytic
structures, and bounded-domain embeddings. These statements are related, not interchangeable.

The catalog fixes neither the surface type nor the Teichmuller-space model, marking and equivalence
relation, Beltrami coefficient space, normalization, chart or quotient construction, dimension,
nor the precise complex-analytic conclusion. Selecting one familiar formulation at intake would
invent or substitute proposition-changing mathematics. The canonical mathematical statement and
Lean target therefore remain null.

The provisional vector is `[H1, M4, R4]`: matching primary bibliographic leads exist, but exact
source selection, assumption and correction mapping, and independent review remain open; no exact
usable formal artifact is credited; and no source-faithful reconstruction can attach to an
unfrozen root. `IntakeProbe.lean` elaborates only adjacent pinned APIs. All six downstream phases
remain open in `task-dag.json`. No H0, M0, R0, accepted execution state, audit completion, theorem
completion, accepted receipt, or master acceptance is claimed.
