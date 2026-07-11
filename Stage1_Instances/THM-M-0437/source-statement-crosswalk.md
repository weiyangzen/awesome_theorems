# Source-statement crosswalk

| Claim component | Human source family | Formal candidate | Intake assessment |
|---|---|---|---|
| Shimura datum, reflex field, and canonical model | Goro Shimura, *Introduction to the Arithmetic Theory of Automorphic Functions*, Princeton University Press, 1971 | no exact Lean declaration frozen | Primary monograph family identified; edition page/theorem, assumptions, and errata are not yet pinned |
| Canonical-model formulation and reciprocity characterization | Pierre Deligne, "Travaux de Shimura," *Seminaire Bourbaki* 1970/71, expose 389, Lecture Notes in Mathematics 244 (1971) | no repo-local root expression | Primary expository source family; exact node and relationship to the construction claim require audit |
| Hodge-type embedding into a Siegel datum | the Hodge-type/abelian-type classification in the sources above and their cited Shimura construction results | legacy `HodgeEmbeddingData` | The legacy structure records fields but is not a source-faithful definition or theorem |
| Complex double quotient | standard Shimura-variety construction in the sources above | quotient and algebraic-geometry APIs in mathlib | Infrastructure candidate only; no checked root bridge |
| Canonical model over reflex field | canonical-model theorem selected during source audit | scheme APIs in mathlib | Major formalization boundary remains open |

The repository metadata supplies only the Chinese phrase, an attribution to
Goro Shimura, and the year 1964; it supplies no theorem number or assumptions.
Consequently the wording above is a scope freeze, not H0 source fidelity. The
statement phase must not choose between a general canonical-model theorem, a
Hodge-type moduli construction, and an integral-model theorem by convenience.

To raise the human status, record an immutable edition identifier, exact pages
and theorem numbers, every hypothesis and notation translation, corrections or
errata, and independent review. Until then the source status is `H2`.
