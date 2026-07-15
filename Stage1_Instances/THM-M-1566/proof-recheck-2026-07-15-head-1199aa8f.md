# THM-M-1566 proof-phase recheck at current base

Item: `S56-M-1566-PROOF`

Recorded at: `2026-07-15T12:20:22+08:00`

Base revision: `1199aa8f32fcf4e871ea300f8a3c0109ae24b664`

Base tree: `e1e9e8cb1d023d46eaa4a550e9d5a4f5358d49ea`

## Verdict

`blocked`. No consistent positive proof body can inhabit the exact frozen Lean
target. The unchanged, placeholder-free declaration

```text
Stage1Instances.THMM1566.not_GIPCorollary59Target :
  Not (Stage1Instances.THMM1566.GIPCorollary59Target.{0})
```

was replayed at trust level zero against the existing pinned Lean and mathlib
objects. It uses `Omega := Unit`, the Dirac probability measure, `Unit` for all
non-solution carriers, and `Empty` for `Solution`. The numerical premises are
inhabited at `alpha = beta = 3/4`; applying the claimed target produces an
inhabitant of `Empty`.

This refutes the frozen abstract encoding, not Corollary 5.9 in the cited GIP
paper. Merely requiring `Nonempty api.Solution` would also be insufficient:
the universally quantified API could instead set `solvesLimitEquation` to
`False`. Repair requires concrete source-faithful semantics or substantive,
noncircular adequacy hypotheses, followed by an authorized statement refreeze
and refreshed downstream receipts.

The canonical Lake environment was not usable during this run because the
automation-provided, shared `.lake/packages/flt-regular` checkout had its HEAD
at `refs/heads/.invalid`. The manifest-pinned object remains present, but this
worker did not repair, fetch, update, or otherwise mutate `.lake`. The narrow
kernel replay instead invoked the pinned Lean 4.29.0 binary directly with an
explicit `LEAN_PATH` composed solely from the existing pinned build artifacts.
This current kernel result is valid nonrelease blocker evidence; it is not a
hermetic release replay.

## Validation

All commands ran in this worker clone. The pre-existing untracked `.lake`
symlink was treated as read-only input.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required. |
| `python3 scripts/stage1_target.py show THM-M-1566` | 0 | Rank 182; planned lifecycle; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1566/check_anchor_audit.py` | 0 | Four candidates, four searches, five Lean probes, and the M4 boundary agreed. |
| `python3 Stage1_Instances/THM-M-1566/check_obligation_tree.py` | 0 | 15 obligations and 40 typed edges passed; root remains open M4. |
| `(cd Formalizations/Lean && env -u LEAN_PATH LEAN_NUM_THREADS=1 timeout --foreground 60s lake env lean --version)` | 1 | Lake reported that `.lake/packages/flt-regular` could not resolve HEAD; no dependency mutation was attempted. |
| `python3 Stage1_Instances/THM-M-1566/check_statement.py` and `python3 Stage1_Instances/THM-M-1566/validate_obligation_tree.py` | not credited | Their Lake-backed elaborations were not used as current evidence because the shared Lake environment was unusable; the direct replay below covers the exact statement and countermodel. |
| Direct pinned Lean trust-zero replay below | 0 | The exact statement and refutation elaborated; object hashes were `1e1c07...2793` and `611605...62f3`; the temporary directory was removed. |
| `rg -n '\b(sorry\|admit\|sorryAx\|native_decide\|implemented_by)\b\|^[[:space:]]*(axiom\|opaque\|constant\|unsafe\|external)[[:space:]]' Stage1_Instances/THM-M-1566 --glob '*.lean'` | 1 | Expected no-match exit; no prohibited proof escape was found. |
| `python3 -m json.tool Stage1_Instances/THM-M-1566/proof-recheck-2026-07-15-head-1199aa8f.json` | 0 | The paired blocker is valid JSON. |
| Inline Python assertions over the paired JSON and eight source hashes | 0 | Identity, hashes, open-root flags, empty proof credit, `[ ]` state, and absent self-test agreed. |
| `git diff --no-index --check /dev/null <new-artifact>` for each artifact | 1, 1 | Expected added-file status with no diagnostic output; no whitespace error. |
| `git diff --check -- Stage1_Instances/THM-M-1566` | 0 | No whitespace errors in tracked owned-path changes. |
| `test ! -e .stage1-worker-selftest.json` | 0 | The incomplete proof phase emitted no completion manifest. |

Exact direct replay, run from the repository root:

```bash
set -euo pipefail
repo=$PWD
tmp=$(mktemp -d /tmp/thm-m-1566-proof-recheck-1199aa8f-direct.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
cp "$repo/Stage1_Instances/THM-M-1566/Statement.lean" "$tmp/Statement.lean"
cp "$repo/Stage1_Instances/THM-M-1566/ProofCountermodel.lean" "$tmp/ProofCountermodel.lean"
lean="$HOME/.elan/toolchains/leanprover--lean4---v4.29.0/bin/lean"
lib="$repo/Formalizations/Lean/.lake/packages"
lean_path="$lib/batteries/.lake/build/lib/lean:$lib/Qq/.lake/build/lib/lean:$lib/aesop/.lake/build/lib/lean:$lib/proofwidgets/.lake/build/lib/lean:$lib/importGraph/.lake/build/lib/lean:$lib/LeanSearchClient/.lake/build/lib/lean:$lib/plausible/.lake/build/lib/lean:$lib/mathlib/.lake/build/lib/lean:$repo/Formalizations/Lean/.lake/build/lib/lean:$HOME/.elan/toolchains/leanprover--lean4---v4.29.0/lib/lean"
cd "$tmp"
LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" timeout --foreground 300s \
  "$lean" --trust=0 -t0 -R "$tmp" -o Statement.olean Statement.lean
LEAN_NUM_THREADS=1 LEAN_PATH=.:"$lean_path" timeout --foreground 300s \
  "$lean" --trust=0 -t0 -R "$tmp" -o ProofCountermodel.olean ProofCountermodel.lean
sha256sum Statement.olean ProofCountermodel.olean
```

## Status boundary

The proposed vector is `H1 / M5 / R3`; no authoritative state was changed.
The first failed gate is positive exact-root kernel closure at `M1566-ROOT`,
originating in the unconstrained `M1566-S-INTERFACE` and directly refuting
`M1566-T-EXISTENCE`. The actionable cut set is the statement/interface,
existence, and root. The proof item remains `[ ]`, `root_closed=false`,
`audit_complete=false`, and `theorem_complete=false`; there is no accepted
receipt, provisional completion, or `.stage1-worker-selftest.json`.
