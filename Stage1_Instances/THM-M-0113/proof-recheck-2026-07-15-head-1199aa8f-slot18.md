# THM-M-0113 proof phase blocked at `1199aa8f` (`slot18`)

Item: `S56-M-0113-PROOF`

Intent: `prove`

Recheck date: `2026-07-15` (`Asia/Shanghai`)

Base revision: `1199aa8f32fcf4e871ea300f8a3c0109ae24b664`

Base tree: `e1e9e8cb1d023d46eaa4a550e9d5a4f5358d49ea`

## Verdict

`blocked`. No legal positive proof body can inhabit the exact frozen target.
The existing placeholder-free declaration

```text
Stage1Instances.THMM0113.not_hodgeDecompositionTarget :
  Not Stage1Instances.THMM0113.HodgeDecompositionTarget.{0, 0, 0, 0}
```

was re-elaborated at trust level zero against a fresh `Statement.olean`. The
statement's `HodgeData.isKahler` field is an unconstrained proposition and has
no relationship to the independently chosen `cohomology` family or
`hodgePiece` submodules. The countermodel takes the zero-dimensional compact
complex manifold `Fin 0 -> Complex`, sets `isKahler := True`, interprets every
cohomology space as `Complex`, and makes every Hodge piece bottom. Complex
conjugation supplies all declared algebraic laws. In degree zero, the target
would force the supremum of bottom submodules to be top and hence force
`1 = 0`.

This refutes the frozen Lean encoding, not the mathematical Hodge
decomposition theorem. Repairing or narrowing the target inside this proof
item would be a forbidden theorem substitution. The positive obligation
registry therefore cannot receive closure credit from the negative body.

The assigned item remains `[ ]`. No proof receipt, state transition, audit
completion, theorem completion, validation completion, release, or master
acceptance is claimed. Because the requested positive proof phase is not
genuinely complete, `.stage1-worker-selftest.json` is deliberately absent.

## Failed Gate And Retry

The first semantic theorem gate is
`S56-5.1-EXACT-TARGET-CONSISTENCY / M0113-S-DATA`. Replace the disconnected
`isKahler` proposition and arbitrary cohomology/Hodge-piece fields with native
definitions tied to the compact complex manifold, or add noncircular
law-bearing hypotheses sufficient to derive the intended conclusion. Then
publish a new statement fingerprint and freshly freeze and accept the
statement, anchor audit, obligation registry, and typed graphs before resuming
positive proof work. Alternatively, redirect the item explicitly to the
checked counterexample target.

The frozen positive graph still records the downstream analytic cut set
`M0113-A-DR`, `M0113-A-DOL`, `M0113-A-ELL`, `M0113-K-ID`, and
`M0113-C-CHAIN`, but the earlier statement defect blocks entry to that proof
architecture. This recheck proposes only M5 backend-target blocker evidence;
it does not change the H4 status of the intended mathematical theorem or any
predecessor state. The prerequisite obligation-tree item also remains
provisional rather than master-accepted.

This target already had 20 tracked Markdown rechecks and 20 structured
rechecks before this run. Those files demonstrate repeated scheduling but are
not an authoritative execution-tick ledger; the DAG still reports attempts
`0` and no children. The authoritative counter therefore needs reconciliation.
Regardless of the exact tick count, repeated execution of the unchanged
positive root cannot repair a refuted statement. The master should route
statement repair through the prerequisite chain, or redirect the task, rather
than schedule another identical root proof attempt. This worker did not edit
the authoritative DAG or checklist.

## Validation

All commands ran in this automation clone. The automation-provided `.lake`
symlink was treated as read-only; no `lake update`, `lake build`, dependency
clone/fetch, checkout, repair, or network action was performed by this worker.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0113` | 0 | Rank 25; lifecycle `planned`; baseline `L0/rework_required`; legacy artifacts unaccepted; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0113/check_anchor_audit.py` | 0 | Target boundary, four candidate rows, 12 Lean probes, and pinned mathlib revision agree. |
| `python3 Stage1_Instances/THM-M-0113/check_obligation_tree.py` | 0 | `PASS`: 26 obligations and 49 typed edges; denominator `e509c192...cbd5`; the frozen positive root remains M4. |
| `cd Formalizations/Lean && timeout 30 lake env lean --version` | 1 | The shared `flt-regular` checkout has `HEAD` at `refs/heads/.invalid`, so Lake stopped before dispatching Lean. No fetch or repair was attempted. |
| Direct read-only pinned Lean `--trust=0 -t0` replay of `Statement.lean` and `Proof.lean` with temporary output | 0 | Both modules elaborated; the countermodel exact type was printed; Lean reported axioms exactly `[propext, Classical.choice, Quot.sound]`. Kernel-output SHA-256: `539fbb6d...331b1f9`; `Statement.olean` SHA-256: `94fe8a21...975e0`. |
| Scoped prohibited-construct scan over owned `*.lean` | 1 (expected) | No `sorry`, `admit`, `sorryAx`, `native_decide`, bodyless declaration, unsafe declaration, `implemented_by`, or `extern` declaration matched. |
| Shared dependency revision/artifact checks | mixed, recorded | mathlib is at pinned revision `8a178386...`; `flt-regular` cannot resolve `HEAD`, although the manifest-pinned commit object `56161b6e...` is present. |
| Frozen structured-input JSON checks | 0 | `obligation-registry.json`, `typed-graphs.json`, and `anchor-audit.json` parse successfully. |
| Shared mathlib and Batteries status checks | 0 | mathlib is clean at `8a178386.../bdc39a31...`; Batteries is clean at `756e3321.../02666252...`. |
| JSON parse and current-base invariant assertions | 0 | Item, base, hashes, blocked/open state, countermodel, empty receipt lists, changed paths, and deliberate self-test absence agree. |
| New-file and tracked-diff whitespace checks | 0 | No whitespace diagnostics. |
| `test ! -e .stage1-worker-selftest.json` | 0 | The incomplete proof phase emitted no worker completion manifest. |

