# THM-M-0491 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the catalog entry named Maynard's
theorem. The repository supplies only the gloss "improvement of the upper bound on prime gaps,"
attributes it to James Maynard in 2013, and labels it verified. Under rev-5.6 that label is
untrusted inventory metadata, not an exact mathematical statement, source review, or Lean proof.

The matching primary source family is James Maynard's *Small gaps between primes*. Its 2013
preprint and 2015 journal version contain several inequivalent headline results: a bound for
arbitrarily many consecutive primes, a positive-proportion tuple theorem, an unconditional
adjacent-gap bound of 600, and conditional Elliott-Halberstam bounds. The short catalog gloss does
not select among them. In particular, it does not authorize changing an infinite-subsequence
`liminf` result into an eventual bound for every prime gap.

The source crosswalk records the published paper and its four headline candidates, while the scope
map freezes every proposition-changing choice that remains open. `IntakeProbe.lean` authenticates
adjacent nth-prime, prime-counting, Selberg-sieve, and von Mangoldt interfaces in pinned mathlib;
none states the requested root. A bounded local search found no exact Maynard or bounded-prime-gap
declaration. Those facts are discovery evidence only, not the later formal anchor audit.

The provisional vector is `[H1, M4, R4]`: a matching complete primary paper and theorem locators
are known, but the catalog-to-source selection, complete assumption mapping, correction audit, and
independent review remain open; no usable exact formal artifact is credited; and no source-faithful
readable proof reconstruction exists. `instance.json` is the structured scope authority and
`task-dag.json` keeps all six downstream phases open.

This intake claims no canonical proposition, expression fingerprint, H0, M0, R0, accepted proof
state, audit completion, theorem completion, or master acceptance. Commands and exact boundaries
are recorded in `validation.md`.
