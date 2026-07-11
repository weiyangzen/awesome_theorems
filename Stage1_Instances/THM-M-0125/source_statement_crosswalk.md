# Source-statement crosswalk

## Primary source anchor

B. H. Gross and D. B. Zagier, *Heegner points and derivatives of L-series*, Inventiones
Mathematicae **84** (1986), 225-320, DOI `10.1007/BF01388809`. The paper is the primary source for
the theorem family. A stable scan, file hash, precise theorem/page selection, and errata search are
still required before H0; discovery-level references commonly point to the formula near the final
theorems of the paper, but this intake does not promote that recollection to a pinpoint citation.

| Claim component | Human-source target | Lean representation required | Intake assessment |
|---|---|---|---|
| Modular/Rankin arithmetic input | Gross-Zagier's modular-form, character, order, and level data | Genuine modular form/elliptic curve and character/order structures | Exact binders and restrictions await pinpoint audit |
| Heegner hypothesis | Source splitting and conductor conditions | Named predicates on primes, ideals, conductor, and discriminant | Must not be compressed into an opaque proposition |
| Central derivative | The source's normalized L-series and central point | Constructed arithmetic L-series plus derivative and continuation data | Mathlib discovery module has only a generic interface, not this object |
| Heegner point/divisor | CM point/divisor and its image under the chosen parametrization | Constructed point/divisor with field-of-definition and trace data | No rev-5.6 construction credited |
| Height | Source Neron-Tate height pairing and conventions | Actual canonical height/pairing and a checked convention bridge | An arbitrary complex field is not an acceptable encoding |
| Equality constant | Periods, degrees, discriminants, unit indices, and local factors of the selected variant | Explicit typed factor with nonzero and convention side conditions | Exact factor is deliberately not guessed at intake |
| Formula | Equality of the analytic and height sides | Exact Lean proposition after all preceding rows are fixed | Statement gate remains open (`M4`) |

## Repository crosswalk

The metadata phrase "elliptic-curve derivative formula" is only a discovery summary. The legacy
`S1_M_044.lean` file provides useful names for missing interfaces and locally checked elementary
wrappers, but its main formula shape accepts the derivative, height, factor, and hypotheses as
fields. It therefore cannot serve as the source-faithful root and supplies no theorem closure.

The statement phase must obtain and hash the primary source, choose one theorem/corollary, transcribe
its ordered binders and assumptions, record all conventions, and justify any elliptic-curve
specialization. It must then elaborate that exact target and mutation-test omitted hypotheses,
changed fields/orders, the central point, height scaling, and local factors before anchor evidence is
observed. No H0, M0, or checked transport claim is made here.

