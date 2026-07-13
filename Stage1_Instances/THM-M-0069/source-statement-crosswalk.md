# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md:512-517` supplies exactly:

- title: `伯恩赛德定理`;
- attribution: William Burnside;
- year: 1904;
- gloss: `p^a q^b阶群可解`;
- importance: high;
- untrusted formalization status: `已验证`.

All six catalog lines originate in repository commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. `Docs/Stage0_Blueprint.md:2001-2026`
repeats the gloss while explicitly leaving exact definitions, premises, proof route, axioms,
machine status, and artifact links open. These records establish catalog identity, not `H0`.

## Primary-source lead and boundary

Crossref metadata identifies W. Burnside, "On Groups of Order p-alpha q-beta," *Proceedings of
the London Mathematical Society* s2-1(1), 1904, pages 388-392,
DOI `10.1112/plms/s2-1.1.388`. This matches the repository's author, year, and subject. The
publisher PDF endpoints returned HTTP 400/403 in this intake, so the article text was not admitted
or inspected. No exact theorem passage, incorporated definition, proof-node map, correction or
errata disposition, edition history, or independent source review was completed. Bibliographic
metadata is discovery evidence only, so the human status remains `H1`.

## Clause crosswalk

| Repository phrase | Required mathematical meaning | Pinned Lean interface | Intake status |
|---|---|---|---|
| "group" | a group `G`, with finiteness made explicit or derived noncircularly | `[Group G]`, `[Finite G]` | exact domain and finiteness premise open |
| "order" | finite cardinality of the carrier | `Nat.card G` or `Fintype.card G` | representation and transport open |
| `p`, `q` | prime natural numbers, commonly distinct | `Nat.Prime p`, `Nat.Prime q` | distinctness and binder style open |
| `a`, `b` | exponents, commonly natural numbers | `a b : Nat`, natural powers | zero and positivity policy open |
| `p^a q^b` | exact product, up to commutativity, or a prime-support condition | `p ^ a * q ^ b` | equality and alternate encodings open |
| "solvable" | derived series eventually equals the trivial subgroup | `IsSolvable G`, `isSolvable_def G` | definition located; source identity open |
| `已验证` | untrusted inventory label | no expression or evidence | explicitly rejected as credit |

## Pinned formal leads

At mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`:

1. `Mathlib.GroupTheory.Solvable` defines `IsSolvable` and proves `isSolvable_def`.
2. `Mathlib.GroupTheory.PGroup` proves `IsPGroup.of_card`; `Mathlib.GroupTheory.Sylow` proves
   `Sylow.exists_subgroup_card_pow_prime`. These are prime-power and subgroup interfaces.
3. `Mathlib.GroupTheory.Transfer` proves `MonoidHom.ker_transferSylow_isComplement'`, explicitly
   documented as Burnside's normal p-complement theorem.
4. `Mathlib.GroupTheory.SpecificGroups.ZGroup` provides an `IsSolvable` instance for finite
   Z-groups, a proper special class with cyclic Sylow subgroups.

`IntakeProbe.lean` checks these declarations and their axiom reports in the pinned environment.
A bounded exact-topic search found no direct p-alpha q-beta solvability declaration. The checked
items are genuine definition, reduction, and partial-route interfaces, supporting provisional
`M3`; they do not close the exact root. Exact normalized types, terminal proof-body provenance,
transitive dependencies, placeholders, unsafe/oracle boundaries, and exhaustive external-project
search remain for the anchor audit.

## First failed statement/source gate

No accepted source fixes finiteness, prime distinctness, exponent boundaries, cardinality encoding,
binder order, or the precise solvability convention. Therefore neither the recognizable textbook
family nor an adjacent pinned result can be installed as the canonical target without inventing
or substituting proposition-changing mathematics.
