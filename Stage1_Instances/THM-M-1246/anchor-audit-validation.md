# Anchor audit validation

Item: `S56-M-1246-ANCHOR_AUDIT`. Base revision:
`c00bc6793b3d4c186b81b80bbaf165b32e125b58`.

The audit used the existing canonical pinned `.lake` symlink. It did not run a Lake update, build,
clone, or fetch. Network searches were discovery-only; they did not enter the dependency closure.

| Command | Exit | Result |
|---|---:|---|
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | Exact pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `rg -n -i --glob '*.lean' 'hardy|hardy.?inequal' Formalizations/Lean/.lake/packages/mathlib/Mathlib` | 0 | Only bibliography uses of the author name Hardy; no inequality declaration |
| `rg -n --glob '*.lean' 'HasCompactSupport.*ContDiff|ContDiff.*HasCompactSupport|fderiv.*∫|∫.*fderiv' Formalizations/Lean/.lake/packages/mathlib/Mathlib` | 0 | Located Sobolev analogues and calculus infrastructure; manual type comparison found no exact target |
| `rg -n -i --glob '*.lean' --glob '*.md' 'Hardy inequality|Hardy不等式|hardy_inequality|hardyInequality' . --glob '!Stage1_Instances/THM-M-1246/**'` | 0 | Only Stage0/research/manifest prose; no repo-local Lean candidate |
| GitHub repository search API for `Hardy inequality Lean4`, `Hardy inequality theorem prover Lean`, and `Hardy Lean mathlib` | 0 | Each query returned zero repositories on 2026-07-12 |
| Sourcegraph global Lean searches for `Hardy inequality`, `HardyInequality`, `hardy_inequality`, and `Hardy` with `fderiv` | 0 | Each bounded query completed with `matchCount: 0` on 2026-07-12 |
| `python3 Stage1_Instances/THM-M-1246/check_statement.py` | 0 | Exact root elaborated at the recorded expression and statement hashes |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1246/AnchorAudit.lean` | 0 | Kernel elaboration resolved all four nearest pinned mathlib declarations |
| `python3 -m json.tool Stage1_Instances/THM-M-1246/anchor-audit.json >/dev/null` | 0 | Structured audit record parsed |
| `python3 Stage1_Instances/THM-M-1246/check_anchor_audit.py` | 0 | Fail-closed pin, hash, candidate-list, forbidden-token, and Lean elaboration checks passed |
| `git diff --check -- Stage1_Instances/THM-M-1246 .stage1-worker-selftest.json` | 0 | No whitespace errors |

The nearest mathlib file is pinned and content-addressed as SHA-256
`bbd0840b2f0c1145c325577c18bb136053d2712dc1c24ad66c8aba0370a4623b`. Negative global search
results are necessarily bounded by indexing and the recorded query vocabulary. They justify the
inventory verdict, not a universal nonexistence claim. No exact proof candidate was found, so the
first theorem gate remains exact kernel proof closure.
