# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md:9887-9892` records the title `Routh-Hurwitz criterion`, the names
Edward Routh and Adolf Hurwitz, the year 1895, and the complete gloss `conditions for the real parts
of a polynomial's roots to be negative`. All six lines originate at repository commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record supplies no bibliography, coefficient
domain, degree convention, determinant construction, quantifiers, hypotheses, proof, or formal
artifact. `Docs/Stage0_Blueprint.md:36885-36910` repeats the gloss while leaving exact definitions,
premises, proof, dependencies, equivalents, axioms, and machine artifacts open.

## Inspected mathematical sources

Adolf Hurwitz, *Ueber die Bedingungen, unter welchen eine Gleichung nur Wurzeln mit negativen
reellen Theilen besitzt*, Mathematische Annalen 46(2), 1895, pages 273-284, DOI
`10.1007/BF01446812`. The Goettingen Digitisation Centre article scan was inspected under stable
work/range identifiers `PPN235181684_0046` / `LOG_0026`; its downloaded PDF SHA-256 was
`e625ad366a91e771ce45319fbaae53959dd35a1ed384b95e4a4046cfda99fbad`. Page 273 introduces a
degree-`n` equation with real coefficients and reduces to positive `a_0`. Page 274 defines the
determinants and states that positivity of `Delta_1, ..., Delta_n` is necessary and sufficient for
all roots to have negative real parts. This is a primary source passage inspected for intake, but
its complete proof, historical notation, translation, errata, and independent review are not yet
accepted as `H0`.

Yury S. Barkovsky, *Lectures on the Routh-Hurwitz problem*, arXiv:0802.1805v1, 43 pages, PDF
SHA-256 `da0e65cd8b8f0fe68622e2814a2714ab30eb0e2b97577ae9407f8270d26d02c6`. Printed page 6 defines
stability by the open left half-plane. Section 6, printed page 18, gives the alternating-row finite
Hurwitz matrix and leading principal minors. Theorem 40 on printed page 19 states the equivalence
for real `p(z) = a_0 z^n + ... + a_n` with `a_0 > 0`. Printed page 20 separates the ascending-
coefficient reciprocal form and warns that nonnegative minors do not imply closed-half-plane roots.
The notes acknowledge corrected typos in a prior version, while arXiv exposes only v1; no separate
errata was located, so independent source review remains required.

Olga Holtz, *Hermite-Biehler, Routh-Hurwitz, and total positivity*, arXiv:math/0512591v1, PDF
SHA-256 `38b234adbff843c05b8b2a5d1a28c0a7f6a276ba60dc8e3999aef3869bcd2c79`, gives another modern
form. Its page 2 defines strict stability, while Theorem 3 on page 3 uses ascending coefficients,
an infinite Hurwitz matrix, and a positive factorization. It corroborates the family but is a
materially different candidate encoding, not a substitute root.

## Component crosswalk

| Catalog/source component | Mathematical content | Prospective Lean surface | Intake status |
|---|---|---|---|
| "polynomial" | finite degree `n`, real coefficients, nonzero positive leading coefficient | `Polynomial Real`, coefficient vector, or a degree-indexed representation | carrier and exact-degree encoding open |
| "roots" | complex roots after embedding real coefficients | `Polynomial.IsRoot`, `Polynomial.map Complex.ofRealHom`, or `rootSet` | multiplicity/carrier convention open |
| "real parts negative" | every root lies in the strict open left half-plane | `forall z, IsRoot ... z -> Complex.re z < 0` | recognizable conclusion component; not elaborated |
| Hurwitz determinants | finite alternating coefficient matrix, zero extension, first-`k` principal determinants | `Matrix (Fin n) (Fin n) Real`, indexed entry function, `submatrix`, `Matrix.det` | definitions and orientations open |
| positivity condition | every determinant for `1 <= k <= n` is strictly positive | finite universal quantification and ordered-field inequalities | index/empty cases open |
| criterion | stability iff all selected determinants are positive | `Iff` | likely source direction, but canonical root unaccepted |
| catalog `verified` | inventory metadata only | no declaration or proof object | explicitly rejected as evidence |

Lean's `Polynomial.coeff` order is ascending, unlike the source display: under an exact-degree
encoding, source `a_j` would be `p.coeff (n - j)`. A prospective zero-based Hurwitz entry uses
source index `2 * column + 1 - row`, guarded against a negative or greater-than-`n` index. This
adapter must be checked rather than copied as prose. Pinned mathlib's `docs/1000.yaml` mentions the
Routh-Hurwitz theorem as a wishlist/catalog entry only; it is not a Lean declaration or proof.

## Source and Lean exit gate

The statement phase must select and independently approve one exact source theorem and notation
crosswalk, including degree, coefficient order, matrix entries, determinant indexing, boundary
cases, proof boundary, translation, and errata. It must then implement the definitions, elaborate
and fingerprint the binder-complete Lean expression with minimal pinned imports, add checked
transports for any alternate encoding, and run removed-hypothesis, changed-domain, changed-scope,
and boundary mutations. Until then the provisional human-source status is `H1`, the machine status
is `M4`, and no statement or proof closure is claimed.
