# Source-statement crosswalk

| Claim component | Human source anchor | Lean candidate | Intake assessment |
|---|---|---|---|
| Isometry for the stochastic integral | K. Ito, "Stochastic Integral", *Proceedings of the Imperial Academy* 20 (1944), 519-524, especially Theorem 2.1 as identified by modern bibliographies | No canonical continuous-time declaration selected | Primary historical source located, but scan hash, exact notation/premise transcription, and independent review are open: `H1` |
| Brownian continuous-time specialization | Root claim fixes the integrator to standard real Brownian motion and quadratic variation `dt` | Planned Lean expression over a filtered probability space | Exact completion, filtration, predictability, and integral conventions remain to be frozen |
| Square-integrability premise | Finite expected integral of `H_t^2` over `[0,T]` | Planned `L2`/integrability predicate on a time-product measure | Candidate encoding only; equivalence of iterated and product integrals is unverified |
| Second-moment equality | Expected square of the Ito integral equals expected integrated square of the integrand | Planned equality in `Real` after finiteness proofs | Codomain and integral coercions await elaboration |
| General martingale bracket form | Later standard generalization `E[(H dot M)_T^2] = E[integral H^2 d[M]]` | Legacy `ItoIsometryHypotheses` / `ItoIsometryConclusion` shape | Strictly broader candidate, not a substitute and not credited |
| Discrete predictable sums | Standard simple-process/finite-sum precursor | Legacy `finitePredictableSum` branch | Approximation leaf only; it cannot establish the root without construction and limit passages |

The canonical intake claim uses the familiar Brownian finite-horizon form because the source
metadata says only "Ito isometry" and "isometry of the stochastic integral." This choice prevents
the existing discrete abstract wrapper from silently becoming the theorem. The statement phase
must verify the historical theorem numbering and wording against an immutable scan, then either
justify this specialization or revise the planned intake before expression freezing. It must also
serialize the normalized Lean expression and mutation-test predictability, square integrability,
the Brownian domain, the horizon binder, and the zero boundary cases.

Discovery links, not immutable evidence receipts:

- Ito paper metadata and scan landing page: <https://projecteuclid.org/journals/proceedings-of-the-imperial-academy/volume-20/issue-8/Stochastic-Integral/10.3792/pia/1195572786.full>
- DOI: <https://doi.org/10.3792/pia/1195572786>

No `H0` claim is made. Required follow-up includes immutable source hashing, verified page/theorem
pinpoints, notation and assumption mapping, translation/errata search, and independent review.
