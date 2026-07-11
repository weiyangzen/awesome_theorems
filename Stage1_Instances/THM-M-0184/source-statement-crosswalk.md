# Source-statement crosswalk

| Claim component | Human source discovery anchor | Lean candidate | Intake assessment |
|---|---|---|---|
| Repository metadata phrase | `Docs/researches/math_theorems.md`, entry "Donaldson theorem" (1983): moduli spaces of ASD connections on four-manifolds | none | Secondary metadata is too broad to identify a theorem; it cannot support `H0` |
| Foundational ASD moduli construction | S. K. Donaldson, "An application of gauge theory to four-dimensional topology," *J. Differential Geometry* 18 (1983), 279-315 | historical `S1_M_131.StatementShape` | Primary discovery anchor, but theorem/page, conventions, assumptions, and errata are not yet pinned; historical shape is abstract and uncredited |
| Gauge-theoretic moduli/invariant package | S. K. Donaldson and P. B. Kronheimer, *The Geometry of Four-Manifolds*, Oxford Mathematical Monographs (1990), especially the ASD moduli-space development | no exact repo-local declaration | Book-level discovery anchor only; exact edition, chapter/theorem/page crosswalk remains open |
| ASD equation | curvature satisfies `F_A^+ = 0` (or `*F_A = -F_A` under selected orientation conventions) | historical `S1_M_131.IsAntiSelfDual` | Formula candidate only; it is a definition, not Donaldson's theorem |
| Moduli quotient | ASD connections modulo the appropriate gauge group | historical `S1_M_131.asdModuliOrbitSet` | Set-of-orbits inventory only; it does not construct the analytic quotient or its geometry |
| Regularity and dimension | regular irreducible locus is finite-dimensional with an index-determined dimension under suitable genericity | none exact | Root-level hypotheses and the index convention must be selected from a pinpointed primary theorem |
| Compactification | Uhlenbeck compactification adds ideal connections/bubbling strata | none exact | Must not be conflated with compactness of the uncompactified moduli space |

At intake, the broad source phrase admits several inequivalent results: local smoothness of the
irreducible ASD moduli space, expected-dimension and orientation results, Uhlenbeck compactification,
Donaldson polynomial invariants, and Donaldson's intersection-form/diagonalization theorem. The
repository wording favors the moduli-space family, but does not determine a single ordered list of
hypotheses and conclusion. Consequently exact statement fidelity is blocked rather than guessed.

Discovery links (not immutable evidence receipts):

- Donaldson 1983: <https://projecteuclid.org/journals/journal-of-differential-geometry/volume-18/issue-2/An-application-of-gauge-theory-to-four-dimensional-topology/10.4310/jdg/1214437665.full>
- Donaldson-Kronheimer bibliographic record: Oxford University Press, ISBN 978-0-19-850269-2.

Required statement/anchor follow-up: select one named theorem; obtain an immutable source file and
hash; record exact edition, theorem/page, definitions, sign conventions, assumptions, and errata;
map every premise and conclusion component; then independently review the selection before Lean
elaboration or proof credit.

