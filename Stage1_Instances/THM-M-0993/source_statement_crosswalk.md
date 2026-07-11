# Source-statement crosswalk

The repository phrase "tail probability of a sum of independent random variables" names a family,
not a unique theorem. This intake selects the general exponential-moment upper-tail form rather than
silently substituting a Bernoulli multiplicative bound.

| Claim component | Human source anchor | Intended Lean surface | Assessment |
|---|---|---|---|
| Exponential upper bounds for sums of independent random variables | H. Chernoff, "A Measure of Asymptotic Efficiency for Tests of a Hypothesis Based on the Sum of Observations", *Annals of Mathematical Statistics* 23(4), 1952, pp. 493-507 | finite sum, event measure, exponential integral | Primary paper and pagination located; exact result/premise and errata audit remains open: `H1` |
| Positive tilt | Exponential Markov method in that paper | `0 < t` | Required by selected upper-tail transformation; pinpoint open |
| Product of moments | Independence of summands | independence plus integral-of-product bridge | Part of root; exact Lean API deliberately unfrozen |
| Arbitrary real threshold | General transform inequality | event `{omega | a <= sum i, X i omega}` | Boundary and measurability mutation checks remain open |
| Bernoulli/binomial forms | Optimized corollaries | possible later corollaries | Excluded as root substitutes |

Discovery identifiers, not immutable evidence receipts:

- DOI: <https://doi.org/10.1214/aoms/1177729330>
- Project Euclid: <https://projecteuclid.org/journals/annals-of-mathematical-statistics/volume-23/issue-4/A-Measure-of-Asymptotic-Efficiency-for-Tests-of-a-Hypothesis/10.1214/aoms/1177729330.full>

No `H0` claim is made. Source audit must preserve a digest, pinpoint the result and assumptions,
check errata, crosswalk every premise, and obtain independent review. Statement work must freeze the
exact mathlib measurability, independence, integral, sum/product, and probability representations.

