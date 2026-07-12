# THM-M-0716 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the repository label
`递归函数` ("recursive functions"). The only supplied claim is `原始递归函数与部分递归函数`
("primitive recursive functions and partial recursive functions"). That phrase names two classes
of functions, but supplies no relation between them and therefore is not a proposition.

Several materially different statements fit the phrase: primitive recursive total functions embed
into computable functions; their coercions are partial recursive; partial recursive functions are
closed under unbounded minimization; or the primitive recursive functions form a proper subclass
of a larger computability class. Choosing one would substitute invented mathematics for the source.

The intake freezes this ambiguity and its exclusion boundary. The root remains `[H3, M4, R4]`.
A pinned Lean probe confirms that mathlib exposes the relevant predicates and the bridge
`Primrec.to_comp`; this is API evidence only, not the canonical statement or a proof of the target.
Exact validation commands and results are recorded in `validation.md`.
