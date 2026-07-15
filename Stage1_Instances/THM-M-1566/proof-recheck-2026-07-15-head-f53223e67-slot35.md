# THM-M-1566 proof-phase recheck at current base

Item: `S56-M-1566-PROOF`

Recorded at: `2026-07-15T18:00:28+08:00`

Base revision: `f53223e6746df4856b00068d3e8723264dfd044a`

Base tree: `bb293e5342b6501791d40c7464d150820aafe441`

## Verdict

`blocked`. No consistent positive proof body can inhabit the exact frozen Lean
target. The unchanged placeholder-free declaration

```text
Stage1Instances.THMM1566.not_GIPCorollary59Target :
  Not (Stage1Instances.THMM1566.GIPCorollary59Target.{0})
```

was replayed at trust level zero against the existing pinned Lean and mathlib
objects. Its model sets `Omega := Unit`, uses the Dirac probability measure,
takes every non-solution carrier to be `Unit`, and takes `Solution := Empty`.
The numerical premises are inhabited at `alpha = beta = 3/4`. Applying the
positive target therefore supplies an inhabitant of `Empty`.

This refutes the frozen abstract encoding, not Corollary 5.9 in the cited
Gubinelli--Imkeller--Perkowski paper. Adding only `Nonempty api.Solution` would
not repair the encoding: a universally quantified API could instead interpret
`solvesLimitEquation` as false. A source-faithful concrete semantics or
substantive noncircular adequacy hypotheses are required. Such a repair belongs
to the statement phase and must produce a new exact expression fingerprint and
refrozen downstream receipts before proof execution resumes.

The conditional theorem `root_of_existence_and_uniqueness` remains a valid
placeholder-free proof body, but it consumes the open existence and uniqueness
packages and therefore cannot close the root. No positive root body, proof
receipt, or frozen obligation was added or closed. The proof item remains
`[ ]`; the recorded vector remains `H1 / M4 / R3`, with `H1 / M5 / R3` only
the proposed diagnosis of the refutable encoding. Because the assigned phase
is incomplete, `.stage1-worker-selftest.json` is deliberately absent.

## Validation

All commands ran in this worker clone. The pre-existing automation-provided
`Formalizations/Lean/.lake` symlink was reused without update, build, clone,
fetch, network access, or dependency mutation. Lean outputs were restricted to
a fresh `/tmp` directory, and the shell trap removed that directory. The
worktree was already non-clean solely because of the untracked symlink, so this
is nonrelease evidence.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-1566` | 0 | Rank 182; planned lifecycle; theorem incomplete. |
| `timeout --foreground 300s python3 Stage1_Instances/THM-M-1566/check_statement.py` | 0 | Exact expression SHA-256 `70ee4869...473a`; all four structural mutations were distinguished. |
| `python3 Stage1_Instances/THM-M-1566/check_anchor_audit.py` | 0 | Four candidates, four search records, five Lean support probes, and the M4 boundary agreed. |
| `python3 Stage1_Instances/THM-M-1566/check_obligation_tree.py` | 0 | 15 obligations and 40 typed edges passed; denominator `7ae15c07...3fe640`; root remains open M4. |
| `(cd Formalizations/Lean && env -u LEAN_PATH LEAN_NUM_THREADS=1 timeout --foreground 60s lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e...`; the pinned project environment resolved without mutation. |
| `timeout --foreground 300s python3 Stage1_Instances/THM-M-1566/validate_obligation_tree.py` | 0 | Exact statement plus conditional composition elaborated; the assembler reported `[propext, Classical.choice, Quot.sound]`. |
| Isolated trust-zero `lake env lean` recipe below | 0 | Exact statement and refutation elaborated; the refutation reported `[propext, Classical.choice, Quot.sound]`; object hashes were `1e1c07...2793` and `611605...62f3`; the temporary directory was removed. |
| `rg -n '\b(sorry|admit|sorryAx|native_decide|implemented_by)\b|^[[:space:]]*(axiom|opaque|constant|unsafe|external)[[:space:]]' Stage1_Instances/THM-M-1566 --glob '*.lean'` | 1 | Expected no-match exit; no prohibited proof escape was found. |
| `python3 -m json.tool Stage1_Instances/THM-M-1566/proof-recheck-2026-07-15-head-f53223e67-slot35.json` | 0 | The structured current-base blocker is valid JSON. |
| Inline Python assertions over identity, source hashes, negative evidence, state, and changed paths | 0 | Base identity, source hashes, target hash, negative declaration, open-root flags, empty proof credit, `[ ]` state, and absent self-test agreed. |
| `git diff --no-index --check /dev/null` for each new artifact | 1, 1 | Expected added-file status with empty diagnostic output; no whitespace errors. |
| `git diff --check -- Stage1_Instances/THM-M-1566` | 0 | No whitespace errors in owned-path changes. |
| `test ! -e .stage1-worker-selftest.json` | 0 | The incomplete proof phase emitted no completion manifest. |

Exact narrow replay, run from the repository root:

```bash
set -euo pipefail
repo=$PWD
target=$repo/Stage1_Instances/THM-M-1566
lean_root=$repo/Formalizations/Lean
tmp=$(mktemp -d /tmp/thm-m-1566-proof-f53223e67-slot35.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
cp "$target/Statement.lean" "$tmp/Statement.lean"
cp "$target/ProofCountermodel.lean" "$tmp/ProofCountermodel.lean"
lean=$(cd "$lean_root" && lake env which lean)
lean_path=$(cd "$lean_root" && lake env printenv LEAN_PATH)
LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" timeout --foreground 300s \
  "$lean" --trust=0 -t0 -R "$tmp" -o "$tmp/Statement.olean" \
  "$tmp/Statement.lean"
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" timeout --foreground 300s \
  "$lean" --trust=0 -t0 -R "$tmp" -o "$tmp/ProofCountermodel.olean" \
  "$tmp/ProofCountermodel.lean"
sha256sum "$tmp/Statement.olean" "$tmp/ProofCountermodel.olean"
```

## Status Boundary

The first failed gate is positive exact-root kernel closure at `M1566-ROOT`,
originating in the unconstrained `M1566-S-INTERFACE` and directly refuting
`M1566-T-EXISTENCE`. The actionable cut set is statement/interface, existence,
and root. The proof item remains `[ ]`, `root_closed=false`,
`audit_complete=false`, and `theorem_complete=false`; there is no accepted
receipt, provisional completion, or `.stage1-worker-selftest.json`.

Resume only after an authorized statement revision replaces the universal
unconstrained API with a fixed source-faithful implementation or substantive
noncircular adequacy hypotheses. It must receive a new exact expression
fingerprint and refrozen anchor/obligation receipts before proof execution.
