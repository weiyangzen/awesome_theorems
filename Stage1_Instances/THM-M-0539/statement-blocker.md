# Exact-statement blocker

Item: `S56-M-0539-STATEMENT`  
Theorem: `THM-M-0539`  
Verdict: blocked; no state change

## Source boundary

The repository source says only "computation of the homology of a CW complex." The intake names
Hatcher, *Algebraic Topology* (2002), Theorem 2.35 as a source lead, but this worker clone contains
no immutable copy of that source and no accepted quotation, page image digest, errata review, or
independent statement crosswalk. The wording therefore does not decide whether the root is the
degreewise cellular-versus-singular homology isomorphism, the chain-complex construction, the
free-abelian basis by cells, or the incidence-number boundary formula. It also does not fix an
absolute versus relative theorem or an alternate coefficient object.

Selecting one of those materially different propositions from general mathematical knowledge
would broaden or substitute the source record. This fails the rev-5.6 exact-source-identity gate.

## Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, narrow source searches
found the CW skeletal filtration in `Mathlib.Topology.CWComplex.Classical.Basic` and singular chains
and homology in `Mathlib.AlgebraicTopology.SingularHomology.Basic`. They found no cellular homology,
cellular chain complex, or relative singular-homology construction. In particular, the library
does not expose the object classically written
`C_n(X) = H_n(X^n, X^(n-1); Z)` or the connecting maps needed for its differential.

`StatementProbe.lean` kernel-elaborates the available substrates with exactly those two imports.
It is not a theorem statement. A proposition quantifying over an arbitrary purported cellular
chain complex or over a comparison isomorphism would assume the missing mathematical construction
and would not be the requested theorem. A proposition merely mentioning `CWComplex` and
`singularHomologyFunctor` would likewise be a weakened substitute.

## Retry condition

The statement phase can be retried after both of these inputs exist:

1. an immutable, reviewed source assertion fixing the root, coefficients, absolute/relative scope,
   grading, differential convention, naturality strength, and boundary cases; and
2. a pinned Lean encoding of relative homology for consecutive skeleta and the cellular chain
   complex/comparison map, sufficient to express that exact assertion without assuming its result.

No `Statement` declaration, expression hash, mutation-equivalence claim, receipt, H/M/R upgrade,
audit completion, or theorem completion is claimed. The first failed gate is exact source assertion
identity; the next concrete Lean blocker is the absent relative/cellular construction.

## Validation evidence

Validation ran on 2026-07-12 from repository base
`ed59c567ee1108d190e4682deda1f19ec0a8577d`. Existing `.lake` artifacts were read only.
No update, build, clone, fetch, or dependency mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Standard structure passed: 15 assurance groups and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | Manifest passed: 1546 unique targets, ranks 1 through 1546 |
| `python3 scripts/stage1_target.py show THM-M-0539` | 0 | Rank 596, planned, rework required, theorem incomplete |
| `rg -n -i 'cellular homology|cellular.*chain|homology.*CW|CWComplex.*homology|skelet.*homology' Mathlib .lake/packages/mathlib/Mathlib` from `Formalizations/Lean` | 1 | No matching declaration text |
| `rg -n 'relative.*[Hh]omology|Relative.*Homology' .lake/packages/mathlib/Mathlib/AlgebraicTopology` from `Formalizations/Lean` | 1 | No relative-homology declaration text |
| `lake env lean ../../Stage1_Instances/THM-M-0539/StatementProbe.lean` from `Formalizations/Lean` | 0 | All six pinned CW, skeleton, singular-chain/homology, and chain-complex interfaces elaborated |
| `python3 -m json.tool Stage1_Instances/THM-M-0539/instance.json` and the same check for `task-dag.json` | 0 | Existing intake authorities remain parseable and unchanged |
| `git diff --check -- Stage1_Instances/THM-M-0539` | 0 | No whitespace errors |
