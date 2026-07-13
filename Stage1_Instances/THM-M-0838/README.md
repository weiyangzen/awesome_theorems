# THM-M-0838 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for `Gonthier的形式化证明`, catalogued
as `四色定理的Coq形式化` (Gonthier's Coq formalization of the Four Color Theorem). The title
names a proof artifact rather than one binder-complete proposition, and the catalog's `已验证`
value is untrusted inventory metadata under rev-5.6.

An immutable historical source mirror exposes Gonthier's final Coq declaration `four_color`:
for every map over an abstract real model, `simple_map m` implies `map_colorable 4 m`. Its
definitions model maps as relations on real-plane points, require properness plus open connected
regions, and express coloring through a second map with at most four regions. The maintained Rocq
community source preserves the same final mathematical boundary with declarations
`four_color_finite` and `four_color`.

This source discovery identifies the likely mathematical root, but it does not settle whether this
provenance-specific catalog item should own that proposition, a claim about the Coq artifact's
kernel closure, or a combined formalization/provenance assertion. The generic Four Color Theorem
already has separate target `THM-M-0833`. The Appel-Haken and Robertson-Sanders-Seymour-Thomas
proofs have separate targets `THM-M-0836` and `THM-M-0837`. Intake therefore records the root
decision and neighbor boundaries instead of silently duplicating or broadening one of them.

Pinned mathlib provides simple-graph coloring APIs but no matching real-plane map interface or
planarity bridge; its coloring module lists planar graphs as future work. `IntakeProbe.lean`
authenticates only `Coloring`, `Colorable`, the chromatic-number equivalence, and a parameterized
graph schema. It declares no theorem and gives no Four Color proof credit.

The provisional target vector is `[H5, M4, R4]`. `H5` classifies the received artifact label as not
yet one stable truth-valued proposition; it does not refute the Four Color Theorem or Gonthier's
work. No exact Lean target, accepted upstream kernel evidence, or source-faithful reconstruction is
credited. All six downstream phases remain open. No H0, M0, R0, accepted execution state, audit
completion, theorem completion, or master acceptance is claimed.
