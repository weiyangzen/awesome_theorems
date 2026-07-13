# Scope map

## Preserved repository scope

The repository fixes only the label `二分法`, the gloss `方程求根的线性方法`, the collective
attribution `众多数学家`, the period `古代`, importance "high," and an untrusted `已验证` status.
This identifies bisection as a numerical root-finding method and describes its rate only as linear.
It supplies no bibliographic source, theorem locator, definition, premise, recurrence, or
conclusion.

The intake preserves only that topic boundary. It does not infer a canonical proposition from the
usual sign-changing-interval presentation.

## Proposition-changing decisions

An approved source correction must freeze:

- the function, domain and codomain, scalar or ordered topological structure, and exact equation;
- the initial endpoints, their order, the interval convention, continuity domain, and oriented or
  unoriented endpoint sign hypotheses;
- the endpoint-root convention, midpoint formula, sign test, tie behavior, retained half, and exact
  recursive or iterative definition of both endpoint sequences;
- the reported approximant, such as midpoint or an endpoint, and whether the theorem is about the
  nested intervals, a chosen point sequence, or both;
- the exact conclusion: recurrence totality, bracket preservation, interval nesting, root existence,
  convergence, limit is a root, a linear-rate/error inequality, finite iteration complexity,
  stopping correctness, or a conjunction;
- the error measure and constants, strict versus non-strict inequalities, natural-number indexing,
  tolerance conditions, and uniformity of every bound;
- exact real arithmetic, rational or interval arithmetic, floating point, or another computational
  model, plus any rounding and certificate assumptions; and
- all ordered binders, universes, typeclasses, excluded cases, and the separation from neighboring
  root-finding targets.

These choices yield inequivalent propositions. They are a resolution checklist, not a canonical
statement.

## Candidate families not credited

- Intermediate-value root existence for a continuous function with opposite endpoint signs.
- An exact bisection recurrence on real intervals.
- Preservation of ordered sign-changing brackets and nesting of all generated intervals.
- Convergence of endpoints or midpoint approximants to some root.
- A geometric width or point-error bound, often written using division by `2 ^ n`.
- A finite number of iterations sufficient for a specified positive tolerance.
- Correctness, termination, and rounding robustness of a finite-precision implementation.

No family in this list is selected or credited at intake.

## Explicit exclusions

- The intermediate value theorem alone. It provides an existence substrate but no bisection
  recurrence, bracket invariant, convergence result, rate, complexity, or implementation theorem.
- Newton, secant, or fixed-point iteration (`THM-M-1440`, `THM-M-1441`, and `THM-M-1443`), even if
  they also find roots or have iterative encodings.
- Discrete binary search or the pinned `norm_num` metaprogram that uses interval halving to find a
  natural power certificate.
- A theorem that assumes the desired root, invariant, convergence, error estimate, or solver
  correctness as a hypothesis or structure field.
- A constant, affine, polynomial, or other toy function offered as the general method theorem.
- A finite sampled trajectory, plot, floating-point run, or empirical stopping event presented as
  a mathematical convergence theorem.
- Pinned mathlib's intermediate-value or geometric-decay APIs without an accepted source-to-target
  mapping.
- The untrusted catalog label `已验证` as evidence of human proof or kernel closure.

## Degenerate and boundary scope

The statement phase must decide reversed and equal endpoints, endpoint roots, a midpoint root,
same-sign endpoints, both sign orientations, zero sign products, discontinuity, multiple roots,
flat zero intervals, uniqueness versus convergence to some root, zero iterations, midpoint tie and
branch conventions, zero or negative tolerances, strict versus non-strict estimates, and exact
versus approximate arithmetic. None is silently excluded at intake.

## Formal boundary

No canonical Lean expression is frozen. At pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, `intermediate_value_Icc`,
`intermediate_value_Icc'`, and `intermediate_value_uIcc` elaborate as adjacent root-existence
substrates. `tendsto_pow_atTop_nhds_zero_of_lt_one` is adjacent to a possible geometric-rate proof.
The only explicit pinned source phrase "bisection method" is the unrelated
`Tactic.NormNum.findNotPowerCertificateCore` metaprogram for natural power certificates. These
interfaces demonstrate feasibility and ambiguity only. They select no source proposition and
receive no statement or proof credit.
