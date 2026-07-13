# Source-statement crosswalk

## Repository authority

`Docs/researches/math_theorems.md:1703-1708` supplies exactly the title `单值性定理`, attribution
to "many mathematicians," a nineteenth-century date, the gloss `全纯函数沿曲线的解析延拓`, high
importance, and status `已验证`. All six uncited lines entered in commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. They contain no bibliography, formula,
definitions, ordered binders, hypotheses, conclusion, proof, errata, or formal artifact.

`Docs/Stage0_Blueprint.md:6545-6570` repeats the gloss and explicitly leaves the formal system,
precise definitions and premises, proof route, dependencies, equivalent forms, axioms, machine
state, and artifact links open. The rev-5.6 manifest preserves `已验证` only as
`source_status_untrusted` and resets the target to `L0 / rework_required`.

## Human-source discovery

The permanent Encyclopedia of Mathematics entry *Monodromy theorem*, revision 36520 (27 June
2015), was inspected as a secondary statement discriminator. It gives both the simply-connected
single-valuedness formulation and the endpoint-fixed homotopy-invariance formulation for analytic
elements, and notes extensions to Riemann surfaces and Riemann domains. It cites A. I.
Markushevich, *Theory of Functions of a Complex Variable*, vol. 2, Chelsea, 1977, and J. B.
Conway, *Functions of One Complex Variable*, Springer, 1978, among other books.

Springer's lawfully accessible front matter for J. B. Conway, *Functions of One Complex Variable
I*, second edition, Graduate Texts in Mathematics 11, DOI `10.1007/978-1-4612-6313-5`, locates
Chapter IX section 2, "Analytic Continuation Along A Path," at page 213; section 3, "Monodromy
Theorem," at page 217; section 5, the sheaf of analytic germs, at page 227; and section 7, covering
spaces, at page 245. Only the front matter and table of contents were accessible and inspected;
the theorem and proof pages were not.

The encyclopedia entry is not a primary proof source. The Conway locator is a discovery pointer,
not inspected theorem text. No lawful immutable theorem-and-proof copy, incorporated definition
chain, full assumption mapping, proof boundary, correction or errata audit, or independent review
was accepted. These leads support `H1`, not `H0`.

## Literal crosswalk

| Repository element | Source-supported mathematical component | Prospective Lean component | Intake result |
|---|---|---|---|
| `单值性定理` | monodromy theorem / single-valuedness criterion | one canonical theorem expression | family identified; branch open |
| "holomorphic functions" | analytic element or germ with a representative near a basepoint | analytic-function sheaf, stalk/germ, or approved equivalent | object model and codomain open |
| "along paths" | continuation along endpoint-fixed paths and possibly a homotopy family | continuous paths, relative homotopy, and continuation/lift predicate | path and continuation conventions open |
| omitted existence premise | continuation along every required path | quantified existence of continuations/lifts | scope and binder order open |
| omitted topological premise | arbitrary domain for homotopy form, simply-connected domain for global form | topology plus connectedness/local-path-connectedness/simple-connectedness classes | branch-dependent hypotheses open |
| omitted conclusion | equal terminal elements, path independence, or global single-valued branch | equality of terminal germs or existence/uniqueness of a global analytic section | no conclusion selected |
| `已验证` | untrusted catalog label | no proposition or proof object | rejected as evidence |

## Pinned formal candidate crosswalk

At mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, module
`Mathlib.Topology.Homotopy.Lifting` contains `IsLocalHomeomorph.monodromy_theorem`:

| Abstract declaration input | Analytic reading in its docstring | Target gap |
|---|---|---|
| `X`, `E`, `p : E -> X` | analytic base, etale space of germs, projection | analytic etale space not instantiated |
| `IsLocalHomeomorph p` | local continuation of germs | bridge not proved for a selected sheaf/model |
| `IsSeparatedMap p` | uniqueness from the identity principle | source and Lean identity bridge open |
| `gamma : gamma0.HomotopyRel gamma1 {0,1}` | endpoint-fixed path homotopy | source path/homotopy convention open |
| `Gamma : I -> C(I,E)`, lift and common-start premises | analytic continuations along the homotopy family | continuation-to-lift equivalence open |
| `Gamma t 1 = Gamma 0 1` | terminal continuation is homotopy invariant | only the homotopy branch; no direct global branch |

`SimplyConnectedSpace.paths_homotopic` is relevant to deriving path independence, and
`IsCoveringMap.existsUnique_continuousMap_lifts` is adjacent lifting substrate. Neither chooses the
catalog's exact analytic claim. The candidate's introduction at mathlib commit
`9994bf5ce8169d080d40ef2652ad7fdca3eb49a5`, current kernel availability, name, or docstring is
not a normalized statement match or target completion receipt.

## Gate result

The source-statement crosswalk freezes the ambiguity rather than filling it with familiar
mathematics. A downstream statement phase must approve an exact source branch, definitions,
assumptions, conclusion, and boundary cases; then elaborate that same Lean proposition and check
any transport to the abstract mathlib theorem. Until then the canonical statement and formal
target remain null, and no proof status transfers.
