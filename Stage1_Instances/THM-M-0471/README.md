# THM-M-0471 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the fundamental theorem of
arithmetic. The repository supplies the claim that every integer greater than one has a unique
factorization into primes, attributes it to Euclid around 300 BCE, and labels it verified. The
claim is mathematically recognizable, but the attribution and verification label are uncited
catalog metadata and confer no rev-5.6 proof credit.

## Intake result

The human scope is: every natural number `n > 1` is a finite product of primes, and any two such
prime lists differ only by permutation. This preserves the positive-integer meaning of the catalog
while avoiding an invented sign or unit convention for all integers. `Statement.lean` now freezes
and elaborates that exact list/permutation expression, and its checked direct expansion preserves
the binder, primality, product, nonempty, and permutation clauses. Prime-exponent and integer
formulations remain uncredited alternate encodings.

Pinned mathlib exposes canonical prime-factor lists, product reconstruction, uniqueness up to list
permutation, and a prime-supported exponent-map equivalence. `IntakeProbe.lean` checks these APIs
and representative boundary instances in the pinned environment. That is real feasibility evidence
for an `M3` candidate, not an accepted target, terminal-body audit, or theorem proof.

## Scope and evidence boundary

`scope-map.md` records the number domain, representation choices, boundary cases, and excluded
substitutions. `source-statement-crosswalk.md` separates the repository record, the inspected
Euclid translation leads, and the pinned Lean candidates. `statement.json` and
`statement-receipt.json` bind the exact expression and environment fingerprints. `instance.json`
remains the structured planned scope record, and `task-dag.json` keeps authoritative task state open
pending master acceptance.

The provisional vector remains `[H1, M3, R4]`: a complete classical proof is known but no pinpoint
edition-to-modern-statement proof crosswalk or independent source review is accepted; the exact
canonical expression now elaborates but no proof body is credited; and no source-faithful readable
proof reconstruction exists. No H0, M0, R0, accepted execution state, audit completion, theorem
completion, or master acceptance is claimed.
