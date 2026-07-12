# Scope map

## Received scope

The repository fixes only `皮卡-林德勒夫定理`, the attribution Picard/Lindelof, the year 1894,
and `ODE解的存在唯一性` ("existence and uniqueness of ODE solutions"). It supplies no primary
source, definitions, assumptions, theorem locator, proof boundary, or exact formal artifact.

## Candidate mathematical boundary

An eventual exact target may be called Picard-Lindelof only after a reviewed source fixes all of
the following:

- real time and the state space: scalar, `Real^n`, finite-dimensional normed space, or Banach
  space;
- an autonomous field `f : E -> E` or time-dependent field `f : Real -> E -> E`;
- the field domain, initial time and value, and the neighborhood on which all assumptions hold;
- continuity in time and the exact local or global Lipschitz condition in the state variable,
  including whether its constant is uniform in time;
- any boundedness premise and the quantitative relation between the spatial radius and time
  interval;
- an open, closed, one-sided, or two-sided nontrivial interval and the derivative convention at
  endpoints;
- the regularity and encoding of a solution, and whether the conclusion is one solution, a local
  flow, or continuous/Lipschitz dependence on initial data; and
- the set or interval on which uniqueness is asserted and the condition that compared solutions
  remain inside the Lipschitz region.

These are scope questions, not a canonical claim. The common textbook slogan "continuous in time
and locally Lipschitz in state implies a unique local solution" is a candidate family description,
not an accepted transcription of the repository source.

## Proposition-changing cases

The statement phase must decide and mutation-test at least:

1. removal or weakening of the spatial Lipschitz hypothesis;
2. replacement of completeness or finite dimensionality by an arbitrary normed space;
3. autonomous versus time-dependent quantifier scope;
4. local versus global existence and uniqueness;
5. a prescribed quantitative closed interval versus existence of some open neighborhood;
6. uniqueness among all curves versus only curves staying in the controlled region; and
7. zero-width intervals, zero spatial/time radii, zero bounds or Lipschitz constants, endpoint
   initial times, and a center different from the actual initial value.

## Explicit exclusions

- `THM-M-1331` (the separately cataloged generic existence-uniqueness theorem under a Lipschitz
  condition) merged into this target without a reviewed duplicate/identity decision.
- `THM-M-1333` Peano existence under continuity, which does not provide uniqueness.
- continuation, maximal-interval, comparison, Gronwall, continuous-dependence, parameter, or
  manifold-flow results substituted for the root; nearby targets own these topics.
- The existence declarations in `Mathlib.Analysis.ODE.PicardLindelof` alone, because that module
  states that uniqueness is proved elsewhere.
- A uniqueness theorem alone, a local-flow strengthening, a `C^1` special case, or a global
  Lipschitz special case treated as the catalog root without a source-faithful checked bridge.
- A structure that assumes the desired solution or uniqueness as data, an empty/degenerate
  interval used to trivialize the ODE condition, or the catalog label `已验证` used as proof credit.

## Formal boundary

No canonical Lean expression is frozen at intake. The pinned modules
`Mathlib.Analysis.ODE.PicardLindelof` and `Mathlib.Analysis.ODE.Gronwall` expose relevant existence
and uniqueness ingredients. A later statement phase must select a source-faithful root, elaborate
it with minimal imports, fingerprint it, and check any composition/transport and the mandated
mutations before any formal proof closure is credited.
