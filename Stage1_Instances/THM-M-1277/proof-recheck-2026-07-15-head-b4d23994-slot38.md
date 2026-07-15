# THM-M-1277 proof-phase recheck at current base

Item: `S56-M-1277-PROOF`

Date: `2026-07-15` (`Asia/Shanghai`)

Base revision: `b4d239943a37f6c25c377bbfd85c0e1ec7f4acaa`

Base tree: `5f13e0e86bde3bcaaef38b979819490c648166e3`

Worker slot: `38`

## Verdict

`blocked`. The exact frozen Lean target cannot have the requested positive
proof body. A fresh trust-level-zero replay at this base checks the tracked,
placeholder-free countertheorem

```text
Stage1Rev56.THMM1277.not_statement :
  Not Stage1Rev56.THMM1277.Statement
```

The defect is in `SmoothCompactIn`: `ContDiff Real top` elaborates at
mathlib's analytic order `omega`, rather than smooth order `infinity` (the
coerced top of `ENat`). Analytic uniqueness makes every compactly supported
approximant identically zero. The encoded `ZeroBoundarySobolev` predicate then
forces every admitted scalar field to vanish almost everywhere, so every
admissible exponential integral equals `volume Omega` for every exponent. On
the bounded open unit ball, the supercritical clause with `C = volume Omega`
demands `volume Omega < volume Omega`.

This refutes only the frozen formal encoding, not the mathematical
Moser-Trudinger theorem. Editing the statement or proving a corrected theorem
inside this proof item would be an illegal target substitution. No positive
root proof, proof-node receipt, obligation closure, audit completion, or
theorem completion is claimed. The recorded vector remains `[H1, M3, R3]`;
`M5` is only the proposed machine diagnosis for this exact statement mismatch.

The prerequisite obligation-tree item remains provisional `[_]`, not
master-accepted `[x]`. Its positive architecture is structurally valid but
predates the refutation: the conditional branch composer cannot supply the
false sharpness premise and its root remains open `M3`. Independently, the
statement record lacks a normalized elaborated-expression fingerprint and
mutation tests, while `scope-map.md` conflicts with the formal target about
the nonempty-domain condition.

## Validation

All Lean checks read the existing pinned artifacts without modifying them. No
`lake update`, `lake build`, dependency clone/fetch, or network access was
used. The automation-provided untracked `.lake` symlink makes this nonrelease
blocker evidence.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1277` | 0 | Rank 328; lifecycle `planned`; legacy artifacts unaccepted; theorem incomplete |
| `git status --short` (before edits) | 0 | Only the automation-provided untracked `Formalizations/Lean/.lake` symlink was present; the owned path and root self-test path were clean |
| `python3 Stage1_Instances/THM-M-1277/check_obligation_tree.py` | 0 | `PASS`: 24 obligations, 48 typed edges, denominator `e17739e...f60575`; root open `M3` |
| Fresh temporary-olean recipe below | 0 | Statement and proof both elaborated; exact countertheorem observed; all 13 axiom reports were exactly `propext`, `Classical.choice`, and `Quot.sound` |
| Independent fresh statement replay and separately reconstructed `/tmp/THMM1277Research.lean` counterproof at `--trust=0` | 0 | A read-only reviewer independently reproduced the analytic-order defect and complete `Not Statement` proof |
| Second independent read-only mathematical review | 0 | The reviewer confirmed the exact false-target diagnosis and counterproof chain and found no legal positive proof route |
| `lake env lean --version` from `Formalizations/Lean` | 0 | Lean 4.29.0 commit `98dc76e...fab16740` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD^{commit} HEAD^{tree}` | 0 | Mathlib `8a178386...eea95`, tree `bdc39a31...2c19e5c2b` |
| `rg -n '\b(sorry\|admit\|sorryAx)\b\|^[[:space:]]*(axiom\|unsafe)\b' Stage1_Instances/THM-M-1277 --glob '*.lean'` | 1, expected | No prohibited placeholder, declared axiom, generated placeholder constant, or unsafe declaration |
| Current-base JSON/invariant/hash checks and per-new-file `git diff --no-index --check` | 0 | Structured blocker is valid and base-bound; all recorded input hashes agree; both new artifacts have no whitespace diagnostics |
| `test ! -e .stage1-worker-selftest.json` | 0 | No positive proof self-test manifest was written |

Exact fresh Lean recipe, run from the workspace root:

```bash
set -u
ROOT=$(git rev-parse --show-toplevel)
LEAN_ROOT="$ROOT/Formalizations/Lean"
TMP=$(mktemp -d /tmp/thm-m-1277-proof-b4d239943-slot38.XXXXXX)
trap 'rm -rf "$TMP"' EXIT
cd "$LEAN_ROOT"
BASE=$(env -u LEAN_PATH timeout --foreground --kill-after=5s 60 \
  lake env printenv LEAN_PATH)
LEAN_NUM_THREADS=1 timeout --foreground --kill-after=5s 300 \
  lake env lean --trust=0 -t0 --root=../.. -o "$TMP/Statement.olean" \
  ../../Stage1_Instances/THM-M-1277/Statement.lean \
  >"$TMP/statement.out" 2>&1
LEAN_NUM_THREADS=1 LEAN_PATH="$TMP:$BASE" \
  timeout --foreground --kill-after=5s 300 \
  lake env lean --trust=0 -t0 --root=../.. -o "$TMP/Proof.olean" \
  ../../Stage1_Instances/THM-M-1277/Proof.lean \
  >"$TMP/proof.out" 2>&1
sha256sum "$TMP/Statement.olean" "$TMP/Proof.olean" \
  "$TMP/statement.out" "$TMP/proof.out"
```

The fresh SHA-256 values were
`84f541c01763ee25facdce4cfc28cc3380e52a5f55d9c3c295c0cefe99159e63`
for `Statement.olean`,
`fe8744f2d174c01c443bc4c34ce0f9ed934e5e39b7bba12eed53b718b24c0e91`
for `Proof.olean`,
`593f08c48172c08e242b8073f6550e2d3f100806c26d98d9ddb387dc8a1fb3a8`
for statement output, and
`2f47380b9e5a682199aa7e433ad923111d99b9612a1d9bb3a050fa4f8c10d9c8`
for proof output. The temporary directory was removed after validation.

## Retry condition

The first failed gate is exact canonical statement correctness. Reopen
`S56-M-1277-STATEMENT`, replace the ambiguous analytic order with the intended
smooth order `((top : ENat) : WithTop ENat)`, reconcile the nonempty-domain
scope text, run exact-expression identity and mutation gates, and publish a
new version of the obligation registry, typed graphs, and validation
specifications for the changed fingerprint before another proof attempt.

The remaining root cut set is `S56-M-1277-STATEMENT`. Because the assigned
positive proof phase is not genuinely self-tested as complete,
`.stage1-worker-selftest.json` is deliberately absent and the item remains
`[ ]`.
