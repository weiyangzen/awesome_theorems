# THM-M-0741 rev-5.6 dossier

This directory is the fail-closed `planned` dossier for the recursion-theory target
`停机问题` (the halting problem). The repository's complete target gloss is `停机问题不可判定`
("the halting problem is undecidable"), attributed to Alan Turing in 1936. A separate
proof-theory record, `THM-M-0707`, expresses the same English theorem family more fully. That
record is a duplicate discovery lead, not a dependency, substitute, or source of proof credit.

The theorem family is clear: no one effective total procedure decides for every encoded program
and input whether the computation eventually halts. The statement phase now freezes that
conventional reading in mathlib's universal partial-recursive-code model. The exact target is
`Not (ComputablePred Halts)`, where `Halts (code, input)` is the domain of `Code.eval code input`.
Every inductive code and natural input is included; halting means production of some output rather
than a timeout observation. The sole direct import is `Mathlib.Computability.Halting`.

`Statement.lean` checks a definitional iff to the expanded target, four structural mutations, and
a terminating and divergent program boundary. `check_statement.py` fingerprints every explicit
expression and verifies that replacing the import by `PartrecCode` fails because `ComputablePred`
is unavailable. These are statement-identity checks only. They do not inspect or credit
`ComputablePred.halting_problem`, import state or proof credit from `THM-M-0707`, or prove this
item.

The target-bearing catalog still does not provide a source-exact machine model, and no immutable
Turing 1936 passage, historical definition transport, correction/errata review, or independent
source review is accepted. Consequently the provisional vector is `[H1, M3, R4]`: the exact
conventional machine statement is self-tested, while human-source fidelity and every proof gate
remain open. The lifecycle stays `planned`; the statement awaits dependency-ordered master
acceptance; no proof state or receipt is master-accepted; and neither audit nor theorem completion is
claimed. See `statement-validation.md` and `statement-receipt.json` for the current boundary.
