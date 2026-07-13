# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:7050-7055` supplies exactly the name
`Ahlswede-Khachatrian完全相交定理`, authors Ahlswede/Khachatrian, year 1997, gloss
`t-相交族的完整刻画`, importance "high," and status `已验证`. All six lines originate at
commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. They contain no citation, definitions, ordered
binders, hypotheses, conclusion, equality-case policy, proof boundary, or formal artifact.

`Docs/Stage0_Blueprint.md:26308-26333` repeats the gloss while leaving exact definitions and
premises, proof route, dependencies, equivalent formulations, axioms, machine status, and artifact
links open. Rev-5.6 retains `已验证` only as untrusted metadata and resets the target to
`L0 / rework_required`.

## Primary source

Rudolf Ahlswede and Levon H. Khachatrian, "The Complete Intersection Theorem for Systems of
Finite Sets," *European Journal of Combinatorics* 18(2) (1997), 125-136, DOI
`10.1006/eujc.1995.0092`, PII `S0195669885700923`. The directly inspected author-hosted 12-page PDF
has 392690 bytes and SHA-256
`2a0d46d73ae6a445ebb2c838785855c2af82d1901a7ecbc7394d1427e472a365`; extracted text has
SHA-256 `cb9768e716f80db8f988adc2c76222c7504c81eee9f89e9628a23c9f72601fff`.
Crossref independently confirms the bibliographic identity. No correction or erratum was displayed
in the inspected PDF, but no systematic publisher/author correction search or independent source
review is accepted, so this is not H0.

## Clause crosswalk

| Source locator | Source clause | Prospective formal component | Intake result |
|---|---|---|---|
| p.125, (1.1) | `[n]`, its `k`-subsets, and finite set-family notation | ground type, `Finset.powersetCard`, family encoding | exact encoding open |
| p.125, (1.2) | every two members have intersection cardinality at least `t` | uniform `t`-intersection predicate | adjacent vocabulary only |
| p.125, (1.3) | `M(n,k,t)` is the maximum family size | finite extremal function or maximum proposition | root strength open |
| p.126, (1.9) | canonical family indexed by `i`, using `[t+2i]` and threshold `t+i` | candidate-family definition and finite index range | transcription open |
| p.126, (1.10) | `M(n,k,t)` equals the maximum candidate size | sharp cardinality/equality root | candidate root only |
| p.126, main theorem (i) | in an open transition interval, candidate `r` is uniquely optimal up to permutations | exact rational inequalities and isomorphism classification | stronger candidate; open |
| p.126, main theorem (ii) | at a transition equality, candidates `r` and `r+1` tie and exhaust optimizers up to permutations | boundary equality and two-family classification | stronger candidate; open |
| pp.126-127, Remark (1) | only `n > 2k-t` needs proof; below the boundary the full layer is `t`-intersecting | degenerate/low-`n` branch | must be frozen explicitly |
| pp.127-136 | generating sets, pushing, weighted estimates, cases, and terminal argument | downstream source-node proof graph | not intake proof credit |

The PDF's older typography is imperfectly extracted (`<=` often appears as `<`, unions and
intersections are mangled, and fractions require visual reading). The displayed piecewise theorem
must be transcribed and independently checked from the page image before it becomes a canonical
statement.

## Secondary discriminator

Gyula O. H. Katona, "Around the Complete Intersection Theorem," arXiv `1602.02634v1` (2016),
pp.2-3, defines the same uniform candidate family and states Theorem 4 as the upper bound
`|F| <= AK(n,k,t)`. The inspected seven-page PDF has 92754 bytes and SHA-256
`df9d325ced01434ef156680cdabbc8690614b373c2c5a2b51c898a0b15c48da3`. It is useful for
discriminating the bound-only formulation but is secondary evidence and receives no H0 credit.

## Formal boundary

Pinned mathlib provides `Set.IsIntersectingOf`, `Set.Intersecting`, `Set.Sized`, powerset-cardinality
infrastructure, binomial coefficients, and `Finset.erdos_ko_rado`. It does not expose a located
Ahlswede-Khachatrian complete `t`-intersection declaration. `Set.Intersecting` and
`Finset.erdos_ko_rado` are ordinary `t = 1` concepts; `AhlswedeZhang` is unrelated. The intake probe
and bounded search are discovery only, not the later immutable formal-anchor audit.

## Review and errata boundary

Source edition, locators, assumptions, main clauses, proof-section boundary, and an accessible
snapshot are recorded. Exact catalog-clause selection, visual transcription of all inequalities,
complete premise-to-node mapping, publisher/author correction audit, and an identified independent
reviewer remain open. The source classification is therefore `H1`, not `H0`.
