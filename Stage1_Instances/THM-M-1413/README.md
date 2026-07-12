# THM-M-1413 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the repository label "Axiom A
system". The repository supplies only the gloss "axioms for hyperbolic systems", attributes the
item to Stephen Smale, and gives the year 1967. It supplies no primary-source locator, definition,
ordered hypotheses, or theorem-grade conclusion. The metadata label `已验证` is untrusted and
provides no human-source or machine-proof credit.

The historical referent is pinpointed in Stephen Smale's 1967 paper *Differentiable dynamical
systems*: item (6.1) on printed page 777 defines Axiom A for a diffeomorphism of a compact manifold
by hyperbolicity of its nonwandering set and density of its periodic points there. That source
confirms that "Axiom A" names a property, not a proved proposition. A nearby actual result about
such systems, the spectral decomposition theorem in item (6.2), is separately scheduled as
`THM-M-1414` and cannot be substituted here.

This intake therefore freezes that primary-source definition boundary and the decisions required to
redirect the item to a theorem-grade claim. It does not reclassify the definition as a theorem or
freeze a canonical Lean proposition. The root is provisionally `[H5, M4, R4]`: the received target
is not a stable theorem proposition; no exact formal artifact has been identified; and no proof
reconstruction exists. A pinned Lean probe checks only generic diffeomorphism, tangent-map,
omega-limit, periodic-point, and density interfaces. Those are feasibility surfaces, not an Axiom A
encoding or proof.

The lifecycle remains `planned`, all downstream tasks are open, and neither audit nor theorem
completion is claimed. Exact worker validation is recorded in `validation.md` and
`intake-receipt.json`.
