# THM-M-0628 rev-5.6 intake

This directory is the self-tested `planned` intake dossier for `局部紧性定理` (local
compactness theorem). The repository catalog supplies only the gloss `局部紧空间的性质`
("properties of locally compact spaces"), attributes it to many mathematicians in the twentieth
century, and labels it `已验证`. It gives no proposition, citation, definition convention,
assumptions, conclusion, proof, or formal artifact. The status label is untrusted discovery
metadata under rev-5.6.

The received wording names a topic family, not a truth-valued theorem. The intake therefore leaves
the canonical mathematical statement and Lean target null. It does not silently choose a compact
neighborhood characterization, a basis theorem, a product or subspace preservation theorem, a
regularity or Baire consequence, or a compactification result. Those choices have different
hypotheses and conclusions, and local compactness conventions can differ without separation
assumptions.

`IntakeProbe.lean` checks adjacent pinned mathlib interfaces for weak and strong local compactness,
compact neighborhoods, and the extra consequences available in an R1 space. These declarations
show that future formalization is feasible, but they do not select or prove the catalog target.

The provisional root vector is `[H5, M4, R4]`. Here `H5` classifies the received wording as an
unstable proposition; it does not claim that standard local-compactness results are false or open.
There is no accepted statement, proof state, source review, audit completion, theorem completion,
or master acceptance. The scope map and crosswalk record the retry boundary, while the task DAG
keeps every downstream phase open.
