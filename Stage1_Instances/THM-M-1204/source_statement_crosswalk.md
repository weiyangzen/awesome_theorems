# Source-statement crosswalk

| Claim component | Human source anchor | Lean target | Intake assessment |
|---|---|---|---|
| Multidimensional scalar conservation-law Cauchy problem | S. N. Kruzkov, "First order quasilinear equations in several independent variables," *Mathematics of the USSR-Sbornik* 10(2) (1970), 217-243, DOI 10.1070/SM1970v010n02ABEH002156 | not selected | Primary publication identified, but theorem/page wording and hypotheses have not been inspected from a pinned copy: `H1` |
| Entropy admissibility | Kruzkov 1970, constant-level entropy inequalities | future `KR-DEF` | Manifest omits the inequality, distribution/test-function convention, and trace |
| Existence | Kruzkov 1970 existence theory for generalized solutions | future `KR-APPROX` | Exact data and flux classes require source pinpointing |
| Uniqueness/comparison | Kruzkov 1970 comparison via doubling of variables | future `KR-COMP`, `KR-UNIQ` | Whether the named root is uniqueness alone or full well-posedness is unresolved |
| Stability | Kruzkov 1970 stability estimate | future `KR-STAB` | Global/local `L1` form and finite-propagation constants require exact audit |

The Stage0 wording is too short to decide among several commonly named "Kruzkov theorem"
statements. In particular, this intake does not broaden the autonomous scalar equation to systems
or x/time-dependent fluxes, and does not narrow the root to uniqueness merely because that is easier
to state. The statement phase must obtain an immutable source copy, record exact theorem/page and
translation, check corrections, and map every premise and conclusion before selecting a Lean type.

Discovery link (not an evidence receipt): <https://doi.org/10.1070/SM1970v010n02ABEH002156>.
