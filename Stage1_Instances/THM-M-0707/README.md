# THM-M-0707 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the halting-problem
undecidability target. The repository claim says that no Turing machine decides, for every
machine and input, whether that computation halts. This identifies a standard theorem family,
but it does not yet fix a machine model, encoding, operational semantics, or the formal meaning
of a decider.

The intake preserves that universal machine-and-input scope. It does not substitute termination
of one Lean program, undecidability for partial-recursive codes without a checked equivalence, or
a generic diagonal proposition that assumes its own interpreter. The next phase must select an
immutable source formulation and elaborate the corresponding Lean target.

The provisional root vector is `[H1, M4, R3]`. A narrow pinned Lean probe confirms that mathlib
provides codes for partial recursive functions, their universal partial evaluator, computability,
and the `S_n^m` theorem. These are candidate interfaces only, not the requested theorem or proof.
There is no accepted proof state, audit completion, or theorem completion.
