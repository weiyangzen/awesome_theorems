# Anchor audit record

Item: `S56-M-0464-ANCHOR_AUDIT`  
Base revision: `d9657b35845b4b10e25345050fe228f872bc50ad`

## Frozen target

This audit is against `AwesomeTheorems.THM_M_0464.PilaWilkieStatement` in `Statement.lean`
(file SHA-256 `17f12ef1ddf29bd25ef0928243339acd452b7d1534aa7a73efca01686ae81917`).
The declaration is a definition of a proposition, not a theorem. No arbitrary predicate package,
uniform-family variant, or nearby legacy target receives credit.

## Pinned mathlib

`Formalizations/Lean/lake-manifest.json` pins mathlib at
`8a178386ffc0f5fef0b77738bb5449d50efeea95`; the toolchain is Lean 4.29.0 at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`. `AnchorAudit.lean` checks the actual available
ingredients: first-order definability, real multivariate polynomials, connectedness/non-singleton
predicates, finite-set cardinality, and real powers. Complete source searches found no Pila-Wilkie
declaration or terminal counting proof in pinned mathlib or the repository. These APIs elaborate
the target but do not close it.

## External Lean 4 candidates

On 2026-07-12, unauthenticated GitHub repository searches for `PilaWilkie language:Lean`,
`Pila-Wilkie language:Lean`, `o-minimal language:Lean`, `ominimal language:Lean`, `o-minimality
Lean4`, and `Pila Wilkie Lean theorem` returned counts `0, 0, 2, 1, 0, 0`. All three returned Lean
repositories were downloaded by immutable commit archive and their complete Lean trees, pins, and
placeholder/trust surfaces were inspected. Unauthenticated code search was unavailable, so this is
a complete classification of the frozen returned inventory, not exhaustive-discovery credit.

| Candidate and immutable revision | Archive SHA-256 | Finding | Decision |
|---|---|---|---|
| `theominimalist/monotonicity@6e3ee129f0d9cc0d9d6a58cac4fc03bc7b121b30` | `9a7d3a22fc16e4822eb857b366a3ab1459b448adb3b79c3deb327e2f4b11c603` | no manifest/toolchain; local monotonicity material contains axioms, opaque boundaries, and `sorry`; no counting theorem | `M5`, infeasible |
| `tonysf/lean-OMIN@fd8b4f3423265d9beb290a08992ad866eb5230e0` | `38b2c53b0c7ca03d5c36069c9eb981d9999d67938933b7433c490d67f5dcc012` | Lean 4.30.0-rc1/mathlib `f8770bc8...`; substantial `OMinStructure`, but cell decomposition and other milestones are assumption fields; no Pila-Wilkie/height/counting theorem | `M5`, incompatible and no closure |
| `KittySaya/Lean-ominimal@4429c2cc75e49a83043175f7a85c4c1bf284c2eb` | `37a5cf8e8440a633e923fe9e2909b5d7217e181f8171ead6337b64b88b1ccc9f` | Lean 4.19.0-rc3/mathlib `44efe040...`; pure dense-order example with root-imported `sorry` placeholders; no real-field counting result | `M5`, incompatible and wrong scope |

No candidate supplies an exact statement transport, wrapper, terminal proof body, or feasible pinned
integration. No archive was installed and `.lake` was not mutated.

## Validation

The exact commands and results are recorded below after running them from the worker clone.

| Command | Exit | Result |
|---|---:|---|
| `lake env lean ../../Stage1_Instances/THM-M-0464/AnchorAudit.lean` from `Formalizations/Lean` | 0 | all six pinned anchor declarations elaborated and printed |
| `lake env lean ../../Stage1_Instances/THM-M-0464/Statement.lean` from `Formalizations/Lean` | 0 | frozen statement re-elaborated; output SHA-256 `5f467e148ffd7fe060f55e1371cf8be5ce9aee16770c53cb868b6dcf427ecd92` |
| `python3 -m json.tool Stage1_Instances/THM-M-0464/anchor-audit.json >/dev/null` | 0 | structured audit parsed |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique uniform-L0 targets passed |
| `python3 scripts/stage1_target.py show THM-M-0464` | 0 | rank 310; planned; theorem incomplete |
| `git diff --check -- Stage1_Instances/THM-M-0464 .stage1-worker-selftest.json` | 0 | no whitespace errors before self-test creation |

Phase verdict: the anchor inventory is fully classified and pending master acceptance. Machine state
remains `M3`; theorem completion is false. The obligation tree, proof, trust closure, reproducible
release, and independent-verification gates remain open.
