# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:9817-9822` supplies exactly the title `稳定流形定理`, the
attribution `众多数学家` (many mathematicians), the twentieth century, the gloss
`双曲平衡点的稳定与不稳定流形`, importance "high," and status `已验证`. Git provenance places all
six uncited lines in repository commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record
contains no phase space, equation or map, definition, binder, hypothesis, conclusion, source,
proof, erratum, or formal artifact.

`Docs/Stage0_Blueprint.md:36615-36640` repeats the gloss while explicitly leaving the exact
definitions and premises, proof route, dependency graph, equivalent formulations, axioms, machine
status, and artifact links open. Its generic planning text about a known closed result is not
source evidence. The rev-5.6 manifest retains `已验证` only as `source_status_untrusted` and resets
the target to `L0 / rework_required`.

## Literal crosswalk

| Catalog phrase | Necessary mathematical component | Prospective Lean component | Intake status |
|---|---|---|---|
| "hyperbolic equilibrium" | an autonomous vector field, equilibrium, derivative/linearization, and spectral gap excluding the imaginary axis | vector field and integral curves or flow; derivative; an explicit hyperbolicity predicate | dynamics, phase space, and predicate absent |
| "stable manifold" | local or global points converging in forward time, with manifold, tangency, and invariance clauses | convergence filter; orbit/flow; manifold chart or graph; smooth embedding/immersion | exact set and conclusion bundle absent |
| "unstable manifold" | backward-time convergence and an inverse/complete negative-time orbit | group-valued flow or source-specified local inverse; corresponding convergence predicate | backward-time semantics absent |
| "stable and unstable" | both branches, their stable/unstable splitting, dimensions, rates, and conjunction/composition | paired subspaces and two leaf constructions | no spectral split or clause list supplied |
| `已验证` | untrusted inventory label | no proposition or proof object | explicitly rejected as evidence |

The noun phrase does not quantify over a system or assert existence. Treating the familiar theorem
as implicit would still require choosing among materially different formulations.

## Inspected discovery source

Gerald Teschl, *Ordinary Differential Equations and Dynamical Systems*, Graduate Studies in
Mathematics 140, American Mathematical Society (2012), DOI `10.1090/gsm/140`, Section 9.2,
printed pages 255-260, was inspected in the author's preliminary version made available with the
publisher's permission. It is a stable modern source-family candidate, not the uncited catalog's
accepted source.

| Source locator | Source component | Prospective target component | Intake disposition |
|---|---|---|---|
| equations (9.7), (9.9), (9.10) | global stable/unstable sets, exponential-rate local sets, and local stable/unstable manifolds | exact convergence, neighborhood, orbit, and rate definitions | candidate definitions only |
| definition before (9.9) | hyperbolic fixed point means the Jacobian has no eigenvalue with zero real part | derivative and real-part spectral-gap predicate | candidate only; finite-dimensional ODE convention |
| Theorem 9.3, pp. 257-258 | rate-indexed stable graph, tangency, and nesting under shifted hyperbolicity | graph map over the selected spectral subspace plus smoothness/tangency | distinct stronger technical branch |
| Theorem 9.4, p. 259 | local stable and unstable `C^k` graphs, tangency, and exponential estimates | paired graph/manifold existence and estimates | named stable-manifold candidate; notably no explicit hyperbolicity premise in this wording |
| Theorem 9.5, p. 259 | under a hyperbolic fixed point, local-orbit characterization and `W^+/- = M^+/-` | local/global orbit predicate and set equality | distinct hyperbolic identification result |

The catalog's word "hyperbolic" aligns most directly with Theorem 9.5's premise, while its word
"manifolds" aligns with Theorem 9.4's construction; selecting one, the other, or their conjunction
changes the theorem. The source also works in a finite-dimensional continuous-time setting and
does not authorize a diffeomorphism, Banach-space, normally hyperbolic, or Pesin substitution.

The inspected Section 9.2 extract has SHA-256
`a0a4aa8051f349eb10eae28160b71c6d030a31973f71bf78b25e791570ad56e0`. This hash records the
discovery extract used for discrimination; the mutable remote PDF is not admitted as immutable H0
evidence, and no complete errata, historical genealogy, translation, or independent review is
claimed.

## Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the intake probe
elaborates generic integral-curve, flow, invariant-set, fixed-point, orbit, and smooth-embedding
interfaces. A bounded exact-name search found no stable/unstable/invariant-manifold declaration.
The absence of an exact catalog proposition prevents statement matching; the observations are not
a complete external audit or an absence claim beyond the searched closure.

The statement phase must obtain accountable source selection, freeze exactly which source clauses
are the root, record all incorporated definitions and assumptions, audit errata and translations,
and preserve the boundaries above. Only then may it fix ordered binders, universes, degenerate
cases, minimal imports, an elaborated expression and fingerprint, alternate transports, and the
required statement mutations.
