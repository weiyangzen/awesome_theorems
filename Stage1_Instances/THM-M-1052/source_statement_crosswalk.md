# Source-statement crosswalk

| Claim component | Human source anchor | Lean candidate | Intake assessment |
|---|---|---|---|
| Existence of an invariant measure | Repository source record, `Docs/Stage0_Blueprint.md`, THM-M-1052: `不变测度的存在性` | `ProbabilityTheory.Kernel.Invariant` and `ProbabilityMeasure` | Source record fixes the topic but omits domain and hypotheses; it cannot support an exact root by itself |
| Classical compact dynamical-system form | Discovery citation: N. Kryloff and N. Bogoliouboff, *La theorie generale de la mesure dans son application a l'etude des systemes dynamiques de la mecanique non lineaire*, Annals of Mathematics (2) 38 (1937), 65-113 | candidate `DeterministicStatementShape` in `AwesomeTheorems.Stage1.S1_M_219` | Bibliographic lead only; theorem/page, translation, assumptions, and errata have not been audited |
| Feller Markov form | Standard modern formulation: a Feller transition operator with tight Cesaro occupation measures has an invariant probability measure | candidate `StatementShape` and `KrylovBogolyubovData` in `AwesomeTheorems.Stage1.S1_M_219` | Likely useful generalization, but the local data package includes the desired invariant probability as a field and is not a terminal proof |
| Compactness/tightness step | Empirical measures admit a weakly convergent subnet/subsequence under compactness/tightness | mathlib Prokhorov, tightness, and weak-convergence APIs named by the legacy module | Candidate bridge only; exact topology and sequential-versus-net assumptions require audit |
| Invariance step | Cesaro shift error vanishes; the Feller property permits passage to the weak limit | kernel composition/integration APIs in pinned mathlib | Proof architecture only; no checked terminal bridge is credited at intake |

The proposed canonical direction is the Feller Markov-kernel theorem with an
explicit tightness hypothesis, with the compact deterministic theorem recorded
as a specialization. That choice is not final until a primary-source pinpoint
and exact Lean statement are reviewed. In particular, compactness, Hausdorff or
Polish assumptions, nonemptiness, measurability compatibility, and whether the
original theorem concerns flows, transformations, or transition kernels must
not be inferred away.

No `H0` claim is made. Required source work includes obtaining an immutable
copy of the 1937 paper, recording its hash/edition, locating the exact result
and all preceding definitions, checking corrections and modern attribution,
and mapping each premise to the selected Lean binder. The existing Lean module
is also unaccepted legacy material and must be re-elaborated and mutation-tested
in the statement phase.

