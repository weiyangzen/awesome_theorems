# Source-statement crosswalk

## Human-source discovery anchors

- Hermann Minkowski, *Geometrie der Zahlen*, 1896, is the historical primary source family for the
  geometry-of-numbers argument. The exact edition/page and whether it states the ideal-class
  representative corollary in the modern normalization remain unverified.
- J. Neukirch, *Algebraic Number Theory*, Springer, 1999, Chapter I, Section 6 (Minkowski theory), is
  a candidate stable exposition for the ideal-class corollary. Exact theorem/page, translated
  wording, assumptions, and errata must be inspected before `H0`.
- Daniel A. Marcus, *Number Fields*, second edition, Springer, 2018, Chapter 5 (Minkowski theory), is
  a second candidate exposition. Exact theorem/page and normalization remain to be inspected.

These are discovery citations, not primary-source receipts and not an `H0` claim.

## Statement crosswalk

| Intended component | Source-side question | Lean-side candidate | Intake disposition |
|---|---|---|---|
| every ideal class | class of fractional ideals modulo principal ideals; orientation varies | `C : ClassGroup (𝓞 K)` | included, orientation open |
| integral representative | source may first choose a fractional ideal then clear denominators | `I : (Ideal (𝓞 K))⁰` | included |
| represents `C` | source conventions may yield `C` or its inverse | `ClassGroup.mk0 I = C` | exact mapping open |
| absolute norm bound | confirm norm is the positive index norm | `absNorm (I : Ideal (𝓞 K)) <= ...` | included, type open |
| constant | confirm `(4/pi)^r2 n!/n^n sqrt(|d_K|)` and endpoint `<=` | real expression in legacy wrapper | exact normalization open |
| hypotheses | number field, characteristic zero, finite degree are often implicit | `[Field K] [NumberField K]` | candidate binders only |

## Repo-local Lean discovery

`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_073.lean` imports
`Mathlib.NumberTheory.NumberField.ClassNumber`, defines `StatementShape`, and wraps the candidate
declaration `NumberField.exists_ideal_in_class_of_norm_le`. It also records the repository mathlib
pin `8a178386ffc0f5fef0b77738bb5449d50efeea95`. Under the uniform L0 rule this legacy file is only a
locator: intake has not accepted its elaboration, exact source identity, axiom closure, terminal
body provenance, or build freshness.

The next nodes must inspect a stable human source, settle the class/inverse convention, elaborate
the canonical target with minimal imports, compare the mathlib declaration by exact type, and only
then decide whether the candidate earns `M0-W`. The convex-body proof and class-group reduction must
remain visible provenance/obligation boundaries rather than being credited as a local proof body.
