# THM-M-0721 obligation-tree validation

Item: `S56-M-0721-OBLIGATION_TREE`  
Date: `2026-07-12`  
Base revision: `4586a02100c5be8974b9cb0ab2d4e9e51d0480f0`

## Frozen result

The version-1 registry contains 18 canonical obligations. Its denominator SHA-256 is
`375921a1792cc56322b0f0f3d241a5fa10e02345a66a9f007554978cc932b92a`.
The proof, refinement, provenance, evidence, trust, documentation, and workflow graphs contain 45
typed edges in total. The exact root remains open at `M3`; the immediate cut set is SAT membership
and universal Cook-Levin hardness, both `M4`. No theorem-completion credit is claimed.

## Commands and results

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | rev-5.6 standard passed: 15 assurance groups and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | manifest passed: 1546 unique ranks and all targets L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0721` | 0 | rank 578, planned, theorem incomplete |
| `python3 Stage1_Instances/THM-M-0721/build_obligation_artifacts.py` | 0 | deterministically rebuilt 18 obligations and the frozen denominator |
| `python3 Stage1_Instances/THM-M-0721/check_obligation_tree.py` | 0 | all node fields, denominators, typed reciprocal proof edges, graph indexes, acyclicity, recipes, open-root boundary, and prohibited Lean tokens passed |
| `{ sed -n '1,$p' Stage1_Instances/THM-M-0721/Statement.lean; sed -n '1,$p' Stage1_Instances/THM-M-0721/ObligationTree.lean; } > /tmp/THM-M-0721-ObligationTree.lean && cd Formalizations/Lean && lake env lean /tmp/THM-M-0721-ObligationTree.lean` | 0 | exact statement and conditional composition elaborated; axioms reported only `propext` and `Quot.sound` |
| `python3 -m json.tool` on each of `obligation-registry.json`, `typed-graphs.json`, and `validation-specs.json` | 0 | all structured artifacts parsed as JSON |
| `git diff --check -- Stage1_Instances/THM-M-0721 .stage1-worker-selftest.json` | 0 | no whitespace errors |

The first direct attempt, `cd Formalizations/Lean && lake env lean
../../Stage1_Instances/THM-M-0721/ObligationTree.lean`, exited 1 because the worker-owned directory is
outside the Lake source root and therefore `import Statement` could not resolve. No dependency was
fetched or changed. The recorded successful check concatenates the already validated statement and
composition into a temporary file, preserving the exact declarations while using the pinned Lake
environment.

## Status boundary

This evidence self-tests only the obligation registry and graph freeze. It does not prove SAT is in
the frozen NP, formalize Cook-Levin, accept a human source, close the root, or satisfy validation,
release, freshness, hermetic, or independent-verification gates.
