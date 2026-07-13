# THM-M-0846 source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:6208-6213` supplies exactly the title `图极限理论`, attribution
Laszlo Lovasz/Balazs Szegedy, year 2006, gloss `图序列的极限`, importance `高`, and status
`已验证`. All six uncited lines originate in repository commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. They contain no graph model, density definition,
convergence criterion, ordered binder, hypothesis, conclusion, theorem/page locator, proof,
correction record, reviewer, or formal artifact.

`Docs/Stage0_Blueprint.md:23090-23115` repeats the gloss while explicitly leaving the formal
system, precise definitions and premises, proof route, dependencies, alternate forms, axioms,
machine status, and artifact links open. Its generic closed-result and leaf-audit prose is planning
metadata, not evidence. Rev-5.6 retains `已验证` only as untrusted metadata and resets the target to
`L0 / rework_required`.

## Inspected primary source lead

Laszlo Lovasz and Balazs Szegedy, *Limits of dense graph sequences*, *Journal of Combinatorial
Theory, Series B* 96(6), 2006, pages 933-957, DOI
`10.1016/j.jctb.2006.05.002`, matches the repository authors, date, and topic. Immutable arXiv
version `math/0408173v2` (22 September 2004) was inspected; its PDF digest and mutable Crossref
metadata digest are recorded in `instance.json` and `intake-receipt.json`.

The source defines a graph sequence as convergent when `t(F,G_n)` converges for every finite simple
unweighted graph `F`, where `t` is normalized homomorphism density. Section 2.5 defines, for a
symmetric measurable `W : [0,1]^2 -> [0,1]`, the integral density `t(F,W)`. Theorem 2.2 then says
that the following conditions on a simple-graph parameter `f` are equivalent:

1. `f` is a pointwise limit of homomorphism-density parameters of a convergent simple-graph
   sequence;
2. `f = t(.,W)` for a symmetric measurable `W`;
3. `f` is normalized, multiplicative, and reflection positive;
4. `f` is normalized and multiplicative and its connection matrix `M_0(f)` is positive
   semidefinite; and
5. `f` is normalized and multiplicative and its source-defined transform `f dagger` is
   nonnegative.

Corollary 2.6 is a distinct realization claim: the random graph sequence `G(n,W)` converges almost
surely and has limit `W`. The repository does not cite the paper, name Theorem 2.2 or Corollary
2.6, or choose the existence implication, converse, two-way limit-object equivalence, full five-way
theorem, or random realization. The source is therefore a strong `H1` lead, not an accepted H0
crosswalk. Published-version comparison, correction/errata review, incorporated-definition mapping,
and independent review remain open.

## Literal crosswalk

| Repository component | Source-family component | Prospective Lean component | Intake result |
|---|---|---|---|
| graph sequences | finite simple graphs `G_n` | sequence of finite vertex types/graphs or a bundled encoding | carrier and loop/weight conventions open |
| limits | convergence of every normalized `t(F,G_n)` | `Tendsto` over all finite test graphs | density and convergence formulation open |
| limit object | symmetric measurable `W : [0,1]^2 -> [0,1]` | measurable bounded symmetric function, possibly modulo equivalence | representative and equality conventions open |
| Lovasz/Szegedy, 2006 | primary paper and several results | provenance only | family identified, root not selected |
| verified | untrusted inventory field | accepted source and kernel receipts | no H or M credit |

## Candidate-meaning boundary

Existence of limits of each scalar density is the definition of convergence, not yet construction
of a common measurable limit object. Existence of `W` does not by itself state uniqueness. The
converse realization is not logically the same implication. Reflection positivity and connection
matrix conditions add definitions and equivalences absent from the gloss. Almost-sure convergence
of `G(n,W)` is a probabilistic construction, not the arbitrary-sequence existence direction.
Selecting among these without review would broaden or substitute the target.

## Pinned Lean crosswalk

| Declaration | What it supplies | Why it is not the target |
|---|---|---|
| `SimpleGraph.Hom` | adjacency-preserving graph maps | no normalized homomorphism count or sequence limit |
| `SimpleGraph.edgeDensity` | rational edge density between finite vertex sets | not all finite-test-graph homomorphism densities |
| `szemeredi_regularity` | an effective finite regularity partition | major substrate, but no graphon limit object or representation |
| `MeasureTheory.Measure.prod` | product measure construction | no symmetric bounded measurable limit function or graph density |
| `MeasureTheory.integral_prod` | Fubini theorem | integration substrate, not the dense graph limit theorem |

`IntakeProbe.lean` checks these declarations at the pinned revision. Bounded searches found no
exact-topic repo-local or pinned-mathlib terminal declaration for graphons or dense graph limits.
The checks are not a canonical target, exhaustive external audit, global absence proof, or proof
body.

## Source gate

Before the statement phase, accountable reviewers must select one immutable proposition and map
every graph/density/convergence/limit-object definition, ordered binder, premise, conclusion,
boundary case, proof passage, published-version difference, and correction. They must also resolve
the boundary with `THM-M-0845` and `THM-M-0847`. A formal reviewer must then map only that claim to
a minimal-import Lean expression and checked transports.

Until then, `H1` records a primary source family whose exact statement mapping is incomplete, `M4`
records that no exact usable formal artifact is credited, and `R4` records the lack of an anchorable
proof reconstruction. These classifications do not say that the Lovasz-Szegedy results are open or
false.
