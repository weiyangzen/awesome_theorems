# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md` records `Petersen定理`, Julius Petersen, 1891, and the gloss
`三次桥less图有完美匹配` ("a cubic bridgeless graph has a perfect matching"). Stage0 repeats that
metadata but leaves exact definitions, assumptions, proof path, axioms, and machine artifacts open.
The rev-5.6 manifest preserves `已验证` only as `source_status_untrusted`.

## Inspected primary source

Julius Petersen, "Die Theorie der regulären graphs," *Acta Mathematica* 15 (1891), 193-220,
DOI `10.1007/BF02392606`, was inspected using the CC0 scan in Zenodo record 2304433. The observed
29-page, 2,288,748-byte PDF has SHA-256
`8762abd5e2f1fb3edcd1917b4db3b0c213a75d4ecfe026829b58e2e7913cca8c`.

- Printed page 194 states that multiple lines may join the same two points. Petersen's graph model
  is therefore not mathlib's simple-graph model.
- Printed page 210 defines a `Blatt` as a graph part connected to the rest by only one line, the
  historical bridge-separated-piece notion used later.
- Printed page 218 concludes: `Ein primitiver graph vom dritten Grade muss wenigstens drei
  Blätter haben.` A primitive cubic graph must have at least three such leaves.
- Printed pages 218-219 state that a nonprimitive cubic graph decomposes into a factor of degree
  two and a factor of degree one, and discuss a line forced into one factor.

These passages give the historical route: absence of a bridge-separated leaf rules out the
primitive case, and the resulting degree-one spanning factor is the modern perfect matching.
However, an accountable translation, a complete definition and proof-node mapping, corrections or
errata review, and independent review remain open. In particular, the catalog does not state whether
it means Petersen's connected multigraph setting or the standard modern finite simple-graph
specialization. The intake source status is therefore `H1`, not `H0`.

## Crosswalk

| Repository/source phrase | Candidate modern component | Pinned Lean component | Intake status |
|---|---|---|---|
| `graph dritten Grades` | every vertex has degree three | `SimpleGraph.IsRegularOfDegree 3` | API checked; multigraph degree transport open |
| no `Blätter` / `bridge-less` | no present edge disconnects its endpoints when removed | `SimpleGraph.IsBridge` | API checked; source terminology and quantifier transport open |
| `Factor ersten Grades` | spanning one-regular factor / perfect matching | `SimpleGraph.Subgraph.IsPerfectMatching` | API checked; representation transport open |
| factor of degree two | complement/two-factor route | no credited root expression | alternate encoding not frozen |
| modern matching criterion | Tutte condition | `SimpleGraph.tutte` | exact pinned theorem checked; bridge/cubic reduction absent |
| `已验证` | untrusted inventory status | no proposition or proof | explicitly rejected as evidence |

## Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the intake probe checks
the types of regularity, bridge, edge-connectivity, matching, and Tutte interfaces. A bounded
case-insensitive search of repo-local Lean and pinned mathlib for `Petersen`, `bridgeless`,
`bridge-free`, and cubic/perfect-matching combinations found no exact closure. That search is
intake discovery, not the later immutable external anchor audit and not an absence proof.

Tutte's theorem is a plausible proof architecture, but it does not itself prove that a bridgeless
cubic graph satisfies the Tutte condition. No theorem body, source transport, or closure credit is
claimed here.
