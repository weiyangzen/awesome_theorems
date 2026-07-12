# THM-M-0737 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the repository label "lower bounds
for Frege systems". The repository supplies only that gloss, attributes it to Alexander Razborov,
and gives the year 1985. It does not state a proposition or cite a source.

"Frege" is not enough to identify a lower-bound theorem. Unrestricted Frege, bounded-depth Frege,
and restricted variants have materially different lower-bound status, and a lower bound must also
fix a formula family, proof-size encoding, rate, and quantifiers. The supplied attribution and year
could also be a conflation with nearby circuit-complexity work; intake does not repair metadata by
silently selecting a different theorem.

The intake therefore freezes the ambiguity and exclusion boundary rather than inventing a claim.
The root remains `[H3, M4, R4]`. A pinned Lean probe confirms only that generic encodings, encoded
length, and asymptotic APIs elaborate; it is neither a Frege formalization nor a proof. Exact
commands and results are recorded in `validation.md`.
