# Scope map

## Preserved source scope

The repository fixes only the Chinese label `复动力系统` ("complex dynamical systems"), the gloss
`复解析映射的动力学` ("dynamics of complex analytic maps"), an attribution to many
mathematicians in the twentieth century, importance "high," and the untrusted status `已验证`. It
supplies no bibliography, mathematical definition, premise, conclusion, or formal artifact. Intake
therefore preserves only a field boundary: iteration-related questions for maps with genuinely
complex-analytic structure.

This boundary does not select a canonical proposition. In particular, "complex analytic map" may
mean a holomorphic self-map of a plane domain, an entire or meromorphic map, a polynomial, a
rational self-map of the Riemann sphere, or a map between complex manifolds. Their dynamics and
even the totality of their iterates require different data.

## Proposition-changing decisions

An approved target correction must select one immutable primary-source proposition and freeze:

- the phase space: `Complex`, a source-defined domain, the extended complex plane/Riemann sphere,
  or a complex manifold, including topology, charts, universes, and compactness assumptions;
- the map class: holomorphic, analytic on a domain, entire, meromorphic, polynomial, rational, or
  another exact class, including whether it is a self-map and its degree and nonconstancy clauses;
- how iterates are defined when a map is partial or has poles, and whether zero iteration is in
  scope;
- the orbit or invariant-set predicates, including forward/backward scope and exceptional or
  critical points;
- the exact conclusion family: regularity of iterates, periodic-point behavior, normality or
  stability, Julia/Fatou decomposition, connectivity, critical-orbit criterion, local
  linearization, entropy, parameter-space behavior, or another source result;
- the placement of every universal, existential, local, and uniform quantifier and the exact
  topology or convergence notion; and
- all constant, degree-zero/one, empty-domain, pole, infinity, critical, parabolic, and boundary
  cases.

These choices produce inequivalent propositions. They are a resolution checklist, not a theorem
statement.

## Candidate families not credited

- Closure of holomorphic or analytic maps under finite iteration.
- Fixed-point, periodic-point, multiplier, attraction, repulsion, or preperiodicity results.
- A Julia/Fatou-set definition or theorem based on normality or stability of the iterates.
- Polynomial or rational-map results relating critical orbits to invariant-set connectivity.
- Local linearization around an indifferent or attracting fixed point.
- A global classification, equidistribution, entropy, rigidity, or no-wandering-domain theorem.

No family in this list is selected, asserted, or credited at intake. A generic iterate identity is
not enough: it omits the complex-analytic content named by the catalog.

## Explicit exclusions

The repository separately catalogs Julia sets (`THM-M-1428`), Fatou sets (`THM-M-1429`), the
Mandelbrot set (`THM-M-1430`), the Douady-Hubbard theorem (`THM-M-1431`), Yoccoz's theorem
(`THM-M-1432`), the Brjuno condition (`THM-M-1433`), and Sullivan's no-wandering-domain theorem
(`THM-M-1434`). None may be chosen merely because it is a familiar theorem of complex dynamics.

Also excluded are a definition or structure containing the desired conclusion as a field, a
tautological preservation theorem, a real-dynamics theorem with no checked complex-analytic bridge,
one convenient polynomial example, and numerical orbit or escape-time experiments. Such artifacts
cannot identify or close the received catalog item.

## Formal boundary

No canonical Lean expression is frozen. Pinned mathlib provides adjacent APIs for `AnalyticAt`,
`MeromorphicAt`, function iteration, and fixed and periodic points. The intake-only name search
found no named Julia-set, Mandelbrot-set, complex-dynamics, or holomorphic-dynamics declaration; the
unrelated algebraic-geometry `RationalMap` API does not supply the intended analytic dynamics.
These are substrate and negative-discovery facts only, not a complete anchor audit, exact-statement
elaboration, or machine-proof evidence.
