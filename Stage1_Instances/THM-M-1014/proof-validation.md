# THM-M-1014 proof-phase validation

Item: `S56-M-1014-PROOF`. Base revision:
`9a198a2d8ff0981d17df1c1b8d4b11e4babaf7ed`.

`Proof.lean` applies the unique exact theorem in the pinned mathlib dependency to the unchanged
binders and premise of `StatementShape`. The result is checked at
`ObligationTree.ContinuousMappingTerminal`, composed through
`root_of_continuousMappingTerminal`, and exposed as the exact statement-phase proposition.

Validation ran in the worker clone on 2026-07-12. It reused the canonical pinned Lake artifacts.
No update, build, dependency fetch/clone, network operation, or `.lake` mutation was performed.

## Commands and results

```text
cd Stage1_Instances/THM-M-1014
LEAN_BIN=$(cd ../../Formalizations/Lean && lake env which lean)
LEAN_PATH_BASE=$(cd ../../Formalizations/Lean && lake env printenv LEAN_PATH)
LEAN_PATH="$LEAN_PATH_BASE" "$LEAN_BIN" -o Statement.olean Statement.lean
LEAN_PATH=".:$LEAN_PATH_BASE" "$LEAN_BIN" -o ObligationTree.olean ObligationTree.lean
LEAN_PATH=".:$LEAN_PATH_BASE" "$LEAN_BIN" Proof.lean
rm -f Statement.olean ObligationTree.olean Proof.olean
  exit 0: the statement, frozen composition, and four proof declarations elaborated from isolated
  temporary oleans; every proof declaration reports exactly propext, Classical.choice, Quot.sound

python3 Stage1_Instances/THM-M-1014/check_proof.py
  exit 0: exact pinned declaration, terminal interface, frozen composition, exact root,
  placeholder scan, and four axiom probes passed; Proof.lean SHA-256
  7806ff31b02d9914da2b07d3ca481810a3d30d13eea11f409bab88e34511f6cf

python3 Stage1_Instances/THM-M-1014/check_obligation_tree.py
  exit 0: 14 frozen obligations and 22 typed edges passed; denominator
  2547bce4e55d4d787d3e3224fc97ca57424e6916f36a3a09e0101560ba58e07b

python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and all 1546 uniform-L0 targets passed

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required

python3 scripts/stage1_target.py show THM-M-1014
  exit 0: rank 293, planned, legacy artifacts unaccepted, theorem_complete false

cd Formalizations/Lean && lake env lean --version
  exit 0: Lean 4.29.0, commit 98dc76e3c0a9b856c9b98726b713fb04fab16740

git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD
  exit 0: 8a178386ffc0f5fef0b77738bb5449d50efeea95

python3 -m json.tool Stage1_Instances/THM-M-1014/proof.json >/dev/null
  exit 0: structured proof record parses

git diff --check -- Stage1_Instances/THM-M-1014 .stage1-worker-selftest.json
  exit 0: no scoped whitespace errors
```

The obligation-tree validator truthfully retains its immutable pre-proof observation (`M1`, cut
set `THM-M-1014-X-PINNED`); this phase supplies that body without rewriting an earlier phase's
artifacts. The proposed root classification is `M0-P`, pending master acceptance.

## Status boundary

This is proof-phase self-test evidence, not master acceptance or theorem completion. Human-source
`H0`, readable `R0`, structured downstream validation, hermetic replay, independent verification,
release, `AUDIT-Z`, and `THEOREM-Z` remain open.
