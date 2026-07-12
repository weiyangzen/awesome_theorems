# Statement validation

Item: `S56-M-0594-STATEMENT`. Base revision:
`45ecc126e04773079f94f7b6f73d4f4c9a6da900`.

The canonical target elaborates using the single direct import
`Mathlib.Geometry.Manifold.WhitneyEmbedding`. It is the unrestricted,
existence-only statement: it has second-countability and boundarylessness but
no compactness premise and no fixed Euclidean dimension. The declaration is a
`def` of a proposition, not an inhabitant or proof of that proposition.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 1546 uniform-L0 targets, and the execution skill agree |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets with ranks 1 through 1546 |
| `python3 scripts/stage1_target.py show THM-M-0594` | 0 | rank 255, planned, L0/rework-required, theorem incomplete |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0594/Statement.lean` | 0 | exact target and checked `Iff.rfl` expansion elaborated; `#print` emitted the target |
| `cd Formalizations/Lean && lake env lean -Dpp.universes=true -Dpp.explicit=true ../../Stage1_Instances/THM-M-0594/Statement.lean` | 0 | explicit serialized declaration emitted; extracted declaration SHA-256 is `32943593a17c04d3b6fab019d7cf0db88d5e59b59f3d73703e82514987e97ef6` |
| `cd Formalizations/Lean && lake env lean -R ../../Stage1_Instances/THM-M-0594 -o ../../Stage1_Instances/THM-M-0594/Statement.olean ../../Stage1_Instances/THM-M-0594/Statement.lean && LEAN_PATH="$(pwd)/../../Stage1_Instances/THM-M-0594:${LEAN_PATH:-}" lake env lean -R ../../Stage1_Instances/THM-M-0594 ../../Stage1_Instances/THM-M-0594/StatementMutations.lean` | 1 (expected) | exactly four type mismatches reject removal of second-countability, addition of compactness, a fixed `2m+1` dimension, and weakening to continuous injection; temporary `Statement.olean` removed |
| `python3 -m json.tool Stage1_Instances/THM-M-0594/statement.json >/dev/null` | 0 | statement record is valid JSON |
| `rg -n '\\b(sorry\|axiom\|admit)\\b' Stage1_Instances/THM-M-0594/Statement.lean Stage1_Instances/THM-M-0594/StatementMutations.lean` | 1 (expected) | no prohibited proof escape or declaration |
| `git diff --check -- Stage1_Instances/THM-M-0594 .stage1-worker-selftest.json` | 0 | no whitespace errors |

Lean is `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`; mathlib is pinned at
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. No update, build, fetch, clone, or
write under `.lake` was performed; the canonical `.lake` symlink was used
read-only.

Worker verdict: statement elaboration is self-tested and provisional (`M3`),
pending master acceptance. The pinned mathlib theorem adds compactness and is
not the frozen root. No proof, audit, or theorem-completion status is claimed.
