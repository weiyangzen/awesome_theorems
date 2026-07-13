# THM-M-0034 anchor audit

Item: `S56-M-0034-ANCHOR_AUDIT`

This audit used the exact positive-variable field target frozen in `Statement.lean`. It did not
replace that target with stable freeness, a unimodular-row statement, the reverse free-to-projective
implication, or the adjacent `THM-M-0033` catalog item. The candidate inventory and search rules are
frozen in `anchor-discovery-protocol.json`; `anchor-audit.json` is the structured result.

## Result

Pinned mathlib contains useful interfaces but no terminal Quillen-Suslin body. In the exact target
context it synthesizes `Module.Flat` from projectivity but cannot synthesize `Module.Free`.
`Module.Projective.of_free` has the wrong direction, the local-ring and PID freeness theorems have
scalar-ring hypotheses unavailable for a multivariable polynomial ring, and
`MvPolynomial.basisMonomials` frees the polynomial ring over its coefficients rather than an
arbitrary module over the polynomial ring. `AnchorAudit.lean` checks these distinctions and their
standard axiom footprints in the pinned kernel.

The bounded public audit found two serious external Lean 4 closures:

| Candidate | Immutable source | Comparison | Classification |
|---|---|---|---|
| `edmund-ukaisi/QuillenSuslin.QuillenSuslin.quillenSuslin` | commit `e8d85a6f6fa210ba0be12bd02aa22009699f0c35`; archive SHA-256 `6072221d...7e6d2` | exact field/`Fin n`/finite-projective/free statement, stronger only because it also covers `n = 0`; independent universes and the same Lean/mathlib pins | `M3` exact source anchor; highest-priority replay/integration candidate |
| `mbkybky/QuillenSuslin.quillenSuslin` | commit `51ed173b17b274e61f759556ab3e1c090267d1bd`; tree `264c487a...eb`; archive SHA-256 `ad8bd766...7babf` | stronger PID-coefficient and arbitrary-finite-variable statement | `M1`, but older incompatible pins |
| Atlas `quillen_suslin_UEA_nminus` | commit `34ffed396f376454c1a9b297f3fd74c5c801fb50` | unrelated universal-enveloping-algebra statement and terminal `by sorry` | rejected `M5` name collision |

The exact source candidate's declaration calls `quillenSuslin_bridge`, whose terminal architecture passes
through the same-universe induction, Quillen patching, global/local descent, and an `ULift`
semilinear transport. Its immutable project ledger records a clean 2,372-job from-source build,
zero live prohibited constructs, the axiom set `[propext, Classical.choice, Quot.sound]`, and an
independent fidelity/circularity review. The worker replayed the project's lexer-aware source scan
over the immutable archive and obtained `0 sorry, 0 #exit, 0 native_decide, 0 axiom` across the 76
production files.

This does not yet establish upstream or local kernel closure under the rev-5.6 evidence hierarchy.
The upstream build/axiom claim is a prose ledger without retained raw output, so it is `E3/M3`, not
`E2/M1`. Separately, the older `mbkybky` candidate has an immutable successful GitHub Actions build
and is the inventory's provisional `E2/M1`, but its Lean/mathlib pins differ. Both projects are
absent from the repository dependency
graph, no external source or compiled artifact was installed, the raw upstream build/axiom output
for the exact candidate was not archived, and neither project has a usable license artifact. Therefore the audit
proposes the root candidate vector `[H1, M1, R4]` but leaves the accepted vector
`[H1, M3, R4]`. Licensing, immutable dependency integration, an exact local wrapper, local kernel
and axiom replay, and the complete transitive provenance/trust graph are concrete downstream work.

## Coverage boundary

All five records in inventory `S56-M-0034-ANCHOR-INVENTORY-20260713-01` are classified. Searches
covered repo-local Lean, pinned mathlib, the other materialized Lake packages, locally stored
mathlib refs, Sourcegraph with forks and archives, GitHub repository search and attempted code
search, two topic repositories, and the immutable formal-conjectures tree. Sourcegraph did not index
the two topic repositories; GitHub code search denied anonymous access and then rate-limited REST.
These are bounded results, not an internet-wide absence or saturation claim.

The human source remains `H1`: independent translation, errata review, Quillen full-text
reconciliation, proof-node crosswalk, and `THM-M-0033` boundary review remain open. No obligation
tree or readable proof is frozen here. This node is worker-self-tested only, accepts no receipt,
changes no master state, and does not claim `AUDIT-Z` or theorem completion.
