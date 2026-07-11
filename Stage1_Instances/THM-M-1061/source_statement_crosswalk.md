# Source-statement crosswalk

| Frozen claim component | Human source anchor | Lean candidate | Intake assessment |
|---|---|---|---|
| LDP input with good rate function | Dembo and Zeitouni, *Large Deviations Techniques and Applications*, 2nd ed., Springer (1998; corrected printing 2010), Theorem 4.3.1 | no exact declaration selected | Secondary standard theorem anchor; edition/hash and premise audit remain open |
| Exponential integral asymptotic | Dembo-Zeitouni, Theorem 4.3.1, displayed conclusion (4.3.2) | future exact expression using `Measure.integral`, `Real.exp`, `Real.log`, and a filter limit | Formula correspondence is conceptual only, not elaborated |
| Bounded continuous specialization | Theorem 4.3.1 allows continuous functions satisfying a tail or moment condition; bounded continuity supplies the standard safe specialization | no checked wrapper | Frozen root deliberately narrows the source theorem; implication must be proved in Lean |
| Historical genealogy | S. R. S. Varadhan, "Asymptotic probabilities and differential equations", *Communications on Pure and Applied Mathematics* 19 (1966), 261-286 | none | Primary historical source located by bibliographic identity; exact page/result and errata audit remain open |
| Inverse-speed notation | Standard `beta -> infinity` Laplace-principle convention | no checked transport | Reparameterization candidate only |

The blueprint's label `Laplace principle` can also mean the family of these limits
for all bounded continuous functions, or an equivalence between that family and an
LDP. Those are broader propositions. They are not silently substituted for the
frozen single-function integral lemma.

No `H0` or machine-closure claim is made. Later phases must acquire immutable source
copies, pin edition and file hashes, inspect corrections, map every premise, select
the exact topology and extended-real conventions, locate or build the Lean APIs,
and check the bounded-tail specialization and inverse-speed transport.

Discovery identifiers (not evidence receipts): DOI `10.1002/cpa.3160190303` for
Varadhan (1966); Dembo-Zeitouni ISBN `978-3-642-03311-7` for the corrected printing.
