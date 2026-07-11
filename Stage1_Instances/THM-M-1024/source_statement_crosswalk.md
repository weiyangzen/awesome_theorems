# Source-statement crosswalk

| Claim component | Human source anchor | Planned Lean surface | Intake assessment |
|---|---|---|---|
| Infinite divisibility iff exponential representation | Ken-iti Sato, *Levy Processes and Infinitely Divisible Distributions*, Cambridge Studies in Advanced Mathematics 68 (1999), Theorem 8.1, pp. 37-38 | Predicate on a probability measure, equivalent to existence of triplet data | Primary theorem pinpointed; edition hash and line-by-line premise audit remain open (`H1`) |
| Gaussian term | Sato, Theorem 8.1, quadratic-form component | Symmetric positive-semidefinite operator on finite Euclidean space | Matrix/operator encoding and coefficient convention require exact checking |
| Jump term and integrability | Sato, Theorem 8.1, Levy measure component | Measure vanishing at zero with finite integral of `min 1 (norm x)^2` | Atom-at-zero and integrability must be expressed without weakening |
| Compensation convention | Sato, Theorem 8.1, canonical representation convention | Unit-ball indicator in the complex Bochner integral | Boundary choice `< 1` versus `<= 1` and induced drift transport must be reconciled against the edition before statement acceptance |
| Uniqueness of characteristics | Sato, Theorem 8.1, uniqueness clause | Uniqueness relative to the frozen truncation | Must not be silently dropped from the theorem package |

Bibliographic discovery anchor: ISBN 978-0-521-55302-5; Cambridge University Press. This citation is
not an immutable evidence receipt. The statement phase must inspect the pinned source pages, resolve
the unit-sphere boundary convention, and freeze an exact Lean expression. The source audit must then
record file identity, assumptions, corrections/errata, and an independent review.

No repo-local Lean declaration has been credited. Candidate searches belong to `ANCHOR_AUDIT`, only
after the exact statement is elaborated. In particular, nearby characteristic-function, convolution,
or Levy-process APIs cannot establish this probability-law equivalence merely by name similarity.

Required statement mutations include removing infinite divisibility, omitting the Levy integrability
condition, allowing an atom at zero, dropping positive semidefiniteness, reversing the Fourier sign,
changing the Gaussian factor, changing truncation, deleting uniqueness, specializing to dimension
one, and probing dimension zero. Each accepted alternative needs a checked transport rather than a
prose assertion.
