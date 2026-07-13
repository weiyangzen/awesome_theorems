# THM-M-1007 proof-phase validation

Item: `S56-M-1007-PROOF`. Base revision:
`8f22279fd1216cdfb5676c758e6bdb08e0ba3e01`.

Commands ran in this worker clone on 2026-07-14 (`Asia/Shanghai`). The Lean recipe copied only
`Statement.lean`, `ObligationTree.lean`, and `Proof.lean` into a fresh temporary directory, built
disposable statement and obligation-tree oleans, and replayed the proof with `--trust=0 -t0`. The
existing canonical pinned `.lake` symlink
was reused read-only. No `lake update`, `lake build`, dependency clone/fetch, checkout, or network
operation was invoked.

## Commands and exact results

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups, 41 legacy rows, 300 legacy slots, and all
  1546 uniform-L0 Lean 4 targets passed

python3 scripts/stage1_target.py check
  exit 0: 1546 unique ordered targets and ranks 1 through 1546 passed

python3 scripts/stage1_target.py show THM-M-1007
  exit 0: rank 287; planned; L0/rework_required; theorem_complete=false

python3 Stage1_Instances/THM-M-1007/check_obligation_tree.py
  exit 0: the frozen 19-obligation registry, 54 typed edges, and open M3 root passed

python3 Stage1_Instances/THM-M-1007/check_statement.py
  exit 0: exact target expression hash
  3b1a82b3fc0ce70be489e8a49279e3f29cfe244f7a50c28f5c4e5de26894cf38
  and four distinct statement mutations passed

bash Stage1_Instances/THM-M-1007/check_proof.sh
  exit 0: fresh disposable Statement.olean and ObligationTree.olean plus Proof.lean replay passed at
  --trust=0 -t0; all 33 theorem/lemma declaration reports were exactly
  [propext, Classical.choice, Quot.sound]

python3 -B Stage1_Instances/THM-M-1007/check_proof.py
  exit 0: base, target, registry, graph, source hash, dependency pin, receipt,
  blocker, worker packet, hygiene, and exact dirty-scope checks passed

python3 -m json.tool Stage1_Instances/THM-M-1007/proof-receipt.json
python3 -m json.tool Stage1_Instances/THM-M-1007/proof-blocker-2026-07-14.json
python3 -m json.tool .stage1-worker-selftest.json
  exit 0: all three structured artifacts parsed

rg -n '\b(sorry|admit|sorryAx|implemented_by|native_decide|run_tac)\b|^[[:space:]]*(axiom|constant|opaque|unsafe)[[:space:]]+|\bextern[[:space:]]+' Stage1_Instances/THM-M-1007/*.lean
  exit 1 with empty output: expected pass; no sorry, admit, sorryAx, axiom,
  constant, opaque, unsafe, implemented_by, native_decide, run_tac, or extern

git diff --check -- Stage1_Instances/THM-M-1007 .stage1-worker-selftest.json
  exit 0: no scoped whitespace errors
```

The proof source SHA-256 is
`6a8f198527b1f8f915e979991a0e89a06b1728a1bf9e191910a6c63660ecb6c5`.
The pinned environment is Lean 4.29.0 at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, and clean mathlib tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`.

## Status boundary

This validation establishes the 33 local theorem/lemma declarations at their stated types,
including a target-specialized martingale core and the exact frozen sufficiency implication. The
generic bounded-series target remains planned rather than formally frozen. This validation does
not establish
bounded independent-series necessity, the exact biconditional root, a whole
frozen-obligation state transition, master acceptance, H0/R0, cold offline reproduction,
independent verification, validation/release phases, audit completion, or theorem completion.
