# THM-M-1480 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the numerical-analysis catalog
label `拟Monte Carlo方法` (quasi-Monte Carlo methods). The repository attributes the item to Harald
Niederreiter in 1978 but supplies only the gloss `低差异序列的积分` (integration using low-discrepancy
sequences). It does not select a point set or sequence, discrepancy notion, integrand class,
integration domain, estimator, finite-sample inequality, asymptotic theorem, constants, or exact
conclusion. The catalog value `已验证` is untrusted metadata and supplies no source or proof credit.

The attribution and year have a strong bibliographic match: Harald Niederreiter,
*Quasi-Monte Carlo methods and pseudo-random numbers*, *Bulletin of the American Mathematical
Society* 84(6), 957-1041 (1978), DOI `10.1090/S0002-9904-1978-14532-7`. Crossref metadata was
inspected. The publisher full-text endpoint returned HTTP 403, so no proposition, definition,
theorem/page locator, proof boundary, correction record, or source-to-catalog identity is accepted.

The gloss names a result family. It could refer to a Koksma-Hlawka-type finite-`N` error inequality,
convergence of quadrature along a uniformly distributed or low-discrepancy sequence, a discrepancy
rate for a named construction followed by an integration-error corollary, or a randomized or
weighted variant. These claims have different hypotheses and conclusions. Intake records them as
discovery directions and does not silently substitute the familiar Koksma-Hlawka theorem.

The provisional vector is `[H5, M4, R4]`. `H5` means that the received catalog gloss is not yet one
stable truth-valued proposition; it does not refute established quasi-Monte Carlo theorems.
`IntakeProbe.lean` checks adjacent pinned APIs only. All six downstream phases remain open. No
canonical statement, H0, M0, R0, accepted state, audit completion, theorem completion, or master
acceptance is claimed.
