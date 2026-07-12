# THM-M-0852 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the catalog item "Hamilton-cycle
threshold." The repository supplies only the gloss "existence of Hamiltonian cycles in random
graphs," attributes the topic to many mathematicians in the twentieth century, and labels it
`已验证`. It does not identify a probability model, a threshold theorem, ordered asymptotic
quantifiers, hypotheses, or a conclusion. The status label is explicitly untrusted and supplies no
source or proof credit.

Several inequivalent results fit that gloss: a one-sided high-probability bound in `G(n,p)`, a
sharp threshold or critical-window limit law, a result in the fixed-edge model `G(n,m)`, and a
hitting-time theorem in the random graph process. Selecting one from mathematical folklore would
substitute a convenient theorem for an unresolved catalog target.

The intake therefore freezes the ambiguity, relevant mathematical scope, source candidates, Lean
substrate, and downstream work. It deliberately leaves the canonical human statement and Lean
target null. The provisional root vector is `[H5, M4, R4]`. `H5` classifies only the supplied
catalog wording as not yet a stable truth-valued proposition; it does not refute or declare open
the published random-graph Hamiltonicity results. No exact formal artifact is identified, and no
readable proof reconstruction exists.

Pinned mathlib exposes both the independent-edge distribution `SimpleGraph.binomialRandom` and the
predicate `SimpleGraph.IsHamiltonian`. The checked `IntakeProbe.lean` establishes only that these
encoding ingredients are available. It states and proves no threshold theorem. All six downstream
tasks remain open in `task-dag.json`; no accepted proof state, audit completion, theorem completion,
or master acceptance is claimed.
