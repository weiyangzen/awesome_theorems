# THM-M-1566 proof-phase recheck at current base

Item: `S56-M-1566-PROOF`

Recorded at: `2026-07-15T13:45:02+08:00`

Base revision: `9bce865a14bcc270344ea909d6936c6ea22aa1c2`

Base tree: `523a9471aac257c4cf54acceee07172fab22f5b4`

## Verdict

`blocked`. No consistent positive proof body can inhabit the exact frozen Lean
target. The unchanged, placeholder-free declaration

```text
Stage1Instances.THMM1566.not_GIPCorollary59Target :
  Not (Stage1Instances.THMM1566.GIPCorollary59Target.{0})
```

was replayed at trust level zero against existing pinned Lean and mathlib
objects. The countermodel sets `Omega := Unit`, uses the Dirac probability
measure, takes every non-solution carrier to be `Unit`, and takes
`Solution := Empty`. The numerical premises are inhabited at
`alpha = beta = 3/4`. Applying the positive target therefore supplies an
inhabitant of `Empty`.

This refutes the frozen abstract encoding, not Corollary 5.9 in the cited
Gubinelli--Imkeller--Perkowski paper. Merely requiring
`Nonempty api.Solution` would not repair the encoding: the universally
quantified API can instead make `solvesLimitEquation` false. A source-faithful
concrete semantics or substantive noncircular adequacy hypotheses are needed.
That repair belongs to the statement phase and requires new fingerprints and
refrozen downstream receipts before proof work can resume.

The project-root Lake preflight timed out without output after 60 seconds.
Separate read-only inspection found that the automation-provided shared
`.lake/packages/flt-regular` checkout has no resolvable `HEAD`. This worker did
not repair, fetch, update, build, or otherwise mutate `.lake`. The narrow
kernel replay used `lake env lean` from the existing pinned mathlib
subworkspace, with `LEAN_PATH` composed only from existing pinned package
objects. This is current nonrelease blocker evidence, not a hermetic release
replay.

## Validation

All commands ran in this worker clone. The pre-existing untracked `.lake`
symlink was treated as read-only input.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required. |
| `python3 scripts/stage1_target.py show THM-M-1566` | 0 | Rank 182; planned lifecycle; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1566/check_anchor_audit.py` | 0 | Four candidates, four search records, five Lean support probes, and the M4 boundary agreed. |
| `python3 Stage1_Instances/THM-M-1566/check_obligation_tree.py` | 0 | 15 obligations and 40 typed edges passed; denominator `7ae15c07...3fe640`; root remains open M4. |
| `(cd Formalizations/Lean && env -u LEAN_PATH LEAN_NUM_THREADS=1 timeout --foreground 60s lake env lean --version)` | 124 | The project-root preflight timed out with no output; no dependency mutation was attempted. |
| `git -C Formalizations/Lean/.lake/packages/flt-regular rev-parse HEAD` | 128 | The shared manifest checkout has no resolvable `HEAD`. |
| Pinned mathlib-subworkspace `lake env lean` trust-zero replay below | 0 | The exact statement and refutation elaborated. `not_GIPCorollary59Target` reported `[propext, Classical.choice, Quot.sound]`; object hashes were `1e1c07...2793` and `611605...62f3`; the temporary directory was removed. |
| `rg -n '\b(sorry\|admit\|sorryAx\|native_decide\|implemented_by)\b\|^[[:space:]]*(axiom\|opaque\|constant\|unsafe\|external)[[:space:]]' Stage1_Instances/THM-M-1566 --glob '*.lean'` | 1 | Expected no-match exit; no prohibited proof escape was found. |
| `python3 -m json.tool Stage1_Instances/THM-M-1566/proof-recheck-2026-07-15-head-9bce865a-slot31.json` | 0 | The structured current-base blocker is valid JSON. |
| Inline Python assertions over identity, source hashes, negative evidence, state, and changed paths | 0 | Base identity, hashes, open-root flags, empty proof credit, `[ ]` state, and absent self-test agreed. |
| `git diff --no-index --check /dev/null` for each new artifact | 1, 1 | Expected added-file status with empty diagnostic output; no whitespace errors. |
| `git diff --check -- Stage1_Instances/THM-M-1566` | 0 | No whitespace errors in tracked owned-path changes. |
| `test ! -e .stage1-worker-selftest.json` | 0 | The incomplete proof phase emitted no completion manifest. |

Exact narrow replay, run from the repository root:

```bash
set -euo pipefail
repo=$PWD
tmp=$(mktemp -d /tmp/thm-m-1566-proof-9bce865a-slot31.XXXXXX)
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
