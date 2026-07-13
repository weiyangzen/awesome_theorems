# Source-statement crosswalk

## Repository source record

The complete repository record is `Docs/researches/math_theorems.md:3504-3509`. Git history traces
all six uncited lines to commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`.

| Catalog field | Received value | Intake consequence |
|---|---|---|
| title | `中国剩余定理` | Names the Chinese-remainder theorem family, but not one formal proposition. |
| attribution | ancient Chinese mathematicians | Does not identify an authorial passage, edition, translation, or proof. |
| time | approximately the third century CE | Historical metadata only; not a theorem locator. |
| statement | `同余方程组的解法` | Mentions solving systems of congruences but omits every binder, premise, and exact conclusion. |
| importance | high | Scheduling metadata only. |
| formalization status | `已验证` | Explicitly untrusted; supplies no human-source or kernel credit. |

The generated projection at `Docs/Stage0_Blueprint.md:13082-13107` repeats the gloss and explicitly
leaves exact definitions and premises, proof route, equivalent forms, axioms, machine status, and
artifact links pending. It adds no exact proposition or source.

No primary or authoritative edition, theorem/page locator, incorporated definitions, assumption
map, proof boundary, translation, correction or errata disposition, or independent review is
present in the repository. The provisional human status is therefore `H5`: the received catalog
target is not yet a stable truth-valued proposition. This classification does not refute the
classical Chinese remainder theorem; it requires an accountable redirection to one immutable
statement before ordinary theorem execution.

## Phrase-to-statement map

| Repository phrase | Candidate mathematical component | Prospective Lean surface | Intake assessment |
|---|---|---|---|
| `同余` / congruence | congruence of integer-like values modulo a modulus | `Nat.ModEq`, integer divisibility, or equality in `ZMod` | carrier and zero-modulus convention are absent |
| `方程组` / system | two, finitely many, or another explicitly delimited family of residue/modulus constraints | conjunction, list/finset predicate, or indexed `forall` | finiteness, cardinality, indexing, duplicates, and quantifier order are absent |
| `解法` / method or solution | a constructed witness, existence theorem, or algorithm | subtype-valued construction, `Exists`, equivalence, or executable function | the source does not select construction versus proposition or specify correctness |
| classical CRT hypothesis | pairwise coprime moduli or compatible residues modulo gcds | `Nat.Coprime`, `List.Pairwise`, `Set.Pairwise`, or a `ModEq` premise | no premise appears in the catalog gloss |
| classical CRT uniqueness | one residue class modulo product or lcm | `Nat.ModEq` modulo a product/lcm or a `ZMod` equivalence | existence, uniqueness, and canonical bounds are not distinguished |
| `已验证` | inherited catalog status | no Lean component | no source, proof-body, or receipt credit |

## Pinned formal candidate crosswalk

| Module and declaration | Exact candidate role | Intake credit and boundary |
|---|---|---|
| `Mathlib.Data.Nat.ModEq` / `Nat.chineseRemainder'` | Constructs a natural satisfying two congruences when the two residues agree modulo the gcd of the moduli. | Direct compatible two-modulus candidate. It is not a finite-family statement and no source selects its zero-modulus semantics. M3 discovery only. |
| same module / `Nat.chineseRemainder` | Constructs a natural satisfying two congruences under coprime moduli. | Familiar special case, but the catalog does not state coprimality or restrict the system to two equations. No root credit. |
| same module / `Nat.chineseRemainder_lt_mul` and `Nat.chineseRemainder_modEq_unique` | Supplies a bounded representative for nonzero coprime moduli and uniqueness modulo their product. | Candidate conclusion extensions; they cannot be appended to the root without source authority. |
| `Mathlib.Data.Nat.ChineseRemainder` / `Nat.chineseRemainderOfList` | Constructs a solution for a list of pairwise-coprime natural moduli. | Direct finite-family candidate; list order and duplicate semantics are material. M3 discovery only. |
| same module / `Nat.chineseRemainderOfList_lt_prod` and `Nat.chineseRemainderOfList_modEq_unique` | Adds nonzero-modulus boundedness and uniqueness modulo the list product. | Candidate bound/uniqueness package, not automatically part of the received claim. |
| same module / `Nat.chineseRemainderOfFinset` | Constructs a simultaneous solution over a finset with nonzero pairwise-coprime moduli. | Direct finite-set candidate; its stronger explicit premises and finset carrier remain unselected. |
| `Mathlib.Data.ZMod.Basic` / `ZMod.chineseRemainder` | Gives a ring equivalence from residues modulo a product to a product of residue rings for two coprime moduli. | Structural alternate encoding, not identical by name to a source statement about solving equation systems. |
| `Mathlib.RingTheory.Ideal.Quotient.Operations` / `Ideal.quotientInfRingEquivPiQuotient` | Gives the general quotient-ring CRT for pairwise coprime ideals. | Broader algebraic generalization, explicitly outside the elementary root unless a source later selects it. |

The immutable mathlib revision and source-file hashes are recorded in `instance.json`. The
successful probe authenticates the Nat and ZMod interfaces actually named in `IntakeProbe.lean`
and their representative reported axioms. The ideal-theoretic row is a pinned source-inspection
observation and was not checked by the scoped probe. Neither kind of observation selects a
canonical declaration or audits terminal proof bodies.

## Human-source and machine boundary

Before H0, an independent reviewer must approve one immutable source edition and pinpoint
statement, incorporated definitions, all material assumptions, exact conclusion bundle, proof
boundary, translation, correction and errata findings, historical attribution boundary, and the
mapping to every formal binder and credited alternate encoding.

Before any M0 classification, downstream phases must freeze and elaborate the same source-selected
Lean target, check alternate transports and mutations, audit every candidate and terminal body,
freeze obligations and typed graphs, and pass composition, placeholder, axiom, provenance, trust,
hermetic, and independent-verification gates. The intake probe covers none of those proof gates.
