# THM-M-0370 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the repository label "weighted norm
inequality". The repository supplies only the gloss "A_p weights and operator boundedness",
Benjamin Muckenhoupt, and 1972. It does not identify an operator or state a proposition.

The metadata plausibly points toward Muckenhoupt's characterization of weights for which the
Hardy-Littlewood maximal operator satisfies a strong weighted `L^p` bound. It is not enough to
decide whether the intended result is that characterization, one direction of it, a weak endpoint,
or a weighted estimate for another operator. Choosing among them would substitute mathematics.

The intake freezes that ambiguity and the scope boundary. The provisional root is
`[H1, M4, R4]`: a classical source is plausibly identifiable, but its exact statement has not been
pinpoint-crosswalked; no formal target is selected. `IntakeProbe.lean` only verifies that pinned
mathlib exposes weighted measures and `L^p` seminorm ingredients. It is not a theorem or proof.
