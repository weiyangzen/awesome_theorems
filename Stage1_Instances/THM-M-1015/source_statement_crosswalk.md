# Source-statement crosswalk

| Claim component | Human source anchor | Lean candidate | Intake assessment |
|---|---|---|---|
| Basic Slutsky principle | E. Slutsky, "Uber stochastische Asymptoten und Grenzwerte", *Metron* 5(3) (1925), 3-89 | `TendstoInDistribution.prodMk_of_tendstoInMeasure_const` | Original primary source identified bibliographically; exact theorem/page, edition scan hash, assumptions, and errata review remain open (`H1`) |
| Pair convergence | Standard joint formulation from convergence in distribution and convergence in probability to a constant | legacy `slutsky_pair_real` | Candidate only; exact type and provenance are statement/anchor-audit work |
| Addition and multiplication | A. W. van der Vaart, *Asymptotic Statistics*, Cambridge University Press (1998), Lemma 2.8, p. 11 | legacy `slutsky_add_real`, `slutsky_mul_real` | Secondary statement anchor located; no H0 or machine credit |
| Quotient for `c != 0` | van der Vaart, Lemma 2.8, p. 11, division clause | no declaration in the legacy slot | Mandatory branch of the frozen standard statement; concrete Lean target remains open |
| No independence premise | Standard theorem needs no independence of `X_n` and `Y_n` | legacy imports `Probability.Independence.Basic`, but wrapper hypotheses do not use independence | Independence is explicitly outside the canonical hypotheses; minimal imports are deferred |

The generated legacy description says only "convergence of combinations of random variables" and
does not itself determine a formal theorem. The conventional real-valued Slutsky statement above
is therefore frozen without inheriting the historical wrapper. In particular, accepting its
pair/add/product package as the whole theorem would substitute a narrower claim by deleting the
division clause.

Discovery links, not immutable evidence receipts:

- Slutsky bibliographic record: <https://zbmath.org/?q=an%3A51.0431.01>
- van der Vaart book DOI: <https://doi.org/10.1017/CBO9780511802256>

The statement phase must elaborate the full package, select the precise probability-convergence
encoding, check API-added measurability assumptions, and mutation-test the convergence modes,
shared sample space, constant limit, arithmetic branches, and `c != 0` boundary. The later source
audit must obtain immutable copies and independently review the page/theorem mapping and errata.
