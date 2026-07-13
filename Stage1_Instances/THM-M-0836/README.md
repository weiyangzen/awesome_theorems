# THM-M-0836 rev-5.6 dossier

This directory is the fail-closed `planned` intake dossier for the catalog row named "computer
proof of the four-color theorem." Its complete gloss is "reducible configurations and the
discharging method for the four-color theorem." That wording names a proof architecture, not a
truth-valued proposition, and the repository deliberately catalogs the ordinary four-color theorem,
the later Robertson-Sanders-Seymour-Thomas proof, and Gonthier's Coq formalization as separate
targets.

The bibliographic trail confirms why the boundary matters. Appel and Haken's two-page 1976
announcement, *Every planar map is four colorable*, was inspected from an author-publisher PDF. It
states the ordinary map-coloring theorem and sketches how an unavoidable set of reducible
configurations, discharging, and computer programs compose to prove it. The detailed 1977 source is
a suite: Part I is *Discharging*, Part II is *Reducibility* and adds John Koch as an author, and
separate microfiche supplements carry computational material. Their metadata was inspected but
their primary text was not admitted. The announcement is a strong source-family lead, not `H0`:
the detailed definitions, exact configuration inventory, programs, certificates, proof map,
corrections, and independent review remain open.

Pinned mathlib supplies `SimpleGraph.Coloring`, `SimpleGraph.Colorable`, finite-graph degree APIs,
and the degree-sum formula. `IntakeProbe.lean` authenticates those adjacent interfaces. The same
pinned source explicitly lists planar graphs as future coloring work, and a bounded exact-topic
search found no Appel-Haken, four-color, reducible-configuration, or discharging-method declaration.
The probe does not define planarity, configurations, reducibility, discharging, a computation
certificate, or a canonical root, and receives no proof credit.

The provisional vector is `[H5, M4, R4]`. Here `H5` records that this catalog proof-method label is
not yet a stable proposition; it does not say that the four-color theorem is false or open. The
canonical statement and Lean target remain null, all six downstream tasks remain open, and no H0,
M0, R0, accepted proof state, audit completion, theorem completion, or master acceptance is
claimed. Only the integration lane may accept the self-tested worker proposal.
