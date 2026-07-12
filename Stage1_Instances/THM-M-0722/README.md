# THM-M-0722 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for "Karp's 21 NP-complete problems".
The historical source is Richard M. Karp's 1972 chapter *Reducibility among Combinatorial
Problems*. Its main theorem says that all problems on the chapter's list are complete, using
Karp's definitions of polynomial completeness and reducibility.

The repository gloss, however, does not enumerate the list or choose modern encodings of the 21
decision problems. The source also groups names differently from many later accounts. The intake
therefore freezes the collective theorem and its source boundary, but leaves the exact 21-component
Lean proposition to the statement phase. Substituting a single familiar result such as SAT,
CLIQUE, or Hamiltonian cycle completeness is explicitly forbidden.

The provisional root is `[H1, M4, R4]`. A pinned Lean probe only confirms that basic language,
many-one reduction, graph coloring, clique, and Hamiltonian APIs elaborate. It is not the canonical
statement and receives no proof credit. No H0, M0, R0, audit completion, or theorem completion is
claimed.

