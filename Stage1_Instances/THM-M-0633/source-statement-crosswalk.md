# Source-statement crosswalk

## Repository source record

The complete repository record is `Docs/researches/math_theorems.md:4692-4697`. Git history traces
all six uncited lines to commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`.

| Catalog field | Received value | Intake consequence |
|---|---|---|
| title | `一致连续性定理` | Names the uniform-continuity theorem family. |
| attribution | many mathematicians | Does not identify an author, source, edition, or proof. |
| time | nineteenth century | Historical metadata only; not a theorem locator. |
| statement | `紧集上连续函数一致连续` | Identifies the compact-set Heine-Cantor family but omits domains, structures, binders, and definitions. |
| importance | high | Scheduling metadata only. |
| formalization status | `已验证` | Explicitly untrusted; supplies no human-source or kernel credit. |

The generated record at `Docs/Stage0_Blueprint.md:17314-17339` repeats the gloss and explicitly
leaves precise definitions and premises, proof route, equivalent forms, axioms, machine status, and
artifact links pending. It adds no exact source statement.

No primary or authoritative edition, theorem/page locator, incorporated definitions, assumption
map, proof boundary, translation, correction or errata disposition, or independent review is
present in the repository. Accordingly, the provisional human status is `H1`: a famous proved
theorem family is recognizable, but exact source fidelity is not audited. This is not H0.

## Phrase-to-statement map

| Repository phrase | Candidate mathematical component | Prospective Lean component | Intake assessment |
|---|---|---|---|
| `紧集` / compact set | a compact subset `s` of an ambient space | `{s : Set α}` and `hs : IsCompact s` | subset reading is strongly indicated, but ambient structures and binders are absent |
| `连续函数` / continuous function | a function continuous relative to the compact set | `{f : α -> β}` and `hf : ContinuousOn f s` | likely relative-continuity reading; source definition and carrier choice remain open |
| `一致连续` / uniformly continuous | uniform continuity with both arguments restricted to the compact set | `UniformContinuousOn f s` | direct candidate, but source and formal definition crosswalk is not accepted |
| compact whole domain | a continuous function whose entire domain is compact | `[CompactSpace α]`, `Continuous f`, `UniformContinuous f` | related alternate candidate, not silently identified with the compact-set wording |
| `已验证` | inherited catalog status | no Lean component | no proof, source, or receipt credit |

Pinned mathlib defines `ContinuousOn f s` pointwise through `ContinuousWithinAt` on `s`. It defines
`UniformContinuousOn f s` by entourage convergence restricted to `s x s`. These definitions make
the direct candidate precise, but mathlib's precision cannot retroactively supply the missing
human-source edition or approve the catalog-to-Lean transport.

## Pinned formal candidate crosswalk

| Module and declaration | Exact candidate role | Intake credit and boundary |
|---|---|---|
| `Mathlib.Topology.UniformSpace.HeineCantor` / `IsCompact.uniformContinuousOn_of_continuous` | For uniform spaces `α` and `β`, compact `s : Set α`, and `f : α -> β`, `ContinuousOn f s` implies `UniformContinuousOn f s`. | Direct compact-subset Heine-Cantor candidate; supports M3 discovery only. No canonical root, source transport, proof-body audit, or M0 credit. |
| `Mathlib.Topology.UniformSpace.HeineCantor` / `CompactSpace.uniformContinuous_of_continuous` | On a compact uniform domain, `Continuous f` implies `UniformContinuous f`. | Direct whole-domain alternate candidate; its relation to the received subset wording must be checked before credit. |
| same module / `IsCompact.uniformContinuousAt_of_continuousAt` | Stronger control when the first point lies in the compact set and the second is merely close. | Adjacent stronger theorem, explicitly not the root. |

The module documentation names the family “Heine-Cantor,” but the repository catalog gives no
Heine or Cantor attribution and no citation. The formal anchor is therefore machine-side discovery,
not a human historical-source substitute.

## Human-source and machine boundary

Before H0, an independent reviewer must approve one immutable source edition and pinpoint
statement, all incorporated definitions and material assumptions, the proof boundary, any
translation, correction and errata findings, and the mapping to every formal binder and alternate
encoding. Before any M0 classification, downstream phases must freeze and elaborate the exact Lean
target, audit candidate identity and terminal bodies, freeze obligations and typed graphs, and run
the required composition, placeholder, axiom, provenance, trust, hermetic, and independent gates.

The successful intake probe proves only that the recorded declarations elaborate in the pinned
environment. It neither performs the scheduled exhaustive anchor audit nor claims that the root
theorem is accepted or theorem-complete.
