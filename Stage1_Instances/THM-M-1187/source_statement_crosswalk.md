# Source-statement crosswalk

| Repository surface | Exact wording | What it establishes | What it does not establish |
|---|---|---|---|
| `Docs/researches/math_theorems.md` | name: `抛物型方程`; statement: `热方程及其推广` | Intended subject is the heat equation and parabolic generalizations | Any hypotheses, conclusion, theorem reference, edition, page, or proof |
| `Docs/Stage0_Blueprint.md` | theorem content: `热方程及其推广` | Preserves the same source wording | An exact mathematical claim; its verification label is metadata only |
| rev-5.6 target manifest | name/category, untrusted status, hard anchor/wrapper lane | Membership and execution metadata | Source fidelity or machine closure |
| legacy generated Stage1 entry | `抛物型方程的正则性` | A prior candidate interpretation | Authority to replace the source wording; this also risks collision with `THM-M-1189` |

## Statement blocker

"Parabolic equations" names a class, not one theorem. A usable proposition must at minimum select:

1. the operator (for example the constant-coefficient heat operator or a uniformly parabolic
   divergence/non-divergence operator);
2. spatial domain and time interval, coefficient/data regularity, boundary and initial conditions,
   and solution notion;
3. one conclusion such as existence, uniqueness, regularity, an estimate, or a qualitative law;
4. a primary source pinpoint whose theorem actually has those assumptions and conclusion.

Choosing any of these at intake would broaden or substitute the source rather than crosswalk it.
In particular, the maximum principle, Schauder estimates, and L-p estimates are separately indexed
as `THM-M-1188`, `THM-M-1189`, and `THM-M-1190`. They are therefore excluded as silent replacements.

No `H0` or Lean anchor claim is made. After authoritative clarification, the statement phase must
freeze ordered binders and boundary cases, identify a primary edition/theorem/page and errata, and
elaborate and mutation-test the exact Lean expression.
