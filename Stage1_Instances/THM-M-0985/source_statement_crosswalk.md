# Source-statement crosswalk

| Claim component | Human source anchor | Lean target/candidate | Intake assessment |
|---|---|---|---|
| iid integrable real variables obey the strong law | A. N. Kolmogorov, *Grundbegriffe der Wahrscheinlichkeitsrechnung* (1933), strong-law material in Chapter VII | Exact declaration not yet selected | Historical primary source identified only at book/chapter granularity; edition, page, assumptions, translation differences, and errata remain open: `H1` |
| Modern iid finite-first-moment formulation | P. Billingsley, *Probability and Measure*, 3rd ed. (Wiley, 1995), Section 22, strong law treatment | Candidate proposition over `X : Nat -> Omega -> Real` | Secondary normalization anchor only; exact theorem/page and premise-by-premise review remain open |
| Almost-sure convergence | Convergence holds outside a probability-zero exceptional set | Candidate mathlib `Tendsto` statement restricted by `∀ᵐ omega ∂P` | Object model and expression must be selected and elaborated in the statement phase |
| Common expectation | Identical distribution and integrability make the expectations agree | Integral of `X 0` with respect to `P` | Common-law integral transport is an explicit bridge obligation, not assumed proof credit |
| Arithmetic means | First `n` observations divided by `n` | Finite sum over an explicitly chosen range, coerced to `Real` | Zero/one-based indexing and `n = 0` behavior require checked transports |
| Centered partial-sum form | `(S_n - n * E[X_0]) / n -> 0` almost surely | Candidate alternate expression | Mathematical equivalence is plausible but remains unchecked |

The repository's Chinese label names Kolmogorov's strong law and its legacy summary says only
"the strong law for independent identically distributed variables." That wording omits the
codomain, measurability, moment condition, convergence mode encoding, and indexing convention.
The intake therefore selects the standard real-valued iid finite-first-absolute-moment theorem,
while marking source pinpoint fidelity and every formal encoding choice as open. A variance
assumption, a weak-law conclusion, or a non-iid sufficient criterion must not be substituted for
this root.

Discovery links, not immutable evidence receipts:

- Kolmogorov bibliographic record: <https://doi.org/10.1007/978-3-642-49888-6>
- Billingsley publisher record: <https://www.wiley.com/en-us/Probability+and+Measure%2C+3rd+Edition-p-9780471007104>

These discovery URLs must be verified during source audit and are deliberately not treated as
evidence. Required follow-up includes immutable edition hashes, exact page/theorem
pinpoints, translation and errata checks, premise-to-binder mapping, a mathlib declaration search,
and independent review. No `H0` or machine-closure claim is made.
