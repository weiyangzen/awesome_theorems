# THM-M-1256 rev-5.6 intake

This directory is the fail-closed `planned` intake for the repository label "Hörmander theorem".
The repository narrows the intended family to solvability of constant-coefficient partial
differential equations and attributes it to Lars Hörmander in 1955. It does not supply a
bibliographic source or specify whether solvability is local or global, the function/distribution
spaces, the domain, or the exact conclusion. Those choices distinguish inequivalent statements.

Accordingly, this intake preserves the source wording but does not select a canonical human or
Lean statement. In particular it does not silently substitute the related Malgrange-Ehrenpreis
fundamental-solution theorem (`THM-M-1255`). The provisional root vector is `[H4, M4, R4]`; no
source fidelity, kernel closure, audit completion, or theorem completion is claimed.

`scope-map.md` records the admissible boundary, `source-statement-crosswalk.md` records every
available source field and unresolved formal choice, and `task-dag.json` opens the downstream
rev-5.6 work. Exact intake validation evidence is recorded in `validation.md`.
