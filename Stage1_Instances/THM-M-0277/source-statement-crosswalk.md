# Source-statement crosswalk

## Repository authority

`Docs/researches/math_theorems.md:1992-1997` supplies exactly the title "closed graph theorem," the
attribution Stefan Banach, the year 1932, the gloss "continuity of closed linear operators," high
importance, and status `已验证` ("verified"). An identical second record appears at lines 2267-2272
under functional analysis. Both entered the repository unchanged in commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. Neither record cites a work, edition, theorem, page,
definition, assumption, proof boundary, correction, erratum, or formal artifact.

The generated Stage0 projection at `Docs/Stage0_Blueprint.md:7657-7682` repeats the gloss and
explicitly leaves precise definitions and premises, proof route, dependencies, equivalent
formulations, axioms, classical dependence, machine status, and artifact links open. The rev-5.6
manifest preserves `已验证` only as `source_status_untrusted` and resets this target to
`L0 / rework_required`. The manifest category `分析学 / 实分析` comes from the first retained duplicate
and does not by itself select real scalars.

## Human-source status

Banach's attribution and year are catalogue leads only. This intake does not claim a versioned
primary proof source, theorem/page locator, complete premise-to-conclusion map, correction or errata
audit, proof-node crosswalk, or independent review. H1 records a historically proved theorem family
with explicit source-reconstruction debt. Reaching H0 requires a lawful immutable primary or
authoritative edition, its incorporated definitions and assumptions, the complete proof boundary,
all corrections and errata, a node-specific crosswalk, and an identified independent functional-
analysis reviewer.

## Literal crosswalk

| Repository phrase | Mathematical decision | Prospective Lean component | Intake status |
|---|---|---|---|
| `闭图像定理` | classical closed graph theorem, not merely the definition of a closed operator | one source-approved root plus checked alternate transports | family identified; exact root open |
| "linear operator" | total linear map or partially defined operator | `g : E ->ₗ[𝕜] F` versus `E ->ₗ.[𝕜] F` | totality is omitted and proposition-changing |
| "closed" | the graph is topologically closed | `IsClosed (g.graph : Set (E × F))` in the product norm topology | likely premise; topology/source mapping open |
| implicit spaces | complete normed vector spaces in the standard Banach-space form | `NormedAddCommGroup`, `NormedSpace`, and `CompleteSpace` instances for `E` and `F` | omitted by repository source |
| implicit scalar | traditionally real or complex; mathlib candidate is more general | `[NontriviallyNormedField 𝕜]` | source field and generalization transport open |
| "continuity" | continuity of the underlying total map, equivalently boundedness in the normed linear setting | `Continuous g`, with any boundedness form linked by a checked theorem | conclusion encoding open |
| `已验证` | untrusted catalogue status | no proposition, proof object, or accepted receipt | explicitly rejected as evidence |

## Pinned formal candidates

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the minimal direct
module is `Mathlib.Analysis.Normed.Operator.Banach`.

- `LinearMap.continuous_of_isClosed_graph` is the direct total-map candidate. It quantifies over a
  nontrivially normed field, complete normed spaces `E` and `F`, and `g : E ->ₗ[𝕜] F`; a closed graph
  implies `Continuous g`.
- `LinearMap.continuous_of_seq_closed_graph` is a sequential criterion. It is a candidate alternate
  encoding, not statement identity by name.
- `ContinuousLinearMap.ofIsClosedGraph` packages the direct conclusion as a continuous linear map;
  it is a constructor/wrapper rather than a separately credited theorem root.
- `LinearPMap.IsClosed` defines closedness for partially defined operators. It exposes why an
  unqualified "closed linear operator" is ambiguous; it does not imply the target continuity claim.

The intake probe elaborates these APIs and reports `[propext, Classical.choice, Quot.sound]` for the
two total-map theorem candidates. This is E3-style candidate evidence only. The statement phase must
serialize an exact target, pin the minimal environment, and check all required transports and
mutations before any proof-body or M0 credit can be considered.

## Source gate

Before statement acceptance, accountable reviewers must select and preserve an immutable exact
human statement; map total domain, completeness, scalar, topology, graph, and conclusion
conventions; resolve real/complex versus generalized scalar scope; audit boundary cases and errata;
and elaborate the same proposition with checked alternate directions. Until then the canonical
human and Lean statements remain null, and the direct mathlib theorem is a non-credited candidate.
