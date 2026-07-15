# THM-M-0113 proof-phase recheck at `443b8bbc`

Item: `S56-M-0113-PROOF`

Recheck date: `2026-07-15` (`Asia/Shanghai`)

Base revision: `443b8bbc23bf35a1e7a4bb7b3183073f76bbee2b`

Base tree: `c5771c47c12b80aba613e6d844570f83b39ded6d`

## Verdict

`blocked`. No legal positive proof body can inhabit the exact frozen target.
The existing placeholder-free declaration

```text
Stage1Instances.THMM0113.not_hodgeDecompositionTarget :
  Not Stage1Instances.THMM0113.HodgeDecompositionTarget.{0, 0, 0, 0}
```

kernel-checks at trust level zero against a freshly elaborated
`Statement.olean`.

The statement's `HodgeData.isKahler` field is an unconstrained proposition and
does not relate the geometric hypothesis to the independently chosen
`cohomology` family or `hodgePiece` submodules. The countermodel takes the
zero-dimensional compact complex manifold `Fin 0 -> Complex`, sets
`isKahler := True`, interprets every cohomology space as `Complex`, and makes
every Hodge piece bottom. Complex conjugation supplies the additive,
conjugate-linear, and involutive laws. In degree zero, the target would force
the supremum of bottom submodules to be top and hence force `1 = 0`.

This refutes the frozen Lean encoding, not the mathematical Hodge
decomposition theorem. Repairing, strengthening, or narrowing the target in
this proof item would be a forbidden theorem substitution. The existing
positive obligation registry therefore cannot receive closure credit from the
negative declaration.

The assigned item remains `[ ]`. No positive proof receipt, state transition,
audit completion, theorem completion, validation completion, release, or
master-acceptance claim is made. No `.stage1-worker-selftest.json` is written
because the requested proof phase is not genuinely complete.

## Failed Gate And Retry

The first failed gate is
`S56-5.1-EXACT-TARGET-CONSISTENCY / M0113-S-DATA`. Replace the disconnected
`isKahler` proposition and arbitrary cohomology/Hodge-piece fields with native
definitions tied to the compact complex manifold, or add noncircular
law-bearing hypotheses sufficient to derive the intended conclusion. Then
publish a new statement fingerprint and freshly freeze and accept the
statement, anchor audit, obligation registry, and typed graphs before resuming
positive proof work. Alternatively, redirect the item explicitly to the
checked counterexample target.

The frozen positive graph still records the analytic cut set `M0113-A-DR`,
`M0113-A-DOL`, `M0113-A-ELL`, `M0113-K-ID`, and `M0113-C-CHAIN`, but the
earlier statement defect `M0113-S-DATA` blocks entry to that proof
architecture. The prior registry projection remains open at M4; this recheck
proposes H5/M5 blocker evidence without changing predecessor state.

The prerequisite `S56-M-0113-OBLIGATION_TREE` remains provisional `[_]`, not
master-accepted, so dependency-legal proof acceptance is independently
unavailable. The scheduler still records `attempts: 0` despite repeated
blocker rechecks. Another unchanged-target proof dispatch cannot produce
positive proof progress; integration must repair or explicitly redirect the
statement chain.

## Validation

The target checks used the existing canonical pinned Lake artifacts read
only. No `lake update`, `lake build`, dependency clone/fetch, network action,
or intentional `.lake` write was performed. Lean output was confined to a
fresh directory under `/tmp` and removed after validation. The pre-existing
untracked `.lake` symlink makes this nonrelease evidence.

