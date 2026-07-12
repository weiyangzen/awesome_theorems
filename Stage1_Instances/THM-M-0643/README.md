# THM-M-0643 rev-5.6 intake

This directory is the self-tested `planned` intake dossier for the catalog item `Wecken定理`
(Wecken theorem). The repository supplies only the gloss `不动点类的Nielsen数` ("the Nielsen
number of fixed-point classes"), attribution to Franz Wecken, and the year 1942. That wording names
an invariant and a theorem family, but it is not a truth-valued, binder-complete proposition.

The intake therefore does not silently choose the familiar minimum-realization form `MF[f] = N(f)`
or one of its dimension-, manifold-, polyhedron-, boundary-, or surface-specific variants. It also
does not turn the definition of the Nielsen number, its homotopy lower bound, or its invariance into
the requested realization theorem. Those choices have different domains and proof obligations.

The primary bibliographic leads are Franz Wecken's three *Fixpunktklassen* papers in
*Mathematische Annalen*: volume 117 (1940), pages 659-671, DOI `10.1007/BF01450034`; and volume
118 (1941), pages 216-234 and 544-577, DOIs `10.1007/BF01487362` and
`10.1007/BF01487386`. Their publisher metadata conflicts with the catalog's 1942 date. No exact
proposition, incorporated definitions, assumptions, proof boundary, or correction history from
these papers has yet been admitted and independently crosswalked, so they are source leads rather
than `H0` evidence.

`IntakeProbe.lean` checks adjacent pinned fixed-point and homotopy APIs. A bounded repo-local and
mathlib search found no relevant Wecken, Nielsen-number, or fixed-point-class declaration. The
probe and search are discovery observations only, not a downstream anchor audit or a proof.

The provisional vector is `[H1, M4, R4]`: published primary leads are named but their exact theorem
mapping remains open; no usable exact formal artifact has been located; and no source-faithful
readable proof can attach to an unfrozen root. All six downstream tasks remain open. No accepted
proof state, audit completion, theorem completion, or master acceptance is claimed.
