# THM-M-1600 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the catalog item `零知识证明`
(`zero-knowledge proofs`). The repository supplies only the gloss `不泄露信息的证明`, attributes it to
Goldwasser, Micali, and Rackoff in 1985, and labels it verified. Those fields identify a subject
and an intuition, not a truth-valued proposition with ordered binders, hypotheses, and a conclusion.

## Intake result

The author-hosted journal version of Goldwasser, Micali, and Rackoff's *The Knowledge Complexity of
Interactive Proof Systems* was inspected as a primary source-family lead. It makes the ambiguity
concrete. Section 3.3 defines perfect, statistical, and computational zero knowledge for an
interactive protocol against every probabilistic polynomial-time verifier with auxiliary input.
The same paper then proves different existence results: Theorem 1 gives a perfectly zero-knowledge
proof system for quadratic residuosity, while Theorem 2 gives a statistically zero-knowledge proof
system for quadratic nonresiduosity.

The catalog does not select the definition, either theorem, or a later general existence theorem.
It also does not fix the language, protocol, verifier model, simulator, auxiliary input, completeness
and soundness convention, indistinguishability notion, security parameter, or boundary cases.
Intake therefore does not silently substitute the adjacent GMR-definition or GMW/3-color targets.

## Status boundary

The provisional vector is `[H5, M4, R4]`. `H5` classifies only the received catalog slogan as not
yet a stable proposition; it does not dispute the published GMR definitions or theorems. `M4`
records that no usable exact formal artifact is credited for an unselected root. `R4` records that
no source-faithful reconstruction can attach to an unspecified conclusion.

`IntakeProbe.lean` authenticates only generic pinned language, polynomial-time computation,
probability-mass, and superpolynomial-decay APIs. It contains no zero-knowledge definition, target
theorem, or proof body. `instance.json` is the structured scope authority, and `task-dag.json` keeps
all six downstream phases open. No canonical proposition, `H0`, `M0`, `R0`, accepted execution
state, audit completion, theorem completion, or master acceptance is claimed.
