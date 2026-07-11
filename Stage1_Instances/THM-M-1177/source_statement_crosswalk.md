# Source-statement crosswalk

| Claim component | Human source anchor | Intended formal surface | Intake assessment |
|---|---|---|---|
| Maximum estimate for a linear nondivergence operator | I. Bakelman, *Theory of Quasilinear Elliptic Equations*, Siberian Mathematical Journal 2 (1961), 179-186; A. D. Aleksandrov, *Majorization of solutions of second-order linear equations*, Vestnik Leningrad University 21 (1966), 5-25 | Root inequality in `intake.json` | Historical primary-source genealogy is identified, but translations, exact editions, assumptions, and errata have not been independently checked: `H1` |
| Determinant-weighted classical ABP estimate and contact-set proof | C. Pucci, *Limitazioni per soluzioni di equazioni ellittiche*, Annali di Matematica Pura ed Applicata 74 (1966), 15-30; D. Gilbarg and N. S. Trudinger, *Elliptic Partial Differential Equations of Second Order*, 2nd ed., Springer, 1983, section 9.1, Theorem 9.1 | finite-dimensional Hessian, determinant, contact set, and `L^n` integral | The textbook is a secondary normalization anchor. The theorem/page premises and constants need an edition-locked audit before `H0` |
| Convex-envelope/normal-map mechanism | Gilbarg-Trudinger, section 9.1; L. C. Evans, *Partial Differential Equations*, 2nd ed., AMS, 2010, section 6.4.1 | convex envelope, gradient image, area formula, determinant/trace inequality | Proof architecture only; no node or Lean declaration receives credit |
| Uniform ellipticity corollary | Lower eigenvalue bound implies `det A >= lambda^n` | Candidate alternate Lean theorem | A derived variant, not the frozen root; transport remains unchecked |
| Pucci extremal/viscosity formulation | L. A. Caffarelli and X. Cabre, *Fully Nonlinear Elliptic Equations*, AMS Colloquium Publications 43 (1995), chapter 3 | Candidate viscosity-theory theorem | Related modern ABP family, deliberately excluded from root equality until a statement audit fixes conventions |

The Stage0 phrase "nondivergence-form maximum principle" names a theorem family, not a sufficiently
typed proposition. This intake chooses the classical, drift-free, determinant-weighted upper
estimate so that later work cannot silently switch between linear, uniformly elliptic, and
viscosity/Pucci statements. The exact value of the dimensional constant is existential here; later
strengthening to a sharp constant is not required to prove this frozen claim.

No repository-local Lean declaration was found or credited during intake, and no `H0` or machine
closure claim is made. The statement phase must define the upper contact set, choose the regularity
encoding, elaborate the complete binder order, and mutation-test the sign, boundary, dimension,
determinant weight, and contact-set restriction. The source-audit phase must obtain immutable scans
or editions, hashes, pinpoint premise mapping, correction/errata results, and independent review.

Discovery identifiers (not evidence receipts): Pucci DOI `10.1007/BF02411289`; Gilbarg-Trudinger
ISBN `978-3-540-41160-4`; Caffarelli-Cabre ISBN `978-0-8218-0437-7`.
