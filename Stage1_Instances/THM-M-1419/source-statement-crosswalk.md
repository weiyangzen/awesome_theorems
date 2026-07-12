# Source-statement crosswalk

## Repository record and candidate source

The repository inventory supplies the name, Valery Oseledets, the year 1968, and only the gloss
"existence of Lyapunov exponents". Its `已验证` status is untrusted under rev-5.6. It gives no
theorem number, exact hypotheses, cocycle convention, filtration/splitting form, or quantifiers and
therefore does not identify an exact proposition.

The historical primary-source candidate is V. I. Oseledets, *A multiplicative ergodic theorem.
Lyapunov characteristic numbers for dynamical systems*, **Transactions of the Moscow Mathematical
Society** 19 (1968), 197-231 (English translation of the original Russian publication). This is a
discovery locator only: an immutable edition has not yet been inspected theorem by theorem, and its
numbered result, translation fidelity, definitions, assumptions, corrections, and errata remain
open. It is therefore not `H0` evidence.

## Crosswalk

| Repository/source phrase | Mathematical component to freeze | Required Lean component | Intake status |
|---|---|---|---|
| "multiplicative ergodic theorem" | products of a linear cocycle over dynamics | measurable base map, cocycle law, ordered products | family identified; convention open |
| "Lyapunov exponents" | almost-sure asymptotic logarithmic growth rates | norm, logarithm, normalized limit, finite exponent data | conclusion family identified; exact form open |
| invariant subspaces | filtration or splitting realizing each rate | measurable submodule/flag map and equivariance | required for full family; variant open |
| integrability | logarithmic moment condition on maps and possibly inverses | strongly measurable norm functions and integrals | hypothesis family identified; exact bounds open |
| ergodicity | makes exponent data almost surely constant | ergodic measure-preserving transformation | source dependence unresolved |
| 1968 / Oseledets | bibliographic disambiguation | no machine-proof credit | primary candidate identified only |

## Existing formal boundary

Repository search found a substantial historical Lean boundary at
`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_248.lean`, owned by `THM-M-1056`. It explicitly
states that it provides support APIs and checked statement shapes but no terminal Oseledets proof.
Because it belongs to another target, this intake neither modifies nor imports it and grants it no
rev-5.6 credit. Its types and negative anchor notes may be re-audited as discovery evidence only
after this target's exact statement is frozen.

Before `H0`, an independent reviewer must inspect the selected immutable edition, pinpoint the
theorem and pages, verify translation and errata, map every definition and assumption, and approve
the source-to-statement rows. Before statement credit, those rows must map to an elaborated Lean
expression without dropping inverse integrability, changing one-sided/two-sided dynamics, replacing
a splitting by a filtration, or weakening simultaneous almost-everywhere vector growth.
