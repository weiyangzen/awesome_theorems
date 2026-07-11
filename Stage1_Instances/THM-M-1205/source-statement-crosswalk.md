# Source-statement crosswalk

## Available source record

`Docs/researches/math_theorems.md` records Tartar/Murat, 1978, and only the phrase "a compactness
method for conservation-law equations", with the untrusted label `已验证`. The generated Stage0 and
legacy Stage1 records add no theorem number, hypotheses, or bibliography. This wording identifies a
method family, not a unique proposition.

## Primary-source candidates

- Francois Murat, "Compacite par compensation", *Annali della Scuola Normale Superiore di Pisa*,
  Classe di Scienze (4), 5 (1978), 489-507.
- Luc Tartar, "Compensated compactness and applications to partial differential equations", in
  *Nonlinear Analysis and Mechanics: Heriot-Watt Symposium*, volume IV, Research Notes in
  Mathematics 39, Pitman (1979), 136-212.

These bibliographic candidates are discovery anchors only. The exact theorem/page, definitions,
assumptions, edition scan, and errata have not been inspected and therefore do not establish `H0`.

## Crosswalk

| Source element | Mathematical information fixed | Lean information required | Intake result |
|---|---|---|---|
| "compensated compactness" | a family using interacting weak differential constraints | exact proposition and constraint operators | unresolved |
| Tartar/Murat | historical attribution | selected primary theorem and stable citation | candidates only |
| "compactness method" | some compactness/nonlinear weak-continuity conclusion | sequence, topology, compact target, conclusion | unresolved |
| "conservation laws" | a possible PDE application | domain, flux, solution and entropy notions | unresolved |
| 1978 | historical locator | edition/theorem/page/errata | insufficient |
| `已验证` | untrusted metadata | inspectable proof or kernel receipt | no credit |

## Existing Lean boundary

`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_170.lean` defines useful distributional,
entropy-pair, compactness, and convergence vocabulary. Its own audit says no terminal compensated
compactness, div-curl, Young-measure reduction, or entropy compactness theorem was found. Its
`StatementShape` keeps the hard mechanism as a hypothesis, so it is neither an exact source target
nor terminal proof evidence. Its search results must be repeated against the pinned revision during
anchor audit.

Before `H0`, an independent reviewer must verify a selected primary theorem's exact wording,
theorem/page, definitions, all assumptions, errata, and every row of the source-to-Lean mapping.
