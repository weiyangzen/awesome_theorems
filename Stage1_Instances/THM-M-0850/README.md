# THM-M-0850 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the catalog item "giant-component
theorem." The repository supplies only the gloss "the appearance of a giant component in a random
graph," attributes it to Erdos and Renyi in 1960, and labels it `已验证`. It does not identify a
random-graph law, a proposition-level source locator, ordered asymptotic quantifiers, hypotheses,
or a quantitative conclusion. The status label is explicitly untrusted and supplies no source or
proof credit.

Several inequivalent results fit that gloss: a supercritical existence theorem, existence plus
uniqueness and an asymptotic density, a paired subcritical/supercritical phase-transition theorem,
or a critical-window result. The historical uniform fixed-edge process and the modern binomial
`G(n,p)` law also require a checked mathematical crosswalk. Selecting one from mathematical
folklore would substitute a convenient theorem for the unresolved catalog target.

The intake therefore freezes the ambiguity, relevant scope, a historical source candidate, the
available Lean substrate, and the downstream work. It deliberately leaves the canonical human
statement and Lean target null. The provisional root vector is `[H5, M4, R4]`. Here `H5`
classifies only the supplied catalog wording as not yet a stable truth-valued proposition; it does
not refute or declare open the published giant-component results. No exact formal artifact is
identified, and no readable proof reconstruction exists.

Pinned mathlib exposes the independent-edge distribution `SimpleGraph.binomialRandom` and finite
connected-component vocabulary. The checked `IntakeProbe.lean` establishes only that these
encoding ingredients are available. It states and proves no giant-component theorem. The
near-duplicate catalog target `THM-M-1114` and neighboring random-graph targets remain separate and
supply no inherited evidence. All six downstream tasks remain open in `task-dag.json`; no accepted
proof state, audit completion, theorem completion, or master acceptance is claimed.
