# THM-M-0892 rev-5.6 intake

`THM-M-0892` is the graph-theory catalog item "Hoffman-Singleton theorem." The
repository attributes it to Alan Hoffman and Robert Singleton in 1960 and gives only the gloss
"existence of Moore graphs" plus an untrusted `verified` label. Those fields identify a result
family but not one proposition with fixed parameters, binders, and conclusion.

## Intake result

This directory is a fail-closed `planned` dossier. The 1960 bibliographic match is Hoffman and
Singleton, *On Moore Graphs with Diameters 2 and 3*. Later literature describes several closely
related but non-interchangeable claims: existence and uniqueness of the 50-vertex degree-7
diameter-2 Moore graph, the restriction of diameter-2 Moore-graph degrees to `2`, `3`, `7`, or
possibly `57`, and the still-open existence question at degree `57`. The catalog's bare existence
gloss neither fixes a degree nor says whether it requests the explicit Hoffman-Singleton graph,
the degree classification, uniqueness, or a conjunction.

The primary article's bibliographic metadata was checked, but a lawful complete article text,
numbered result, incorporated definitions, proof boundary, corrections, and independent source
review were not available at intake. A modern construction paper confirms that the
Hoffman-Singleton graph is the unique strongly regular graph with parameters `(50, 7, 0, 1)`;
that is a useful discriminator, not authority to rewrite the received target.

## Formal boundary

`IntakeProbe.lean` elaborates pinned finite simple-graph, regularity, diameter, girth, and strongly
regular graph APIs. A bounded exact-topic search found no Hoffman-Singleton or Moore-graph target
declaration in repo-local Lean or pinned mathlib. These are intake observations only, not the
downstream immutable anchor audit.

The canonical mathematical statement and Lean expression remain null. The provisional vector is
`[H1, M4, R4]`: a credible primary source family is known but its exact root and complete mapping
are not accepted; no exact formal artifact is credited; and no source-faithful reconstruction can
attach to an unfrozen root. All six downstream tasks remain open. No accepted execution state,
audit completion, theorem completion, or master acceptance is claimed.
