# Source-statement crosswalk

| Claim component | Human source anchor | Lean target surface | Intake assessment |
|---|---|---|---|
| Classical weak maximum principle for the heat equation | L. C. Evans, *Partial Differential Equations*, 2nd ed., AMS Graduate Studies in Mathematics 19 (2010), section 2.3, "Maximum principles" | Root equality/inequality for a classical caloric function on a cylinder | Standard published textbook anchor located; exact theorem/page, scanned edition hash, assumptions, and errata remain unaccepted |
| Maximum occurs on the parabolic boundary | Evans, section 2.3 definition of the parabolic boundary and maximum-principle discussion | `closure U x {0}` union `frontier U x [0,T]` | The terminal interior face is deliberately excluded from the boundary; exact endpoint encoding awaits elaboration |
| Perturbation argument for the weak principle | Evans, section 2.3 proof using a strict subsolution perturbation | Future proof obligations for strict inequality, interior extremum derivatives, and limiting perturbation | Proof architecture discovery only; no leaf or proof-body credit |
| Earlier classical treatment | A. Friedman, *Partial Differential Equations of Parabolic Type*, Prentice-Hall (1964), maximum-principle chapters | Candidate corroborating source boundary | Bibliographic lead only; edition/page/assumption crosswalk not yet performed |

The source label in `Docs/Stage0_Blueprint.md` says only "maximum principle for solutions of the
heat equation" and supplies no domain, regularity, sign convention, or weak/strong qualifier.
Accordingly, the dossier does not pretend that the source already fixed a unique formal theorem.
It chooses the standard weak classical cylinder theorem because that is the minimal conventional
reading that yields the stated "maximum on the boundary" conclusion.

The following distinctions are normative for later phases:

- `u_t - Delta u = 0` implies the selected result by specialization of a subsolution principle, but
  a subsolution theorem is not itself the frozen root.
- A comparison principle follows by applying a maximum principle to a difference, but requires a
  checked bridge and matching regularity.
- The strong maximum principle has a rigidity conclusion after an interior extremum. It is not an
  alternate spelling of this root.
- Existence or uniqueness of heat-equation solutions is not asserted.

No `H0` or machine-closure claim is made. Source audit must pin an immutable edition, verify the
exact theorem/page and every premise, check corrections/errata, and obtain independent review.
Source discovery links (not evidence receipts):

- Evans book record: <https://bookstore.ams.org/gsm-19-r>
- Friedman bibliographic DOI: <https://doi.org/10.1016/B978-0-486-46629-1.50005-5>
