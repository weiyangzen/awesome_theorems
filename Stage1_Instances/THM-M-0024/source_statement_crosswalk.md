# Source-statement crosswalk

| Claim component | Human source anchor | Planned Lean surface | Intake assessment |
|---|---|---|---|
| Historical theorem identity | B. Mazur and A. Wiles, *Class fields of abelian extensions of Q*, Inventiones Mathematicae 76 (1984), 179-330, DOI `10.1007/BF01388599` | namespace and root declaration not yet assigned | Primary publication identified, but theorem/page pinpoint, scan hash, assumptions, and errata review remain open: `H1` |
| Algebraic object | Source's inverse-limit/class-group module and its character component | a finitely generated torsion module over a completed group/Iwasawa algebra | Exact module, action convention, involution, and coefficient ring must be transcribed |
| Algebraic invariant | Characteristic ideal or characteristic power series | `Ideal` equality or associated-element relation | “Ideal equality” versus “up to a unit” must be selected from the pinpointed source formulation |
| Analytic object | Source-normalized p-adic L-function/measure | an element or principal ideal in the same completed algebra | Period, Euler-factor, and interpolation conventions are root-relevant, not documentation details |
| Quantified scope | Abelian extensions of `Q`, decomposed into appropriate character components | explicit field/extension, prime, character, parity, and conductor binders | Metadata does not determine restrictions such as `p = 2` or exceptional/trivial characters |
| Root conclusion | Algebraic and analytic sides generate the same ideal | exact typed equality after checked transports | No Lean expression exists yet; `M4` is retained |

The repository metadata phrase “proof of the Iwasawa main conjecture” is a discovery label, not an
exact claim. It could incorrectly broaden the historical result or erase character and
normalization hypotheses. Therefore this intake freezes the theorem family and its non-negotiable
components while deliberately deferring the unique exact variant to source audit and statement
elaboration.

Discovery links, not immutable evidence receipts:

- EuDML bibliographic record: <https://eudml.org/doc/143060>
- DOI resolver: <https://doi.org/10.1007/BF01388599>

No `H0` or machine-closure claim is made. Required follow-up: obtain an immutable primary-source
copy, hash it, pinpoint theorem/page and definitions, check published corrections/errata, map every
premise and convention, and obtain independent source review.
