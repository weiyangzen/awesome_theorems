# Source-statement crosswalk

## Available repository source

The source record is `Docs/researches/math_theorems.md`, lines 4438-4443. It provides a title,
attribution, year, and one-line gloss, but no bibliography, theorem label, coefficient convention,
manifold hypotheses, or choice between weak and strong inequalities. `Docs/Stage0_Blueprint.md`
adds no exact mathematical scope.

## Candidate primary sources

- Marston Morse, "Relations between the Critical Points of a Real Function of n Independent
  Variables," *Transactions of the American Mathematical Society* 27 (1925), 345-396.
- Marston Morse, *The Calculus of Variations in the Large*, American Mathematical Society
  Colloquium Publications, volume 18 (1934).

These are bibliographic discovery candidates, not `H0` evidence. This intake did not inspect and
hash a stable scan, select an exact theorem/page, translate the historical terminology, or check
errata. The repository year suggests the monograph but does not uniquely determine a theorem.

## Crosswalk

| Repository/source phrase | Provisional mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| "Morse inequalities" | weak and/or strong inequalities | one exact proposition or a source-faithful theorem package | family identified; root open |
| "Betti numbers" | ranks/dimensions of homology groups | concrete homology theory, coefficients, degree, and finite-dimensionality | coefficients and API open |
| "Morse indices" | counts `c_k` of nondegenerate critical points of index `k` | derivative/Hessian, nondegeneracy, index, critical set, and finite count | encoding open |
| alternating form | `c_k-c_(k-1)+... >= b_k-b_(k-1)+...` with parity-sensitive endpoint | finite sums and a fixed sign/order convention | expected strong form; not frozen |
| polynomial form | `M_f-P_M=(1+t)Q`, coefficients of `Q` nonnegative | polynomial definitions plus checked equivalence to inequalities | alternate candidate only |
| `verified` | inventory metadata | no human-proof or kernel evidence | no proof credit |

## Source and machine boundary

No theorem-specific Lean artifact for `THM-M-0599` exists in the repository. Intake does not claim
that pinned mathlib has or lacks a terminal Morse-inequalities theorem; the dependency-ordered
anchor audit must make that determination only after the exact statement is elaborated. Nearby
Morse-index and critical-point artifacts concern different results and cannot close this target.

Before `H0`, an independent reviewer must approve a fixed edition, theorem/page, definitions, all
hypotheses, coefficient and sign conventions, historical-to-modern translation, and errata record.
Before statement credit, the approved row-level mapping must reach an elaborated Lean expression,
with checked transports for every credited weak, strong, or polynomial encoding.
