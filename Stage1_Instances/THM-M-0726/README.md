# THM-M-0726 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the repository label
"probabilistic complexity classes". The source record says only "BPP, RP, ZPP, and other
classes". This is a list of topics, not a proposition with ordered binders, hypotheses, and a
conclusion. The manifest's historical `verified` label is explicitly untrusted.

The intake freezes that ambiguity instead of turning a definition or a familiar inclusion into a
substitute theorem. BPP, RP, coRP, and ZPP depend on choices of computation model, randomness
source, input encoding, running-time convention, error thresholds, and worst-case or expected-time
semantics. Even after those choices are fixed, definitions, closure properties, containments, and
derandomization results are different possible roots.

The root remains `[H5, M4, R4]`: the recorded topic is not a stable theorem, no exact formal target
has been selected, and no readable proof route exists. A pinned Lean probe confirms only that
mathlib exposes languages, polynomial-time deterministic computation, and discrete probability
mass functions that could be ingredients of a future encoding. It is not a definition or theorem
about BPP, RP, or ZPP. Exact commands and results are recorded in `validation.md`.

## Open task DAG

All dependent phases remain open in `task-dag.json`. The first blocker is an accountable selection
and independent inspection of one immutable exact source proposition, including the randomized
machine model, encoding, random-bit semantics, time bound, error convention, quantifier order, and
conclusion. This intake supplies no `H0`, `M0`, or `R0` credit, no audit completion, and no theorem
completion.
