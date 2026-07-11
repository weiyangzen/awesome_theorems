# Source-statement crosswalk

| Claim component | Human source anchor | Lean candidate | Intake assessment |
|---|---|---|---|
| Half-integral form admits an integral-weight lift defined by Fourier coefficients | G. Shimura, *On modular forms of half integral weight*, Annals of Mathematics (2) 97 (1973), 440-481, especially the lifting results in the paper's main development | future exact replacement for `S1_M_047.StatementShape` | Primary paper identified, but theorem number, page-level premises, scanned edition, and errata have not been accepted: `H1` |
| Divisor-sum formula for lift coefficients | Same paper; formula depends on character and normalization conventions | no exact local declaration | Mandatory root content; the legacy `coefficientFormula : Prop` field does not encode it |
| Modularity, target weight, level, and character | Same paper, with convention-sensitive hypotheses and refinements in later literature | ordinary `CuspForm` target API in the legacy module | Object API is only an anchor; exact target subgroup and character are not frozen |
| Cuspidality and Hecke compatibility | Same paper's lifting/eigenform results; bad primes and normalizations require pinpoint mapping | no half-integral Hecke operator or checked bridge located at intake | Required branch, wholly open on the machine side |
| Kohnen plus-space correspondence | W. Kohnen, *Modular forms of half-integral weight on \(\Gamma_0(4)\)*, Mathematische Annalen 248 (1980), 249-266 | none credited | Later specialization/refinement; excluded from silently replacing the classical root |

The repository label `志村提升定理` names a theorem family rather than a unique typed statement.
The canonical prose in `intake.json` deliberately includes the construction's coefficient and Hecke
content, so a proof of mere target nonemptiness cannot pass. The statement phase must choose one
precise Shimura theorem and serialize its ordered binders and every arithmetic convention. If the
primary-source audit shows that the selected level/character formulation is not faithful, the
intake must be revised and reaccepted rather than broadening or weakening the theorem downstream.

Discovery links, not immutable evidence receipts:

- Shimura 1973: <https://doi.org/10.2307/1970831>
- Kohnen 1980: <https://doi.org/10.1007/BF01421949>

No `H0` claim is made. Required follow-up includes immutable source hashes, exact theorem/page and
formula pinpoints, assumption and notation mapping, errata/correction search, source genealogy for
the chosen refinement, and independent review.
