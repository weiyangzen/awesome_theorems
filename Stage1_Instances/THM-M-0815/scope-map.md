# Scope map

## Frozen identity

| Field | Intake value | Status |
|---|---|---|
| repository ID | `THM-M-0815` | frozen |
| execution item | `S56-M-0815-INTAKE`, rank 1374 | frozen |
| catalog name | `霍尔婚配定理` | frozen as source wording |
| catalog claim | `二部图完美匹配存在的条件` | frozen literally |
| attribution | Philip Hall, 1935 | catalog metadata and bibliography agree |
| lifecycle | `planned`, uniform `L0 / rework_required` | frozen |

The intake preserves the graph-theoretic subject and the literal claim that a condition concerns a
perfect matching. It does not reinterpret "perfect" as one-side saturation or add balance,
finiteness, and graph-coverage assumptions merely to fit a convenient library declaration.

## Candidate roots, not credited

1. **Finite indexed-family form.** For a finite index type `I` and finite sets `X i`, there is an
   injective representative `f` with `f i in X i` iff every finite `J` satisfies
   `|J| <= |union (X i, i in J)|`.
2. **One-side bipartite form.** For a bipartition `p1`, `p2`, there is a graph matching saturating
   `p1` iff every `s subset p1` satisfies `|s| <= |N(s)|`, under the needed finiteness premises.
3. **Balanced perfect-matching corollary.** With both parts covering the graph and having equal
   finite cardinality, one-side saturation becomes a perfect matching. The exact balance and
   coverage contract requires an explicit checked bridge.
4. **Pinned global sufficient form.** If the neighborhood inequality holds for every subset of the
   entire vertex type, pinned mathlib constructs a perfect matching. This premise is stronger and
   differently scoped than the ordinary one-side Hall condition.

None is selected as the canonical proposition at intake.

## Proposition-changing decisions

The statement phase must freeze:

- indexed families, the source's finite-relation specialization or a pinned finite-fiber/
  finite-codomain relation generalization, or simple bipartite graphs as the canonical domain;
- finite versus arbitrary index type with finite neighborhoods;
- explicit `Fintype`, `Finite`, locally finite graph, or finite-set encodings;
- whether the two bipartition sets cover the vertex type, are disjoint, and have equal cardinality;
- a matching saturating one part versus `Subgraph.IsPerfectMatching` on every vertex;
- whether the result is an implication, the standard necessary-and-sufficient condition, or a
  corollary with balance assumptions;
- `Finset.card`, `Set.ncard`, or `Fintype.card`, and the precise neighborhood/union construction;
- ordered binders, universes, typeclass instances, decidable-equality requirements, and logical
  principle policy;
- checked transports among every credited encoding.

## Boundary-case ledger

No degenerate case is excluded at intake. Later statement work must settle empty index/parts,
empty and edgeless graphs, isolated vertices, empty family members, singleton parts, unequal part
sizes, vertices outside `p1 union p2`, overlapping proposed parts, infinite vertex types with finite
neighborhoods, and the distinction between a vacuous empty-side matching and graph-wide
perfectness.

## Formal boundary

The minimal discovery probe imports `Mathlib.Combinatorics.SimpleGraph.Hall`, which transitively
exposes the pinned family, relation, and graph declarations listed in the crosswalk. It authenticates
their names and types but does not establish that this import is minimal for an unidentified root.
It creates no local theorem, wrapper, transport, or proof credit.

The graph interfaces also use `Set.ncard`, whose value is zero on infinite sets, while
`G.LocallyFinite` makes each vertex neighborhood finite but does not make the vertex type or every
union of neighborhoods finite. Their behavior outside a source-approved finite scope therefore
cannot be read as ordinary infinite-cardinal Hall inequalities without a separate formal analysis.

## Gate boundary

`S56-M-0815-STATEMENT` must resolve the source identity and proposition-changing choices, elaborate
the exact target under minimal imports, serialize its expression and environment fingerprints,
check transports, and run removed-hypothesis, changed-domain, changed-binder-scope, and boundary
mutations. Anchor audit, obligation freeze, proof, validation, and release then remain dependency-
ordered and open. Intake grants none of their state.
