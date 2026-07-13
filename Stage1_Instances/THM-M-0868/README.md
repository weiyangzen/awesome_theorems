# THM-M-0868 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the catalog item `图子式定理`
(`Graph Minor Theorem`). The repository supplies only the gloss `Wagner猜想的证明` ("proof of
Wagner's conjecture"), attributes it to Robertson and Seymour over 1983-2004, and carries an
untrusted `已验证` label. It does not state a binder-complete proposition or define a graph minor.

## Intake result

The publication identity of Robertson and Seymour's *Graph Minors. XX. Wagner's conjecture* was
confirmed from bibliographic services. A secondary abstract record describes the familiar result
that every infinite collection of finite graphs contains one member isomorphic to a minor of
another. The primary article text, however, was not available for proposition-level inspection in
this run. The exact graph conventions, minor definition, quantifier form, theorem locator, proof
boundary, and correction history therefore remain unaccepted.

The immediately preceding target `THM-M-0867`, `Robertson-Seymour图子式定理`, has the gloss
`图子式良拟序定理`. Those two catalog records appear to identify the same theorem family, but the
repository contains no accepted duplicate decision or scope distinction. This intake keeps both
IDs independent. It does not inherit source, statement, status, receipt, or proof credit from the
neighbor.

## Formal boundary

Pinned mathlib exposes finite-simple-graph deletion and isomorphism infrastructure and the generic
`WellQuasiOrdered` predicate. `IntakeProbe.lean` authenticates those interfaces. A bounded search
found no `SimpleGraph` edge-contraction or graph-minor relation and no Graph Minor Theorem
declaration. Mathlib's matroid minor order is a different theory and is not a substitute.

The provisional vector is `[H1, M4, R4]`: the published theorem family and primary-paper identity
are known, but exact source fidelity and duplicate ownership are unresolved; no usable exact Lean
artifact is credited; and no source-faithful proof reconstruction exists. The canonical human and
Lean statements remain null, all six downstream phases remain open, and no H0, M0, R0, accepted
execution state, audit completion, theorem completion, or master acceptance is claimed.
