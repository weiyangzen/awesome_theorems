# THM-M-0707 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the halting-problem
undecidability target. The repository claim says that no Turing machine decides, for every
machine and input, whether that computation halts. This identifies a standard theorem family,
but it does not yet fix a machine model, encoding, operational semantics, or the formal meaning
of a decider.

The statement phase now freezes that universal machine-and-input scope in mathlib's concrete,
denumerable `Nat.Partrec.Code` model: halting means that `Code.eval code input` has a defined
partial result, and deciding means a total Boolean indicator satisfying `ComputablePred`. This is
the standard computability-complete program-code formulation selected as the canonical claim, not
termination of one Lean program or unrestricted propositional decidability.

`Statement.lean` elaborates the exact target with the minimal direct import
`Mathlib.Computability.Halting`; `check_statement.py` distinguishes four altered claims and the
kernel checks terminating and divergent boundary cases. The statement is self-tested pending
master acceptance. The provisional human-source and readability debt remains open, and there is
no accepted proof state, audit completion, or theorem completion.
