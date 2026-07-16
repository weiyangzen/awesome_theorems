# THM-M-0137 rev-5.6 intake

This directory is the `planned` intake for the Kac-Peterson character-formula target. Repository
metadata does not contain enough mathematics to choose uniquely between the Weyl-Kac character
formula and the Kac-Peterson modular-transformation results for affine characters. The ambiguity is
preserved as an explicit statement-phase blocker rather than silently choosing a nearby theorem.

The scope map and source crosswalk record the candidate interpretations and the exact decision that
must be made from a primary source. No legacy artifact is accepted as rev-5.6 statement or proof
evidence. The provisional root vector is `[H2, M4, R4]`; no Lean expression, proof, audit completion,
or theorem completion is claimed.

The open downstream nodes are recorded in `task-dag.json`. Exact intake checks and their results are
in `validation.md`.

The statement execution has now been replayed against the current HEAD contract and remains
blocked. `statement.json` records the deliberately null canonical target, `Statement.lean` checks
only pinned adjacent interfaces, `dependency-reuse-ledger.json` records the exact empty v2 closure,
and `statement-receipt.json` plus `check_statement.py` provide a typed negative result. The
validator reports `phase_accepted=false`. The root worker packet proposes only `[_]`, meaning the
negative boundary was self-tested; it does not claim the positive statement predicate or master
acceptance.
