# THM-M-0202 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the repository item
`婆罗摩笈多公式` (Brahmagupta's formula). The catalog supplies only the gloss
`圆内接四边形面积公式` ("area formula for a cyclic quadrilateral"), attributes it to
Brahmagupta in 628, and labels it `已验证`. Those fields identify a familiar theorem family, but
they are untrusted inventory metadata rather than an exact mathematical statement, source
crosswalk, or machine-proof receipt.

The conventional family relates the nonnegative area `K` of a cyclic quadrilateral with side
lengths `a`, `b`, `c`, and `d` and semiperimeter `s = (a + b + c + d) / 2` by
`K = sqrt ((s-a)(s-b)(s-c)(s-d))`. Intake records that formula only as a scope lead. The repository
does not define the quadrilateral, cyclic boundary order, convexity, area, sides, semiperimeter,
nondegeneracy, equality orientation, square-root-versus-squared form, or boundary cases, so choosing
any one of those encodings here would silently change the proposition.

Two inspected secondary web sources corroborate the conventional formula and historical family.
MathWorld states the four-factor formula as the cyclic specialization of the general
quadrilateral formula. MacTutor associates the area formula with the 628
*Brahmasphutasiddhanta* but reports a material historical ambiguity: the source does not explicitly
restrict the rule to cyclic quadrilaterals. These mutable secondary pages are discovery leads, not
H0 evidence; they strengthen the reason not to invent a source-faithful premise at intake.

A bounded search of repo-local Lean and pinned mathlib found no declaration or module for
Brahmagupta's cyclic-quadrilateral area formula. Pinned mathlib does expose adjacent exact geometry
interfaces for `Cospherical`, `Concyclic`, cyclic-quadrilateral angle relations, Euclidean triangle
identities, and `Real.sqrt`; the discovery-only Lean probe checks those APIs. They are generic
substrate, not a Brahmagupta statement, reduction, proof, or machine-completion candidate.

The provisional vector is `[H1, M4, R4]`: a classical proved family is credibly identified, but no
immutable pinpoint human source and complete source-to-statement mapping has been independently
accepted; no target-specific formal artifact was located; and no source-faithful reviewed proof
reconstruction exists. `instance.json` is the structured scope authority and `task-dag.json` keeps
all six downstream phases open.

No canonical mathematical or Lean proposition, accepted source or proof body, H0, M0, R0,
accepted execution state, audit completion, theorem completion, or master acceptance is claimed.
