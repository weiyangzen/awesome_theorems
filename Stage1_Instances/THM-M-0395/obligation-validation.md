# THM-M-0395 obligation-tree validation

Item: `S56-M-0395-OBLIGATION_TREE`  
Base revision: `e9c516bd976b6850ddcab868f808a7895bb7e826`  
Validation date: `2026-07-12` (`Asia/Shanghai`)

## Result

The frozen registry contains 17 unique semantic obligations and has denominator
SHA-256 `03edd3b7a2326a33c61913fbc6caa75eb6520c70f1baadfb69c4cb27e2d86a74`.
The validator checked all required registry/node fields, one-to-one coverage,
eligibility denominators, seven graph families, reciprocal proof/composition
edges, edge indexes, the root-reaching proof path, recipe references, and the
honest open-root boundary. There are 46 typed edges.

The proof route explicitly exposes the finite-extension normalization,
Jacobian and Abel-Jacobi construction, Mordell-Weil bridge, Mordell-Lang/Faltings
core, no-positive-dimensional-coset lemma, finite-union conclusion, and terminal
composition. Only `M0395-S3`, a statement-encoding transport already present in
`Statement.lean`, is `M0-L`. The root and every substantive Faltings obligation
remain open at `M4`; no proof or theorem completion is claimed.

## Commands and exact outcomes

| command | exit | outcome |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique ranks and targets passed |
| `python3 scripts/stage1_target.py show THM-M-0395` | 0 | rank 8, planned, L0/rework-required, theorem incomplete |
| `python3 Stage1_Instances/THM-M-0395/build_obligation_artifacts.py` | 0 | deterministically regenerated registry, graphs, and validation specifications |
| `python3 Stage1_Instances/THM-M-0395/check_obligation_tree.py` | 0 | `PASS THM-M-0395 obligation tree: 17 obligations, 46 typed edges`; root open M4 |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0395/Statement.lean)` | 0 | printed `Stage1Rev56.THMM0395.Statement.{u} : Prop`; checked transport elaborated |
| `python3 -m json.tool` on all three generated JSON artifacts | 0 | all JSON parsed successfully |
| `git diff --check -- Stage1_Instances/THM-M-0395 .stage1-worker-selftest.json` | 0 | no whitespace errors |

Generated artifact hashes:

```text
2461eef24bec0c53faf36b2a16f1cb7c61fb13341544fad2cc64113be64381be  obligation-registry.json
c130159ff5c46af19263bae478720e4fe33ec8007f8d6bb15c6e444096bb1e81  typed-graphs.json
3c02d1a5f5f9afb590541be5d8bdcb5653d521af1018875b01374a5133cdf93c  validation-specs.json
```

The pre-existing untracked `Formalizations/Lean/.lake` link/artifact was reused
without mutation. No `lake update`, `lake build`, clone, fetch, or dependency
mutation was run.

## Status boundary

This self-test covers only the obligation-tree phase. Planned signatures are not
Lean declarations; architecture coverage is not mathematical proof coverage;
and no composition, human-source, readability, trust, hermetic, independent-
verification, audit-completion, or theorem-completion gate is claimed. Master
acceptance remains required.
