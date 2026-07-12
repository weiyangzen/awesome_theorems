# THM-M-0012 proof-phase validation

Item: `S56-M-0012-PROOF`. Base revision:
`c2467750f2cdb3960045c83e819d96687253303d` (tree
`0f79eb697267dc28b29d41a1e282f319d758a2ac`).

## Implemented proof

`Proof.lean` imports the exact frozen statement and obligation interfaces. It closes
`FundamentalTheoremOfAlgebraTarget` directly with the pinned `Complex.exists_root` declaration
after applying the checked nonconstant-to-positive-degree bridge. A separate root declaration
instantiates every frozen analytic engine: reciprocal differentiability, reciprocal decay,
Liouville vanishing, and polynomial extensionality. The frozen composition certificates then
consume those children to obtain the no-root contradiction, the positive-degree anchor, and the
exact canonical root.

The proof contains no `sorry`, `admit`, custom axiom, `sorryAx`, unsafe/opaque declaration, native
oracle, external code, numerical experiment, or weakened theorem. Lean reports exactly `propext`,
`Classical.choice`, and `Quot.sound` for the exact root, pinned anchor, expanded root, and engine
declarations.

The terminal proof body is `Complex.exists_root` in pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, source SHA-256
`f6159d7625ca323846088b04ae89fca501bb040fcdce982f8f24c453e587d491`.

## Commands and results

Validation ran on 2026-07-13 (`Asia/Shanghai`) using the automation-provided canonical `.lake`
symlink read-only. No `lake update`, `lake build`, dependency clone/fetch, or `.lake` mutation ran.

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required

python3 scripts/stage1_target.py show THM-M-0012
  exit 0: execution rank 1062, planned, theorem_complete false

cd Formalizations/Lean &&
  bash ../../Stage1_Instances/THM-M-0012/check_proof.sh
  exit 0: isolated Statement.olean and ObligationTree.olean were built; Proof.lean elaborated;
  every printed proof declaration reports [propext, Classical.choice, Quot.sound]

python3 -B Stage1_Instances/THM-M-0012/check_proof.py
  exit 0: exact target, frozen graph inputs, terminal source pin, source hashes, receipt, composition,
  placeholder boundary, and worker packet passed

python3 -B Stage1_Instances/THM-M-0012/check_obligation_tree.py
  exit 0: 20 frozen obligations and 41 typed edges passed; accepted root remained H1/M3/R4

python3 -m json.tool Stage1_Instances/THM-M-0012/proof-receipt.json
python3 -m json.tool .stage1-worker-selftest.json
  exit 0: both structured artifacts parsed

cd Formalizations/Lean && lake env lean --version
  exit 0: Lean 4.29.0, commit 98dc76e3c0a9b856c9b98726b713fb04fab16740

git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}
  exit 0: revision 8a178386...ea95, tree bdc39a31...c2b

git -C Formalizations/Lean/.lake/packages/mathlib status --short
  exit 0: empty output; pinned dependency worktree clean

git diff --check -- Stage1_Instances/THM-M-0012 .stage1-worker-selftest.json
  exit 0: no tracked whitespace diagnostics

git diff --no-index --check /dev/null <each untracked proof-phase file>
  exit 1 for each expected new-file difference, with no whitespace diagnostics
```

## Status boundary

This is provisional proof-phase evidence and proposes `M0-W` only after master acceptance. The
authoritative accepted state remains `H1/M3/R4` with an empty accepted proof state. The obligation
tree prerequisite and proof receipt require dependency-ordered master acceptance. Validation,
release, H0, R0, full transitive trust/provenance closure, hermetic replay, independent verification,
and deterministic evidence remain open. Neither audit completion nor theorem completion is claimed.
