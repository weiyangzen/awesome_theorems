# THM-M-0014 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the repository's field-theory
record of the Kronecker-Weber theorem. The literal catalog claim is that every finite abelian
extension of the rational field is contained in a cyclotomic field. The catalog supplies no
bibliography, definitions, proof, or formal artifact, and its `已验证` label is untrusted metadata.

The intake preserves the classical theorem family but does not silently choose an exact
presentation of a finite extension. In particular, it leaves open whether the source intends a
literal tower of subfields, an abstract finite extension with an embedding into a cyclotomic
field, or a number-field typeclass presentation. Those forms require a reviewed source decision
and checked transports before one may become the canonical Lean target.

The repository separately owns `THM-M-0419`, another Kronecker-Weber record with a legacy Lean
statement-shape artifact. That target and artifact are discovery inputs only: they confer no
statement, source, or proof credit on `THM-M-0014` and are not modified here.

Lifecycle is `planned`; the provisional root vector is `[H1, M4, R3]`. `IntakeProbe.lean` checks
only adjacent pinned number-field, abelian-Galois, cyclotomic-field, and algebra-embedding APIs.
No canonical Lean expression, accepted proof state, audit completion, theorem completion, or
master acceptance is claimed. The scope boundary, source crosswalk, open downstream DAG, and exact
self-test commands are recorded in the other dossier artifacts.
