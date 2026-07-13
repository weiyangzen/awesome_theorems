# THM-M-0910 source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:6656-6661` records only:

- title: `Caucal定理`;
- attribution: Didier Caucal;
- year: 1996;
- gloss: `图的可判定性`;
- importance: high; and
- untrusted formalization label: `已验证`.

All six lines originate at repository commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. `Docs/Stage0_Blueprint.md:24818-24843`
repeats the gloss while explicitly leaving exact definitions and premises, proof route,
dependencies, equivalent formulations, axioms, machine status, and artifact links open. These
records establish catalog identity only and do not state a truth-valued proposition.

## Primary source-family lead

Didier Caucal, *On Infinite Transition Graphs Having a Decidable Monadic Theory*, in F. Meyer auf
der Heide and B. Monien (eds.), *Automata, Languages and Programming*, ICALP 1996, Lecture Notes in
Computer Science 1099, pages 194-205, DOI `10.1007/3-540-61440-0_128`.

The inspected IRISA-hosted full text is a 50-page expanded manuscript of unresolved exact
version/date, available as
`monadic.ps.gz`. Its compressed SHA-256 is
`601c0129e4faade8c926935cbc8b0cdaf3feb6a7694451289c2f17dc2b2c3d8f`; decompressed PostScript
SHA-256 is `fce643da40002fd0083ef3477f39732a8420a0f38df6518046975b1ec16cdd5e`.
The paper says it was partially presented at ICALP 1996, defines monadic second-order sentences on
labelled directed graphs, and exposes several candidate results rather than one theorem named
"Caucal theorem."

A later same-title journal publication is Didier Caucal, *Theoretical Computer Science* 290(1)
(2003), pages 79-115, DOI `10.1016/S0304-3975(01)00089-5`. It is a possible revision
lead, but its relationship to the proceedings and IRISA manuscript is unverified. It is not an
admitted replacement for the catalog's 1996 attribution. Version reconciliation, errata/corrections, exact
proof boundaries, and independent review remain open.

## Candidate result crosswalk

| Candidate source node | Source content observed | Missing mapping gate | Intake credit |
|---|---|---|---|
| Proposition 2.5 | decidability is preserved by a rational inverse substitution followed by a rational restriction, under a uniquely rooted input graph | exact transformation encodings, effectiveness, binders, and whether this is the catalog root | source discovery only |
| Theorem 2.7 | Rabin's decidability theorem for complete deterministic binary-labelled trees | external dependency rather than Caucal's root; source and formal integration open | no root credit |
| Corollary 2.8 | every graph in `REC_Rat` has a decidable monadic theory | complete definition of `REC_Rat`, effective presentation, uniformity, and source selection | strongest title-level candidate, not canonical |
| Corollary 3.7 | `MTh((G . N*)|L)` is decidable for recognizable `G` and rational `L` | notation, word-graph encoding, input representation, and relationship to Corollary 2.8 | candidate alternate, no checked transport |
| Corollaries 3.8/3.14 | pushdown transition graphs / regular graphs have decidable monadic theory | separate inherited results and narrower graph families | consequences only |
| Structural results | representative completeness, strict containment, Boolean closure, and transformation closure | these conclusions are not decidability itself | excluded as silent root substitutions |

The source family supports at most discovery evidence. It does not support `H0`: the repository has
not selected a proposition, no admitted immutable edition and complete definition/premise/proof
crosswalk exists, the 1996/2003 relationship and errata are unaudited, and no independent reviewer
has accepted the mapping. The received gloss remains `H5` because it is not a stable proposition.

## Repository-to-source fields

| Repository field | Source-family relationship | Frozen at intake? |
|---|---|---|
| Didier Caucal | exact author match | yes, as catalog identity |
| 1996 | exact ICALP publication-year match | yes, as catalog identity |
| `图的可判定性` | broadly resembles decidable monadic theories of selected infinite transition graph families | no: omits graph class, logic, presentation, and conclusion |
| `已验证` | no trustworthy meaning under rev-5.6 | no evidence credit |
| exact source | DOI and full-text leads located | no: catalog does not cite them and master has not admitted an edition |
| exact theorem | several candidates located | no selection or transport |

## Formal candidate crosswalk

| Pinned declaration | Candidate role | Missing gate |
|---|---|---|
| `FirstOrder.Language.graph` | an ordinary simple-graph first-order signature | labelled directed edges and monadic second-order set variables |
| `SimpleGraph.structure` | interprets a simple graph as a first-order structure | source graph model and presentation transport |
| `FirstOrder.Language.Sentence` / `Formula.Realize` | first-order syntax and semantics | MSO syntax, set valuation, source satisfaction equivalence |
| `FirstOrder.Language.completeTheory` | set of true first-order sentences | effective decidability and the source's `MTh(G)` |
| `DFA` / `DFA.accepts` / `Language.IsRegular` | finite automata and regular word languages | rational graph transformations, effective encodings, and reduction proof |
| `ComputablePred` | target shape for a computable encoded predicate | formula coding, graph presentation, uniform decider, and exact theorem |

Before statement acceptance, reviewers must select one admitted source proposition, freeze every
definition, binder, assumption, conclusion, and boundary case, elaborate the exact Lean target
under minimal pinned imports, compile every credited transport, serialize the expression and
environment fingerprints, and run the required removed-hypothesis, changed-domain, binder-scope,
and boundary mutations.