The successful narrow fallback replay bypassed only Lake's broken dependency
checkout discovery, not Lean or the kernel. It copied the two target files to
a fresh `/tmp` directory, invoked the toolchain-pinned Lean 4.29.0 binary with
`--trust=0 -t0`, and assembled `LEAN_PATH` read-only from the existing compiled
package directories. All temporary files were removed afterward. This is
nonrelease blocker evidence; it does not turn the failed required `lake env
lean` entry point into a passing gate.

The exact diagnostic fallback, run from `Formalizations/Lean`, used:

```bash
set -euo pipefail
tmp=$(mktemp -d /tmp/thm-m-0113-manual-lean.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
cp ../../Stage1_Instances/THM-M-0113/Statement.lean "$tmp/Statement.lean"
cp ../../Stage1_Instances/THM-M-0113/Proof.lean "$tmp/Proof.lean"
root="$PWD"
path="$root/.lake/packages/batteries/.lake/build/lib/lean:$root/.lake/packages/Qq/.lake/build/lib/lean:$root/.lake/packages/aesop/.lake/build/lib/lean:$root/.lake/packages/proofwidgets/.lake/build/lib/lean:$root/.lake/packages/LeanSearchClient/.lake/build/lib/lean:$root/.lake/packages/plausible/.lake/build/lib/lean:$root/.lake/packages/importGraph/.lake/build/lib/lean:$root/.lake/packages/mathlib/.lake/build/lib/lean:$root/.lake/build/lib/lean"
lean_bin=$(elan which lean)
LEAN_NUM_THREADS=1 LEAN_PATH="$path" timeout --foreground 600 \
  "$lean_bin" --trust=0 -t0 --root="$tmp" -o "$tmp/Statement.olean" \
  "$tmp/Statement.lean" >"$tmp/statement-output.txt" 2>&1
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$path" timeout --foreground 600 \
  "$lean_bin" --trust=0 -t0 --root="$tmp" "$tmp/Proof.lean" \
  >"$tmp/proof-output.txt" 2>&1
cat "$tmp/statement-output.txt" "$tmp/proof-output.txt" \
  >"$tmp/kernel-output.txt"
cat "$tmp/kernel-output.txt"
sha256sum "$tmp/kernel-output.txt" "$tmp/Statement.olean"
```

This recorded command is a diagnostic replay, not a content-addressed
structured recipe or completion receipt.

The checked input SHA-256 values are:

| Input | SHA-256 |
|---|---|
| `Statement.lean` | `73010040e7a16c02d00bfa95db270e2370440f433e8c3519e5e2ab429cd236dd` |
| `Proof.lean` | `b05f2ef3eef236e026930097803c614d53eeaba65d5fa936b0293a7c4879ec6f` |
| `ObligationTree.lean` | `c9fe3593539b1a3d221496ad45c3b5a9cfcd1355b3875f7b42d4012337273a95` |
| `obligation-registry.json` | `c8f592dd2961e08782a241355e0eaf2f1d6841b8e66b325bab5d07c936847f2d` |
| `typed-graphs.json` | `31b91ed2b0c42702819148e6ab02e222e06f801bd0e1cc9e81788d26f2606e34` |
| `anchor-audit.json` | `96d93459b27f3a95357e041e0a9cf589d849ef5066894551e646b5dbb5027795` |
| `Formalizations/Lean/lake-manifest.json` | `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81` |
| `Formalizations/Lean/lean-toolchain` | `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2` |

## Status Boundary

This current-base artifact is nonrelease blocker evidence, not a proof
receipt. It does not satisfy `S56-M-0113-PROOF`, proposes no provisional or
accepted state, and supports neither audit nor theorem completion. The next
legal work is upstream statement repair or explicit task redirection, plus
canonical restoration of the already-pinned `flt-regular` artifact before a
Lake-derived recheck.
