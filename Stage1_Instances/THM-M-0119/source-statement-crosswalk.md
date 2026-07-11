# THM-M-0119 Source-Statement Crosswalk

This is a provisional intake crosswalk, not an `H0` source audit. Exact scans, theorem/page
pinpoints, assumption reconciliation, errata searches, and independent review remain tasks for
`S56-M-0119-ANCHOR_AUDIT`.

| Canonical component | Primary-source anchor | Intake mapping | Open verification |
|---|---|---|---|
| Historical vanishing theorem and positivity hypotheses | Y. Kawamata, "A generalization of Kodaira-Ramanujam's vanishing theorem," *Mathematische Annalen* 261 (1982), 43-46 | Historical Kawamata vanishing source | exact theorem number/page; field and singularity conventions; errata |
| Kawamata-Viehweg formulation | E. Viehweg, "Vanishing theorems," *Journal fur die reine und angewandte Mathematik* 335 (1982), 1-8 | Companion primary development of the named theorem family | exact statement and relation to the selected pair form |
| klt pair and `D-(K_X+Delta)` formulation | J. Kollar and S. Mori, *Birational Geometry of Algebraic Varieties*, Cambridge Tracts in Mathematics 134 (1998), vanishing-theorem chapter | Modern reference used to normalize the executable scope | exact theorem/page, base-field convention, and Q-Cartier assumptions |
| Higher coherent cohomology conclusion | the same modern reference | Fixes the output as `H^i(X,O_X(D))=0` for all `i>0` | notation, integrality of `D`, and degree quantifier against the printed edition |

The legacy repository phrase "vanishing theorem for log canonical singularities" is insufficient
and potentially broader than the standard klt vanishing claim: ordinary Kawamata-Viehweg vanishing
does not permit silently replacing klt by log canonical. This dossier therefore freezes the klt
pair form and records the discrepancy instead of treating the legacy label `已验证` as source or
proof evidence. Any source-driven correction must be an explicit reviewed scope change.
