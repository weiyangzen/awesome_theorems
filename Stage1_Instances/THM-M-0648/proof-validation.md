# THM-M-0648 proof-phase validation

Item: `S56-M-0648-PROOF`  
Date: `2026-07-12` (`Asia/Shanghai`)  
Base revision: `3249eebf1d6d90d75e4ab28fe97dd9f92c906b59`

`Proof.lean` provides a placeholder-free inhabitant of the exact paired
`CanonicalTarget`. The downward half applies pinned mathlib's
`Language.exists_elementarySubstructure_card_eq`; the upward half applies
`Language.exists_elementaryEmbedding_card_eq_of_ge`. Both declarations are
used at the frozen binder, lift, distinguished-set, exact-cardinality, and
elementary-embedding types, and conjunction construction closes the root.

This is provisional worker evidence for the proof node only. Master
acceptance, H0/R0, hermetic replay, independent validation, release, and
theorem completion are not claimed.

## Exact commands and results

All commands ran inside this worker clone, reused the existing pinned `.lake`
artifacts, and used no network. No update, build, clone, or fetch was run.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0648` | 0 | rank 694, planned, theorem incomplete |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0648/Proof.lean` | 0 | exact paired root elaborated; axioms were `propext`, `Classical.choice`, and `Quot.sound` |
| `cd Formalizations/Lean && python3 ../../Stage1_Instances/THM-M-0648/check_proof.py` | 0 | both exact pinned bodies and the root declaration present; forbidden-boundary scan passed |
| `python3 Stage1_Instances/THM-M-0648/check_obligation_tree.py` | 0 | frozen registry structure passed: 12 obligations and 30 typed edges |
| `git diff --check -- Stage1_Instances/THM-M-0648 .stage1-worker-selftest.json` | 0 | no whitespace errors |

Environment: Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`; pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. The proof source SHA-256 is
`dd5b6aa59ba2ea6584e6862ca05cb2a85aea7384e99eea9726eae43fc61250b1`;
the unchanged statement SHA-256 is
`27605643e4706bbcec0ea4db6c13ce95bc16b035db5de85adfaab245cf062ec2`.

