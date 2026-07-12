# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md` records the Chinese title `韦伊显式公式`,
attributes it to Andre Weil, dates it to 1952, and gives only `ζ函数的显式公式`
("an explicit formula for the zeta function"). Stage0 repeats that metadata.
Neither record supplies an equation, test-function hypotheses, transform
normalization, convergence convention, edition, page, proof, or formal
artifact. The manifest deliberately carries `已验证` only as
`source_status_untrusted`, so it grants no `H` or `M` credit.

## Historical discovery anchor

Andre Weil, *Sur les "formules explicites" de la theorie des nombres
premiers*, Communications du Seminaire Mathematique de l'Universite de Lund,
dedicated to Marcel Riesz (1952), pp. 252-265, is a historical primary-source
candidate matching the repository attribution and date. This intake has not
bound an immutable scan hash, selected a formula and surrounding hypotheses,
checked pagination/edition metadata or corrections, or obtained independent
review. The citation is therefore a discovery locator, not `H0` evidence.

## Crosswalk

| Repository phrase | Mathematical component to freeze | Required Lean component | Intake status |
|---|---|---|---|
| `ζ函数` | Riemann zeta, its pole, trivial zeros, and nontrivial zeros with multiplicity | `riemannZeta` plus reviewed zero/multiplicity encoding | zeta API probed; zero encoding open |
| "explicit formula" | one exact equality pairing zero and prime distributions with a test function | a concrete `Prop` with all binders and convergence witnesses | absent from repository source |
| test function (unstated) | admissible space, regularity/decay/symmetry, transform | functions on the selected domain and Fourier/Mellin APIs | candidate APIs probed; choices open |
| prime side (unstated) | prime powers and logarithmic weights | `ArithmeticFunction.vonMangoldt` or a checked equivalent | API probed; role and indexing open |
| zero sum (unstated) | multiplicity and limiting/summation prescription | zero subtype/multiset and `Summable`/limit formulation | not selected |
| archimedean side (unstated) | Gamma/pole/trivial-zero terms and constants | complex Gamma, integrals, logarithms | ingredient APIs present; exact terms open |
| `已验证` | untrusted inventory label | no proposition or proof credit | explicitly rejected as evidence |

## Fidelity boundary

The metadata distinguishes the Weil explicit-formula family from unrelated
zeta theorems but is too weak to select one formal proposition. Later source
work must preserve the original hypotheses and constants rather than importing
a modern convenient variant. A checked equivalence is required before a
distributional, Fourier-normalized, Mellin-normalized, or prime-counting form
can stand for another. Until an exact primary passage and independent review
are attached, the human status remains `H2`, not `H0`.

The bounded pinned-tree search and Lean probe locate only ingredients. They do
not constitute the immutable formal-candidate audit scheduled after statement
freeze and do not establish that a Lean proof of the formula exists.
