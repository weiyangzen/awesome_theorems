# Source-statement crosswalk

| Claim component | Human source anchor | Lean candidate | Intake assessment |
|---|---|---|---|
| Riemann's prime-power counting formula in terms of zeta zeros | B. Riemann, *Ueber die Anzahl der Primzahlen unter einer gegebenen Groesse*, Monatsberichte der Berliner Akademie (1859), pp. 671-680 | a future exact `J`/weighted-prime-power declaration | Primary historical source identified; transcription, edition hash, precise displayed formula, branch conventions, and page-to-node review remain open |
| Rigorous development of Riemann's explicit-formula argument | H. von Mangoldt, *Zu Riemanns Abhandlung \"Ueber die Anzahl der Primzahlen unter einer gegebenen Groesse\"*, Journal fuer die reine und angewandte Mathematik 114 (1895), pp. 255-305 | future contour, residue, and zero-sum obligations | Primary paper identified bibliographically; theorem/page/assumption and errata crosswalk remains open |
| Weighted `psi` formulation | Classical von-Mangoldt-weight reformulation; exact primary pinpoint not yet accepted | `Chebyshev.psi` and candidate `PsiFirstPublicVariant` in legacy `S1_M_258` | Selected as the primary formal candidate, but exact coefficients and discontinuity convention are not frozen |
| Ordinary prime-counting formulation | Derived through a `J`-type function and Mobius inversion rather than definitionally equal to `psi` | candidate linked prime-counting transfer | Must be a checked transport; it cannot be inferred from the manifest's short wording |
| Riemann-von Mangoldt zero-counting formula | A distinct theorem giving the asymptotic count of zeta zeros | none for this target | Explicitly excluded because the source record says prime-counting function |

## Fidelity boundary

The source corpus names a theorem family, not one fully specified equality.
Different standard presentations use `J(x)`, a half-weighted discontinuous
variant, `psi(x)`, or `pi(x)`; infinite zero sums also require a symmetric or
limiting convention. Consequently this crosswalk supports `H2` discovery and
disambiguation, not `H0` source fidelity.

The dependent statement phase must record an edition/file hash and exact
pinpoints, transcribe the chosen formula, define all correction terms and zero
summation, and prove checked transports for any advertised alternatives. The
later source audit must also search corrections/errata and obtain independent
review.

Discovery identifiers, not immutable evidence receipts:

- Riemann 1859 bibliographic record: `Monatsberichte der Koeniglich Preussischen Akademie der Wissenschaften zu Berlin`, 1859, 671-680.
- von Mangoldt 1895 bibliographic record: `Journal fuer die reine und angewandte Mathematik`, volume 114, 255-305, DOI `10.1515/crll.1895.114.255`.

No historical source, legacy source label, or legacy Lean wrapper is credited
as a completed human or machine proof by this intake.
