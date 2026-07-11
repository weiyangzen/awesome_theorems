# Source-statement crosswalk

| Claim component | Source anchor | Lean target | Intake assessment |
|---|---|---|---|
| Repository identity | `Docs/researches/math_theorems.md`, entry `Aubin定理`: Thierry Aubin, 1976, "Yamabe问题(非共形平坦)" | none | This is metadata, not proof evidence |
| Non-locally-conformally-flat branch | Thierry Aubin, *Équations différentielles non linéaires et problème de Yamabe concernant la courbure scalaire*, Journal de Mathématiques Pures et Appliquées 55 (1976), 269-296 | expression not selected | Primary paper identified bibliographically; theorem/page, assumptions, edition hash, and errata remain unaudited (`H2`) |
| Strict sphere comparison | Expected source role: establish a strict Yamabe-functional bound using a test function near a point of nonzero Weyl curvature | no repo-local declaration identified | Provisional claim component only; exact constants and quantifiers must come from the paper |
| Existence of a constant-scalar-curvature conformal metric | Standard variational consequence once the strict comparison prevents concentration | no repo-local declaration identified | Must not replace the strict-comparison root; source must decide whether it is part of Aubin's stated theorem |
| Conformally flat complementary case | Later Schoen branch, represented separately by `THM-M-1282` | excluded | Outside this theorem's scope |

Discovery bibliography is not an immutable receipt. No `H0` claim is made. The next source audit
must inspect a stable scan or edition, record exact theorem/page and assumptions, map each premise
to the eventual binders, search corrections/errata, and obtain independent review. The statement
phase must then select real Lean interfaces for smooth manifolds, Riemannian/conformal geometry,
integration, Sobolev quotients, and scalar curvature. It must elaborate the exact expression before
any nearby mathlib declaration can receive proof credit.

