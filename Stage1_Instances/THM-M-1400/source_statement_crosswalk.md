# Source-statement crosswalk

| Claim component | Repository source anchor | Prospective Lean representation | Intake assessment |
|---|---|---|---|
| Named theorem | `Docs/researches/math_theorems.md`, "Poincare-Bendixson定理" | namespace and declaration to be selected after source audit | The name identifies a theorem family, not an exact proposition |
| Historical attribution | Henri Poincare / Ivar Bendixson; year 1901 | documentation only | Metadata is not a primary-source edition or theorem locator |
| Source wording | `二维系统的极限集` (limit sets of two-dimensional systems) | an omega-limit-set predicate over a planar flow | Domain, dynamics, hypotheses, and conclusion are absent |
| Legacy expanded wording | `Docs/researches/physics_theorems.md`: bounded orbits of a two-dimensional continuous dynamical system tend to a fixed point or periodic orbit | a disjunction involving an equilibrium and a periodic orbit | Discovery wording only; "tend to" is ambiguous and can overstate standard omega-limit-set formulations |
| Blueprint scope | `Docs/Stage1_Blueprint.md`: map/flow definitions, invariance, fixed/periodic special cases, finite or compact cases | candidate auxiliary definitions and lemmas | Partial-verification plan, not the root statement |

The exact classical theorem has several variants. They differ on whether the phase space is an open
subset of the plane or a two-manifold, whether the vector field is continuously differentiable,
whether a forward orbit is contained in a compact set, whether its omega-limit set contains an
equilibrium, and whether the conclusion is that the omega-limit set is a periodic orbit or a larger
classification. Those choices affect the theorem and cannot be supplied from memory.

No primary mathematical source is cited by the repository entry. Therefore the human-source status
is `H4`: the source is too weak to freeze premise fidelity. Required source work is to locate a
specific edition, theorem number and page; transcribe its ordered assumptions and conclusion; check
errata; and map each clause to the eventual Lean binders. Until then there is no canonical formal
target, no statement fingerprint, and no claim that the metadata label `已验证` represents machine
verification.
