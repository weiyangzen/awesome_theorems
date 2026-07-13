# THM-M-0039 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the catalogue item called the
Kaplansky theorem. The repository supplies only the Chinese gloss `关于PI环的结构` ("the structure
of PI rings"), attributes it to Irving Kaplansky, dates it 1958, and labels it `已验证`. Under
rev-5.6 those fields are untrusted metadata, not an exact source statement, source audit, Lean
target, or proof receipt.

An inspected primary paper gives a strong source lead: Irving Kaplansky, *Rings with a polynomial
identity*, *Bulletin of the American Mathematical Society* 54 (1948), 575-580, DOI
`10.1090/S0002-9904-1948-09049-8`. Its Theorem 1 says that a primitive algebra satisfying a
polynomial identity is finite-dimensional over its center. This matches the gloss well, but the
catalogue year differs by ten years and the paper contains several other PI-ring results. The
intake therefore records the theorem as a candidate and does not silently correct or select it.

The source also leaves proposition-changing formalization choices to resolve: algebra versus the
ring extension in section 4(c), unitality, the definition and handedness of primitive, the base
field and center-as-field encoding, the noncommutative polynomial-identity witness, and all ordered
binders and boundary cases. A later statement phase must obtain source/scope review and freeze one
exact choice before constructing a canonical Lean expression.

Pinned mathlib supplies adjacent infrastructure for free noncommutative algebras, simple modules,
Jacobson density, simple-ring centers, module finiteness, and finite simple-algebra matrix
decomposition. It does not supply a polynomial-identity predicate or a declaration connecting a
primitive PI algebra to finiteness over its center. `IntakeProbe.lean` authenticates only those
interfaces and claims no target theorem or proof body.

The provisional theorem-family vector is `[H1, M3, R4]`: an inspected primary source lead exists
but its identity and premise mapping are not accepted; supporting Lean interfaces exist but neither
the exact statement nor the decisive PI-to-finiteness implication is formalized; and no
source-faithful readable proof reconstruction exists.

`instance.json` is the structured intake authority. `scope-map.md` and
`source-statement-crosswalk.md` freeze the interpretation and non-substitution boundaries.
`task-dag.json` keeps all six downstream phases open, and `validation.md` records exact worker
checks. No H0, M0, R0, accepted proof state, audit completion, theorem completion, or master
acceptance is claimed.
