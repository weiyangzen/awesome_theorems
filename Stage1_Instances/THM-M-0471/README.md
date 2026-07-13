# THM-M-0471 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the fundamental theorem of
arithmetic. The repository supplies the claim that every integer greater than one has a unique
factorization into primes, attributes it to Euclid around 300 BCE, and labels it verified. The
claim is mathematically recognizable, but the attribution and verification label are uncited
catalog metadata and confer no rev-5.6 proof credit.

## Intake result

The provisional human scope is: every natural number `n > 1` is a finite product of primes, and
any two such prime lists differ only by permutation. This preserves the positive-integer meaning
of the catalog while avoiding an invented sign or unit convention for all integers. The equivalent
prime-exponent formulation remains a candidate encoding; the dependent statement phase must choose
and fingerprint one exact Lean expression and check any transport it credits.

Pinned mathlib exposes canonical prime-factor lists, product reconstruction, uniqueness up to list
permutation, and a prime-supported exponent-map equivalence. `IntakeProbe.lean` checks these APIs
and representative boundary instances in the pinned environment. That is real feasibility evidence
for an `M3` candidate, not an accepted target, terminal-body audit, or theorem proof.

## Scope and evidence boundary

`scope-map.md` records the number domain, representation choices, boundary cases, and excluded
substitutions. `source-statement-crosswalk.md` separates the repository record, the inspected
Euclid translation leads, and the pinned Lean candidates. `instance.json` is the structured planned
scope record, and `task-dag.json` keeps all six dependent phases open.

The provisional vector is `[H1, M3, R4]`: a complete classical proof is known but no pinpoint
edition-to-modern-statement proof crosswalk or independent source review is accepted; usable pinned
statement/proof interfaces exist but no canonical expression or proof body is credited; and no
source-faithful readable proof reconstruction exists. No H0, M0, R0, accepted execution state,
audit completion, theorem completion, or master acceptance is claimed.
