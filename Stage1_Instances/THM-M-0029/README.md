# THM-M-0029 rev-5.6 intake

`THM-M-0029` is the repository's Nakayama lemma catalog item. The repository calls it a lemma
"about generators of modules", attributes it to Tadashi Nakayama in 1951, and labels it verified.
That label is untrusted metadata, not a source statement or proof receipt.

The wording identifies a classical theorem family but not one truth-valued proposition. Common
forms include the determinant-trick annihilator statement, vanishing under multiplication by an
ideal in the Jacobson radical, a local-ring maximal-ideal specialization, and lifting generators
from a quotient. They differ in binders, hypotheses, and conclusions. This planned intake records
the choices rather than silently selecting the most convenient pinned declaration.

Pinned mathlib contains several close forms in `Mathlib.RingTheory.Finiteness.Nakayama` and
`Mathlib.RingTheory.Nakayama`. `IntakeProbe.lean` authenticates their public interfaces under the
pinned toolchain. This is discovery-only evidence: the source-to-variant identity, canonical Lean
target, expression fingerprint, terminal proof-body provenance, and trust closure remain open.

The provisional root vector is `[H1, M3, R4]`. A known theorem family and source leads support only
`H1`; strong pinned interfaces support only `M3`; no readable proof reconstruction supports `R0`
through `R3`. Lifecycle remains `planned`, all six downstream tasks remain open, and no accepted
execution state, audit completion, theorem completion, or master acceptance is claimed.
