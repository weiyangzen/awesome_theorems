# THM-M-0709 proof-phase validation

Item: `S56-M-0709-PROOF`. Base revision:
`4ba3f2fd1e609b5958f24e0415eef9300da16924`.

## Implemented bodies

`Proof.lean` imports the exact target frozen in `Statement.lean`. It implements
the generic fact that a computable many-one reduction pulls a target decider
back to a source decider, pins mathlib's fixed-input halting theorem in the
selected `HaltingPredicate` shape, and composes those results into the exact
`PostCorrespondenceUndecidable` conclusion conditional on
`HaltingPredicate input <=0 HasSolution`.

The reduction premise is intentionally visible. No body constructs the
halting-to-binary-PCP map, so the conditional composition is not an
unconditional root proof. The only provisionally closed frozen proof node is
`M0709-N-HALTING`. The terminal and root declarations are partial progress
toward `M0709-T-UNDECIDABLE` and `M0709-ROOT`, not closure of either node.

Lean checked all three local declarations and both pinned terminal
declarations as sorry-free. Their axiom reports contain only `propext`,
`Classical.choice`, and `Quot.sound`. `Proof.lean` contains no `sorry`, `admit`,
added axiom or constant, opaque or unsafe declaration, external implementation,
or native-decision shortcut.

## Commands and results

Commands ran in the worker clone on 2026-07-15 (Asia/Shanghai). Existing
canonical pinned Lake artifacts were reused through the pre-existing `.lake`
symlink. No update, build, dependency clone or fetch, network validation, or
`.lake` mutation was performed.

```text
(cd Formalizations/Lean &&
  bash ../../Stage1_Instances/THM-M-0709/check_proof.sh)
  exit 0
  isolated Statement.olean and Proof.lean elaboration passed
  all five local/pinned declarations reported sorry-free
  axioms: [propext, Classical.choice, Quot.sound]

python3 Stage1_Instances/THM-M-0709/check_proof.py
  exit 0
  exact declarations, frozen hashes and pins, receipt/blocker boundary,
  prohibited-device scan, and worker packet passed

python3 Stage1_Instances/THM-M-0709/check_statement.py
  exit 0
  expression SHA-256 5d375802...6d03; all four mutations killed

python3 Stage1_Instances/THM-M-0709/check_obligation_tree.py
  exit 0
  18 obligations and 81 typed edges passed; root remains open M3

python3 Docs/tools/check_stage1_standard.py
  exit 0
  15 assurance groups and 1546 uniform-L0 targets passed

python3 scripts/stage1_target.py check
  exit 0
  1546 unique targets at ranks 1 through 1546 passed

python3 scripts/stage1_target.py show THM-M-0709
  exit 0
  rank 750, planned, L0/rework_required, theorem_complete false

git diff --check -- Stage1_Instances/THM-M-0709 \
  .stage1-worker-selftest.json
  exit 0; no whitespace errors
```

The first failed gate is `M0709-C-MACHINE`: the pinned closure contains no
placeholder-free computable normalization from mathlib's halting-code model to
the finite machine model of the frozen PCP route. The remaining reduction cut
also includes MPCP construction and correctness, MPCP-to-PCP transport, binary
normalization and preservation, and computability of their composition.

This is provisional, warm-cache, nonrelease proof-phase evidence. The root
remains M3; accepted state, master acceptance, source/readability closure,
validation, hermetic and independent replay, release, audit completion, and
theorem completion remain open.
