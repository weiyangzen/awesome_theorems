# THM-M-1234 proof-phase recheck at `c74f595e` (slot26)

Item: `S56-M-1234-PROOF`

Date: `2026-07-15` (`Asia/Shanghai`)

Base revision: `c74f595e99fe574f4619307c859ec20986bb2297`

Base tree: `b27451453ff7d1e87d296c6634bd270799c666d9`

## Verdict

`blocked`. The exact universal declaration
`Stage1Rev56.THMM1234.Statement` still has no repo-local or pinned proof body.
This recheck adds no proof body and closes no obligation. The proof item remains
`[ ]`, the lifecycle remains `planned`, and the root vector remains
`[H1, M3, R3] -> [H1, M3, R3]`. No proof, validation, release, audit-completion,
theorem-completion, or master-acceptance receipt is claimed.

The existing kernel-checked bodies are narrower than the target. The root
assembler consumes both open package premises. Constant-in-time initial fields
inhabit the under-specified `CandidateConstructionPackage`, but this body does
not consume the frozen approximation, energy, or compactness children. The
zero-fields construction proves only the zero-data boundary case.

The frozen `EquationAndTraceClosurePackage` is not a suitable replacement for
the missing analysis: it quantifies over every `CandidateFields` witness rather
than the candidate selected by a construction. The checked diagnostic applies
it to unrelated zero fields and derives that every admissible initial velocity
and vorticity test pairing must vanish. No honest Yudovich proof can be credited
through that interface without a master-owned registry revision.

## Failed Gates

The immediate dependency is not master accepted:
`S56-M-1234-OBLIGATION_TREE` is `[_]`, not `[x]`. Independently, the first
expanded proof gap is `M1234-A-APPROX`: the repository and pinned dependency
closure contain no construction of global smooth Euler approximants for every
frozen `InitialData` witness. Uniform energy and bounded-vorticity estimates,
nonlinear-compatible compactness, structural preservation, linear and
quadratic momentum limit passage, and the one-sided initial trace remain open.

The direct frozen root cut remains `M1234-A-STRUCTURE` plus
`M1234-E-CLOSURE`. A truthful retry requires an accepted registry version 2
whose construction consumes its analytic children and whose closure is linked
to the specifically constructed candidate. The analytic leaves must then be
split and implemented. An immutable exact external Lean 4 terminal body would
be an alternative only after exact-type, provenance, trust, and composition
checks.

There are eleven integrated `stage1-proof-blocker` JSON packets before this
one (plus one structured proof-attempt packet), while the authoritative proof
item still records `attempts: 0` and
`children: []`. Blueprint section 10.2 requires the master/scheduler to
reconcile the attempt count and split this repeatedly unresolved oversized
item. This worker did not edit the DAG, generated blueprint, frozen registry,
typed graphs, or any dependency.

## Validation

