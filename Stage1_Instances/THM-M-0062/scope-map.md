# Scope map

## Preserved catalog scope

The repository fixes target `THM-M-0062`, the label `西罗定理` (Sylow theorems), Ludwig Sylow,
1872, and the gloss `有限群中p-子群的存在性、共轭性和计数`: existence, conjugacy, and counting of
`p`-subgroups in finite groups. The three nouns are conjunctive scope. Intake may not replace the
package by only existence, only conjugacy, or only the congruence count.

The modern intended family is: for every finite group `G` and prime natural `p`, Sylow
`p`-subgroups exist; every two are conjugate; and their number has the standard divisibility and
congruence properties. A Sylow `p`-subgroup must be tied either to maximality among `p`-subgroups or
to order `p^a`, where `p^a` is the largest power of `p` dividing `|G|`, with a checked equivalence.
This family boundary is frozen; one exact conjunction and its ordered binders remain statement work.

## Proposition-changing decisions

The statement phase must freeze all of the following from an approved source crosswalk:

- `G : Type u` with `Group G` and `Finite G` versus an explicitly finite carrier such as
  `Fintype G`, and how `Nat.card G` is used;
- `p : Nat` with primality represented explicitly or through `Fact p.Prime`;
- maximal `p`-subgroup versus exact maximal-prime-power order as the canonical definition, and the
  direction of every transport between them;
- whether existence is expressed as `Nonempty (Sylow p G)`, an existential subgroup of exact order,
  or both through checked implications;
- conjugacy as an explicit element `g : G` acting on two Sylow subgroups, conjugacy of subgroup
  carriers, or transitivity of the conjugation action;
- the exact counting bundle: `n_p ≡ 1 [MOD p]`, `n_p` divides the Sylow index, and/or
  `n_p = [G : N_G(P)]`, without dropping a clause supplied by the selected source target;
- whether the historical substitution-group statement reaches arbitrary finite groups through an
  explicit Cayley/permutation representation bridge or a separately admitted modern source; and
- quantifier order, universe levels, coercions, normalizer convention, and every boundary case.

These choices are a resolution ledger, not a canonical Lean expression.

## Boundary cases

The exact target must address `p` not dividing `|G|`, where the trivial subgroup is the unique
Sylow `p`-subgroup; the trivial finite group; `p = 2`; nontrivial `p`-groups; a normal Sylow subgroup;
and disconnected encodings caused by `Finite` versus `Fintype`. Prime `p` excludes `0` and `1`.
No boundary may be discarded merely to match a convenient declaration.

## Explicit exclusions

- Lagrange's theorem, Cauchy's theorem, Hall subgroup theory, or a general group-action theorem
  without checked assembly into all three Sylow clauses.
- Existence of an arbitrary `p`-subgroup, including the trivial subgroup, without maximality or the
  maximal-prime-power order conclusion.
- Conjugacy or counting for one selected Sylow subgroup without quantifying over the full family.
- Only `n_p ≡ 1 [MOD p]` when the selected canonical counting statement also requires divisibility
  or the normalizer-index identity.
- A structure that stores existence, conjugacy, or counting as assumed fields and a projection from
  that structure.
- The catalog's `已验证` label, a theorem name, a successful `#check`, or a library URL as proof or
  source acceptance.

## Formal boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, module
`Mathlib.GroupTheory.Sylow` defines `Sylow p G` as a maximal `p`-subgroup and exposes candidates for
all three branches. The intake probe checks and invokes those APIs under `Finite G`. It neither
selects the exact conjunction nor audits normalized statement identity, terminal proof bodies,
transitive dependencies, placeholders, accepted axioms, or composition. Those are downstream
statement and anchor-audit gates.
