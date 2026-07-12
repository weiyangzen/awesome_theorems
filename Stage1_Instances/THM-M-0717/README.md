# THM-M-0717 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the repository label "Turing
machine". The source inventory gives only the gloss "the computational model of a Turing
machine". That identifies a mathematical object, not a theorem with binders, hypotheses, and a
conclusion.

The intake therefore freezes a topic boundary rather than inventing a proposition. Plausible later
targets include the definition and deterministic operational semantics of a machine, a simulation
theorem between machine variants, or a theorem characterizing Turing-computable functions. These
are not interchangeable. The neighboring manifest target `THM-M-0718` separately owns the
universal-machine claim, and the halting problem and model-equivalence claims are separate source
records, so none is silently substituted here.

Pinned mathlib does contain concrete `TM0`, `TM1`, `TM2`, and finite bundled `TM2` interfaces. The
bounded Lean probe checks representative types from that API; it supplies encoding feasibility
only, not a canonical theorem or proof. The root remains `[H3, M4, R4]`. Exact commands and results
are recorded in `validation.md`.
