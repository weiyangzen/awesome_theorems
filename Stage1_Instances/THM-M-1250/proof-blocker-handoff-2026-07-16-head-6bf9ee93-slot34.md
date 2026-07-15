# THM-M-1250 proof blocker handoff at `6bf9ee93` (slot34)

Item: `S56-M-1250-PROOF`

Verdict: `blocked`; state remains `[ ]`.

## Dependency context

The required `stage1-dependency-reuse-ledger/1.1` ledger was created before
proof execution. It binds graph digest
`73e99d2276c8ba9fec8f89ed41b712308d7f5667e95ba8185e49f1f5bfd40eca`,
target context
`068170c76abd4579d643ede04d731b974412185bd285e7b40255ec4044adec5c`,
and repository revision
`6bf9ee93a322e7d25cf9249226222095f95d1cff`.

The v2 node has no direct hard parents, transitive hard ancestors, incoming
hard edges, reuse hints, or shared groups. Accordingly the ledger has empty
`inspections`, `reuse_decisions`, and
`unresolved_compatibility_obligations`. The target-scoped schema validator
accepted this exact empty closure. This does not assert that the theorem is
mathematically independent.

## Mathematical blocker

No placeholder-free positive proof can inhabit the frozen target. Its
`IsSchwartzFunction` definition contains:

```lean
ContDiff Real (top : WithTop ENat) f
```

This is mathlib's analytic order `omega`. A `SchwartzMap` supplies:

```lean
ContDiff Real ((top : ENat) : WithTop ENat) f
```

which is the infinitely differentiable order `infinity`. The tracked theorem

```text
Stage1Instances.THM_M_1250.Counterexample.not_schwartzSpaceCharacterization :
  Not Stage1Instances.THM_M_1250.SchwartzSpaceCharacterization
```

constructs a nonzero compactly supported smooth bump, bundles it as a
`SchwartzMap`, and derives a contradiction from the analytic uniqueness
principle. The target-local certificate

```text
Stage1Instances.THM_M_1250.not_m1250ForwardPackage :
  Not Stage1Instances.THM_M_1250.M1250ForwardPackage
```

binds this refutation to the exact forward interface used by the conditional
composition architecture. Both declarations are placeholder-free and report
only `propext`, `Classical.choice`, and `Quot.sound`.

The reverse direction is genuine partial work:
`reversePackage_from_frozen_conditions` weakens analytic regularity to smooth
regularity and constructs the bundle. It does not rescue the impossible
forward direction or close the positive root. An independent disposable
trust-zero experiment confirmed that changing the statement to order
`infinity` makes the direct projection/constructor proof elaborate. That is a
differently typed theorem and receives no credit in this proof item.

The predecessor `S56-M-1250-OBLIGATION_TREE` is also only worker-provisional
`[_]`, not master-accepted `[x]`.

## Validation

No update, build, dependency fetch/clone/checkout, network action, or `.lake`
mutation was performed. The automation-provided pinned `.lake` symlink was
read only. Six copied modules were replayed from a disposable `/tmp`
directory, which was removed by `trap`:

```bash
set -euo pipefail
repo=$PWD
target=$repo/Stage1_Instances/THM-M-1250
lean_root=$repo/Formalizations/Lean
tmp=$(mktemp -d /tmp/thm-m-1250-slot34-6bf9ee93.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
for f in Statement Counterexample ProofBlocker M1250ObligationTree \
  M1250ProofRefutation ProofRefutation; do
  cp "$target/$f.lean" "$tmp/$f.lean"
done
base=$(cd "$lean_root" && lake env printenv LEAN_PATH)
cd "$lean_root"
LEAN_NUM_THREADS=1 LEAN_PATH="$base" timeout --foreground --kill-after=5s 600 \
  lake env lean --trust=0 -t0 -R "$tmp" -o "$tmp/Statement.olean" \
  "$tmp/Statement.lean"
for f in ProofBlocker Counterexample M1250ObligationTree; do
  LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$base" \
    timeout --foreground --kill-after=5s 600 \
    lake env lean --trust=0 -t0 -R "$tmp" -o "$tmp/$f.olean" \
    "$tmp/$f.lean"
done
for f in M1250ProofRefutation ProofRefutation; do
  LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$base" \
    timeout --foreground --kill-after=5s 600 \
    lake env lean --trust=0 -t0 -R "$tmp" "$tmp/$f.lean"
done
```

Every invocation exited `0` at trust level zero:

| Module | Log SHA-256 | Bytes |
|---|---|---:|
| `Statement` | `2f7f47d31193d167181eab4606af44bc6d2ad6f1eac751581414659b479f5faa` | 3170 |
| `ProofBlocker` | `535657cf2f2e5daab81470ec801591ae719f488b9f2032c49ff6b69fb18d896a` | 2667 |
| `Counterexample` | `478b93b48893d7ff76281bafdb7c20ee9464a9758d85b4081a5fc788c5d67ed4` | 365 |
| `M1250ObligationTree` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 0 |
| `M1250ProofRefutation` | `c381cdbee0efb5d74115de513ba879183804c1a5179f1658edd74c978ebc571d` | 187 |
| `ProofRefutation` | `2ccc1339ca05d191d6900b175614d156b57e2176e11c09f05194452434eeb175` | 220 |

The pinned environment was Lean `4.29.0`, commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, executable SHA-256
`3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf`,
and mathlib `8a178386ffc0f5fef0b77738bb5449d50efeea95` (tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`).

Other checks:

| Command | Exit | Result |
|---|---:|---|
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1250` | 0 | rank 430; planned; theorem incomplete |
| `python3 Stage1_Instances/THM-M-1250/check_anchor_audit.py` | 0 | pinned candidates match; positive root open |
| `python3 Stage1_Instances/THM-M-1250/check_obligation_tree.py` | 0 | 15 obligations and 30 edges pass; root open M3 |
| target-scoped dependency-ledger validator | 0 | exact graph, context, base, and empty closure pass |
| `python3 Docs/tools/check_stage1_theorem_dag_v2.py` | 1 | checked-in DAG differs from deterministic regeneration |

The last result is a global preflight disagreement. This worker did not edit
either graph authority and may not repair it. An attempted broad standard
check was interrupted after more than two minutes under severe concurrent
host load; it therefore supplies no pass evidence. Narrow target checks and
the trust-zero replay above completed.

## Retry condition

The master must first reconcile the global v2 DAG. Then reopen
`S56-M-1250-STATEMENT`, replace the ambiguous order with
`((top : ENat) : WithTop ENat)`, and regenerate and accept the statement,
anchor-audit, obligation-registry, and typed-graph artifacts before another
positive proof attempt. Alternatively, explicitly redirect this node to a
checked counterexample or barrier target.

Because the positive proof phase is blocked, no node-specific proof receipt
or `.stage1-worker-selftest.json` exists. The item stays `[ ]`; no audit,
validation, release, theorem-completion, or master-acceptance claim is made.
