# Scope map

## Received claim

`Docs/researches/math_theorems.md:1626-1631` supplies only the title `最大模原理`, the attribution
Karl Weierstrass, the year 1875, and `全纯函数的模在内部不能达到最大值` ("the modulus of a
holomorphic function cannot attain a maximum in the interior"). It gives no bibliographic source,
definitions, assumptions, theorem locator, proof boundary, exception, or exact formal artifact.

Read literally, the gloss is false: a constant holomorphic function attains the same modulus at
every interior point. Intake preserves this defect rather than silently repairing it. A later
statement must use an accepted source to decide whether the root is an impossibility theorem for
nonconstant functions or a rigidity theorem concluding constancy.

## Candidate classical boundary

A familiar global scalar form says that if a holomorphic function on a connected open domain
attains its modulus maximum at a point of the domain, then it is constant on that domain. A local
form says that a holomorphic scalar function with a local modulus maximum is locally constant. If
the function is holomorphic throughout a connected domain, analytic continuation or the
open-and-closed local-constancy argument can then propagate constancy globally. For functions into
a general complex normed space,
the same assumptions may yield only constancy of the norm unless the codomain has an appropriate
strict-convexity property.

These are candidate boundaries only. The statement phase must source and fix:

- the ambient domain: a subset of `Complex`, a complex normed space, a Riemann surface, or another
  setting;
- openness, nonemptiness, connectedness or preconnectedness, and whether they are explicit or
  incorporated into the word "domain";
- scalar-valued versus vector-valued functions and any strict-convexity assumptions;
- holomorphicity on the whole domain, differentiability in a neighborhood of one point, or another
  regularity contract;
- a local maximum, maximum on a specified set, strict maximum, or maximum on a closure;
- membership of the maximizing point and the precise meaning of "interior";
- constancy of the function, equality of its norm, local eventual equality, or global equality on
  a connected component; and
- theorem versus contrapositive form, including the explicit nonconstant premise.

## Pinned Lean candidate boundary

At mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, module
`Mathlib.Analysis.Complex.AbsMax` explicitly documents several results called the maximum modulus
principle. `Complex.norm_eventually_eq_of_isLocalMax` is local and codomain-general, with a norm
conclusion. `Complex.eventually_eq_of_isLocalMax_norm` adds strict convexity and concludes local
value equality. `Complex.norm_eqOn_of_isPreconnected_of_isMaxOn` and
`Complex.eqOn_of_isPreconnected_of_isMaxOn_norm` are global connected-open-set versions with norm
and value conclusions, respectively.

The same module also provides boundary forms such as
`Complex.exists_mem_frontier_isMaxOn_norm` and
`Complex.norm_le_of_forall_mem_frontier_norm_le`. These are direct exact-topic interfaces, hence
the provisional family assessment `M3`, but none receives canonical-root identity, proof-body, or
completion credit at intake.

## Boundary cases to resolve

- Constant nonzero functions and the zero function, which refute the literal no-attainment gloss.
- Empty, singleton, nonopen, or disconnected domains and isolated points.
- A maximum at a boundary point versus a point interior to the domain.
- Local versus global maxima, non-strict versus strict maxima, and maximum of norm versus squared
  norm.
- A whole-space domain, bounded versus unbounded domains, and whether closure continuity is needed.
- Scalar `Complex` codomain versus a general normed complex codomain that is not strictly convex.
- Degenerate domain or codomain types and a domain component containing only the maximizing point.

No boundary case is silently excluded before an exact proposition is selected.

## Explicit exclusions

- The minimum modulus principle, open mapping theorem, Liouville theorem, Schwarz lemma, or
  Phragmen-Lindelof principle substituted without a checked exact transport.
- A boundary maximum theorem substituted for the catalog's interior rigidity family.
- A closed-ball-only, unit-disk-only, polynomial-only, harmonic-only, or fixed-function special
  case as the unrestricted root.
- A statement for arbitrary continuous or real differentiable functions.
- A premise or structure that already stores the desired constancy.
- The literal false gloss, catalog `已验证` label, a matching declaration name, or the API probe
  used as statement identity or proof credit.

## Statement retry condition

An accountable source owner must preserve and hash one lawful primary or authoritative edition,
select an exact theorem and all incorporated definitions, account for the constant-function
exception and every premise and conclusion, inspect corrections or errata, and obtain independent
source review. The statement phase can then encode that same claim, establish minimal imports,
serialize its elaborated expression and environment, check alternate transports, and execute the
required semantic mutations.
