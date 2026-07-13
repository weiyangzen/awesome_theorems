# Source-statement crosswalk

## Repository source record

The only repository-supplied record is `Docs/researches/math_theorems.md:4650-4655`, introduced in
commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`:

| Catalog field | Received value | Statement consequence |
|---|---|---|
| title | `道路连通性定理` | Provisionally identifies path-connectedness, but names a family rather than one proposition. |
| attribution | many mathematicians | Does not identify a source, definition, or proof. |
| time | nineteenth century | Does not select a work or edition. |
| statement | `道路连通空间的性质` | Supplies no binders, assumptions, or conclusion. |
| importance | high | Scheduling metadata only. |
| formalization status | `已验证` | Explicitly untrusted; supplies no human or machine proof credit. |

The generated Stage0 record at `Docs/Stage0_Blueprint.md:17152-17177` repeats the gloss while
marking the formal system, definitions and premises, proof route, dependencies, alternate forms,
logical requirements, machine status, and artifact links as pending. It does not refine the claim.

The catalog is a secondary compilation with no bibliography for this entry. No primary source
edition, theorem/page locator, proof boundary, dependent result, correction history, errata check,
translation, or independent reviewer has been supplied or accepted. The repository record is E5
intake provenance, not H0 or H1 evidence for an exact proposition.

## Phrase-to-statement map

| Received or candidate component | Required source decision | Prospective Lean component | Intake result |
|---|---|---|---|
| path-connected space | path versus arc convention, nonemptiness, path domain, and whole-space versus relative-set form | `PathConnectedSpace` or `IsPathConnected` | unresolved; the catalog gives no definition |
| "properties" | one exact implication, equivalence, preservation, or construction theorem | one declaration with fixed binders | no result selected |
| continuous image | domain set/space, `ContinuousOn` versus `Continuous`, image/range, and any surjectivity | `IsPathConnected.image'`, `IsPathConnected.image`, or `Function.Surjective.pathConnectedSpace` | plausible branch only; neighboring `THM-M-0626` is not source authority |
| connectedness consequence | set-level or typeclass-level result and nonempty convention | `IsPathConnected.isConnected` or `PathConnectedSpace.connectedSpace` | plausible branch only |
| component characterization | path component, universal set, subtype, or zeroth homotopy quotient | `isPathConnected_iff_eq`, `pathConnectedSpace_iff_eq`, or related transports | plausible branch only |
| closure property | exact construction and additional structures | union, quotient, group-operation, or other APIs | no construction selected |

There are consequently no ordered binders, hypotheses, exact conclusion, credited alternate
encoding, statement fingerprint, canonical obligation, or proof body.

## Formal-source boundary

A bounded inspection found the following adjacent declarations in
`Mathlib.Topology.Connected.PathConnected` at pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`:

- `Joined`, `JoinedIn`, `IsPathConnected`, and `PathConnectedSpace`;
- `isPathConnected_iff` and `pathConnectedSpace_iff_univ`;
- `IsPathConnected.image` and `Function.Surjective.pathConnectedSpace`;
- `IsPathConnected.isConnected` and the `PathConnectedSpace.connectedSpace` instance;
- `isPathConnected_iff_pathConnectedSpace`.

Their differing types expose rather than resolve the catalog ambiguity. `IntakeProbe.lean`
authenticates names and types only. This bounded inspection is not the dependency-ordered anchor
audit, does not claim exhaustive discovery, and gives no statement or proof credit.

## Human-source gate

To leave `H5`, an accountable reviewer must first approve a stable truth-valued target and an
immutable primary or authoritative source. The crosswalk must then bind the exact theorem and
incorporated definitions, every assumption and conclusion, proof and dependency boundaries,
corrections and errata, translation, and each source component to the mathematical and Lean
encodings. Until that happens, ordinary statement and theorem-proof execution remains blocked.
