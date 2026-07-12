# Anchor audit

Item: `S56-M-1286-ANCHOR_AUDIT`  
Audit date: 2026-07-12  
Worker base revision: `3bb2bb303df87d54d8d5dfafcee61ad3c329e278`

## Result

No exact Lean 4 anchor was found for
`Stage1Instances.THM_M_1286.PolyaSzegoTarget`. The audit searched the repository-local Lean source,
the complete pinned mathlib source tree at
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, and the only specifically named public Lean project
located by GitHub repository search, frozen at
`igorrivin/polya-szego-lean@5cac4f71df47699ff6c90d354447f5f3a6b699cc`.

The closest mathlib results are not root candidates. `Mathlib.Algebra.Order.Rearrangement` proves
finite-sum permutation inequalities such as
`MonovaryOn.sum_smul_comp_perm_le_sum_smul`; it has no measure-theoretic Schwarz rearrangement.
`Mathlib.Analysis.FunctionalSpaces.SobolevInequality` proves Gagliardo-Nirenberg-Sobolev bounds such
as `MeasureTheory.eLpNorm_le_eLpNorm_fderiv_of_eq`; it neither constructs an equimeasurable
radial-antitone function nor compares its weak-gradient norm with the original one. The actual
interfaces of these declarations were elaborated in `AnchorCandidates.lean`.

The external repository is a name collision: it treats exercises from Polya and Szego's *Problems
and Theorems in Analysis I*, rather than the named rearrangement inequality from *Isoperimetric
Inequalities in Mathematical Physics*. Its immutable README declares Lean 4.24.0 and mathlib commit
`f897ebcf72cd16f89ab4577d0c826cd14afaafc7`. The pinned tree contains 318 `original` and 80
`verified` Lean files. A full-text archive scan found no occurrence identifying a Schwarz or
symmetric decreasing rearrangement, equimeasurability, weak gradient, Sobolev space, or Dirichlet
integral candidate. The `verified` files had no `sorry`, `admit`, top-level `axiom`, or `unsafe` hit;
the `original` files had 661 placeholder hits. Those trust observations do not change the semantic
mismatch.

The root therefore remains `M4` with `formalization_debt`, not repo-local integration debt. The
next phase must plan new rearrangement construction, equimeasurability, coarea/isoperimetric (or
polarization) estimates, and approximation/lower-semicontinuity obligations. This audit supplies no
theorem proof or theorem-completion evidence.

## Validation record

Commands ran without updating, fetching, cloning, building, or otherwise mutating `.lake`.

| Command | Exit | Result |
|---|---:|---|
| `lake env lean ../../Stage1_Instances/THM-M-1286/AnchorCandidates.lean` (from `Formalizations/Lean`) | 0 | all seven pinned candidate interfaces elaborated |
| `lake env lean ../../Stage1_Instances/THM-M-1286/Statement.lean` (from `Formalizations/Lean`) | 0 | frozen canonical target and checked expansion still elaborate |
| `rg -nil 'polya.?szego|pólya.?szegő|schwarz symmetric|symmetric decreasing rearrangement|symmetricDecreasingRearrangement' . --glob '*.lean' --glob '!Formalizations/Lean/.lake/**' --glob '!Stage1_Instances/THM-M-1286/**'` | 0 | only neighboring THM-M-1285 statement; no local proof candidate |
| `rg -nil 'polya.?szego|pólya.?szegő|schwarz symmetric|symmetric decreasing rearrangement|symmetricDecreasingRearrangement|equimeasur' Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'` | 1 | no exact or conceptual-name hit in pinned mathlib |
| GitHub API repository search for `"Polya-Szego" lean OR "Pólya-Szegő" lean` | 0 | two same-owner results; the source repository above and a benchmark metadata repository |
| Immutable GitHub tar archive scan at `5cac4f7...` | 0 | 318 original/80 verified files; no canonical-concept hit; trust scan as reported above |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets valid |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-1286` | 0 | rank 457, planned, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-1286/anchor-audit.json` | 0 | structured audit receipt is valid JSON |
| `git diff --check -- Stage1_Instances/THM-M-1286 .stage1-worker-selftest.json` | 0 | no whitespace errors |

The grep.app public code-search endpoint returned HTTP 429 for all three queries and is recorded as a
non-blocking known failure. The immutable mathlib tree and identified external repository were still
audited directly; no claim is made that an unauthenticated web search proves universal absence from
all Lean repositories.
