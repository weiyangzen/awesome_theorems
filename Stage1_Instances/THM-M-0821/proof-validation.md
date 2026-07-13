# THM-M-0821 proof-phase validation

Item: `S56-M-0821-PROOF`. Base revision:
`5931467f7eefac7a6e57777cc3082e4a2edc03d4`.

## Implemented proof

`Proof.lean` installs the lower-middle powerset slice as an attaining
antichain, adopts `IsAntichain.sperner` from the manifest-pinned mathlib
revision as the universal upper bound, and follows all six checked package
composition certificates to the exact frozen `SpernerMaximumTarget`. The
proof therefore includes both necessary halves of a maximum claim: attainment
and a bound for every finite antichain. It does not substitute the narrower
upper-bound theorem for the canonical target.

Lean reports `IsAntichain.sperner` and all three local proof declarations
sorry-free. Their axiom closures are exactly `propext`, `Classical.choice`, and
`Quot.sound`. The proof source and inspected terminal source contain no
placeholder, added axiom, bodyless or opaque declaration, unsafe injection,
oracle, native evaluation, or substituted target.

This is provisional proof-phase evidence for an `M0-W` root proposal, not
accepted closure or theorem completion. The imported terminal maps to the 24
proof-reachable frozen IDs, but the eight internal LYM source-body
decompositions still lack separate abstract-child composition certificates.
They receive no individual closure credit. The accepted dossier remains
`[H1, M3, R4]` with zero accepted obligations.

The checked root composition is two-sided in the sense required by the
maximum claim: `middleLayerAttainment` exhibits a family of the claimed size,
while `universalUpperBound` proves that no antichain is larger. Omitting either
package makes `maximumSplit_of_packages` inapplicable, so the wrapper cannot
accidentally certify only one side.

The receipt is explicitly nonrelease and not content-addressed: this worker
tree is dirty with the six owned handoff files and the pre-existing `.lake`
symlink. It binds the proof, frozen statement/tree/graph, terminal source and
olean, and both proof checkers by SHA-256. Canonical receipt/log hashing and an
immutable clean snapshot remain validation and release work.

## Commands and results

Validation ran in the worker clone on 2026-07-13 (Asia/Shanghai). It reused the
existing canonical pinned `.lake` artifacts. No `lake update`, `lake build`,
dependency clone, fetch, network access, or mutation of `.lake` was performed.

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546
  uniform-L0 Lean 4 targets passed

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required

python3 scripts/stage1_target.py show THM-M-0821
  exit 0: rank 1379, planned, L0/rework_required,
  theorem_complete=false

bash Stage1_Instances/THM-M-0821/check_proof.sh
  exit 0: temporary Statement.olean and ObligationTree.olean elaborated;
  the pinned terminal, attaining package, upper package, and exact root passed
  four assert_no_sorry checks; all four proof-phase axiom reports were
  [propext, Classical.choice, Quot.sound]; the shell passed its captured Lean
  log to check_proof.py, which validated the axiom text and full handoff

python3 -B Stage1_Instances/THM-M-0821/check_obligation_tree.py
  exit 1 at its historical-base assertion: this integrated obligation-tree
  checker is permanently bound to its worker base a3b18eec, while the current
  proof worker starts from integration commit 5931467f. Its generated registry
  and graph bytes are checked directly by check_proof.py instead of rewriting
  the historical receipt or checker.

PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0821-proof-pycache \
  python3 -m py_compile Stage1_Instances/THM-M-0821/check_proof.py
  exit 0: checker syntax compiled outside the owned path

python3 -B Stage1_Instances/THM-M-0821/check_proof.py
  exit 0: reran scoped Lean elaboration, then checked exact wrappers, hashes,
  immutable mathlib pin, source/olean, axiom output, composition boundary,
  placeholder policy, receipt, and worker packet

python3 -m json.tool Stage1_Instances/THM-M-0821/proof-receipt.json
python3 -m json.tool .stage1-worker-selftest.json
  exit 0 for both JSON artifacts

rg -n '\b(sorry|admit|sorryAx)\b|^[[:space:]]*(axiom|constant|opaque|unsafe)\b|\b(implemented_by|native_decide)\b' \
  Stage1_Instances/THM-M-0821/Proof.lean \
  Formalizations/Lean/.lake/packages/mathlib/Mathlib/Combinatorics/SetFamily/LYM.lean
  exit 1 with empty output: expected clean no-match result

git diff --check -- Stage1_Instances/THM-M-0821 \
  .stage1-worker-selftest.json
  exit 0: no whitespace errors

PYTHONOPTIMIZE=1 python3 -B Stage1_Instances/THM-M-0821/check_proof.py
  exit 1 as expected: the checker fails closed instead of permitting Python
  optimization to disable its assertions

run check_proof.sh twice to /tmp logs, then sha256sum and cmp
  exit 0: both 13145-byte outputs matched exactly at SHA-256
  0462d9eba0c69a3ec2ff79d3ced4906abdc4606692a2602b49cb39bb8eb6d619

per-file git diff --no-index --check /dev/null for all six untracked handoff files
  exit 0 aggregate: no whitespace diagnostics; each underlying status 1 meant
  only that the checked file is new
```

Master acceptance, complete transitive provenance and trust closure, the
downstream validation and release nodes, H0/R0, hermetic replay, independent
verification, `AUDIT-Z`, and `THEOREM-Z` remain open.
