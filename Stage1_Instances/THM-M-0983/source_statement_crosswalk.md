# Source-statement crosswalk

| Claim component | Human source anchor | Lean candidate | Intake assessment |
|---|---|---|---|
| Frequency tends to probability in repeated Bernoulli trials | Jacob Bernoulli, *Ars Conjectandi* (1713), Part IV, Chapter V, commonly identified as the classical Bernoulli theorem | local `StatementShape` candidate | Historical primary-source family identified, but edition, exact pages, translation fidelity, assumptions, and errata are not pinned: `H1` |
| Almost-sure convergence of IID sample averages | A. N. Kolmogorov, *Grundbegriffe der Wahrscheinlichkeitsrechnung* (1933), strong-law development; exact theorem/page requires audit | `ProbabilityTheory.strong_law_ae_real` | Modern source family for the chosen strong convergence mode; no theorem-to-premise crosswalk or immutable source receipt yet |
| Bernoulli trials and common success probability | The Bernoulli frequency claim specialized to `{0,1}` observations | legacy `FrequencyLawData` / `IIndepFrequencyLawData` | Candidate object models only; neither has statement-phase credit |
| Empirical frequency | Arithmetic mean of the first `n` indicator variables | legacy `empiricalFrequency` | Candidate encoding uses division by `(n : Real)` and an empty sum at zero; the harmless-initial-term claim needs checking |
| Convergence in probability | Standard consequence of almost-sure convergence on a probability space | legacy `FrequencyLawInProbabilityConclusion` | Consequence candidate only; it cannot replace the almost-sure canonical root |

The generated blueprint says only “frequency converges to probability,” which does not itself fix a
mode of convergence. This intake selects the classical strong, almost-sure Bernoulli-frequency
reading because the discovered legacy artifact explicitly presents that reading. The dependent
statement phase must still verify that choice against pinned primary sources and must expose all
measurability, probability-measure, independence, identical-distribution, and indicator hypotheses.

Discovery references (not immutable evidence receipts):

- Bernoulli, *Ars Conjectandi* (Basel, 1713), Part IV, Chapter V.
- Kolmogorov, *Grundbegriffe der Wahrscheinlichkeitsrechnung* (Springer, 1933).
- Repo-local discovery module: `Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_263.lean`.

No `H0`, exact-statement, or machine-closure claim is made. Required follow-up includes a scan/hash
and bibliographic edition pin, exact page/theorem localization, translation and errata review,
premise-by-premise mapping, declaration type elaboration, normalized expression serialization,
checked transports, boundary probes, and independent review.
