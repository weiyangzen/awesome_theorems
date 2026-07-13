# THM-M-0745 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the recursion-theory catalog item
`递归枚举集` (recursively enumerable sets). The repository supplies only the gloss
`递归可枚举集的性质` ("properties of recursively enumerable sets"), attributes it to many
mathematicians in the twentieth century, and labels it `已验证`. Under rev-5.6 that label is
untrusted metadata, not human-source or machine-proof evidence.

The gloss names a subject, not a truth-valued proposition. It does not choose a definition or
characterization of computable enumerability, a closure property, an example, a completeness
result, or a relationship with decidability. These choices have different binders, hypotheses,
and conclusions. Several are also separately owned by neighboring targets, including the halting
problem, creative and simple sets, Post's problem, computably enumerable degrees, and MRDP.

The canonical mathematical statement and Lean target therefore remain null. `IntakeProbe.lean`
checks adjacent pinned mathlib interfaces for `REPred`, partial-recursive domains, computable
predicates, the r.e./co-r.e. characterization, and the halting example. Their differing types make
the ambiguity concrete; the probe neither selects nor proves this target.

The provisional root vector is `[H5, M4, R4]`. Here `H5` classifies the received wording as an
unstable proposition; it does not say that standard theorems about recursively enumerable sets are
false or open. All six downstream tasks remain open. No accepted statement, proof state, audit
completion, theorem completion, or master acceptance is claimed.
