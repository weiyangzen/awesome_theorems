# Source-statement crosswalk

| Claim component | Human source anchor | Lean discovery surface | Intake assessment |
|---|---|---|---|
| Global correspondence for `GL_r` over a function field | L. Lafforgue, *Chtoucas de Drinfeld et correspondance de Langlands*, Invent. Math. 147 (2002), 1-241, especially the global correspondence stated in Théorème VI.9 | No terminal local declaration identified | Primary proof source located; edition, exact French statement, assumptions and errata require independent audit (`H1`) |
| Irreducible continuous l-adic representations with determinant of finite order | Same theorem and its Galois-side definitions | `LafforgueGaloisParameter` and `LafforgueGaloisWeilSide` in the legacy module | Abstract predicates expose intended fields but are not a checked translation |
| Cuspidal automorphic representations of `GL_r` with central character of finite order | Same theorem and automorphic-side definitions | `LafforgueAutomorphicSide` | Automorphic representation and full adelic quotient are abstract, not mathlib objects |
| Compatibility away from ramification | Same theorem; compare its local Euler/Frobenius normalization | `FrobeniusHeckePolynomialMatches` | Polynomial equality has a useful shape, but source normalization and concrete constructions remain open |
| Function-field and finite-place substrate | Source curve/function-field conventions | `FunctionFieldFinitePlace`, `FunctionFieldFiniteAdeleRing`, `FunctionFieldFiniteAdeleGLn` | Concrete mathlib-adjacent candidates; only finite affine places/adeles are represented |

Discovery link: <https://doi.org/10.1007/s002220100174>. This URL is not an immutable evidence
receipt. Before `H0`, the audit must retain a content hash or edition identifier, transcribe the
exact theorem and definitions, map every premise and conclusion, check corrections/errata, and
obtain independent review.

The English sentence in `intake.json` is deliberately provisional. In particular, it does not
choose arithmetic versus geometric Frobenius, identify Weil-group and absolute-Galois formulations,
or assert that equality of one chosen polynomial convention is already the source's exact local
condition. Those choices belong to the statement phase and require checked transports.
