# THM-M-0521 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the repository label "Kolyvagin's
theorem". The only repository gloss is "BSD for elliptic curves of rank 0 or 1". That phrase does
not determine a theorem: it does not say whether "rank" is algebraic or analytic, what BSD
conclusions are intended, or which modularity, Heegner, conductor, and analytic hypotheses apply.

The commonly cited Kolyvagin/Gross-Zagier consequences run in the other direction from one
possible literal reading of the gloss: analytic rank at most one, under the appropriate hypotheses,
implies the corresponding Mordell-Weil rank and finiteness of the Tate-Shafarevich group. Merely
assuming algebraic rank zero or one is not an interchangeable hypothesis. The nearby repository
entry `THM-M-0522` also labels a Kolyvagin-Gross-Zagier theorem, so adjacency cannot resolve which
result this target intends.

This intake freezes that ambiguity and the exclusion boundary rather than inventing a proposition.
The root remains `[H3, M4, R4]`. A pinned Lean probe confirms that mathlib supplies Weierstrass
elliptic curves, projective points, generic L-series derivatives, and a Dedekind-domain Selmer group.
These are partial encoding ingredients, not the arithmetic BSD statement or a proof. Exact commands
and results are recorded in `validation.md`.
