# Source-statement crosswalk

## Repository source record

`Docs/researches/math_theorems.md:4622-4627` contains exactly six uncited lines, all introduced by
repository commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`:

| Catalog field | Received value | Statement consequence |
|---|---|---|
| title | `乌雷松度量化定理` | Identifies the Urysohn metrization family. |
| attribution | Pavel Urysohn | Historical metadata only; spelling and source identity still require review. |
| time | 1925 | Points toward the historical publication but does not select a passage. |
| statement | `第二可数正则空间可度量化` | Omits the separation convention and metric-versus-pseudometric meaning. |
| importance | high | Scheduling metadata only. |
| formalization status | `已验证` | Explicitly untrusted; gives no human or machine proof credit. |

The generated Stage0 projection at `Docs/Stage0_Blueprint.md:17044-17069` repeats the gloss while
marking exact definitions and premises, proof route, dependencies, equivalent formulations,
axioms, machine status, and artifact links as pending. It is planning metadata, not a source.

## Historical source lead

Crossref metadata identifies Paul Urysohn, "Zum Metrisationsproblem," *Mathematische Annalen*
**94**(1) (1925), pages 309-315, DOI `10.1007/BF01208661`. The publisher metadata records receipt
on 28 September 1924 and issue date December 1925. This is a bibliographic discovery lead, not an
accepted H0 packet.

During intake the publisher article page was inspected, but the original full text was access
gated. No exact theorem passage, German definition of regularity, metric convention, incorporated
lemma, proof boundary, translation, correction history, errata, or independent review was
captured. The catalog's attribution and date therefore support H1 only, not source-fidelity
closure.

## Clause crosswalk

| Catalog component | Required source decision | Prospective Lean component | Intake result |
|---|---|---|---|
| topological space | ambient set/type and topology | `X : Type u`, `[TopologicalSpace X]` | candidate domain only |
| second countable | exact countable-base convention | `[SecondCountableTopology X]` | strong direct interface located |
| regular | whether T0/T1/Hausdorff is included | `[RegularSpace X]` versus `[T3Space X]` or separate `[T0Space X]` | materially unresolved |
| metrizable | genuine compatible metric versus pseudometric | `MetrizableSpace X` versus `PseudoMetrizableSpace X` | materially unresolved |
| compatible topology | structure existence or explicit topology equality | mathlib metrizable structures, inducing map, or embedding | encoding and transports unresolved |
| `已验证` | untrusted inventory label | no proposition or proof object | explicitly rejected as evidence |

Under pinned mathlib definitions, `RegularSpace` need not be Hausdorff or T0;
`T3Space` extends `T0Space` and `RegularSpace`; and `MetrizableSpace` extends
`PseudoMetrizableSpace` and `T0Space`. Consequently the omitted convention changes the truth of
the literal formal reading, not just notation.

## Pinned formal candidates not credited

At mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, source file
`Mathlib/Topology/Metrizable/Urysohn.lean` states both exact-topic variants:

| Declaration | Pinned hypothesis/conclusion boundary | Intake disposition |
|---|---|---|
| `TopologicalSpace.PseudoMetrizableSpace.of_regularSpace_secondCountableTopology` | `[RegularSpace X] [SecondCountableTopology X]` yields `PseudoMetrizableSpace X` | usable candidate for the weak-separation reading, not a metric-root substitute |
| `TopologicalSpace.metrizableSpace_of_t3_secondCountable` | `[T3Space X] [SecondCountableTopology X]` yields `MetrizableSpace X` | usable candidate for the full metric reading, but its extra separation convention is not source-transported |
| `TopologicalSpace.exists_isInducing_l_infty` | weak regularity gives an inducing map to bounded real sequences | construction/alternate-form candidate only |
| `TopologicalSpace.exists_embedding_l_infty` | T3 gives an embedding into bounded real sequences | construction/alternate-form candidate only |

The module header calls the result T3 plus second countability implies metrizability, while comments
also label the weak pseudometric and full metric declarations as Tychonoff versions. Those library
comments are discovery context, not historical source acceptance. The probe reports the candidates'
current axiom sets but does not complete terminal-body provenance, source transport, trust review,
or root proof validation.

## Neighbor and substitution boundary

- `THM-M-0621` owns Urysohn's lemma; it may be a proof dependency but is not this theorem.
- `THM-M-0622` owns Tietze extension; no source or proof state transfers.
- `THM-M-0624` and `THM-M-0625` own different metrization theorems with different hypotheses.
- Pseudometrization of a non-T0 regular space, an embedding alone, or a converse characterization
  cannot replace the catalog's metric conclusion without an accepted checked relationship.

## Required next crosswalk

Before the statement phase can freeze a root, independent reviewers must admit a lawful immutable
source, select the exact theorem and definition convention, map every premise and conclusion, and
resolve metric versus pseudometric and Urysohn/Tychonoff attribution. The Lean statement phase must
then elaborate only that claim, record its minimal imports and expression/environment fingerprints,
compile every credited transport, and execute the four mandatory statement-mutation classes.
