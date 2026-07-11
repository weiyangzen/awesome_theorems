# Source-statement crosswalk

## Available source record

The repository research record (`Docs/researches/math_theorems.md`) attributes the theorem to Boris Moishezon, dates it to 1966, and gives only the Chinese gloss “algebraicity of Moisezon manifolds.” `Docs/Stage1_Blueprint.md` repeats that gloss. Neither record supplies a publication, theorem number, page, hypotheses, or errata, and its `已验证` label is explicitly untrusted under rev-5.6.

No primary mathematical source is asserted by this intake. Consequently the crosswalk is provisional and the source debt is `H3`, not `H0` or `H1`.

## Provisional crosswalk

| Intake component | Repository wording / interpretation | Disposition |
|---|---|---|
| Moishezon manifold | named object in “Moisezon manifolds” | included; exact definition open |
| compact complex manifold | conventional ambient domain of the scoped theorem | provisional; primary-source check required |
| algebraicity | existence of a projective algebraic model up to bimeromorphism | conservative interpretation; disambiguation required |
| bimeromorphic comparison | makes “algebraicity” a relationship to the same analytic object | included; exact category and direction open |
| Kähler hypothesis | belongs to a nearby projectivity formulation | excluded unless primary-source audit proves it is the intended root |

## Legacy boundary

`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_037.lean` explicitly describes itself as a statement-shape/scheme-side wrapper rather than a proof. It is discovery input only. Its abstract `MoishezonAnalyticData`, dimension profile, and projective-model structures neither establish source fidelity nor provide a canonical Lean target for rev-5.6.

## Required H-gate follow-up

Locate a stable primary publication or authoritative edition, record its exact theorem label/page and original hypotheses/conclusion, check translation and spelling variants (`Moishezon`/`Moisezon`), identify errata, and obtain independent review of the mapping. Until that work resolves the bimeromorphic-versus-projective ambiguity, the statement phase must fail closed rather than broaden or substitute the theorem.
