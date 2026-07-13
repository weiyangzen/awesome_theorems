# Scope map

## Frozen identity

| Field | Intake value | Status |
|---|---|---|
| repository ID | `THM-M-0070` | frozen |
| execution item | `S56-M-0070-INTAKE`, rank 1101 | frozen |
| catalog name | `费特-汤普森定理` | frozen |
| catalog gloss | `奇数阶群可解` | frozen source wording |
| primary theorem wording | all finite groups of odd order are solvable | inspected source candidate |
| lifecycle | `planned`, uniform `L0 / rework_required` | frozen |

The word "group" in the catalog must not lose the finiteness condition made explicit in the
primary theorem. "Order" means the cardinality of the group carrier, not the order of an element.
"Solvable" means group solvability, provisionally represented by mathlib's derived-series
predicate `IsSolvable`.

## Candidate mathematical boundary

This is a scope map, not the canonical Lean proposition.

| Component | Candidate representation | Statement-phase decision |
|---|---|---|
| group carrier | `G : Type u` | universe and binder order |
| group structure | `[Group G]` | implicit instance versus explicit parameter |
| finite premise | `[Finite G]` | `Finite` versus `Fintype` and transports |
| group order | `Nat.card G` | exact cardinality encoding |
| oddness | `Odd (Nat.card G)` | factorization versus congruence encoding |
| solvability | `IsSolvable G` | typeclass conclusion versus explicit derived-series witness |
| candidate implication | `Odd (Nat.card G) -> IsSolvable G` | exact binder-complete expression and fingerprint |

The primary paper states that all groups considered are finite unless explicitly stated otherwise
and its displayed root theorem explicitly says "finite groups." Finiteness therefore belongs in
the source-faithful root even if a later encoding makes it inferable in another way.

## Included boundary cases

- the trivial group, whose order is one and is odd;
- all finite abelian groups of odd order;
- all finite nonabelian groups of odd order;
- prime-power, prime order, and arbitrary composite odd order;
- every universe in which the selected finite-group encoding elaborates.

No nontriviality, simplicity, faithfulness, commutativity, or fixed cardinality premise may be added.
The order-one probe confirms that this included boundary is expressible; it does not prove the root.

## Explicit non-substitutions

- solvability only for commutative groups, Z-groups, groups of prime order, or another special class;
- Burnside's `p^a q^b` theorem or a fixed finite-order case;
- a classification of finite simple groups or the statement that an odd-order simple group is
  cyclic of prime order;
- odd order of an element, automorphism, character, graph, or other object rather than `Nat.card G`;
- an implication with `IsSolvable G` assumed as a hypothesis or stored as input data;
- the Coq/MathComp theorem used as Lean kernel closure without pin/import/check integration;
- the title-only entry in mathlib's `docs/1000.yaml` or the catalog's verified label used as proof.

## Formal discovery boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, module
`Mathlib.GroupTheory.Solvable` defines `IsSolvable G` by eventual triviality of `derivedSeries`.
Additional imports expose `Nat.card`, `Odd`, and the trivial group. The probe validates vocabulary
and a proposition-shaped expression only. A bounded search of repo-local Lean, pinned mathlib
sources, and pinned mathlib docs found the Feit-Thompson title only in `docs/1000.yaml`, with no
declaration mapping. This is intake discovery, not a global absence claim or anchor audit.

## Gate boundary

`S56-M-0070-STATEMENT` must freeze the exact ordered binders, minimal imports, canonical Lean
expression, fingerprints, checked alternate encodings, and mutations. The anchor audit must then
audit Lean and external candidates at immutable revisions. Intake grants no downstream state.
