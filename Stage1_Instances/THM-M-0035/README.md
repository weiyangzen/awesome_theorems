# THM-M-0035 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the Jacobson density theorem. The
repository catalogue gives the Chinese gloss `本原环的稠密性定理` ("the density theorem for
primitive rings"), attributes it to Nathan Jacobson in 1945, and labels it `已验证`. Under rev-5.6
that label is untrusted metadata, not an exact statement, source audit, or proof receipt.

The gloss identifies a classical theorem family but omits the ring and module conventions, the
definition and handedness of a primitive ring, faithfulness and simplicity hypotheses, the
division ring of module endomorphisms, finite independence and interpolation quantifiers, and the
finite topology used by the word "dense." The identified 1945 publication metadata does not by
itself select or crosswalk a theorem passage.

Pinned mathlib contains a strong formal candidate, `jacobson_density`, and the finite-over-the-
endomorphism-ring corollary `Module.Finite.toModuleEnd_moduleEnd_surjective`. The first is stated
for a semisimple module and finite sets; the second is a surjectivity result under an additional
finiteness hypothesis. Neither is silently identified with the catalogue's primitive-ring gloss.
The intake probe authenticates their availability and reports their current axiom profiles; it
does not claim an exact source transport or root proof.

The provisional root vector is `[H1, M3, R4]`. The theorem family and a historical publication
lead are identified but no primary theorem passage is accepted; usable pinned formal candidates
exist but the canonical target is not frozen; and no source-faithful proof reconstruction exists.

`instance.json` is the structured scope authority. `scope-map.md` and
`source-statement-crosswalk.md` freeze the admissible family and non-substitution boundary.
`task-dag.json` keeps all six downstream phases open. Exact commands and results are in
`validation.md`. No H0, M0, R0, accepted proof state, audit completion, theorem completion, or
master acceptance is claimed.
