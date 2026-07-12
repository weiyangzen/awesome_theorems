# Scope map

## Frozen identity

| Field | Intake value | Status |
|---|---|---|
| repository ID | `THM-M-0077` | frozen |
| execution item | `S56-M-0077-INTAKE`, rank 1025 | frozen |
| catalog name | `霍尔定理` | frozen as source wording |
| catalog claim | `有限可解群中Hall子群的存在性` | frozen literally |
| intended English identity | existence of Hall `pi`-subgroups in finite solvable groups | candidate interpretation, not an exact statement |
| excluded identity | `THM-M-0815`, Hall's marriage theorem | frozen exclusion |
| lifecycle | `planned`, uniform `L0 / rework_required` | frozen |

The target is existence only. Conjugacy of Hall `pi`-subgroups and containment of every
`pi`-subgroup in one are familiar neighboring Hall results, but adding them would broaden this
catalog claim unless a reviewed primary-source crosswalk later requires a theorem family.

## Candidate mathematical boundary

This is a planning scope, not the canonical proposition.

| Component | Candidate | Unresolved decision |
|---|---|---|
| group | `G : Type u`, `[Group G]`, `[Finite G]` | `Finite` versus `Fintype`, universe and instance order |
| solvability | `[IsSolvable G]` | typeclass versus explicit hypothesis and exact source convention |
| prime selection | `pi`, a selected collection of primes | `Set Nat`, predicate, `Finset Nat`, or support relative to `Nat.card G` |
| subgroup | `H : Subgroup G` | existential binder only after the Hall predicate is fixed |
| `pi`-order condition | every prime divisor of `Nat.card H` belongs to `pi` | exact prime-support/factorization encoding |
| index condition | every prime divisor of `H.index` is outside `pi` | exact complement universe and finite-index encoding |
| conclusion | `exists H, IsHallPi pi H` | no such accepted predicate or expression is frozen |

Bare `Nat.Coprime (Nat.card H) H.index` describes a Hall subgroup in one convention, but it can
forget which `pi` is being quantified. It cannot replace an arbitrary-`pi` target until a checked
equivalence preserves the selected prime support.

## Binder and case ledger

The ordered binder list, hypotheses, conclusion expression, universes, and alternate encodings in
`instance.json` remain empty or null because choosing them before the source and definition gates
would invent mathematics. Statement work must explicitly decide:

- empty `pi`, all primes, and primes absent from `Nat.card G`;
- the trivial group and the cases yielding `H = bot` or `H = top`;
- whether `pi` ranges over all primes or only the finite prime support of the group order;
- whether the source uses order/index support, largest `pi`-divisor order, or coprimality;
- exact equivalence transports among accepted formulations;
- whether choice/classical logic used by a proof is allowed under the foundation profile.

No degenerate case is excluded at intake.

## Formal boundary

At mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the probe authenticates
`IsSolvable`, `Sylow.card_coprime_index`, `IsZGroup.coprime_commutator_index`, and
`Subgroup.exists_right_complement'_of_coprime`. The last three are special or adjacent theorems:
one prime, finite Z-groups, and complements of already-given normal Hall subgroups respectively.
None proves the catalog claim.

A bounded exact-topic search over repo-local Lean and pinned mathlib found neither a general
Hall-`pi` predicate nor finite-solvable Hall-existence declaration. This observation is intake
discovery, not a global absence claim and not the downstream immutable anchor audit.

## Gate boundary

`S56-M-0077-STATEMENT` must inspect and independently crosswalk the primary statement, freeze the
Hall-`pi` definition and binder-complete Lean expression, elaborate it under minimal imports, and
run the required mutations. The anchor audit, obligation tree, proof, validation, and release tasks
then remain dependency-ordered and open. Intake grants none of their state.
