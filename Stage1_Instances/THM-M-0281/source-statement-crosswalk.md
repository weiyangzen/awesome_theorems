# THM-M-0281 source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:2020-2025` records only:

- title: `延森不等式`;
- attribution: Johan Jensen;
- year: 1906;
- gloss: `凸函数的积分不等式`;
- importance: high;
- untrusted formalization label: `已验证`.

All six lines originate at repository commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. `Docs/Stage0_Blueprint.md:7765-7790`
repeats the gloss while explicitly leaving the formal system, exact definitions and assumptions,
proof route, equivalences, axioms, machine status, and artifact links open. These records establish
catalog identity only.

## Primary-source lead

Crossref metadata observed on 2026-07-13 identifies J. L. W. V. Jensen, "Sur les fonctions
convexes et les inegalites entre les valeurs moyennes," *Acta Mathematica* 30 (1906), pages
175-193, DOI `10.1007/BF02418571`. The observed metadata payload has SHA-256
`a82ca423633f1e8d9272a15107fe11068a461855b63dde9a250b48145e6f7dba`.

The DOI resolved to Project Euclid, but automated full-text access returned an access-control page;
the Springer PDF route returned HTML rather than article bytes. No article text was admitted or
transcribed. Consequently no pinpoint proposition, incorporated definitions, exact hypotheses,
proof boundary, corrections or errata, translation, or independent review is available. This is a
matching primary bibliographic lead and supports `H1`, not an `H0` source crosswalk.

## Clause crosswalk

| Catalog clause | Source status | Pinned Lean candidate | Intake decision |
|---|---|---|---|
| "convex function" | domain, codomain, and convexity convention absent | `ConvexOn Real s g` | candidate only |
| "integral" | measure normalization, integral notion, and range absent | Bochner integral under `IsProbabilityMeasure mu` | candidate only |
| inequality direction | formula absent | `g (integral f dmu) <= integral (g compose f) dmu` | likely family shape, not frozen |
| domain conditions | absent | closed convex `s`, continuity of `g` on `s`, and `f` almost everywhere in `s` | source mapping open |
| existence conditions | absent | integrability of `f` and `g compose f` | source mapping open |
| variants | absent | normalized average, restricted set, concave, strict, equality, and finite forms | root selection open |
| `已验证` | untrusted inventory metadata | no proposition or proof object | no H or M credit |

## Formal candidate crosswalk

| Declaration | Candidate role | Unclosed gate |
|---|---|---|
| `ConvexOn.map_integral_le` | probability-measure integral Jensen inequality | primary-source statement identity, expression serialization, transport, provenance, trust, and acceptance |
| `ConvexOn.map_average_le` | nonzero finite-measure normalized average | decision whether normalization is source-faithful |
| `ConvexOn.map_set_average_le` | normalized average over a measurable-domain restriction | source set and measure assumptions |
| `ConvexOn.map_centerMass_le`, `ConvexOn.map_sum_le` | finite convex-combination Jensen variants | not substitutes for the integral root |
| `ConcaveOn.le_map_integral` | concave order-dual | relationship to the convex catalog root |
| `StrictConvexOn.ae_eq_const_or_map_average_lt` | strict average version | additional strictness/equality premises and conclusion |

Before leaving `H1`, an accountable source reviewer must preserve an immutable approved edition,
pinpoint and translate the proposition and its incorporated definitions, map every premise and
conclusion, audit corrections and errata, and obtain independent review. Before statement
acceptance, Lean work must select only that claim, minimize imports, serialize its elaborated
expression and environment, compile all credited transports, and pass removed-hypothesis,
changed-domain, binder-scope, and boundary-case mutations.
