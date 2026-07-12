# THM-M-0537 rev-5.6 intake

This directory is the fail-closed `planned` intake for the repository label "homology axioms."
The source gloss says only "axiomatization of homology theory" and is not itself a proposition.
The intended scope is the classical Eilenberg-Steenrod package for an ordinary homology theory on
topological pairs: functorial graded groups and connecting maps satisfying homotopy, exactness,
excision, and dimension, with the additivity convention still to be fixed from a primary source.

This intake does not manufacture a theorem out of that definition. The statement phase must choose
whether the credited root is (a) a structure expressing the axioms, (b) a model theorem showing
singular homology satisfies them, or (c) a uniqueness/representation result, and must justify that
choice against the source wording. Until then there is no canonical Lean expression. The
provisional root vector is `[H2, M4, R4]`; no statement, proof, audit, or theorem completion is
claimed.

The scope map, source crosswalk, and open task DAG record the exact ambiguity and downstream work.
Commands and results supporting this intake are in `validation.md`.
