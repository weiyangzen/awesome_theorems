# Full study — the AGP lower bound for Carmichael numbers

Let `C(x)` be the number of natural numbers `n ≤ x` satisfying Lean's
`Nat.IsCarmichael`.  The frozen theorem says that eventually, along the real
filter `atTop`,

`C(x) > x^(2/7)`.

The quantifier is an eventual statement: there is a real threshold after
which the strict inequality holds.  The exponent is a real quotient, not
natural-number division.  Those two details are semantic obligations rather
than typographic conveniences; changing either would produce a different
theorem.

This target packages an exact formal transport of the pinned AGP declaration.
It does not restate the historical analytic-number-theory argument as though
prose were kernel evidence.  Instead, the proof DAG distinguishes source
provenance, elaborated semantic identity, the two transport directions, the
machine root, and the independent replay boundary.  That separation makes
the trust surface explicit and permits the canonical Master to recompute the
environment rather than accepting text-identical headers or worker-supplied
hashes.

The readable reconstruction is deliberately node-aligned.  Each substantive
DAG node has exactly one stable anchor, and every anchor points back to one
node.  The reconstruction records hypotheses, inference, output, formal
anchor, downstream uses, exceptional cases, and trust boundary.  Duplicate
narrative is omitted, but no mathematical or audit field is deleted.
