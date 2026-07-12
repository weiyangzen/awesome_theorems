# THM-M-0340 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the repository label
"Banach-Tarski ball paradox". The source inventory gives only the gloss "the ball-splitting
theorem under the axiom of choice", the names Stefan Banach and Alfred Tarski, and the year 1924.
It does not identify an edition, theorem number, page, or exact proposition.

The familiar theorem has materially different formulations: a solid unit ball versus a sphere or
all of Euclidean three-space; two translated balls versus two congruent copies; piecewise rigid
motions versus rotations only; and a finite equidecomposition versus a five-piece refinement.
Those variants cannot be silently exchanged. In particular, the axiom of choice is proof
foundation, not ordinarily an explicit mathematical hypothesis on a ball.

The intake freezes that ambiguity and the exclusions rather than inventing a proposition. The root
remains `[H3, M4, R4]`. A pinned Lean probe confirms that mathlib exposes Euclidean space, metric
balls and spheres, isometries, and finite group-action equidecompositions. This is encoding
feasibility only, not a canonical statement or proof. Exact commands and results are recorded in
`validation.md`.

