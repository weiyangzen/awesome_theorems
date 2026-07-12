# Source-statement crosswalk

The authoritative repository phrase for this item is `七维怪球的存在`
(`there exists a seven-dimensional exotic sphere`). Its accompanying
`已验证` status is explicitly untrusted under rev-5.6. The standard expansion
of "exotic sphere" used at intake is a smooth manifold homeomorphic but not
diffeomorphic to the standard smooth sphere; this expansion still requires
pinpoint primary-source confirmation at the human-source gate.

| ID | Claim component | Repository anchor | Primary-source discovery anchor | Intake assessment |
|---|---|---|---|---|
| `SRC-M0605-ROOT` | Existence of a seven-dimensional exotic sphere | `Docs/researches/math_theorems.md`, entry `米尔诺怪球`; projected as `THM-M-0605` in `Docs/Stage0_Blueprint.md` | John Milnor, *On manifolds homeomorphic to the 7-sphere*, Annals of Mathematics (2) 64 (1956), 399-405, DOI `10.2307/1969983` | Named primary proof source located; edition capture, theorem/page mapping, assumptions, errata, and independent review remain open, so this is not H0 |
| `SRC-M0605-DIM` | Dimension is exactly seven | The repository claim explicitly says `七维` | The primary paper's title and constructions concern the 7-sphere | Stable human scope; the precise manifold-dimension encoding is a statement task |
| `SRC-M0605-TOPO` | The witness is homeomorphic to the standard 7-sphere | Implicit in the term `怪球`, but not defined in the repository record | The paper is explicitly about manifolds homeomorphic to the 7-sphere | The homeomorphism requirement prevents substitution by a merely homotopy-equivalent manifold |
| `SRC-M0605-SMOOTH` | The witness is not diffeomorphic to the standard smooth 7-sphere | Implicit in `怪球` | Milnor's paper is the historical source for nonstandard differentiable structures on the 7-sphere | Exact obstruction, orientation scope, and page-level inference remain unaudited |
| `SRC-M0605-CONSTR` | A suitable sphere-bundle total space provides the witness | Not specified | Milnor's construction studies certain 3-sphere bundles over the 4-sphere | Candidate proof architecture only; no bundle parameters or conclusion are credited at intake |
| `SRC-M0605-MACHINE` | A public Lean proof closes this exact claim | The source metadata only says `已验证` | None accepted at intake | No Lean module, declaration, terminal body, immutable external pin, or kernel receipt has been audited |

## Statement decisions passed forward

The statement phase must preserve the existence quantifier, dimension seven,
homeomorphism, and failure of every diffeomorphism. It must decide the exact
Lean manifold and standard-sphere models; whether orientation data is internal
to the proof or the root; and whether the root uses `IsEmpty` of a
diffeomorphism type or an equivalent negated existential. Any credited
alternate encoding requires a checked transport.

This crosswalk is discovery evidence only. It does not claim that the cited
pages have been inspected in this clone, that the source has no corrections,
or that any formal proof exists. The human axis therefore remains `H1`, and
the machine axis remains `M4`.
