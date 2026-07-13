# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:456-461` supplies only the theorem name, Joseph-Louis Lagrange,
1771, the sentence `有限群G的子群H的阶整除G的阶`, importance "high," and status `已验证`.
Git history attributes these uncited fields to the initial corpus commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record gives no work title, edition, theorem or
page, definitions, proof boundary, corrections, errata, reviewer, or formal artifact.

`Docs/Stage0_Blueprint.md:1785-1808` repeats the sentence while explicitly leaving exact definitions
and premises, formal system, logical foundation, proof route, dependencies, and evidence open. The
Stage1 manifest preserves the catalog status as `source_status_untrusted` and resets this target to
`L0 / rework_required`.

## Human-source lead

David S. Dummit and Richard M. Foote, *Abstract Algebra*, third edition, section 3.2 ("Lagrange's
Theorem") is a bibliographic discovery lead for a standard modern proof. No stable copy was
admitted or inspected in this intake, so edition pagination, exact theorem locator, incorporated
definitions, proof completeness, corrections, errata, and correspondence to every canonical node
remain open. The catalog's attribution and year likewise have not been corroborated against a
primary historical work. This supports only a provisional H1 classification, never H0.

## Statement-token crosswalk

| Repository token | Mathematical content that must survive | Candidate Lean representation | Intake boundary |
|---|---|---|---|
| `有限群 G` | arbitrary finite multiplicative group | `(G : Type u) [Group G] [Finite G]` | frozen in the canonical target |
| `子群 H` | arbitrary subgroup of that same group | `(H : Subgroup G)` | frozen as a universal binder |
| `H 的阶` | finite cardinality of the subgroup carrier | `Nat.card H` | frozen; checked `Fintype.card` alternate |
| `整除` | natural-number divisibility | `∣` on `Nat` | frozen |
| `G 的阶` | finite cardinality of the ambient carrier | `Nat.card G` | frozen; checked `Fintype.card` alternate |

The finite premise is semantically meaningful even though the candidate mathlib theorem does not
need it. Removing it is a domain-broadening mutation, not literal source identity. `Statement.lean`
preserves it and kernel-checks its distinction from the broader shape.

## Pinned Lean candidate

Pinned mathlib module `Mathlib.GroupTheory.Coset.Card` explicitly describes
`Subgroup.card_subgroup_dvd_card` as Lagrange's theorem and gives it type
`(H : Subgroup G) : Nat.card H ∣ Nat.card G` under `[Group G]`. The preceding declaration
`Subgroup.card_eq_card_quotient_mul_card_subgroup` provides the quotient-cardinality product used
by its short proof. `IntakeProbe.lean` checks the public declaration and prints its reported axioms;
the observed list is `[propext, Classical.choice, Quot.sound]`.

The file is pinned by the repository manifest and is a strong candidate for a later exact wrapper.
This statement phase does not credit it as M0: the canonical target and expression fingerprint are
provisional worker evidence, no source-to-formal identity review exists, and no exhaustive
terminal-body, transitive dependency, provenance, placeholder, foundation, or TCB audit has run.

The legacy file `Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_061.lean` is explicitly labeled
`THM-M-0433` and formalizes a Laurent Lafforgue statement shape. Its numeric slot is a legacy
collision, not a THM-M-0061 artifact, and it supplies no scope or proof credit here.

## H0 work still required

An independent group-theory source reviewer must admit an immutable primary proof source, record
edition/theorem/page and invoked definitions, check corrections and errata, and map the finite
group premise, subgroup definition, cardinality convention, divisibility conclusion, coset
partition argument, and every boundary case to the canonical obligation registry. Until then the
human-source axis remains H1.
