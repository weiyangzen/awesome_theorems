# THM-M-0133 Intake Dossier

## Status boundary

This is a rev-5.6 `planned` intake instance. It carries no accepted proof state, does not accept the
legacy Lean file as evidence, and does not claim audit or theorem completion. The next phase must
elaborate and freeze the exact target independently.

## Scope map

| Surface | Intake decision | Boundary |
|---|---|---|
| Root mathematical claim | Fermat's Last Theorem over positive integers, exponent `n > 2` | Provisional human scope; exact binder/domain encoding remains open for statement phase |
| Classical Wiles input | Every semistable elliptic curve over `Q` is modular | Dependency/source boundary, not a substitute root |
| Frey-Ribet reduction | A hypothetical FLT counterexample produces the contradiction with modularity | Root-critical bridge to model later; no closure credited |
| Existing Lean candidate | `AwesomeTheorems.Stage1.S1_M_022.StatementShape`, definitionally `FermatLastTheorem` | Discovery input only; must be freshly elaborated and audited |
| Existing partial branches | mathlib exponent 3, exponent 4, polynomial FLT, and conditional wrappers | Out of root-completion credit at intake |
| Exclusions | ABC, generalized Fermat equations, modularity of all elliptic curves, and polynomial analogues | Related statements cannot broaden or replace the root |

Degenerate-case policy is not yet frozen. In particular, the statement phase must compare mathlib's
nonzero formulation and exponent conventions with the positive-integer source wording, and supply
checked transports rather than treating prose equivalence as identity.

## Source-statement crosswalk

| Source node | Primary locator | Source assertion | Root relationship | Intake fidelity state |
|---|---|---|---|---|
| W95-T0.4 | Andrew Wiles, *Modular elliptic curves and Fermat's Last Theorem*, Annals of Mathematics 141 (1995), pp. 443-551, Theorem 0.4, p. 449 | Every semistable elliptic curve over the rationals is modular | Major dependency in the Wiles route | Edition and theorem locator recorded; assumptions/terminology need node audit |
| W95-C0.5 | Same article, Corollary 0.5, p. 449 | There are no nonzero integers `a,b,c,n` with `n > 2` and `a^n + b^n = c^n` | Direct source statement for the root | Domain and nonzero/positive encoding transport remains unchecked |
| TW95 | Richard Taylor and Andrew Wiles, *Ring-theoretic properties of certain Hecke algebras*, Annals of Mathematics 141 (1995), pp. 553-572 | Supplies the companion ring-theoretic argument used to complete the modularity proof | Proof provenance/dependency, not an alternative root statement | Exact lemma-level crosswalk and errata audit deferred |
| Legacy queue | `Docs/Stage1_Blueprint.md`, `S1-M-022` | Calls the item Wiles theorem and explicitly says its content is the proof of FLT | Repository metadata disambiguation | Untrusted legacy discovery only |
| Lean candidate | `Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_022.lean` | Defines `StatementShape := FermatLastTheorem` | Candidate formal encoding | No rev-5.6 statement or proof credit |

Primary-source URLs for later immutable capture: `https://doi.org/10.2307/2118559` (Wiles) and
`https://doi.org/10.2307/2118560` (Taylor-Wiles). No errata conclusion is asserted at intake.

## Intake receipt

- Receipt ID: `S56-M-0133-INTAKE-local-a8d6489f`
- Base revision: `a8d6489fd935cd71fa4499f2f3f5b051998203f4`
- Membership checks: standard validator and ordered target manifest passed.
- Narrow validation: JSON parsing, required-field assertions, forbidden-placeholder scan, and
  whitespace validation passed; exact commands are in `validation.md`.
- Acceptance boundary: this is worker self-test evidence only. Master acceptance remains required.
