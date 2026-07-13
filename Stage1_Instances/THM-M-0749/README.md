# THM-M-0749 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the Friedberg-Muchnik theorem. The
mathematics catalog gives only the gloss `Post problem's affirmative solution`, attributes it to
Richard Friedberg and Albert Muchnik in 1956, and labels it verified. A second repository record
states the usual theorem-family formulation: there exist incomparable computably enumerable
degrees. These are discovery inputs, not source or machine-proof evidence.

The preserved theorem family is the existence of two computably enumerable sets whose Turing
degrees are incomparable: neither set is Turing reducible to the other. An archived secondary
source states this as Theorem 3.8 and identifies the independent primary publications by Muchnik
(1956) and Friedberg (1957). Friedberg's publication metadata and title independently confirm the
same family. The primary proof texts, however, have not been pinned and inspected for exact
definitions, assumptions, proof boundaries, translations, corrections, or errata. No independent
source review is recorded, so this intake makes no `H0` claim.

Pinned mathlib provides `REPred`, oracle computability, Turing reducibility, Turing equivalence,
and the quotient type `TuringDegree`. `IntakeProbe.lean` authenticates those interfaces and a
prospective predicate-to-partial-function encoding. It does not establish a checked transport from c.e. sets
to partial-function oracles, state the canonical target, or prove incomparable c.e. degrees. A
bounded exact-topic search found no Friedberg-Muchnik or c.e.-degree incomparability declaration.

The provisional root vector is `[H1, M4, R4]`. `instance.json` freezes the scope boundary and
`task-dag.json` keeps all six downstream phases open. No exact statement, proof body, accepted
execution state, audit completion, theorem completion, or master acceptance is claimed.
