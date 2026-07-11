# Scope map

## Available source scope

The repository metadata fixes only an author-associated Chinese label, the year 1985, the broad
area algebraic geometry, and the gloss "minimal models of algebraic varieties." It does not fix a
mathematical proposition. These facts are retained as discovery metadata and are not treated as a
canonical claim.

## Decisions required before statement work

An inspected primary source must determine the exact named result and its bibliographic theorem
anchor. The statement record must then fix: base field and characteristic; normality,
projectivity/properness and dimension of the variety; the singularity condition; the relevant
canonical or log-canonical divisor; numerical versus linear equivalence conventions; all
positivity hypotheses; and whether the conclusion is existence of a minimal model, abundance,
non-vanishing, a Kodaira/Iitaka dimension relation, or another dimension assertion. Degenerate and
boundary cases must be copied from that source rather than guessed.

## Explicit exclusions

- A generic claim that every algebraic variety has a minimal model.
- The Minimal Model Program, abundance conjecture, or Iitaka conjecture used as substitutes.
- A dimension equality or inequality chosen merely because it is associated with Kawamata.
- An abstract Lean structure that assumes the desired conclusion as a field.
- The untrusted repository label `已验证` as evidence of either a human proof or kernel closure.

Until the identity is resolved there is no eligible canonical Lean expression and no mutation or
transport registry. This is the concrete first blocker for `S56-M-0147-STATEMENT`.
