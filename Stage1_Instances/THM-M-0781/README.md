# THM-M-0781 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the repository label "Cohen's
theorem". The repository gloss is `CH和AC独立于ZF` ("CH and AC are independent of ZF"). That
phrase names two independence results but does not specify the metatheory, the encoding of ZF, the
meaning of consistency, or the exact pair of relative-consistency implications.

The common mathematical reading cannot simply be inserted as the target. Independence of CH from
ZF normally has positive and negative halves, while the historical attribution and hypotheses of
those halves differ. Independence of AC from ZF is another two-sided claim. A formal statement must
also distinguish syntactic consistency from model existence and state any soundness or
metatheoretic assumptions. Those choices materially change the proposition.

The intake therefore freezes the literal claim and its unresolved scope rather than inventing a
canonical theorem. The root remains `[H3, M4, R4]`. A pinned Lean probe confirms that mathlib has
first-order theories and satisfiability, cardinal ingredients, and a ZFC model API. It neither
encodes ZF/CH/AC nor proves independence. Exact commands and results are in `validation.md`.
