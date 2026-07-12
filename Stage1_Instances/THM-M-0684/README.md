# THM-M-0684 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for Godel's second incompleteness
theorem. The repository source gives only the gloss "a system cannot prove its own consistency",
an attribution to Kurt Godel, and the year 1931. That gloss omits conditions that are part of the
theorem rather than incidental formalization choices.

In particular, "system" must be replaced by an exact effectively axiomatized theory with stated
arithmetic strength; "prove" needs an arithmetized proof predicate; and "consistency" needs a
specific internal sentence. The exact conclusion and its metatheory must also be fixed. Without
these restrictions the gloss is false for inconsistent systems and is not a unique proposition.

The intake therefore freezes the missing choices and the non-substitution boundary. The root is
provisionally `[H1, M4, R4]`: the historical theorem is established, but this repository has not
supplied the primary-source crosswalk needed for H0 or a formal target. A pinned Lean probe confirms
only that mathlib exposes first-order sentences, theories, and syntax encodings. Exact
commands and results are recorded in `validation.md`; no proof credit is claimed.
