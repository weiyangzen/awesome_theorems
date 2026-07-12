# THM-M-0988 proof-phase validation

Item: `S56-M-0988-PROOF`. Base revision:
`8fae7de1ca4ed3b0645d51573ac87053fb300f40`.

`Proof.lean` supplies the placeholder-free body for the frozen root cut. The
`pinnedMathlibBridge` theorem applies the exact pinned declaration
`ProbabilityTheory.tendstoInDistribution_inv_sqrt_mul_sum_sub` to the unchanged
binders and four hypotheses from `StatementShape`. The bridge is checked again
at `ObligationTree.Root`, composed through the frozen `root_compose`
certificate, and returned as the exact statement-phase target
`lindebergLevyCentralLimit`.

Validation ran in the worker clone on 2026-07-12. It reused the canonical
pinned Lake artifacts. No update, build, dependency fetch/clone, network
operation, or `.lake` mutation was performed.

```text
bash Stage1_Instances/THM-M-0988/check_proof.sh
  exit 0
  Statement.lean, ObligationTree.lean, and Proof.lean elaborated using isolated
  temporary oleans; all four proof declarations report exactly propext,
  Classical.choice, and Quot.sound

python3 Stage1_Instances/THM-M-0988/check_proof.py
  exit 0: pinned bridge, frozen composition, exact root, placeholder scan, and
  four axiom probes passed; Proof.lean SHA-256
  d4c214249284ac28f830e92be9bdc43449a124ba8acdfdd16af7c29072800cb6

python3 Stage1_Instances/THM-M-0988/check_obligation_tree.py
  exit 0: 18 frozen obligations and 29 typed edges passed; denominator
  e5bd80bd684e277b213f25d9bf0a41a2611240e81ff8efd7f3198f20e7bfbdbb

python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and all 1546 uniform-L0 targets passed

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required

python3 scripts/stage1_target.py show THM-M-0988
  exit 0: rank 268, planned, legacy artifacts unaccepted, theorem_complete false

cd Formalizations/Lean && lake env lean --version
  exit 0: Lean 4.29.0, commit
  98dc76e3c0a9b856c9b98726b713fb04fab16740

git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD
  exit 0: 8a178386ffc0f5fef0b77738bb5449d50efeea95

git diff --check -- Stage1_Instances/THM-M-0988 .stage1-worker-selftest.json
  exit 0: no whitespace errors
```

The obligation-tree validator truthfully retains its immutable pre-proof
observation (`M1`, cut set `M0988-X-PINNED`); this proof phase supplies that
body without rewriting the earlier phase artifact. The proof node is
self-tested pending master acceptance. Primary-source and readable review,
full validation, hermetic replay, independent verification, and release remain
downstream, so theorem completion is not claimed.
