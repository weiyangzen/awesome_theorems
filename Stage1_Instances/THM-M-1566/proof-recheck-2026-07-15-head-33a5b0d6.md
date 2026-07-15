# THM-M-1566 proof-phase recheck at current base

Item: `S56-M-1566-PROOF`

Recorded at: `2026-07-15T13:03:51+08:00`

Base revision: `33a5b0d654c92a894e155f5385edaae684091bb0`

Base tree: `74ed89524afb3c118e31a7fce9b5763fee26b180`

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

The project-root Lake environment was not usable during this run because the
automation-provided, shared `.lake/packages/flt-regular` checkout has no
resolvable `HEAD`. The manifest-pinned object remains present, but this worker
did not repair, fetch, update, or otherwise mutate `.lake`. The narrow kernel
replay used `lake env lean` from the existing pinned mathlib subworkspace, with
an explicit `LEAN_PATH` composed solely from existing pinned package build
artifacts. This is current nonrelease blocker evidence, not a hermetic release
replay.

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
| `(cd Formalizations/Lean && env -u LEAN_PATH LEAN_NUM_THREADS=1 timeout --foreground 60s lake env lean --version)` | 1 | Lake reported that `.lake/packages/flt-regular` could not resolve `HEAD`; no dependency mutation was attempted. |
| `python3 Stage1_Instances/THM-M-1566/check_statement.py` and `python3 Stage1_Instances/THM-M-1566/validate_obligation_tree.py` | not credited | Their Lake-backed elaborations were not used as current evidence because the shared Lake environment was unusable; the direct replay below covers the exact statement and countermodel. |
| Pinned mathlib-subworkspace `lake env lean` trust-zero replay below | 0 | The exact statement and refutation elaborated; object hashes were `1e1c07...2793` and `611605...62f3`; the temporary directory was removed. |
| `rg -n '\\b(sorry\|admit\|sorryAx\|native_decide\|implemented_by)\\b\|^[[:space:]]*(axiom\|opaque\|constant\|unsafe\|external)[[:space:]]' Stage1_Instances/THM-M-1566 --glob '*.lean'` | 1 | Expected no-match exit; no prohibited proof escape was found. |
| `git diff --check -- Stage1_Instances/THM-M-1566` | 0 | No whitespace errors in tracked owned-path changes before these two new artifacts. |
| `test ! -e .stage1-worker-selftest.json` | 0 | The incomplete proof phase emitted no completion manifest. |

Exact narrow replay, run from the repository root:

```bash
set -euo pipefail
repo=$PWD
tmp=$(mktemp -d /tmp/thm-m-1566-proof-33a5b0d6.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
cp "$repo/Stage1_Instances/THM-M-1566/Statement.lean" "$tmp/Statement.lean"
cp "$repo/Stage1_Instances/THM-M-1566/ProofCountermodel.lean" "$tmp/ProofCountermodel.lean"
mathlib="$repo/Formalizations/Lean/.lake/packages/mathlib"
extra="$repo/Formalizations/Lean/.lake/packages/Cli/.lake/build/lib/lean:$repo/Formalizations/Lean/.lake/packages/batteries/.lake/build/lib/lean:$repo/Formalizations/Lean/.lake/packages/Qq/.lake/build/lib/lean:$repo/Formalizations/Lean/.lake/packages/aesop/.lake/build/lib/lean:$repo/Formalizations/Lean/.lake/packages/proofwidgets/.lake/build/lib/lean:$repo/Formalizations/Lean/.lake/packages/importGraph/.lake/build/lib/lean:$repo/Formalizations/Lean/.lake/packages/LeanSearchClient/.lake/build/lib/lean:$repo/Formalizations/Lean/.lake/packages/plausible/.lake/build/lib/lean"
(cd "$mathlib" && LEAN_NUM_THREADS=1 LEAN_PATH="$extra" \
  timeout --foreground 300s lake env lean --trust=0 -t0 -R "$tmp" \
  -o "$tmp/Statement.olean" "$tmp/Statement.lean")
(cd "$mathlib" && LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$extra" \
  timeout --foreground 300s lake env lean --trust=0 -t0 -R "$tmp" \
  -o "$tmp/ProofCountermodel.olean" "$tmp/ProofCountermodel.lean")
sha256sum "$tmp/Statement.olean" "$tmp/ProofCountermodel.olean"
```

## Status boundary

The proposed vector is `H1 / M5 / R3`; no authoritative state was changed.
The first failed gate is positive exact-root kernel closure at `M1566-ROOT`,
originating in the unconstrained `M1566-S-INTERFACE` and directly refuting
`M1566-T-EXISTENCE`. The actionable cut set is the statement/interface,
existence, and root. The proof item remains `[ ]`, `root_closed=false`,
`audit_complete=false`, and `theorem_complete=false`; there is no accepted
receipt, provisional completion, or `.stage1-worker-selftest.json`.
