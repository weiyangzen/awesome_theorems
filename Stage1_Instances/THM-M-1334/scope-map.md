# Scope map

## Preserved repository scope

The repository fixes target `THM-M-1334`, the title
`柯西-科瓦列夫斯卡娅定理`, attribution to Augustin Cauchy and Sofia
Kovalevskaya, the year 1875, and the gloss `解析ODE的解析解` ("analytic solution
of an analytic ODE"). The manifest places it in ordinary differential
equations. Importance "high" and status `已验证` are catalog metadata, not
source or kernel evidence.

The intake therefore preserves an analytic ODE initial-value-problem family.
It does not silently replace that family with the historically broader PDE
theorem or with a convenient theorem already present in mathlib.

## Leading ODE candidate

Kepley and Zhang, arXiv:`1912.03836v3`, Theorem 1 (PDF page 2), gives a strong
candidate matching the catalog gloss:

- `V` is an open subset of real `n`-space;
- `f : V -> R^n` is an analytic autonomous vector field;
- `x0` belongs to `V`; and
- the initial-value problem `x' = f(x)`, `x(0) = x0` has a unique solution
  analytic on some open interval containing zero.

Theorem 11 (beginning on PDF page 20, with proof continuing on page 21)
restates the same result at the end of the constructive development, but its
displayed wording omits the interval phrase present in Theorem 1. This source
is a modern proof candidate and a resolution aid. It is not an approved
canonical root, an H0 source crosswalk, or Lean evidence.

## Proposition-changing decisions

An approved statement phase must freeze:

1. Whether the target is the catalog-aligned ODE specialization or the
   historical PDE Cauchy problem, and why that choice preserves `THM-M-1334`.
2. For an ODE target, whether the vector field is autonomous or time-dependent,
   real analytic or holomorphic, and finite-dimensional or Banach-space valued.
3. The open state-space domain, initial time and point, and whether the vector
   field is required analytic on a neighborhood of the initial point or on the
   whole stated domain.
4. The exact definition of vector-valued analyticity and the relationship
   between componentwise, Fréchet-power-series, real-analytic, and holomorphic
   encodings.
5. The solution representation: a function on an open interval, a total
   function plus a local predicate, a germ, or a maximal solution.
6. Whether uniqueness is local, germ-level, or among solutions on a shared
   interval, and whether the theorem claims existence only or existence plus
   uniqueness.
7. Whether the interval is symmetric, merely open around the initial time, or
   represented by an explicit positive radius, including endpoint behavior.
8. All ordered quantifiers, universe/typeclass assumptions, transports between
   `Fin n -> R` and Euclidean-space encodings, and every degenerate case.

For a PDE target, the statement phase must instead freeze the PDE order and
system shape, analytic coefficients and initial data, noncharacteristic
initial hypersurface, normal-derivative form, compatibility conditions, local
neighborhood, and uniqueness class. Those data cannot be inferred from the ODE
gloss.

## Boundary cases

The exact source must decide `n = 0`, empty or disconnected `V`, an initial
point on or outside the boundary, a zero or constant vector field, initial time
zero versus arbitrary time, zero-radius neighborhoods, uniqueness after
shrinking two different solution intervals, and real solutions obtained by
restriction of complex analytic solutions. None is resolved by this intake.

## Explicit exclusions

- The general PDE Cauchy-Kovalevskaya theorem substituted solely because it is
  the historically standard namesake.
- Picard-Lindelof existence and uniqueness under Lipschitz continuity without
  the requested analyticity conclusion.
- The fact that analytic maps are smooth, or that a pre-existing solution is
  `C^n`, substituted for existence of an analytic solution.
- A polynomial, scalar, linear, or one-dimensional special case presented as
  the full source target.
- A structure that assumes the desired solution, analyticity, or uniqueness as
  a field and a theorem that merely projects it.
- A numerical power-series approximation, truncated recurrence, unchecked
  majorant computation, oracle, or placeholder declaration.
- The catalog label `已验证` or a passing API probe treated as source or proof
  evidence.

## Formal boundary

No canonical Lean expression is frozen. Pinned mathlib exposes integral-curve,
Picard-Lindelof, analytic-function, and finite-dimensional Euclidean APIs. It
also contains an explicit TODO to extend a Picard regularity lemma to the
analytic case. A bounded exact-topic name search found no Cauchy-Kovalevskaya
declaration. These are feasibility and blocker observations only, not an
exhaustive anchor audit, statement elaboration, or proof evidence.