All checks used the automation-provided pinned artifacts read-only. No `lake
update`, `lake build`, dependency clone/fetch, network access, or `.lake`
mutation was performed. The untracked `.lake` symlink makes the run nonrelease
evidence. Temporary source copies and Lean objects were removed after replay.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required`. |
| `python3 scripts/stage1_target.py show THM-M-1234` | 0 | Rank 158; planned; legacy artifacts unaccepted; theorem incomplete. |
| `git status --short` | 0 | At preflight the only entry was the pre-existing untracked `Formalizations/Lean/.lake` symlink; the owned path was clean. |
| `python3 Stage1_Instances/THM-M-1234/check_obligation_tree.py` | 0 | 14 obligations and 28 typed edges passed; denominator `cfa0a02c68993c8b3eefc0edfe7d3d7bd20e2b58d140f47a1f5444a8ba734c5d`; root open at M3. |
| `cd Formalizations/Lean && lake env lean --version` | 1 | Lake could not resolve `HEAD` in the pinned `flt-regular` checkout, whose HEAD is `refs/heads/.invalid`. The present required commit object exists, but the checkout has no resolvable HEAD; it was not repaired or fetched. |
| Isolated trust-zero six-module replay below | 0 | All six modules elaborated with the exact pinned Lean 4.29 binary and existing compiled package paths. Printed declarations reported only `propext`, `Classical.choice`, and `Quot.sound`. |
| Prohibited-device scan over owned `*.lean` | 1 | Expected no-match exit with empty output: no `sorry`, `admit`, declared axiom, unsafe/opaque/extern escape, `sorryAx`, `implemented_by`, or `native_decide` was found. |
| Exact-topic scan over pinned mathlib `*.lean` | 1 | Expected no-match exit with empty output: no Yudovich/Yudovitch, incompressible-Euler, or bounded-vorticity theorem was found. |
| `python3 -m json.tool ...slot26.json >/dev/null && jq empty Stage1_Instances/THM-M-1234/*.json` | 0 | The new packet and every owned structured JSON artifact parsed. |
| `git diff --check -- Stage1_Instances/THM-M-1234 .stage1-worker-selftest.json` | 0 | No whitespace error was reported. |
| `test ! -e .stage1-worker-selftest.json` | 0 | The self-test manifest is absent as required for an incomplete proof phase. |

The required `lake env` validation surface is blocked by the malformed pinned
artifact. To obtain the smallest available real kernel check without changing
it, the replay used the exact binary named by `lean-toolchain` and only existing
compiled package paths:

```bash
set -euo pipefail
root=$PWD
tmp=$(mktemp -d "$root/.thm-m-1234-proof-c74f595e-slot26.XXXXXX")
trap 'rm -rf "$tmp"' EXIT
cp Stage1_Instances/THM-M-1234/{Statement,AnchorAudit,ObligationTree,ConstructionProof,Proof,ClosurePackageDiagnostic}.lean "$tmp"/
lean=/home/sansha-2/.elan/toolchains/leanprover--lean4---v4.29.0/bin/lean
lean_path="$root/Formalizations/Lean/.lake/packages/mathlib/.lake/build/lib/lean:$root/Formalizations/Lean/.lake/packages/batteries/.lake/build/lib/lean:$root/Formalizations/Lean/.lake/packages/Qq/.lake/build/lib/lean:$root/Formalizations/Lean/.lake/packages/aesop/.lake/build/lib/lean:$root/Formalizations/Lean/.lake/packages/proofwidgets/.lake/build/lib/lean:$root/Formalizations/Lean/.lake/packages/LeanSearchClient/.lake/build/lib/lean:$root/Formalizations/Lean/.lake/packages/importGraph/.lake/build/lib/lean:$root/Formalizations/Lean/.lake/packages/plausible/.lake/build/lib/lean:$root/Formalizations/Lean/.lake/packages/Cli/.lake/build/lib/lean"
export LEAN_NUM_THREADS=1
LEAN_PATH="$lean_path" timeout 600 "$lean" --trust=0 -t0 -o "$tmp/Statement.olean" "$tmp/Statement.lean"
LEAN_PATH="$tmp:$lean_path" timeout 600 "$lean" --trust=0 -t0 "$tmp/AnchorAudit.lean"
LEAN_PATH="$tmp:$lean_path" timeout 600 "$lean" --trust=0 -t0 -o "$tmp/ObligationTree.olean" "$tmp/ObligationTree.lean"
LEAN_PATH="$tmp:$lean_path" timeout 600 "$lean" --trust=0 -t0 "$tmp/ConstructionProof.lean"
LEAN_PATH="$tmp:$lean_path" timeout 600 "$lean" --trust=0 -t0 "$tmp/Proof.lean"
LEAN_PATH="$tmp:$lean_path" timeout 600 "$lean" --trust=0 -t0 "$tmp/ClosurePackageDiagnostic.lean"
```

Lean was version `4.29.0`, commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`; its binary SHA-256 was
`3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf`.
The explicit `LEAN_PATH` SHA-256 was
`6e6aebd00f5a3d61f32363edc90b976c93b4f1937054ea37c11a82b6c9e490c4`.
This invocation produced `Statement.olean` SHA-256
`1f7bfefd198f8873ca69f11ca44bf9f55e060b64bb18801ac992c06f183be746`
and `ObligationTree.olean` SHA-256
`321dc694573cdbd1a0ff8b62f71a691b5b6caa3cc52445ae3b41f1b6e676115c`.
The paired JSON packet binds source, environment, and output hashes.

## Status Boundary

This is a current-base, target-scoped blocker handoff, not a proof receipt. It
does not satisfy `S56-M-1234-PROOF`, propose `[_]`, or support any later phase.
Because the assigned universal proof phase is not genuinely self-tested as
complete, `.stage1-worker-selftest.json` is deliberately absent.
