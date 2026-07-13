# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md:2069-2074` records only:

- title: `维塔利覆盖定理`;
- attribution: Giuseppe Vitali;
- year: 1908;
- gloss: `覆盖引理与微分定理` ("covering lemma and differentiation theorem");
- importance: high;
- untrusted formalization label: `已验证`.

All six lines originate in commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. `Docs/Stage0_Blueprint.md:7954-7979`
repeats this metadata while leaving the formal system, logical foundation, exact definitions and
premises, proof history, dependencies, axioms, and machine artifacts open. Neither file cites an
edition, theorem number, page, formula, translation, correction, or erratum.

The Chinese conjunction `与` is material: the received record may describe two results, a covering
result and a differentiation consequence. Intake must not erase that possible composition by
selecting a convenient single declaration.

## Historical-source lead

Crossref and an open Zenodo scan identify:

> G. Vitali, *Sui gruppi di punti*, Rendiconti del Circolo Matematico di Palermo 18 (1904),
> 116-126, DOI `10.1007/BF03014093`.

The eleven-page scan discusses extensions and measurable point sets. It is useful historical
provenance but does not, from the inspected text, pinpoint the modern metric/measurable covering
selection theorem or a differentiation theorem. Its 1904 publication metadata also conflicts with
the catalogue's bare year 1908.

A contemporary JFM record, preserved as zbMATH document `2639907` / JFM `39.0101.05`, identifies:

> G. Vitali, *Sui gruppi di punti e sulle funzioni di variabili reali*, Atti della Accademia delle
> Scienze di Torino 43 (1908), 229-246.

Its German review says that, using a theorem about collections of intervals, Vitali gives new proofs
of earlier results from *Sulle funzioni integrali* (Torino Atti 40 (1905), 1021-1034) that extend to
functions of several variables. This is contemporary bibliographic/review evidence for the
covering-to-differentiation relationship, not a transcription of the primary theorem. The primary
text was not obtained. Encyclopedia of Mathematics revision `55740` gives the same title, year, and
JFM identifier but pages 75-92, while stating a modern measurable form with countable disjoint
coverage modulo outer measure zero. The pagination conflict and modernized statement both remain
explicitly unresolved; the contemporary JFM locator is retained provisionally.

The strongest human-source classification is therefore `H1`, not `H0`: the classical family and
credible historical records are known, but no primary-text theorem passage, source-selected exact
proposition or bundle, and premise map has been independently reviewed.

## Clause crosswalk

| Repository phrase or omitted clause | Human-source status | Pinned Lean candidates | Intake decision |
|---|---|---|---|
| "covering lemma" | family named; no exact proposition | topological closed-ball and measurable a.e. extraction | variant open; do not substitute |
| "differentiation theorem" | object and conclusion absent | differentiation of measures, density points, and function averages | meaning and root role open |
| ambient domain | absent | pseudo-metric space, measurable space, second-countable Borel space | open |
| covering family | absent | indexed sets/closed balls or `VitaliFamily` | open |
| size/fineness | absent | bounded radii, fine subfamily, or small-scale doubling | open |
| disjoint selection | cardinality and coverage absent | arbitrary selected set or countable subfamily | open |
| enlargement | constant and set convention absent | `tau > 3` closed-ball dilation | candidate only |
| coverage | exact versus null-set absent | ball inclusion or `mu (s \\ union) = 0` | open |
| differentiated object | absent | locally finite measure or locally integrable function | open |
| limit | absent | Radon-Nikodym derivative, density one, or point value | open |
| `已验证` | untrusted inventory metadata | no proposition or proof object | no H or M credit |

## Formal candidate crosswalk

The intake probe elaborates representative declarations at the pinned revision:

| Declaration | Candidate role | Unclosed gate |
|---|---|---|
| `Vitali.exists_disjoint_subfamily_covering_enlargement_closedBall` | topological closed-ball selection | exact source identity, enlargement convention, expression fingerprint, provenance and trust audit |
| `Vitali.exists_disjoint_covering_ae` | measurable countable a.e. covering | source assumptions and conclusion mapping, exact target or transport, provenance and trust audit |
| `Vitali.vitaliFamily` | bridge from small-scale doubling to the Vitali-family abstraction | decision whether it is a construction child or only an anchor; no root identity |
| `VitaliFamily.FineSubfamilyOn.exists_disjoint_covering_ae` | abstract fine-family extraction | its covering property is inherited from structure data; cannot circularly prove a source construction theorem |
| `VitaliFamily.ae_tendsto_rnDeriv` | differentiation of measures | decision whether differentiation belongs to the target bundle and checked covering-to-differentiation composition |
| `VitaliFamily.ae_tendsto_measure_inter_div` | density-point consequence | set and measurability scope mapping |
| `VitaliFamily.ae_tendsto_average_norm_sub` | norm-form Lebesgue differentiation | function/codomain/source variant mapping |
| `VitaliFamily.ae_tendsto_average` | vector-valued average convergence | stronger structure and completeness assumptions; cannot replace an unspecified scalar result |

All representative candidate axiom reports observed by the probe are
`[propext, Classical.choice, Quot.sound]`. That is discovery evidence only; a later anchor audit must
resolve terminal bodies, imports, full transitive dependencies, and acceptance under a frozen
foundation/TCB profile.

Before leaving `H1`, an accountable source reviewer must admit an immutable edition, select the
exact root or root bundle, transcribe all incorporated definitions and ordered clauses, map every
assumption and conclusion, audit translation/corrections/errata, and approve the 1904/1908 historical
boundary. Before statement acceptance, Lean work must freeze minimal imports and an elaborated
expression and pass removed-hypothesis, changed-domain, binder-scope, and boundary mutations.
