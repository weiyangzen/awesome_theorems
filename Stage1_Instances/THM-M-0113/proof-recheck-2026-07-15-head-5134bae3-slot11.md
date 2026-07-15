# THM-M-0113 proof-phase blocker recheck

Item: `S56-M-0113-PROOF`

Base revision: `5134bae303d5f5104698e8c96d7af4c26306eb47`

Verdict: `blocked`

## Result

No legal positive proof body can inhabit the exact frozen target. The existing
placeholder-free declaration

```lean
Stage1Instances.THMM0113.not_hodgeDecompositionTarget :
  Not Stage1Instances.THMM0113.HodgeDecompositionTarget.{0, 0, 0, 0}
```

kernel-checks at trust level zero against a freshly elaborated
`Statement.olean`.

`HodgeData.isKahler` is an unconstrained proposition. It does not relate the
geometric hypothesis to the independently chosen `cohomology` family or
`hodgePiece` submodules. The countermodel uses the zero-dimensional compact
complex manifold `Fin 0 -> Complex`, sets `isKahler := True`, interprets every
cohomology space as `Complex`, and makes every Hodge piece bottom. Complex
conjugation satisfies the additive, conjugate-linear, and involutive laws. In
degree zero, the target would force the supremum of bottom submodules to be top
and hence force `1 = 0`.

This refutes the frozen Lean encoding, not the mathematical Hodge decomposition
theorem. Strengthening or narrowing the statement inside this proof item would
be a forbidden theorem substitution. The assigned positive item remains `[ ]`;
no proof receipt, state transition, accepted receipt, audit completion, theorem
completion, validation completion, release, or master acceptance is claimed.
No `.stage1-worker-selftest.json` is written because the requested proof phase
is not genuinely complete.

## Failed Gate And Retry

The first failed gate is
`S56-5.1-EXACT-TARGET-CONSISTENCY / M0113-S-DATA`. Replace the disconnected
`isKahler` proposition and arbitrary cohomology/Hodge-piece fields with native
definitions tied to the compact complex manifold, or add noncircular
law-bearing hypotheses sufficient to derive the intended conclusion. Then
publish a new statement fingerprint, repair the mutation evidence, and freshly
freeze and accept the statement, anchor audit, obligation registry, and typed
graphs before resuming positive proof work. Alternatively, redirect the item
explicitly to the checked counterexample target.

The frozen positive graph still records the analytic cut set `M0113-A-DR`,
`M0113-A-DOL`, `M0113-A-ELL`, `M0113-K-ID`, and `M0113-C-CHAIN`, but the earlier
statement defect blocks entry to that architecture. This recheck proposes only
an M4-to-M5 machine classification for the false frozen encoding. H4 and R4
are merely the frozen provisional registry values carried unchanged. This proof
worker does not endorse H4 as a fresh literature classification; source and
readability debt require their own audit phases. The prerequisite
obligation-tree item also remains provisional rather than master-accepted.

The owned target already contained 35 tracked structured proof rechecks at
worker start, while the authoritative DAG still records zero attempts and no
children. The standard requires an unresolved obligation to split after five
execution ticks. Although these files are not themselves the authoritative tick
ledger, another unchanged positive-root dispatch cannot create progress, and
splitting downstream analytic work cannot repair an upstream false statement.
Integration should reconcile the execution counter and route statement repair
or explicit redirection instead of requeuing this unchanged item.

## Validation

All checks used the existing symlink to the canonical pinned Lake artifacts.
No `lake update`, `lake build`, dependency clone/fetch, network action, or
`.lake` mutation was performed. Lean output was confined to a fresh directory
under `/tmp` and removed by a shell trap. The pre-existing untracked `.lake`
symlink makes this nonrelease evidence.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique ordered targets passed. |
| `python3 scripts/stage1_target.py show THM-M-0113` | 0 | Rank 25, `planned`, L0/rework required, legacy artifacts unaccepted, theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0113/check_anchor_audit.py` | 0 | Target boundary, four candidates, 12 probes, and pinned mathlib revision agree. |
| `python3 Stage1_Instances/THM-M-0113/check_obligation_tree.py` | 0 | 26 obligations and 49 typed edges passed; denominator `e509c192...cbd5`; root stays M4. |
| `cd Formalizations/Lean && timeout 60 lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3...b16740`, Release. |
| Isolated trust-zero Lean recipe below | 0 | The exact statement and countermodel elaborated; reported axioms were `[propext, Classical.choice, Quot.sound]`. Kernel-output SHA-256 was `539fbb6d...31b1f9`; temporary `Statement.olean` SHA-256 was `94fe8a21...75e0`. |
| Scoped prohibited-declaration scan | 1 | Expected no-match: no `sorry`, `admit`, `sorryAx`, `native_decide`, bodyless declaration, unsafe declaration, `implemented_by`, or `extern` occurs. |
| `python3 -m json.tool <current blocker JSON> >/dev/null` | 0 | The structured packet is valid JSON. |
| Current-base Python invariant assertions | 0 | Item/base identity, hashes, kernel result, open state, empty receipts, and deliberate self-test absence agree. |
| Scoped tracked and added-file whitespace checks | 0 / expected 1 | The tracked diff check passed; each no-index check returned content-difference status without a whitespace diagnostic. |
| `test ! -e .stage1-worker-selftest.json` | 0 | The incomplete phase emitted no worker-completion packet. |

The isolated replay, run from the repository root, was:

```bash
set -euo pipefail
tmp=$(mktemp -d /tmp/thm-m-0113-slot11.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
cp Stage1_Instances/THM-M-0113/Statement.lean "$tmp/Statement.lean"
cp Stage1_Instances/THM-M-0113/Proof.lean "$tmp/Proof.lean"
cd Formalizations/Lean
base_path=$(timeout 600 lake env printenv LEAN_PATH)
lean_bin=$(timeout 600 lake env which lean)
LEAN_NUM_THREADS=1 LEAN_PATH="$base_path" timeout 600 \
  "$lean_bin" --trust=0 -t 0 --root="$tmp" \
  -o "$tmp/Statement.olean" "$tmp/Statement.lean" \
  >"$tmp/kernel-output.txt" 2>&1
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$base_path" timeout 600 \
  "$lean_bin" --trust=0 -t 0 --root="$tmp" "$tmp/Proof.lean" \
  >>"$tmp/kernel-output.txt" 2>&1
cat "$tmp/kernel-output.txt"
sha256sum "$tmp/Statement.olean" "$tmp/kernel-output.txt"
```

The scoped prohibited-declaration scan was:

```bash
rg -n --pcre2 \
  '\b(?:sorry|admit|sorryAx|native_decide)\b|^[[:space:]]*(?:axiom|constant|opaque|unsafe)[[:space:]]|implemented_by|extern[[:space:]]' \
  Stage1_Instances/THM-M-0113 --glob '*.lean'
```

Its exit code `1` is the expected no-match result. The structured companion
records exact input hashes, recipe arguments, obligation/declaration coverage,
root vector, empty receipts, known failures, and the deliberate absence of a
worker completion manifest. After writing both blocker artifacts, the standard,
target-manifest, anchor-audit, obligation-tree, JSON/invariant, whitespace, and
self-test-absence checks were rerun and retained the exit codes shown above.
