# Scope map

## Preserved catalog scope

The repository fixes only target `THM-M-1362`, the label `叉形分岔` (pitchfork bifurcation), the
gloss `对称性破缺的分岔` (a bifurcation of symmetry breaking), a collective twentieth-century
attribution, and an untrusted `已验证` status. Intake preserves this bifurcation-family boundary. It
does not turn the label into a proposition or select a textbook example or theorem without source
authority.

## Proposition-changing decisions

An approved source correction must freeze all of the following before statement elaboration:

- whether the system is a scalar algebraic equilibrium equation, scalar autonomous ODE, map,
  finite-dimensional vector field, Banach-space equation, flow, or another model;
- parameter and phase spaces, scalar field, domains and universes, distinguished parameter and
  equilibrium, topology or smooth structure, regularity class, and time convention;
- the acting symmetry, usually a `Z2` involution or oddness condition, and whether equivariance is
  global, local, exact, or only a condition on a reduced equation;
- local versus global scope and the equivalence notion: literal roots, smooth coordinate changes,
  topological conjugacy, orbital equivalence, center-manifold reduction, or normal-form agreement;
- the critical linearization and kernel/cokernel dimensions, eigenvalue crossing or
  transversality, genericity, codimension, and source-specific nondegeneracy coefficients;
- whether the result is supercritical or subcritical, which side of the parameter contains the two
  symmetry-related branches, and whether existence, uniqueness, smoothness, stability, exchange of
  stability, or classification is assumed or concluded; and
- one exact truth-valued conclusion with ordered binders, all exceptional cases, and a complete
  source and proof boundary.

These choices define inequivalent propositions. They are a resolution ledger, not a canonical
claim.

The literal gloss also lacks a quantifier. Not every symmetric parameter family undergoes a
pitchfork: constant families and families with vanishing transverse or cubic coefficients provide
immediate boundary cases. An existential reading needs a selected system. A definitional reading
only names a phenomenon. Intake cannot silently rewrite the gloss as a universal normal-form
theorem, an example calculation, an existence result, or a stability classification.

## Candidate families not credited

- The scalar supercritical example `x' = mu*x - x^3`, whose equilibria are `0` for every `mu` and
  the pair `+/-sqrt(mu)` for positive `mu`, together with its stability classification.
- The scalar subcritical sign variant `x' = mu*x + x^3`, with a different branch side and stability
  behavior.
- A local pitchfork theorem for an odd smooth scalar family under derivative and nondegeneracy
  hypotheses at a critical equilibrium.
- An equivariant branching lemma or a center-manifold/normal-form reduction for a
  finite-dimensional or Banach-space dynamical system.
- A definition or characterization of a pitchfork bifurcation under a selected conjugacy or branch
  equivalence relation.

No family in this list is selected, conjoined, asserted, or credited at intake.

## Neighbor boundaries and exclusions

- `THM-M-1358` is the generic bifurcation-theory target; `THM-M-1359` saddle-node,
  `THM-M-1360` Hopf, and `THM-M-1361` transcritical bifurcation remain distinct. Their statements
  and future evidence cannot replace or close this target.
- `THM-M-1363` chaos theory and `THM-M-1366` structural stability are related dynamical topics,
  not pitchfork statements.
- A symmetry predicate, an odd vector field, a zero eigenvalue, or a vanishing derivative alone
  does not establish the two nontrivial branches or their stability.
- A calculation for one cubic polynomial normal form cannot substitute for a general local
  theorem. Conversely, a general theorem cannot be silently reduced to that example.
- A bifurcation diagram, numerical continuation run, phase plot, simulation, or solver trajectory
  is not a kernel-checked proof of any source-selected conclusion.
- A structure field or hypothesis that directly assumes the desired branch diagram supplies an
  interface, not a proof.
- Generic ODE, flow, fixed-point, derivative, smoothness, and polynomial APIs alone receive no
  statement or proof credit.
- The catalog label `已验证` supplies neither a human proof nor a machine artifact.

## Boundary cases

The statement phase must decide constant parameter families; empty, singleton, or
zero-dimensional parameter and phase spaces; nonisolated or nonunique equilibria; one-sided
parameter neighborhoods; nonunique or finite-time trajectories; trivial or nonfaithful symmetry;
symmetry breaking already present away from the critical value; higher-dimensional critical
kernels; repeated or additional imaginary-axis eigenvalues; resonance; vanishing transversality or
normal-form coefficients; higher-order degeneracy; imperfect pitchforks caused by symmetry-breaking
perturbations; supercritical versus subcritical sign; parameter reversal; coordinate and time
changes; and stability at the critical parameter.

## Formal boundary

No canonical Lean expression is frozen. At pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, the intake probe checks generic derivative,
smoothness, integral-curve, flow, and fixed-point interfaces. A bounded local exact-topic search
found no `pitchfork` or `bifurcat` occurrence in pinned mathlib or repo-local Lean sources. This is
an intake discovery observation, not an exhaustive anchor audit or a global absence claim.
