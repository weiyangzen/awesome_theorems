# THM-M-0333 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the von Neumann double commutant
theorem. The repository supplies the title, John von Neumann, the year 1929, and only the gloss
"the double commutant of operator algebras". It does not give a formula, source edition, theorem
number, hypotheses, topology, or boundary conventions.

The standard theorem characterizes a unital self-adjoint operator algebra on a complex Hilbert
space by equality with its bicommutant and by closure in the strong or weak operator topology.
Those formulations require choices the received record does not make: whether the input is an
algebra or merely a set, whether identity and adjoint closure are hypotheses, which operator
topology is used, and whether equality or a closure identity is the conclusion. Selecting one
without a source crosswalk would substitute a more precise theorem for the repository record.

The intake freezes that ambiguity rather than claiming a canonical statement. The root remains
`[H1, M3, R3]`: the named classical theorem is identifiable, and pinned mathlib contains relevant
operator-algebra and weak-operator-topology interfaces, but its own module says the equivalence
still needs to be proved. The API probe is not the theorem or proof. Exact commands and results are
recorded in `validation.md`.
