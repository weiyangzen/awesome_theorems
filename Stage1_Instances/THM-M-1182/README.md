# THM-M-1182 rev-5.6 intake

This is the `planned` dossier for the metadata label "Caffarelli boundary regularity." The inherited
Chinese description says only "boundary regularity of strictly convex domains." That wording does
not identify a unique mathematical proposition: it omits the equation or transport problem, the
unknown, dimensions, boundary and density assumptions, and the asserted regularity class. The
intake therefore freezes the ambiguity rather than silently substituting a familiar Caffarelli
theorem.

## Scope map

| Surface | Candidate scope | Boundary at intake |
|---|---|---|
| Exact root | A primary-source boundary regularity theorem for a convex potential/Monge-Ampere problem or optimal transport map | Not frozen; a unique theorem and pinpoint must be selected |
| Geometric data | Source and target domains in finite-dimensional real space; strict/uniform convexity and boundary smoothness | Dimension, convexity notion, and boundary class are missing |
| Analytic data | Convex solution/potential, Monge-Ampere measure or transported densities, boundary/second-boundary-value conditions | Equation and quantitative density assumptions are missing |
| Conclusion | Boundary regularity such as strict convexity or a `C^(1,alpha)`/higher estimate | Exact norm, exponent, locality, and constants are missing |
| Lean surface | Euclidean topology, convex sets/functions, measures and regularity predicates in pinned mathlib | No exact expression or declaration is credited |
| Foundations | Lean 4 kernel plus a versioned classical/choice/quotient policy | Toolchain, imports, TCB, and environment fingerprint remain open |

The later statement phase must first resolve the source identity, transcribe its ordered hypotheses
and conclusion, and reject neighboring results that merely share the title family. Only then may it
choose a Lean object model and run elaboration or mutation tests.

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H4, M4, R4]`. The first failed gate is exact
source identification. This dossier makes no claim that the untrusted historical label
`已验证` means a human-source audit or a Lean proof. The theorem is not complete.

## Validation

The commands and exact outcomes are recorded in `validation.md`. They validate manifest membership,
repository consistency, JSON syntax, and dossier hygiene only; no Lean theorem exists in this phase.
