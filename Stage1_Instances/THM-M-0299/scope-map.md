# Scope map

## Preserved theorem family

The intake preserves the classical Calderon-Zygmund strong-`L^p` boundedness family named by the
catalog. A typical modern formulation begins with a singular-integral operator associated with a
kernel on Euclidean space and concludes that the operator extends boundedly on `L^p` for
`1 < p < infinity`. That description is a source-search lead, not a frozen proposition: several
inequivalent theorems fit it.

## Decisions required at statement freeze

1. Select and independently approve an immutable primary or authoritative theorem passage, with
   exact theorem/page locator, incorporated definitions, proof boundary, and errata disposition.
2. Fix the operator class: a homogeneous convolution kernel, a translation-invariant operator, or
   a general standard Calderon-Zygmund kernel and operator.
3. Fix the ambient domain, dimension, scalar field, measure, source and target function spaces,
   almost-everywhere quotient conventions, and every universe and typeclass context.
4. Define the off-diagonal kernel representation, size bound, regularity hypothesis (for example
   Holder, Dini, or Hormander), cancellation condition, and all constants and normalizations.
5. Define truncations and the limiting operator: pointwise principal value, almost-everywhere
   limit, convergence in an `L^p` norm, or bounded extension from a dense test-function domain.
6. Decide whether initial `L^2` boundedness is an assumption, an intermediate result derived from
   cancellation or Fourier arguments, or part of the conclusion. Assuming the desired `L^p`
   mapping property itself is prohibited.
7. Freeze the exponent representation and range, normally `1 < p < infinity`, and decide whether
   weak type `(1,1)`, `L^infinity` to BMO, maximal-truncation, or endpoint assertions are part of the
   root or only proof ingredients/consequences.
8. State whether the conclusion is existence and uniqueness of a bounded extension, a quantitative
   norm inequality, almost-everywhere principal-value existence, or a conjunction, and specify the
   allowed dependence of its constant on dimension, exponent, kernel, and operator bounds.
9. Freeze ordered binders, hypotheses, conclusion, foundation/TCB/computation profiles, alternate
   encodings, and checked transports before any obligation tree or proof credit is considered.

## Boundary and degenerate cases

Source review must resolve zero and identity operators; zero or trivial measures; low dimension;
real versus complex scalars; compactly supported smooth, bounded compactly supported, Schwartz,
and completed `L^p` domains; diagonal and null-set behavior of the kernel; changes on almost-
everywhere equivalent representatives; vanishing or nonintegrable kernels; the cases `p = 1` and
`p = infinity`; principal values that exist only on a dense class; and uniqueness of the extension.
No case is silently included or excluded during intake.

## Excluded substitutions

- `THM-M-0298`, the Calderon-Zygmund decomposition, is a possible proof ingredient, not this
  boundedness conclusion.
- `THM-M-0352`, the broad Calderon-Zygmund theory target, cannot choose this target's exact root.
- `THM-M-0350`, Hilbert-transform boundedness, and a Riesz-transform-only theorem are special
  operators, not substitutes for the general family without a source identity decision.
- `THM-M-0364`, the `T(1)` theorem, has distinct generalized-operator testing hypotheses and an
  `L^2` criterion.
- `THM-M-0366`, Cauchy-integral boundedness, and toy or finite-kernel estimates are separate results.
- `THM-M-1171`, the PDE second-derivative estimate, is a consequence/application with a different
  canonical statement.
- Weak type `(1,1)`, maximal-truncation control, pointwise principal-value existence, or `p = 2`
  alone does not silently replace strong `L^p` boundedness for the source-selected range.
- A supplied `ContinuousLinearMap`, a structure field, or a hypothesis already asserting the
  desired bound is circular interface evidence, not a proof of the operator theorem.
- Generic `Lp`, integral, Fourier, or operator APIs; a theorem name; a numerical experiment; or the
  untrusted `已验证` label supplies no exact-statement or proof credit.

## Intake boundary

The source family and proposition-changing decisions are mapped, but the exact claim is not. The
statement phase must keep the canonical Lean target null until a source reviewer makes and approves
all choices above. The narrow pinned-mathlib search is intake discovery only, not an exhaustive
anchor audit or an absence proof.
