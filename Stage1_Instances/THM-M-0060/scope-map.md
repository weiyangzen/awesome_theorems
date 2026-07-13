# THM-M-0060 scope map

## Catalog claim held fixed

The repository title is `史密斯标准形定理` (Smith normal form theorem), with the gloss
`整数矩阵的等价标准形` (an equivalent normal form of integer matrices). Intake preserves both
strings. It does not infer dimensions, an equivalence relation, a diagonal normalization, or a
uniqueness clause from the untrusted `已验证` label.

## Candidate theorem family

The conventional modern family to assess at the statement gate is:

> A rectangular integer matrix can be transformed, by invertible changes of row and column bases,
> to a diagonal matrix whose nonzero diagonal entries may be normalized and ordered by divisibility.

This is a discovery candidate, not the accepted canonical claim. Some sources call diagonal
existence alone Smith form, while others include the divisibility chain, sign/associate
normalization, uniqueness of invariant factors, or a module decomposition. The repository does not
choose among them.

Pinned mathlib expresses an adjacent general-PID formulation. Given a finite basis for a module and
a submodule, `Submodule.exists_smith_normal_form_of_le` constructs bases in which the inclusion is
diagonal. `Module.Basis.SmithNormalForm` records the two bases, an index embedding, coefficients,
and the diagonal relation. It does not itself record a divisibility chain or canonical integer
representatives. `IntakeProbe.lean` checks these APIs only; they are not frozen as this target.

## Decisions required at statement

- Admit and independently review a pinpoint source theorem, incorporated definitions, proof, and
  correction/errata record.
- Fix whether the root is an arbitrary rectangular integer-matrix theorem, a general-PID theorem,
  a submodule-inclusion theorem, or a finitely generated module classification statement.
- Fix row and column dimensions, their orientation, and whether either may be zero.
- Define matrix equivalence: left/right multiplication by unimodular matrices, elementary
  operations, or change of bases with an explicitly checked transport.
- Fix diagonal shape for rectangular matrices, rank, zero entries, and the placement of zeros.
- Decide whether divisibility of consecutive nonzero diagonal entries is part of the root.
- Decide integer sign normalization, PID associate normalization, and existence versus uniqueness.
- Fix ordered binders, hypotheses, conclusion, universes, typeclasses, and all degenerate cases.
- Elaborate and fingerprint one exact expression, check alternate encodings, and mutation-test
  domain, dimensions, binder scope, hypotheses, and boundary cases.

## Boundary cases to resolve

- matrices with zero rows, zero columns, or both;
- the zero matrix, rank zero, and matrices with zero diagonal tail;
- one-row, one-column, square, wide, and tall matrices;
- full rank versus rank deficient matrices;
- units and sign associates, including whether diagonal entries must be nonnegative;
- repeated or equal invariant factors and strict versus non-strict divisibility;
- the zero ring if a general-PID formulation is considered;
- existence only versus uniqueness up to associates and all associated module/cokernel claims.

## Excluded substitutions

- `Submodule.smithNormalForm` used as the exact integer-matrix theorem without a source decision and
  checked matrix-to-submodule transport;
- a diagonal basis relation presented as if it also proves the divisibility chain or uniqueness;
- the structure theorem for finitely generated modules over a PID used without equivalence to the
  selected matrix statement;
- only square, full-rank, nonsingular, fixed-size, or already-diagonal matrices replacing the
  general accepted root;
- a field row-reduction or rank-normal-form theorem replacing the integral/PID result;
- Hermite normal form, Jordan normal form, singular value decomposition, or rational canonical form;
- a hypothesis or structure field that stores the desired normal form;
- computed examples, external computer algebra output, or unchecked certificates;
- the catalog label, theorem-name match, or intake probe used as source or proof credit.

## Neighbor boundaries

- `THM-M-0047` (LU decomposition) is triangular factorization, not integral left/right equivalence.
- `THM-M-0050` (Sylvester's law of inertia) is congruence classification of forms, not Smith form.
- `THM-M-0052` (Moore-Penrose inverse) concerns generalized inverses over analytic scalar domains.
- General module classification is a possible equivalent encoding only after a checked source and
  formal crosswalk; it does not automatically set this matrix theorem's scope.

## Profiles held open

Lean 4 dependent type theory and pinned mathlib are intended. Exact use of classical choice,
quotients, bases, noncomputability, decidable equality, and PID instances remains downstream. No
oracle, native shortcut, experiment, or external computation is eligible for proof credit.
