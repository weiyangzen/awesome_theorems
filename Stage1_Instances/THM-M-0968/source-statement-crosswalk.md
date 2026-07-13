# Source-statement crosswalk

## Repository provenance

- `Docs/researches/math_theorems.md:7071-7076` supplies exactly the title `Erdős盒原理`, Paul Erdős,
  1965, the gloss `超图中的匹配`, high importance, and status `已验证`. All six uncited lines were
  introduced at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`.
- `Docs/Stage0_Blueprint.md:26389-26414` repeats the record but explicitly leaves exact definitions
  and premises, proof route, dependencies, equivalent forms, axiom policy, machine status, and
  artifact links open.
- `Docs/Stage1_Targets_rev-5.6.json` admits the metadata-screened target at execution rank 1502 and
  resets it to `L0 / rework_required`; the source status is expressly untrusted and no legacy
  artifact is accepted.

These records justify intake membership. They are not a primary mathematical statement, source
crosswalk, or formal proof.

## Title, date, and gloss crosswalk

| Repository component | Material reading | Required Lean component | Intake status |
|---|---|---|---|
| `盒原理` / box principle | pigeonhole-style allocation or counting principle | finite objects, boxes, placement, collision or fiber conclusion | conflicts with hypergraph gloss and duplicates `THM-M-0914`; not selected |
| Paul Erdős, 1965 | possible pointer to *A problem on independent r-tuples* | source-versioned set-family proposition | strong bibliographic alignment only; catalog supplies no citation |
| `超图中的匹配` | pairwise-disjoint hyperedges or matching number | uniform family of finite sets plus `PairwiseDisjoint` or an equivalent predicate | topic only; no domain, binders, hypotheses, or conclusion |
| extremal matching problem | largest uniform family avoiding a matching of prescribed size, or minimum size forcing one | exact binomial/cardinality expression and side conditions | plausible later family; formula not authorized at intake |
| 1965 result | sufficiently-large-`n` partial result and previously known special cases | source-exact threshold theorem and checked relationship to any later form | distinct candidate, not silently upgraded to the full conjecture |
| `已验证` | untrusted inventory label | no declaration or proof body | explicitly rejected as evidence |

## Primary-source lead, not admitted

The zbMATH Open record `Zbl 0136.21302` / document `3221072` identifies Pál Erdős, *A problem on
independent r-tuples*, *Annales Universitatis Scientiarum Budapestinensis de Rolando Eötvös
Nominatae, Sectio Mathematica* 8 (1965), pages 93-96, ISSN 0524-9007. Its review describes
`r`-uniform generalized graphs, independent `r`-tuples as pairwise vertex-disjoint hyperedges, the
threshold function for forcing `k` independent edges, two extremal constructions, known `r = 2`
and `k = 2` cases, and a sufficiently-large-`n` theorem. The review explicitly says the complete
problem remained unsolved and records a correction to the right side of equation (8).

The four-page institutional scan at `https://www.renyi.hu/~p_erdos/1965-01.pdf` was inspected
outside the repository. It is 413744 bytes with SHA-256
`56e7147c8e58e48212120d5986d4285ef2fc8b9a3b7ee0c9cf897350e79509bf`; the article occupies
printed pages 93-95 and the fourth scan page is the volume index. Page 93 defines `f(n; r, k)` as
the least edge count forcing `k` independent `r`-tuples and `g(n; r, k-1)` as the count of
`r`-tuples meeting a fixed `(k-1)`-set. Page 94 proves that, for `n > c_r k` with `c_r` depending
only on `r`, `f(n; r, k) = 1 + g(n; r, k-1)`. Page 95 separately says it is "not impossible" that
the maximum-of-two-constructions formula (9) always holds and calls the general case elusive.

The primary paper and metadata align strongly with the catalog's author, year, and hypergraph-
matching gloss, but they do not resolve the conflicting title or prove that the uncited catalog
intended the page-94 theorem rather than the page-95 conjecture. The source was inspected but not
admitted as an immutable repository source packet, the zbMATH correction to equation (8) and any
later errata need a complete audit, and no independent reviewer has approved target identity or the
source-to-statement map. The paper is a primary source candidate, not `H0` evidence for a selected
root.

## Candidate formula boundary

Later sources commonly call a full extremal set-family formula the Erdős Matching Conjecture. Even
within that family, conventions vary between:

- maximum family size under matching number at most `s` versus minimum size forcing `s + 1`
  disjoint edges;
- parameters `k`, `s`, or `t` for uniformity and matching size;
- ground set `Fin n`, subsets of a fixed set, or arbitrary finite carriers;
- a maximum of the complete family on too few vertices and the family meeting a fixed small set;
- unrestricted admissible `n` versus a theorem only above a parameter-dependent threshold.

No formula is transcribed as canonical until a source of record fixes all conventions and a reviewer
approves its relation to the catalog. The 1965 partial theorem must not be mislabeled as a proof of
the full later conjecture, and its `k = 2` intersecting-family boundary must not duplicate the
separately owned Erdős-Ko-Rado target `THM-M-0822`.

## Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the intake probe checks
`Set.Sized`, `Finset.powersetCard`, `Set.PairwiseDisjoint`, `Disjoint`, and cardinality APIs. These
can express a uniform finite set family and pairwise-disjoint edges. They do not define a canonical
matching number, select an extremal convention, state the 1965 result, or prove a full matching
conjecture.

A bounded name/topic search across pinned mathlib and repo-local Lean found no exact Erdős matching,
independent-`r`-tuple, or hypergraph-matching theorem. This is intake discovery only, not the later
exhaustive immutable anchor audit and not evidence of global absence.

## Required source admission

The statement phase must obtain an immutable lawful source, resolve the title/gloss conflict and
catalog ownership, select one exact result, transcribe all incorporated definitions and ordered
binders, map every hypothesis and conclusion, audit the 1965 printed correction and later errata,
identify the proof boundary, and obtain independent review. It must then elaborate, fingerprint,
transport, and mutation-test the same proposition in Lean. Until then the canonical mathematical
and Lean targets remain null and the root remains `H5`.
