# THM-M-0387 Source-Statement Crosswalk

## Repository source record

The repository catalog entry in `Docs/researches/math_theorems.md` identifies Pierre de Fermat,
1637, and the claim `x^n + y^n = z^n (n>2)` has no positive-integer solution. Its status text says
that the `n = 3`, `n = 4`, and regular-prime branches are partly machine checked while the full
proof remains in progress. That status is explicitly untrusted intake metadata, not proof evidence.

| Claim component | Source lead | Planned Lean candidate | Intake decision |
|---|---|---|---|
| All exponents greater than two | Repository catalog; Fermat's historical claim; modern proof literature | `FermatLastTheorem` | Exact root candidate; elaboration and normalized fingerprint remain open |
| No positive integral solution | Historical positive-integer wording | nonzero `Nat` variables in `FermatLastTheoremFor n` | Intended encoding; positivity/nonzeroness and exponent-bound transport must be checked |
| Fixed exponent | Root specialized to one `n` | `FermatLastTheoremFor n` | Decomposition API only; no fixed exponent substitutes for the root |
| Integer and rational forms | Scaling, signs, and denominator clearing | `FermatLastTheoremWith Int n`, `FermatLastTheoremWith Rat n` | Candidate equivalences; no credit before both directions are elaborated and fingerprinted |
| Primitive/coprime form | Standard primitive-solution reduction | `FermatLastTheoremForCoprime n` | Candidate local encoding; return transport to the fixed-exponent target remains open |
| Exponents three and four | Classical special-case proofs | `fermatLastTheoremThree`, `fermatLastTheoremFour` | Discovery leads for later audit; they do not close the all-exponent claim |
| Regular primes | Kummer's regular-prime theorem | pinned `flt_regular` candidate | Discovery lead for a restricted family only |
| Full modern proof | A. Wiles (1995) and R. Taylor/A. Wiles (1995) | all-odd-prime input to `FermatLastTheorem.of_odd_primes` | Primary proof leads; premise-to-node and errata mapping remain open |

## Primary-source leads

- A. Wiles, *Modular elliptic curves and Fermat's Last Theorem*, Annals of Mathematics 141
  (1995), 443-551, DOI `10.2307/2118559`.
- R. Taylor and A. Wiles, *Ring-theoretic properties of certain Hecke algebras*, Annals of
  Mathematics 141 (1995), 553-572, DOI `10.2307/2118560`.

These citations are discovery leads. Intake does not possess immutable local paper bytes, an
edition/page/theorem-to-obligation crosswalk, an errata and correction audit, or independent source
review, so it makes no `H0` claim.

## Exact-statement choices still open

1. Re-elaborate the pinned definition of `FermatLastTheorem` and bind its exact normalized kernel
   expression, minimal imports, options, and environment.
2. Check that the pinned root's `n >= 3` spelling is equivalent to the catalog's `n > 2` spelling.
3. Check the positive-integer to nonzero-natural boundary, including all ordered binders and all
   three nonzeroness hypotheses.
4. Elaborate and bind every credited `Nat`/`Int`/`Rat` and primitive/coprime transport in both
   required directions.
5. Mutation-test a removed nonzeroness hypothesis, changed domain, changed binder scope, and the
   exponent boundary before any proof evidence is inspected.

The source-access and formal-statement choices above are downstream blockers, not defects in the
completed planned intake record. No existing partial branch or shared-module co-mention transfers
proof or acceptance credit to this theorem.
