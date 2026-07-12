# Scope map

## Preserved catalog scope

The repository fixes target `THM-M-0256`, the label "Teichmuller theory," attribution to Oswald
Teichmuller, the year 1939, and the gloss "moduli space of Riemann surfaces." Importance "high"
and status `已验证` are catalog metadata, not source or kernel evidence. Intake preserves the
Riemann-surface deformation and moduli subject boundary without turning an object description into
a theorem.

## Proposition-changing decisions

An approved source correction must select one truth-valued root and freeze:

- the surface category: closed or bordered, compact or finite type, genus, punctures or labeled
  marked points, orientation, smoothness, and all low-complexity exceptions;
- the object being parameterized: conformal structures, complex structures, marked Riemann
  surfaces, quasiconformal equivalence classes, or another precisely sourced model;
- the marking and equivalence conventions, including isotopy versus homotopy, base surface,
  orientation preservation, labels, and the pure or full mapping class group;
- whether the target concerns Teichmuller space, a coarse moduli quotient, an orbifold, a stack, or
  a universal/infinite-dimensional variant;
- whether the desired result is existence and uniqueness of extremal maps, well-definedness of a
  quotient, a dimension/manifold/contractibility result, or a metric/geodesic theorem;
- every quasiconformal regularity, quadratic-differential, normalization, automorphism, stability,
  local/global, and boundary hypothesis; and
- all universes, ordered binders, quantifier dependencies, hypotheses, and conclusion clauses.

These choices produce inequivalent propositions. They form a resolution ledger, not a canonical
statement.

## Candidate families not credited

- Construction of Teichmuller space from marked finite-type Riemann surfaces.
- Teichmuller's existence and uniqueness theorem for extremal quasiconformal representatives.
- Identification of a Riemann-surface moduli space as a mapping-class-group quotient.
- Contractibility, cell/ball, dimension, or manifold properties of Teichmuller space.
- The Teichmuller metric, quadratic-differential parametrization, or geodesic results.

No family in this list is selected, asserted, or credited at intake.

## Neighboring target boundaries

`THM-M-0255` separately names quasiconformal mapping theory. `THM-M-0257` separately names the
Ahlfors-Bers result on the complex structure of Teichmuller space. `THM-M-0258` separately names a
boundary result for Teichmuller space. This target may eventually depend on checked results from
those dossiers, but it cannot absorb their statements or inherit their source or proof credit.

## Explicit exclusions

A generic quotient by a group action, manifold chart, orbit equivalence, or topological moduli
construction is not a Teichmuller theorem without a checked source-faithful bridge. A structure that
stores the desired moduli property as a field and then projects it is not a proof. The
Teichmuller-Tukey lemma and the ring-theoretic Teichmuller maps and lifts in pinned mathlib are
unrelated namesakes. Numerical pictures, meshes, finite samples, and the catalog word `已验证` also
supply no theorem evidence.

## Formal boundary

No canonical Lean expression is frozen. Pinned mathlib provides generic complex-manifold,
group-action, orbit-relation, and quotient APIs. A bounded repo-local and pinned-mathlib search
found no Teichmuller-space, Riemann-surface-moduli, extremal-quasiconformal, or quadratic-
differential target declaration. This is intake discovery only, not an exhaustive anchor audit or
a global absence claim.
