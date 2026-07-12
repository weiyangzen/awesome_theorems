# THM-M-0374 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the harmonic-analysis catalog label
"interpolation theorem." The repository gives only the plural gloss "various interpolation
theorems," a collective attribution, and the twentieth century. It does not identify one theorem.

Several inequivalent results fit that description: Riesz-Thorin strong-type interpolation,
Marcinkiewicz weak-to-strong interpolation, Hadamard's three-lines theorem, and real or complex
interpolation-space results. The catalog separately contains named Riesz-Thorin and Marcinkiewicz
targets, but that adjacency does not select a proposition for this generic record. Choosing one
would broaden or substitute for the source rather than freeze it.

The intake therefore freezes the ambiguity and exclusion boundary, not a Lean proposition. The
root remains `[H3, M4, R4]`. A pinned Lean API probe confirms that mathlib exposes `Lp`, `MemLp`,
continuous linear maps on `Lp`, and a checked Hadamard three-lines theorem. Those declarations are
encoding or discovery ingredients only; none is credited as this target. Exact commands and
results are recorded in `validation.md`.