The root `lake env` preflight failed because the canonical `flt-regular`
checkout currently has no resolvable `HEAD`. In accordance with the
no-fetch/no-repair rule, this run did not alter that dependency. The narrow
kernel check instead invoked `lake env lean` from the fresh `/tmp` validation
directory, with `ELAN_TOOLCHAIN` selecting the pinned toolchain and
`LEAN_PATH` containing only pre-existing Lake build directories.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0113` | 0 | Rank 25; lifecycle `planned`; baseline `L0/rework_required`; legacy artifacts unaccepted; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0113/check_anchor_audit.py` | 0 | Target boundary, four candidate rows, 12 Lean probes, and pinned mathlib revision agree. |
| `python3 Stage1_Instances/THM-M-0113/check_obligation_tree.py` | 0 | `PASS`: 26 obligations and 49 typed edges; denominator `e509c192...cbd5`; the positive root remains open at M4. |
| Isolated `lake env lean` recipe below | 0 | The exact statement and countermodel elaborated at trust level zero. Lean reported axioms exactly `[propext, Classical.choice, Quot.sound]`; output SHA-256 `539fbb6d...331b1f9`; `Statement.olean` SHA-256 `94fe8a21...75e0`. |
| Scoped prohibited-declaration scan | 1 | Expected no-match: no prohibited declaration or placeholder occurs in the owned Lean sources; Lean's axiom report contains no `sorryAx`. |
| `ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release. |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`. |
| Root `lake env lean --version` preflight | 1 | The canonical `flt-regular` checkout could not resolve `HEAD`; recorded as an environment limitation rather than fetching or repairing a moving dependency. |
| `python3 -m json.tool Stage1_Instances/THM-M-0113/proof-recheck-2026-07-15-head-443b8bbc-slot18.json >/dev/null` | 0 | The current-base blocker packet is valid JSON. |
| Current-base blocker invariant assertions | 0 | Item/base identity, open state, source hashes, negative kernel result, empty receipts, and deliberate self-test absence agree. |
| Scoped whitespace checks | 0 | Tracked diff and both new-file whitespace checks passed. |
| `test ! -e .stage1-worker-selftest.json` | 0 | The incomplete proof phase emitted no worker-completion packet. |

The isolated Lean recipe, run from the repository root, was:

```bash
set -euo pipefail
root=$PWD
lean_root="$root/Formalizations/Lean"
tmp=$(mktemp -d /tmp/thm-m-0113-proof-recheck-head443b8bbc-slot18.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
cp Stage1_Instances/THM-M-0113/Statement.lean "$tmp/Statement.lean"
cp Stage1_Instances/THM-M-0113/Proof.lean "$tmp/Proof.lean"
paths="$lean_root/.lake/build/lib/lean"
for pkg in "$lean_root"/.lake/packages/*; do
  if [ -d "$pkg/.lake/build/lib/lean" ]; then
    paths="$paths:$pkg/.lake/build/lib/lean"
  fi
done
(cd "$tmp" && \
  ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 LEAN_NUM_THREADS=1 \
    LEAN_PATH="$paths" timeout --foreground 600 lake env lean \
    --trust=0 -t0 --root="$tmp" -o "$tmp/Statement.olean" \
    "$tmp/Statement.lean" >"$tmp/statement-output.txt" 2>&1 && \
  ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 LEAN_NUM_THREADS=1 \
    LEAN_PATH="$tmp:$paths" timeout --foreground 600 lake env lean \
    --trust=0 -t0 --root="$tmp" "$tmp/Proof.lean" \
    >"$tmp/proof-output.txt" 2>&1)
cat "$tmp/statement-output.txt" "$tmp/proof-output.txt" \
  >"$tmp/kernel-output.txt"
cat "$tmp/kernel-output.txt"
sha256sum "$tmp/statement-output.txt" "$tmp/proof-output.txt" \
  "$tmp/kernel-output.txt" "$tmp/Statement.olean"
```

The scoped prohibited-declaration scan was:

```bash
rg -n --pcre2 \
  '\b(?:sorry|admit|sorryAx|native_decide)\b|^[[:space:]]*(?:axiom|constant|opaque|unsafe)[[:space:]]|implemented_by|extern[[:space:]]' \
  Stage1_Instances/THM-M-0113 --glob '*.lean'
```

Its exit code was `1`, the expected no-match result. Lean's printed axiom
dependency report is the kernel-derived trust evidence for the countermodel.

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
| `Docs/Stage1_Execution_DAG_rev-5.6.json` | `0bb2f433832fe71156aa46c0828102ec3fb61a00dec81fae129c2826a59f63ca` |

This is durable blocker evidence, not a proof receipt. Because the assigned
positive proof phase is not genuinely self-tested as complete,
`.stage1-worker-selftest.json` is deliberately absent.
