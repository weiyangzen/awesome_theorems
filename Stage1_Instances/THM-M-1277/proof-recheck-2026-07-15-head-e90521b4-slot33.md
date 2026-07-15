# THM-M-1277 proof-phase recheck at current base

Item: `S56-M-1277-PROOF`

Date: `2026-07-15` (`Asia/Shanghai`)

Base revision: `e90521b4b150b98d81c4dca2462ad36b64d4673e`

Base tree: `f12951f481d2b51f33d6d300dc2874b3c49ed0e0`

Worker slot: `33`

## Verdict

`blocked`. The exact frozen Lean target cannot have a positive proof body. A
fresh trust-level-zero replay at this base checks the tracked, placeholder-free
countertheorem

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
the bounded open unit ball, the supercritical clause with
`C = volume Omega` demands `volume Omega < volume Omega`.

This refutes only the frozen formal encoding, not the mathematical
Moser-Trudinger theorem. Editing the statement or proving a corrected theorem
inside this proof item would be an illegal target substitution. No positive
root proof, obligation closure, accepted receipt, audit completion, or theorem
completion is claimed. The recorded vector remains `[H1, M3, R3]`; `M5` is
only the proposed machine diagnosis for this exact statement mismatch.

The existing positive obligation registry is structurally valid but predates
the refutation. Its conditional branch composer cannot supply the false
sharpness premise and the root remains open `M3`. The statement record also
lacks the required normalized elaborated-expression fingerprint and mutation
tests, and `scope-map.md` incorrectly says nonemptiness is unnecessary while
the formal target requires it because sharpness is false on the empty domain.
The prerequisite obligation-tree item remains provisional `[_]`, so master
acceptance is unavailable independently of the decisive statement blocker.

## Validation

All successful Lean checks used existing pinned compiled artifacts read-only.
No `lake update`, `lake build`, dependency clone/fetch, network access, or
`.lake` mutation was performed. The worker's untracked
`Formalizations/Lean/.lake` symlink makes this nonrelease blocker evidence.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1277` | 0 | Rank 328; lifecycle `planned`; legacy artifacts unaccepted; theorem incomplete |
| `git status --short` before edits | 0 | Only `?? Formalizations/Lean/.lake`, the automation-provided symlink to the canonical pinned cache |
| `python3 Stage1_Instances/THM-M-1277/check_obligation_tree.py` | 0 | `PASS`: 24 obligations, 48 typed edges, denominator `e17739e...f60575`; root open `M3` |
| Initial narrow `lake env lean` replay | 1 | Environmental Lake failure: `external command 'git' exited with code 128`; this did not elaborate the target and is retained as a known failure |
| Fresh manual-path trust-zero recipe below | 0 | Statement and proof both elaborated; exact countertheorem observed; all 13 axiom reports were exactly `propext`, `Classical.choice`, and `Quot.sound` |
| Independent fresh trust-zero replay by a read-only worker | 0 | Reproduced both successful elaborations, the exact countertheorem, the 13 identical axiom reports, and both `.olean` hashes |
| Pinned `lean --version`; pinned mathlib `rev-parse HEAD^{commit} HEAD^{tree}` | 0 | Lean 4.29.0 commit `98dc76e...fab16740`; mathlib `8a178386...eea95`, tree `bdc39a31...2c19e5c2b` |
| `rg -n '\\b(sorry\|admit\|sorryAx)\\b\|^[[:space:]]*(axiom\|unsafe)\\b' Stage1_Instances/THM-M-1277 --glob '*.lean'` | 1, expected | No prohibited placeholder, declared axiom, generated placeholder constant, or unsafe declaration |

The successful narrow replay ran from the workspace root. It copied only the
two owned Lean inputs to a temporary directory, assembled `LEAN_PATH` from
the existing package outputs, and invoked the pinned Lean executable through
a bounded command:

```bash
set -u
ROOT=$PWD
TARGET="$ROOT/Stage1_Instances/THM-M-1277"
LEAN_ROOT="$ROOT/Formalizations/Lean"
TMP=$(mktemp -d /tmp/thm-m-1277-slot33-manual.XXXXXX)
cleanup(){ rm -rf "$TMP"; }
trap cleanup EXIT
cp "$TARGET/Statement.lean" "$TARGET/Proof.lean" "$TMP"/
TOOLCHAIN_LIB="$HOME/.elan/toolchains/leanprover--lean4---v4.29.0/lib/lean"
MANUAL_LEAN_PATH=$(find -L "$LEAN_ROOT/.lake/packages" \
  -path '*/.lake/build/lib/lean' -type d ! -path '*/flt-regular/*' \
  -print | sort -u | paste -sd: -)
MANUAL_LEAN_PATH="$LEAN_ROOT/.lake/build/lib/lean:$MANUAL_LEAN_PATH:$TOOLCHAIN_LIB"
LEAN_NUM_THREADS=1 timeout --foreground --kill-after=5s 300 \
  env LEAN_PATH="$MANUAL_LEAN_PATH" \
  "$HOME/.elan/toolchains/leanprover--lean4---v4.29.0/bin/lean" \
  --trust=0 -t0 --root="$TMP" -o "$TMP/Statement.olean" \
  "$TMP/Statement.lean"
LEAN_NUM_THREADS=1 timeout --foreground --kill-after=5s 300 \
  env LEAN_PATH="$TMP:$MANUAL_LEAN_PATH" \
  "$HOME/.elan/toolchains/leanprover--lean4---v4.29.0/bin/lean" \
  --trust=0 -t0 --root="$TMP" -o "$TMP/Proof.olean" "$TMP/Proof.lean"
```

Fresh output SHA-256 values were
`6f184999ed81c69800d9f91cd3c969557853b7ff370c05fdd6790cd31de4e65a`
for `Statement.olean`,
`0597c2f2ed998eba1e50fadc0aba30d461226e4bf31a85dc3d3b4560355686db`
for `Proof.olean`,
`593f08c48172c08e242b8073f6550e2d3f100806c26d98d9ddb387dc8a1fb3a8`
for statement output, and
`2f47380b9e5a682199aa7e433ad923111d99b9612a1d9bb3a050fa4f8c10d9c8`
for proof output. The temporary directory was removed.

## Retry Condition

The first failed gate is exact canonical statement correctness. Reopen
`S56-M-1277-STATEMENT`, replace the analytic order with the intended smooth
order `((top : ENat) : WithTop ENat)`, reconcile the nonempty-domain scope
text, run exact-expression identity and mutation gates, and publish a new
version of the obligation registry, typed graphs, and validation
specifications for the changed fingerprint before another proof attempt.

The remaining root cut set is `S56-M-1277-STATEMENT`. Because the assigned
positive proof phase is not genuinely self-tested as complete,
`.stage1-worker-selftest.json` is deliberately absent and the item remains
`[ ]`.
