# THM-M-0718 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the repository label "universal
Turing machine". The mathematical source inventory gives only "universal computation model",
attributes it to Alan Turing, and dates it to 1936. It does not state a quantified theorem or cite
an edition, section, or page.

Universality has several non-interchangeable formal meanings: one machine may interpret encodings
of other machines, a fixed evaluator may compute every partial recursive function after receiving
a program code, or a machine may simulate another machine step by step. These readings require
different machine models, encodings, partial semantics, and correctness relations. Selecting one
from the title alone would broaden or substitute the source claim.

The intake therefore freezes this ambiguity. The root remains `[H1, M3, R4]`. A pinned Lean probe
confirms that mathlib exposes partial-recursive codes, a TM2 interpreter, its initialization, exact
evaluation correspondence, and a finite-support theorem. This is a credible statement candidate,
not an accepted crosswalk or proof of the still-unfrozen target. Exact commands and results are in
`validation.md`.
