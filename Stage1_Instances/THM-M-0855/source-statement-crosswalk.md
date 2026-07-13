# THM-M-0855 source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:6271-6276` supplies the title `Chvatal-Erdos定理`, authors Vaclav
Chvatal and Paul Erdos, year 1972, the gloss `Hamilton圈存在的连通度与独立数条件`, importance
`高`, and status `已验证`. All six uncited catalog lines originate in repository commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`.

`Docs/Stage0_Blueprint.md:23333-23358` repeats the gloss while leaving exact definitions and
premises, proof route, dependencies, alternate forms, axioms, machine status, and artifact links
open. Its generic closed-result and leaf-budget prose is planning metadata. Rev-5.6 retains the
verification label only as untrusted metadata and starts the target at `L0 / rework_required`.

## Primary proposition lead

V. Chvatal and P. Erdos, *A note on Hamiltonian circuits*, *Discrete Mathematics* 2(2) (1972),
111-113, DOI `10.1016/0012-365X(72)90079-9`, is an exact bibliographic and semantic match. The
institutional Erdos archive's three-page scan at
`https://www.renyi.hu/~p_erdos/1972-02.pdf` was observed with SHA-256
`a14dc030b3c2c6364aed0e093ced674d03bd2fc3390e660be036e4b5581492a7`.

Theorem 1 on printed page 111 says:

> Let G be a graph with at least three vertices. If, for some s, G is s-connected and contains no
> independent set of more than s vertices, then G has a Hamiltonian circuit.

The proof occupies printed pages 111-112. It chooses a longest circuit, assumes a vertex lies
outside it, obtains `s` paths that meet only at that vertex and end at distinct vertices of the
circuit, and uses the absence of an independent set of size `s+1` to splice a longer circuit. The
path step cites G. A. Dirac, *Generalisation du theoreme de Menger*, C. R. Acad. Sci. Paris 250(26)
(1960), 4252-4253, Theorem 1.

This evidence supports `H1`, not `H0`. The primary scan pinpoints the root and proof, but the local
paper does not define `s`-connected. Its incorporated Dirac/Menger convention, exact parameter
domain and graph definitions, source preservation and license boundary, correction/errata audit,
assumption-to-modern-statement mapping, and independent review have not been accepted.

Crossref confirms the title, authors, journal, volume, issue, year, and pages. zbMATH Open record
`3368669` / Zbl `0233.05123` independently transcribes Theorem 1 and distinguishes Theorems 2 and
3. Those services are corroborating metadata and review leads, not substitutes for primary source
fidelity.

## Literal crosswalk

| Source component | Mathematical meaning | Prospective Lean surface | Intake result |
|---|---|---|---|
| graph with at least three vertices | finite graph with cardinality at least three | `SimpleGraph V`, finiteness instances, `3 <= Fintype.card V` | human clause frozen; exact encoding open |
| for some `s` | existential connectivity/independence parameter | `exists s : Nat, ...` or source-equivalent positive-integer binder | domain and binder open |
| `s`-connected | vertex connectivity at least `s` | reviewed deletion or disjoint-path predicate | no pinned direct API; definition transport open |
| no independent set of more than `s` vertices | independence number at most `s` | `G.indepNum <= s`, `G.IndepSetFree (s+1)`, or quantified independent sets | adjacent APIs exist; equivalence witness open |
| Hamiltonian circuit | spanning cycle exists | `G.IsHamiltonian` or a direct cycle witness | pinned definition exists; source convention transport open |

## Distinct source results

Theorem 2 says an `s`-connected graph with no independent set of `s+2` vertices has a Hamiltonian
path. Theorem 3 says an `s`-connected graph with no independent set of `s` vertices is
Hamiltonian-connected. They are consequences or variants with different premises and conclusions,
not alternate spellings of Theorem 1. Neither receives root or proof credit here.

The paper also mentions a Nash-Williams/Bondy degree result for relatively large `s`. Dirac's,
Ore's, Nash-Williams/Bondy's, and Menger's results may become proof dependencies or comparison
nodes, but none substitutes for the connectivity-and-independence root.

## Pinned Lean crosswalk

| Declaration | What it supplies | Why it does not close the target |
|---|---|---|
| `SimpleGraph.IsHamiltonian` | existence of a Hamiltonian cycle under mathlib's boundary convention | no connectivity/independence implication |
| `SimpleGraph.IsIndepSet` / `IsNIndepSet` | independent-set predicates | no maximum bound or Hamiltonian conclusion by themselves |
| `SimpleGraph.IndepSetFree` / `indepNum` | two candidate independence-bound encodings | no checked equivalence to a selected root encoding yet |
| `SimpleGraph.Subgraph.deleteVerts` | vertex-deletion substrate | no reviewed vertex `s`-connectivity predicate or convention |
| `SimpleGraph.Connected` | ordinary graph connectedness with a nonempty-carrier convention | not vertex `s`-connectivity |

`IntakeProbe.lean` verifies these declarations elaborate at the pinned revision. A bounded search of
repo-local and pinned package Lean sources found no Chvatal-Erdos declaration and no direct vertex
`s`-connectivity API. `SimpleGraph.IsEdgeConnected` was located but is explicitly the wrong notion.
The bounded observation is feasibility/discovery evidence only, not a complete anchor audit or an
external absence proof.

## Next gate

Before statement acceptance, accountable source and graph-theory reviewers must admit an immutable
source bundle, audit the incorporated definition of `s`-connectivity and corrections, freeze the
graph and parameter domains, ordered binders, all hypotheses and conclusion, reconcile every
boundary convention, and approve why Theorem 1 rather than Theorem 2 or 3 is the catalog root. A
formal reviewer must then elaborate a minimal-import Lean expression, serialize its fingerprints,
check all alternate-form transports, and run the required statement mutations.
