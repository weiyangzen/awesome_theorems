# THM-M-0703 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the repository label "type theory".
The source inventory supplies only the phrase "simple type theory", an attribution to Bertrand
Russell and Alonzo Church, and the year 1940. Simple type theory is a formal system or family of
systems, not by itself a proposition with hypotheses and a conclusion.

Several non-interchangeable targets fit the metadata: Church's 1940 formulation of simple type
theory, the simply typed lambda calculus, a classical higher-order logic based on simple types, or
a metatheorem such as type preservation, normalization, consistency, soundness, completeness, or
decidability of type checking. Choosing one would invent or substitute the theorem.

The intake therefore freezes that ambiguity and its exclusion boundary. The root remains
`[H3, M4, R4]`. A pinned Lean probe confirms that the environment exposes primitive type-forming
and equality-elimination operations suitable for later encodings; it is not a formalization of
simple type theory and receives no statement or proof credit. Exact validation commands and
results are recorded in `validation.md`.
