# Source-statement crosswalk

## Repository authority

`Docs/researches/math_theorems.md:10334` records `谱分解定理`, Stephen Smale, 1967, and the complete
statement gloss `Axiom A系统的分解` ("decomposition of Axiom A systems"). The row first entered the
repository in commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. That commit is repository
provenance, not a mathematical source revision.

`Docs/Stage0_Blueprint.md:38456` repeats the gloss while explicitly leaving exact definitions and
premises, proof route, dependencies, equivalent forms, axioms, machine status, and artifacts open.
The rev-5.6 manifest carries `已验证` solely as `source_status_untrusted`.

## Primary-source candidate inspected

Stephen Smale, *Differentiable dynamical systems*, **Bulletin of the American Mathematical
Society** 73(6) (1967), 747-817, DOI `10.1090/S0002-9904-1967-11798-1`, is an exact historical
candidate. The official AMS PDF was retrieved on 2026-07-12 and had SHA-256
`759e0601e50ceebc812c4a4c67e5b9ed59534848c6d342a2e2cf56871db19551`; it is not vendored into
this worker packet.

For diffeomorphisms, printed pages 776-777 introduce a hyperbolic invariant set, topological
transitivity, and Axiom A (6.1). Theorem (6.2), printed page 777, says that an Axiom A
diffeomorphism of a compact manifold uniquely decomposes its nonwandering set into a finite union
of pairwise disjoint closed invariant indecomposable pieces, on each of which the restriction is
topologically transitive. Section 1.7, printed pages 780-782, gives a proof sketch using Lemmas
(7.1) and (7.2), the generalized stable manifold theorem (7.3), canonical coordinates (7.4), and
Lemma (7.5). The paper says at page 777 that theorem (6.2) then had no proof in the literature and
cites [117]; that cited work has not been inspected here.

The same paper also states "Spectral decomposition" for Axiom A' flows as Part II theorem (5.2),
printed page 803. This materially changes the system, the hyperbolicity premise, fixed/closed orbit
conditions, and time action. The repository gloss does not distinguish the two variants. Thus the
diffeomorphism theorem is the leading candidate, not an accepted canonical identity.

## Candidate crosswalk

| Source component | Mathematical content to freeze | Required Lean surface | Intake status |
|---|---|---|---|
| compact manifold and `f in Diff(M)` | exact smooth manifold, compactness, boundary and regularity conventions; invertible smooth map | pinned manifold/diffeomorphism structures and exact binders | candidate mapped in prose; exact types open |
| nonwandering set `Omega(f)` | source definition using returns of every neighborhood | an exact `Set M` definition and invariance facts | no target-specific pinned interface located |
| Axiom A (6.1)(a) | `Omega(f)` is hyperbolic via invariant stable/unstable tangent splitting and uniform contraction/expansion | tangent/derivative bundles, invariant splitting, norm estimates | no Axiom A or dynamical hyperbolicity interface located |
| Axiom A (6.1)(b) | periodic points are dense in `Omega(f)` | `Function.periodicPts` plus relative density statement | generic periodic-point API probed; hypothesis not encoded |
| finite disjoint union | finitely many pieces covering exactly `Omega(f)` and pairwise disjoint | finite index/family, set union equality, `Pairwise` | generic set infrastructure only |
| closed and invariant pieces | every piece is closed and mapped to itself in the source sense | `IsClosed` and exact forward/backward invariance | generic `IsInvariant` probed; exact restriction open |
| indecomposable pieces | Smale's source definition and nonemptiness boundary | a new source-faithful predicate or checked equivalence | exact definition/relation to transitivity open |
| topologically transitive restrictions | dense-orbit definition on each restricted compact metric system | restricted action/map plus source-equivalent transitivity predicate | generic action class probed; equivalence not credited |
| unique decomposition | exact equality/canonicity, including reindexing convention | equality of finite sets/families or checked quotient relation | representation and uniqueness encoding open |
| section 1.7 proof sketch | stable manifolds, local product/canonical coordinates, local dense iterates, finite equivalence classes | a future obligation tree with explicit bridges and composition | downstream source/obligation audit open |
| Part II theorem (5.2) | continuous-time Axiom A' flow decomposition | `Flow`, fixed/closed orbits, derived-flow hyperbolicity | distinct candidate; not an alternate encoding |
| `已验证` | untrusted inventory metadata | no declaration or proof component | explicitly rejected as evidence |

## Human-source boundary

The provisional `H1` classification records that a published theorem and proof-sketch source are
known, while source reconstruction debt remains. Before `H0`, an independent qualified reviewer
must select the diffeomorphism or flow variant; verify an immutable edition; inspect all dependent
definitions and cited source [117]; map every material premise, proof transition, and conclusion;
audit corrections and errata; and approve the Chinese-to-source identity. This intake is not that
review.

## Lean boundary

The pinned environment is Lean 4.29.0 at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740` with mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. The bounded API probe checks generic invariant-set,
periodic-point, dense-set, topological-transitivity, and flow declarations. A scoped name search
found no obvious dynamical spectral-decomposition, Smale Axiom A, nonwandering-set, or hyperbolic
splitting declaration in pinned mathlib. This is bounded intake discovery only, not an exhaustive
formal-anchor audit or a claim about external Lean projects.

Before statement credit, the selected source variant must map to one exact elaborated Lean
expression with fixed imports, profiles, serialized fingerprint, checked alternate transports, and
all required statement mutations. Until then, the root remains `H1/M4/R3` and no source, statement,
proof, audit-completion, or theorem-completion claim is legal.
