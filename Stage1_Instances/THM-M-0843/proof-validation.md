# THM-M-0843 proof-phase validation

Item: `S56-M-0843-PROOF`. Base revision:
`3815f6945257af057dfb5e6b6dfe2be5b6f451d9`.

## Implemented proof

`Proof.lean` adopts the explicit `szemeredi_regularity` body from the
manifest-pinned mathlib dependency. It proves the exact frozen root through
`compose_root terminal_adapter pinnedTerminal` and separately checks a direct
wrapper at `SzemerediRegularityTarget`. The terminal body is imported once and
not duplicated by the two wrappers.

Lean reports the pinned terminal and all three local declarations sorry-free.
Their axiom closures are exactly `propext`, `Classical.choice`, and
`Quot.sound`. The proof source contains no placeholder, added axiom, opaque or
unsafe declaration, oracle, native evaluation, or substituted target.

This is provisional proof-phase evidence for an `M0-W` machine-root proposal,
not accepted closure or theorem completion. The receipt maps the terminal body
to all 38 proof-reachable frozen IDs but deliberately gives no individual
closure credit to the 18 internal source-body decompositions that lack checked
abstract-child composition certificates. The accepted dossier remains
`[H1, M3, R4]` with zero accepted obligations.

## Commands and results

Validation ran in the worker clone on 2026-07-13 (Asia/Shanghai). It reused the
existing canonical pinned `.lake` artifacts. No update, build, dependency
clone, fetch, network access, or mutation of `.lake` was performed.

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required

python3 scripts/stage1_target.py show THM-M-0843
  exit 0: rank 1032, planned, L0/rework_required,
  theorem_complete=false

TMP=$(mktemp -d /tmp/thm-m-0843-proof.XXXXXX)
LEAN_BIN=$(cd Formalizations/Lean && lake env which lean)
LEAN_PATH_PINNED=$(cd Formalizations/Lean && lake env printenv LEAN_PATH)
LEAN_PATH="$LEAN_PATH_PINNED" "$LEAN_BIN" \
  Stage1_Instances/THM-M-0843/Statement.lean \
  -o "$TMP/Statement.olean"
LEAN_PATH="$TMP:$LEAN_PATH_PINNED" "$LEAN_BIN" \
  Stage1_Instances/THM-M-0843/ObligationTree.lean \
  -o "$TMP/ObligationTree.olean"
LEAN_PATH="$TMP:$LEAN_PATH_PINNED" "$LEAN_BIN" \
  Stage1_Instances/THM-M-0843/Proof.lean
rm -rf "$TMP"
  exit 0: exact terminal, frozen composition root, and direct root elaborated;
  four proof-phase sorry checks passed; all four proof-phase axiom reports
  were [propext, Classical.choice, Quot.sound]

PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0843-proof-pycache \
  python3 -m py_compile Stage1_Instances/THM-M-0843/check_proof.py
  exit 0: checker syntax compiled outside the owned path

python3 -B Stage1_Instances/THM-M-0843/check_proof.py
  exit 0: receipt hashes, exact wrappers, mathlib source/olean pins, graph
  boundary, placeholder scan, and worker packet passed

python3 -m json.tool Stage1_Instances/THM-M-0843/proof-receipt.json
python3 -m json.tool .stage1-worker-selftest.json
  exit 0 for both JSON artifacts

git diff --check -- Stage1_Instances/THM-M-0843 \
  .stage1-worker-selftest.json
  exit 0: no whitespace errors
```

Master acceptance, the downstream validation and release nodes, H0/R0,
transitive provenance and trust acceptance, hermetic replay, independent
verification, and `THEOREM-Z` remain open.
