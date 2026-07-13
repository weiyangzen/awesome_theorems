# Source-statement crosswalk

## Repository source record

`Docs/researches/math_theorems.md:4643-4648`, introduced in commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`, supplies exactly:

| Catalog field | Received value | Intake consequence |
|---|---|---|
| title | `连通性定理` | Names connectedness but is not used alone for identity. |
| attribution | many mathematicians | Does not identify an author, source, definition, or proof. |
| time | nineteenth century | Does not select a work, edition, or theorem locator. |
| statement | `连通集的连续像连通` | Fixes the connected-subset continuous-image claim. |
| importance | high | Scheduling metadata only. |
| formalization status | `已验证` | Explicitly untrusted; no source or machine credit. |

`Docs/Stage0_Blueprint.md:17125-17150` repeats the claim but leaves the target formal system,
logical foundation, exact definitions and premises, proof route, dependencies, alternate forms,
axioms, machine status, and artifact links pending. The repository record has no bibliography,
pinpoint theorem, definition chain, proof, correction history, translation, or reviewer.

## Inspected modern proof source lead

The Stacks Project, *Topology*, Section 5.7, Lemma 5.7.2, stable tag `0376` and source label
`lemma-image-connected-space`, was inspected at immutable Git commit
`3683021e95ea1610e2250658d59abc18fdf0bd7b` (2026-07-10). Its preceding Definition 5.7.1 says a
connected topological space is nonempty and admits no nontrivial clopen decomposition. Lemma 5.7.2
states:

> Let `f : X -> Y` be a continuous map of topological spaces. If `E` is a connected subset of
> `X`, then `f(E)` is connected as well.

Its proof pulls a clopen subset of `f(E)` back to a clopen subset of `E`, uses connectedness to
make that preimage empty or all of `E`, and proves that the original subset is correspondingly
empty or all of `f(E)`. The immutable `topology.tex` blob is
`e93e346dc68083c19c876ff42e804778bc3f27b1`, with SHA-256
`44548f530113104b4e64385090ee1ac7be2d64e5841d749ab986e04efaaf5981`.

The tag history records creation in 2009 and proof edits in 2023. The current tag has one slogan
comment, not a mathematical correction. This is an authoritative modern secondary source lead,
not the catalog's unidentified nineteenth-century source. Its exact historical relationship,
local/global continuity transport, complete correction disposition, and independent review remain
open. It supports provisional `H1`, not `H0`.

## Clause crosswalk

| Catalog/source component | Modern source meaning | Pinned Lean candidate | Intake status |
|---|---|---|---|
| connected set | nonempty subset with no nontrivial separation | `IsConnected s := s.Nonempty ∧ IsPreconnected s` | candidate conventions align; independent approval open |
| continuous image | `f(E)` under a globally continuous `f` | `f '' s` under `ContinuousOn f s` | local version is sharper; checked global-to-local bridge open |
| remains connected | image is nonempty and preconnected | `IsConnected (f '' s)` | direct candidate conclusion |
| arbitrary spaces | no separation or metric assumptions | arbitrary `TopologicalSpace alpha/beta` | aligned candidate domain |
| empty set | excluded by connectedness definition | impossible under `IsConnected s` | explicitly excluded; `IsPreconnected` variant separate |
| nineteenth century / many mathematicians | catalog historical metadata only | no Lean component | attribution and source identity unresolved |
| `已验证` | untrusted inventory label | no declaration or proof object | rejected as evidence |

## Formal-source boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, module
`Mathlib.Topology.Connected.Basic` defines `IsConnected` with the same nonempty convention and
declares:

```text
IsConnected.image :
  IsConnected s -> (f : alpha -> beta) -> ContinuousOn f s -> IsConnected (f '' s)
```

Its source body constructs image nonemptiness and invokes the substantive
`IsPreconnected.image` body. The intake probe reports axioms `propext`, `Classical.choice`, and
`Quot.sound`. Those facts make it a strong direct candidate, not accepted `M0-W`: the canonical
expression and environment are not fingerprinted, the Stacks global-continuity form is not yet
transported, and the anchor, terminal provenance, trust, proof, and master-acceptance phases remain
open.

`IsPreconnected.image`, `isConnected_range`, and `Function.Surjective.connectedSpace` are recorded
only to prevent substitution. Path-connected image preservation belongs to separate target
`THM-M-0627` and supplies no credit here.

Before `H0`, a source reviewer must approve an immutable edition/revision, pinpoint definitions,
statement, proof and premises, correction/errata disposition, attribution boundary, and this
row-by-row map. Before machine credit, the statement and anchor phases must establish exact target
identity and complete provenance/trust evidence.
