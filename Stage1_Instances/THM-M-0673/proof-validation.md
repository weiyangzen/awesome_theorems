# THM-M-0673 proof-phase validation

Item: `S56-M-0673-PROOF`. Base revision:
`310be814cb307a91263e232acf691a6b3eded70e` (tree
`947289604e1bf9c317b6dc3dd174d3f8fb54ba0e`).

## Implemented proof

`Proof.lean` installs the manifest-pinned
`FirstOrder.Language.Ultraproduct.boundedFormula_realize_cast` body at the exact
`BoundedFormulaRealizePackage` interface frozen by `ObligationTree.lean`. It
then consumes the four frozen composition declarations in order: bounded
formulas to formulas, formulas to sentences, sentences to the terminal
package, and the terminal package to the unchanged `LosSentenceTarget`.
`losSentence_pinned` independently checks the same exact root directly through
`FirstOrder.Language.Ultraproduct.sentence_realize`.

The imported body is the structural induction at pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, source SHA-256
`ba32a045647e55dee5bc5b4534ede125eb6cc7bef523aec77dea5e980dfacd54`.
The local bounded package, the composed root, the direct root, and the earlier
audit wrapper all deduplicate to this one transparent upstream proof route.

This receipt observes exact kernel inhabitants for `M0673-A-BOUNDED`,
`M0673-A-FORMULA`, `M0673-A-SENTENCE`, `M0673-T-ADAPTER`, and `M0673-ROOT`.
The fifteen internal induction branches and support nodes are transparently
mapped to the pinned source but are not claimed as separately node-closed.
The frozen graph and accepted instance remain unchanged pending master
reconciliation.

## Commands and results

The proof replay used the automation-provided canonical `.lake` symlink
read-only. It compiled temporary copies of `Statement.lean`,
`ObligationTree.lean`, and `Proof.lean` with `--trust=0`, then removed the
temporary directory. No `lake update`, `lake build`, dependency clone/fetch,
network operation, or `.lake` mutation was performed.

```text
bash Stage1_Instances/THM-M-0673/check_proof.sh
  exit 0
  Statement, ObligationTree, and Proof compiled in a disposable directory.
  The bounded package, four frozen compositions, and direct exact root
  elaborated. Eleven upstream/local declarations each reported exactly
  [propext, Classical.choice, Quot.sound]. The proof-root traversal covered
  5,088 declarations in 192 modules with no bodyless nonaxiom or unsafe
  declaration. Combined output: 2,124 bytes, SHA-256
  16bd58ac43e55aa5088253af47577912c43d94170eb8f0a5a3aacbca019b8045.

python3 -B Stage1_Instances/THM-M-0673/check_proof.py
  exit 0
  Exact target, frozen denominator and graph boundary, terminal source and
  compiled pin, proof source, structured receipt, placeholder policy, and
  worker handoff agreed.

python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and all 1546 uniform-L0 targets passed.

python3 scripts/stage1_target.py check
  exit 0: 1546 unique ordered targets, ranks 1 through 1546, passed.

python3 scripts/stage1_target.py show THM-M-0673
  exit 0: rank 717, planned, L0/rework-required, theorem_complete=false.

python3 -m json.tool Stage1_Instances/THM-M-0673/proof-receipt.json
python3 -m json.tool .stage1-worker-selftest.json
  exit 0: both structured artifacts parsed.

git diff --check -- Stage1_Instances/THM-M-0673 \
  .stage1-worker-selftest.json
  exit 0: no whitespace diagnostics.
```

## Status boundary

This is provisional proof-node evidence proposing only `[_]` and an `M0-W`
root candidate after dependency-ordered master reconciliation. It accepts no
obligation or debt-vector change. The predecessor receipt, graph
reconciliation, foundation and release-grade trust/provenance review, H0, R0,
cold hermetic replay, independent verification, validation, release,
`AUDIT-Z`, and `THEOREM-Z` remain open. Therefore `audit_complete=false` and
`theorem_complete=false`.
