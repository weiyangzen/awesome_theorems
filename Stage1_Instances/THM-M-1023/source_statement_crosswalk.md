# Source-Statement Crosswalk

| Claim component | Source surface | Intended formal component | Intake assessment |
|---|---|---|---|
| Target identity | `Docs/researches/math_theorems.md`, `THM-M-1023` metadata | Entire biconditional | Metadata says "infinitely divisible distributions' Levy-Khinchin representation" and labels it verified; the label supplies no evidence and is not accepted. |
| Infinite divisibility | Classical probability terminology attributed in metadata to Paul Levy and Aleksandr Khinchin (1934) | For every `n >= 1`, existence of a probability convolution root | Definition frozen at the mathematical level; exact convolution API and equality notion remain open. |
| Levy-Khinchin direction | Same metadata wording | Infinitely divisible implies representable characteristic function | In scope, but the exponent formula and analytic side conditions require a primary-source pinpoint and exact convention. |
| Converse direction | Meaning of "representation" as a characterization | Valid Levy-Khinchin data imply an infinitely divisible law | In scope; must not be silently dropped when formalizing. |
| Characteristic function | Adjacent `THM-M-1024` metadata mentions the characteristic function | Fourier transform of the probability measure | Context only. The adjacent theorem is independently owned and provides no proof or statement credit here. |
| Degenerate laws | Boundary analysis of the intended theorem | Zero Gaussian/jump terms and Dirac laws | Included; statement mutation tests must ensure they are not excluded accidentally. |

## Source boundary

The repository gives only an attribution, year, and short description. It does not identify an edition, theorem number, page range, assumptions, normalization, or errata. Accordingly the provisional human status is `H1`, not `H0`. The anchor-audit phase must locate a primary Levy/Khinchin source or an explicitly justified authoritative edition, record immutable bibliographic details, map both implications and every analytic assumption, check corrections/errata, and obtain independent review.

The common truncations `x * 1_{|x| <= 1}` and `x / (1 + x^2)`, Fourier sign choices, and coefficient conventions produce equivalent-looking but not literally identical formulas. No equivalence between them is credited at intake. The statement phase must select one convention and later transports must be checked in Lean.
