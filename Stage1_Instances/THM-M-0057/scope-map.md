# THM-M-0057 scope map

## Preserved theorem family

The intake preserves the catalog's Hoffman-Wielandt family: a global perturbation bound comparing
the eigenvalue multisets of two finite complex normal matrices to the Frobenius norm of their
difference. The dependent statement phase must select the exact source proposition. The familiar
candidate described below is a scope lead, not the frozen target.

For normal `A, B in C^(n x n)` with eigenvalues `lambda_i` and `mu_i` counted with algebraic
multiplicity, a standard form says that some permutation `pi` satisfies

```text
(sum_i |mu_(pi i) - lambda_i|^2)^(1/2) <= ||B - A||_F.
```

The squared inequality is mathematically expected to be equivalent after nonnegativity checks,
but no alternate encoding is credited until a checked transport is attached to an accepted root.

## Decisions required at statement freeze

1. Preserve and independently review a lawful primary or authoritative source edition, exact
   theorem locator, incorporated definitions, assumptions, conclusion, proof boundary, and errata.
2. Fix `n`, the matrix index type (`Fin n` or another finite type), universes, decidable equality,
   and whether dimension zero is included.
3. Define complex normality as `A * Aᴴ = Aᴴ * A`, `IsStarNormal A`, an operator predicate, or a
   checked equivalent encoding; both matrices must carry the correct hypothesis.
4. Represent both eigenvalue multisets with algebraic multiplicity and prove that the chosen
   enumerations are complete. A set-valued spectrum loses multiplicity and is insufficient.
5. Fix the permutation type and direction, including whether it reindexes the first or second
   eigenvalue enumeration and how arbitrary finite index types are transported.
6. Select the Frobenius norm instance/definition and the exact orientation of the matrix
   difference. Decide the square-root form versus the squared-sum form.
7. Freeze ordered binders, all hypotheses, the conclusion, minimal imports, foundation/TCB
   profiles, checked alternate transports, and the required statement mutations.

## Degenerate and boundary cases

Source and statement review must explicitly cover zero-by-zero and one-by-one matrices; identical,
zero, scalar, diagonal, Hermitian, unitary, and repeated-eigenvalue matrices; eigenvalue
multiplicity and nonunique enumerations; repeated spectra with many valid matchings; zero
Frobenius distance; conjugate-transpose and permutation conventions; and the square-root
nonnegativity needed to transport to a squared inequality. No case is excluded at intake.

## Excluded substitutions

- A perturbation bound only for Hermitian, self-adjoint, diagonal, commuting, or fixed-dimension
  matrices is a specialization, not the normal-matrix theorem.
- Weyl's ordered Hermitian eigenvalue inequalities, Bauer-Fike, Elsner bounds, spectral variation
  for a nonnormal matrix, Gershgorin disks, pseudospectrum bounds, and singular-value perturbation
  are different results.
- The spectral theorem or unitary diagonalizability alone does not supply the joint eigenvalue
  matching inequality.
- A set-level Hausdorff distance between spectra discards algebraic multiplicity and cannot replace
  the permutation-matching sum.
- An arbitrary ordering comparison without an existential permutation is stronger or false in
  general and is not a faithful substitute.
- A hypothesis or structure storing the required permutation or inequality is circular.
- A theorem name, source citation, API `#check`, numerical experiment, or the catalog's untrusted
  status supplies no source or proof credit.

## Neighbor boundaries

`THM-M-0055` owns the Rayleigh quotient theorem and `THM-M-0056` Weyl's inequality; their
Hermitian/self-adjoint eigenvalue machinery may become dependencies but cannot replace this
normal-matrix matching theorem. `THM-M-0058` owns the von Neumann trace inequality and
`THM-M-0059` Hadamard's inequality. No status crosses these target boundaries by proximity.

## Formal boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, `IsStarNormal`
expresses star-normality and the Frobenius norm modules define the relevant entrywise matrix norm.
Matrix spectrum and eigenspace APIs exist. `Matrix.IsHermitian.eigenvalues` and the Hermitian
spectral theorem provide an indexed real spectrum for a strict specialization. The bounded intake
search found no analogous indexed spectral theorem for arbitrary normal complex matrices and no
Hoffman-Wielandt root. The probe is discovery evidence only; it does not freeze an expression,
transport, mutation suite, discovery protocol, obligation registry, or proof body.
