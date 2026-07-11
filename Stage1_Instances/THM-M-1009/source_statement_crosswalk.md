# Source-statement crosswalk

| Claim component | Human source anchor | Lean candidate | Intake assessment |
|---|---|---|---|
| Generalized Borel-Cantelli lower bound | P. Erdos and A. Renyi, *On Cantor's series with convergent sum of reciprocals*, Annales Universitatis Scientiarum Budapestinensis de Rolando Eotvos Nominatae, Sectio Mathematica 2 (1959), 93-109, is a bibliographic discovery lead associated with the lemma | `AwesomeTheorems.Stage1.S1_M_289.ErdosRenyiLowerBoundStatement` | Primary paper is identified only provisionally; exact theorem/page, notation, premises, and errata are not yet audited, so this is `H1`, not `H0` |
| Pairwise-intersection ratio | Same source lead; exact displayed formula still requires inspection of a stable scan | `partialEventMass`, `pairwiseEventMass`, and `eventMassRatio` in the legacy module | Candidate correspondence only; finite range indexing and ordered double-sum convention require confirmation |
| Infinitely-often event | Source limsup/infinitely-often event, pinpoint pending | `limsup A atTop` | Expected encoding, but no checked source-to-Lean equivalence is credited |
| Full-probability consequence | Secondary formulations commonly derive probability one when the ratio converges to one | `ErdosRenyiFullProbabilityStatement` | Candidate corollary, not selected as a substitute for the lower-bound root |
| Independent second Borel-Cantelli | Classical special case, not the generalized theorem | `ProbabilityTheory.measure_limsup_eq_one` | Nearby mathlib anchor only; independence strengthens the hypotheses and cannot close the root |
| Levy generalized Borel-Cantelli | Filtration/conditional-expectation theorem | `MeasureTheory.ae_mem_limsup_atTop_iff` | Nearby mathlib anchor only; not an exact statement match |

The repository source record supplies only the Chinese summary "a
generalization of the Borel-Cantelli lemma," attribution to Erdos and Renyi,
and year 1959. It does not determine a unique formal statement. The legacy
Lean artifact's lower-bound formulation is therefore retained as the
provisional root rather than silently treating a stronger independent-event
theorem or the probability-one corollary as equivalent.

No `H0` or machine-closure claim is made. The source-audit phase must obtain a
stable source file and hash, verify the bibliographic lead, record exact
theorem/page/formula and all assumptions, check corrections and nomenclature
(including its relationship to later Kochen-Stone formulations), and obtain
independent review. The statement phase must separately elaborate and
fingerprint the exact Lean expression and test indexing, denominator, domain,
hypothesis, and boundary mutations.
