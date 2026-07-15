# THM-M-0594 partial proof validation

Item: `S56-M-0594-PROOF`

Base revision: `b1a5b03c9eb85b0777b34f58df31029086acf260`

## Result

The worker supplies an unconditional placeholder-free body for frozen bridge
`M0594-L-TOPOLOGICAL`. Given a proper injective map into the exact Euclidean
target, `properInjectiveEuclideanMap_isEmbedding` proves `IsEmbedding`.
`whitneyEmbeddingTarget_of_properInjectiveImmersion` then checks composition
into the unchanged canonical target from an explicit smooth proper injective
immersion witness.

The exact unrestricted Whitney root remains open. In particular, the
composition theorem does not construct its witness: `M0594-C-GLOBAL` and its
exhaustion, dimension, local-coordinate, differential, point-separation, and
properness packages remain unimplemented. The worker proposes only provisional
`[_]` proof progress pending master reconciliation.

## Isolated Replay

```bash
bash Stage1_Instances/THM-M-0594/check_proof.sh
```

Exit code: `0`.

```text
PASS THM-M-0594 partial proof: M0594-L-TOPOLOGICAL
Lean (version 4.29.0, x86_64-unknown-linux-gnu, commit 98dc76e3c0a9b856c9b98726b713fb04fab16740, Release)
declarations: properInjectiveEuclideanMap_isEmbedding, whitneyEmbeddingTarget_of_properInjectiveImmersion
axioms for each declaration: propext, Classical.choice, Quot.sound
root closure: open; M0594-C-GLOBAL remains unimplemented
```

The checker copies `Statement.lean`, `ProofSupport.lean`, and `Proof.lean` to a
temporary directory. It resolves the existing pinned Lean executable and
package path through `lake env`, creates disposable statement/support oleans,
and elaborates `Proof.lean` with `--trust=0 -t0`. It also requires two
`assert_no_sorry`/`#print sorries` successes, exact axiom reports, a clean
prohibited-device scan, and no repository olean output.

No `lake update`, `lake build`, dependency clone/fetch, checkout, repair, or
`.lake` mutation was run. The automation-provided canonical `.lake` symlink and
existing pinned objects were reused read-only. This is warm, nonrelease worker
evidence.

## Structural Checks

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets at ranks 1 through 1546 passed |
| `python3 scripts/stage1_target.py show THM-M-0594` | 0 | rank 255, planned, legacy artifacts unaccepted, theorem incomplete |
| `python3 Stage1_Instances/THM-M-0594/check_obligation_tree.py` | 0 | 16 obligations and 46 typed edges passed; frozen root remains open M3 |
| `python3 -m py_compile Stage1_Instances/THM-M-0594/check_proof.py` | 0 | proof checker syntax passed; generated cache removed |
| owned Lean prohibited-construct scan | 1 | expected no-match: no bodyless declaration, `sorry`, `admit`, `sorryAx`, unsafe/oracle escape, or proof placeholder |
| pinned Whitney endpoint/TODO scan | 0 | unrestricted theorem remains TODO; only finite-index/compact endpoints exist |
| `git diff --check -- Stage1_Instances/THM-M-0594 .stage1-worker-selftest.json` | 0 | no whitespace errors |

Pinned environment: Lean `4.29.0`, commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`; mathlib
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`; frozen registry denominator
`0ad656eddf1e42c8f47912729ceddcab9e45d56fd8a68e24b7bc82d59d367443`.

Status boundary: accepted obligation closure remains empty until integration.
The receipt does not satisfy the full proof node, prove the root, establish
theorem completion, or claim validation, release, receipt acceptance, or
master acceptance.
