# Source-statement crosswalk

| Claim component | Human source anchor | Lean candidate | Intake assessment |
|---|---|---|---|
| Sample means of iid variables converge in probability to their expectation under a first-moment hypothesis | A. Khintchine, "Sur la loi des grands nombres", *Comptes rendus de l'Academie des sciences* 188 (1929), 477-479 | real specialization of `KhinchinWeakLawConclusion` | Primary-source bibliographic lead located, but an immutable scan, exact proposition/page transcription, translation, and errata review are not accepted: `H1` |
| Independent and identically distributed sequence | Same 1929 paper; exact historical independence and distribution assumptions require transcription | `Pairwise ((. independent .) on X)` and `IdentDistrib (X i) (X 0) mu mu` in the legacy candidate | API shape is discovery input; exact agreement with the source remains open |
| Finite first absolute moment | Integrability condition attributed to Khinchin's theorem; exact notation and scope require source inspection | `Integrable (X 0) mu` | Candidate correspondence only |
| Convergence in probability | Historical weak-law conclusion; epsilon/event wording must be pinned from the source | `TendstoInMeasure mu` to the constant expectation | A checked equivalence to the scalar epsilon formulation is deferred |
| Strong-law route | Later stronger theorem, not the canonical historical claim | `ProbabilityTheory.strong_law_ae` via the legacy wrapper | Potential proof bridge, never a replacement source statement |

The canonical intake deliberately selects the classical real-valued weak law. The existing local
candidate quantifies over complete real Banach spaces and derives the result from a strong law.
That generalization may be valuable, but it cannot silently broaden the historical theorem. The
statement phase must elaborate the real target, preserve its normalized expression and environment,
check any bridge to the Banach-valued form, and mutation-test independence, identical distribution,
integrability, codomain, expectation, and convergence mode.

Discovery locator (not an immutable evidence receipt):

- Bibliographic record: A. Khintchine, 1929, volume 188, pages 477-479.

No `H0` or machine-closure claim is made. Follow-up requires a content-addressed primary-source
copy, pinpoint premise mapping, translation review where used, errata search, and independent review.
