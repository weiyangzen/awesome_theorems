# THM-M-1069 rev-5.6 intake

This directory is the `planned` intake for the Skorokhod problem. The repository gloss,
"reflected stochastic differential equation," does not determine a unique theorem: the name may
refer to the deterministic reflection problem, to existence and uniqueness for a reflected SDE,
or to multidimensional reflection in a specified domain. This intake therefore freezes that
ambiguity rather than silently selecting an easier statement.

The leading scope candidate is the classical one-dimensional Skorokhod reflection problem on the
nonnegative half-line. Its solution is a constrained path together with a minimal nondecreasing
regulator. A source audit must decide whether that deterministic theorem is the intended root or a
lemma inside a source-backed reflected-SDE theorem before the statement phase can freeze binders.

The manifest's `已验证` label is untrusted metadata and supplies no human-proof or machine-proof
credit. No canonical Lean expression or proof is claimed. The provisional root vector is
`[H3, M4, R4]`; audit and theorem completion are false. The open downstream phases and the first
statement blocker are recorded in `task-dag.json`, and exact intake checks are in `validation.md`.
