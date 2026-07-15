# THM-M-1566 proof-phase recheck at current base

Item: `S56-M-1566-PROOF`

Recorded at: `2026-07-15T19:41:19+08:00`

Base revision: `90a1d52c43113012c8aa0e2b110da02e58ce1724`

Base tree: `bc399f3ba59411f2a72d4f29d98eb85e7689b28c`

## Verdict

`blocked`. No consistent positive proof body can inhabit the exact frozen Lean
target. The unchanged, placeholder-free declaration

```text
Stage1Instances.THMM1566.not_GIPCorollary59Target :
  Not (Stage1Instances.THMM1566.GIPCorollary59Target.{0})
```

kernel-checks at trust level zero against the current pinned environment. Its
model takes `Omega := Unit`, the Dirac probability measure, every non-solution
carrier to be `Unit`, and `Solution := Empty`. The data assumptions remain
inhabited at `alpha = beta = 3/4`; applying the positive target then supplies
an inhabitant of `Empty`.

This refutes the frozen abstract encoding, not Gubinelli--Imkeller--Perkowski
Corollary 5.9. Merely adding `Nonempty api.Solution` would not suffice because
an unconstrained API may instead interpret `solvesLimitEquation` as false. A
repair therefore requires source-faithful concrete semantics or substantive
noncircular adequacy hypotheses. That changes the statement boundary and must
receive new statement, anchor-audit, and obligation-tree receipts before proof
execution resumes.

The conditional theorem `root_of_existence_and_uniqueness` remains valid, but
it consumes the open existence and uniqueness packages and cannot close the
root. No positive body, proof receipt, or obligation closure was added.

The pre-existing automation `.lake` symlink was reused read-only. No `lake
update`, `lake build`, clone, fetch, network access, or dependency mutation was
performed. Isolated Lean outputs lived only in a fresh `/tmp` directory, which
was removed. The dirty symlink makes this evidence nonrelease.

## Validation

All commands ran from this worker clone against existing pinned artifacts.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required. |
| `python3 scripts/stage1_target.py show THM-M-1566` | 0 | Rank 182; planned lifecycle; theorem incomplete. |
| `env LEAN_NUM_THREADS=1 timeout --foreground --kill-after=5s 300s python3 Stage1_Instances/THM-M-1566/check_statement.py` | 0 | Expression hash `70ee4869...473a`; all four structural mutations were distinguished. |
| `python3 Stage1_Instances/THM-M-1566/check_anchor_audit.py` | 0 | Four candidates, four search records, five Lean support probes, and the M4 boundary agreed. |
| `python3 Stage1_Instances/THM-M-1566/check_obligation_tree.py` | 0 | 15 obligations and 40 typed edges passed; denominator `7ae15c07...3fe640`; root remains open M4. |
| `env LEAN_NUM_THREADS=1 timeout --foreground --kill-after=5s 300s python3 Stage1_Instances/THM-M-1566/validate_obligation_tree.py` | 0 | Exact statement and conditional composition elaborated; the assembler reported `[propext, Classical.choice, Quot.sound]`. |
| Isolated trust-zero recipe below | 0 | The exact statement and refutation elaborated; `not_GIPCorollary59Target` reported `[propext, Classical.choice, Quot.sound]`; object hashes were `1e1c07...2793` and `611605...62f3`; the temporary directory was removed. |
| `rg -n '\b(sorry\|admit\|sorryAx\|native_decide\|implemented_by)\b\|^[[:space:]]*(axiom\|opaque\|constant\|unsafe\|external)[[:space:]]' Stage1_Instances/THM-M-1566 --glob '*.lean'` | 1 | Expected no-match exit; no prohibited proof escape was found. |
| `python3 -m json.tool Stage1_Instances/THM-M-1566/proof-recheck-2026-07-15-head-90a1d52c-slot18.json` | 0 | Structured blocker record is valid JSON. |
| Inline Python invariant and source-hash assertions | 0 | Base identity, exact hashes, refutation state, two-file scope, and absent self-test agreed. |
| `git diff --no-index --check /dev/null` for each new artifact | 1, 1 | Expected added-file status with no whitespace diagnostics. |
| `git diff --check -- Stage1_Instances/THM-M-1566` | 0 | No whitespace errors in tracked owned-path changes. |
| `test ! -e .stage1-worker-selftest.json` | 0 | The incomplete proof phase emitted no completion manifest. |

Exact narrow Lean replay, run from the repository root:

```bash
set -euo pipefail
repo=$PWD
tmp=$(mktemp -d /tmp/thm-m-1566-proof-90a1d52c-slot18.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
cp "$repo/Stage1_Instances/THM-M-1566/Statement.lean" "$tmp/Statement.lean"
cp "$repo/Stage1_Instances/THM-M-1566/ProofCountermodel.lean" "$tmp/ProofCountermodel.lean"
mathlib="$repo/Formalizations/Lean/.lake/packages/mathlib"
extra="$repo/Formalizations/Lean/.lake/packages/Cli/.lake/build/lib/lean:$repo/Formalizations/Lean/.lake/packages/batteries/.lake/build/lib/lean:$repo/Formalizations/Lean/.lake/packages/Qq/.lake/build/lib/lean:$repo/Formalizations/Lean/.lake/packages/aesop/.lake/build/lib/lean:$repo/Formalizations/Lean/.lake/packages/proofwidgets/.lake/build/lib/lean:$repo/Formalizations/Lean/.lake/packages/importGraph/.lake/build/lib/lean:$repo/Formalizations/Lean/.lake/packages/LeanSearchClient/.lake/build/lib/lean:$repo/Formalizations/Lean/.lake/packages/plausible/.lake/build/lib/lean"
(cd "$mathlib" && LEAN_NUM_THREADS=1 LEAN_PATH="$extra" \
  timeout --foreground --kill-after=5s 300s lake env lean --trust=0 -t0 -R "$tmp" \
  -o "$tmp/Statement.olean" "$tmp/Statement.lean")
(cd "$mathlib" && LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$extra" \
  timeout --foreground --kill-after=5s 300s lake env lean --trust=0 -t0 -R "$tmp" \
  -o "$tmp/ProofCountermodel.olean" "$tmp/ProofCountermodel.lean")
sha256sum "$tmp/Statement.olean" "$tmp/ProofCountermodel.olean"
```

## Status Boundary

The authoritative vector remains `H1 / M4 / R3`; `H1 / M5 / R3` is only the
proposed diagnosis pending an authorized refreeze. The first failed gate is
positive exact-root kernel closure at `M1566-ROOT`, caused by the unconstrained
`M1566-S-INTERFACE` and directly refuting `M1566-T-EXISTENCE`.

The proof item remains `[ ]`, `root_closed=false`, `audit_complete=false`, and
`theorem_complete=false`. There is no provisional or accepted receipt. Because
the assigned phase is not genuinely complete, `.stage1-worker-selftest.json`
is deliberately absent.

Resume only after an authorized statement revision replaces the unconstrained
API with fixed source-faithful semantics or substantive noncircular adequacy
hypotheses, then refreezes every downstream fingerprint and receipt.
