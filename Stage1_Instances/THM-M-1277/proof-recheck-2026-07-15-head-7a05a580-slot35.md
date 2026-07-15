# THM-M-1277 proof-phase recheck at current base

Item: `S56-M-1277-PROOF`

Date: `2026-07-15` (`Asia/Shanghai`)

Base revision: `7a05a580f6eb39b1dcd87bbd8f3d9f4c0ecd4cb4`

Base tree: `681b326462f0271a612a5178ae0846f857b96648`

Worker slot: `35`

## Verdict

`blocked`. The requested positive proof body cannot exist for the exact frozen
Lean target. A fresh trust-level-zero replay at this base checks the tracked,
placeholder-free countertheorem

```text
Stage1Rev56.THMM1277.not_statement :
  Not Stage1Rev56.THMM1277.Statement
```

`SmoothCompactIn` uses `ContDiff Real top`. Here `top` is mathlib's analytic
order `omega`, not the intended smooth order `infinity` (the coerced top of
`ENat`). Analytic uniqueness therefore forces every compactly supported
approximant to be zero. The encoded completion makes every admitted scalar
field zero almost everywhere, so its exponential integral is exactly
`volume Omega` at every exponent. On the bounded open unit ball, the
supercritical clause with `C = volume Omega` then requires
`volume Omega < volume Omega`.

This refutes the frozen formal encoding, not the mathematical
Moser-Trudinger theorem. Changing the statement inside this proof item would
be an illegal target substitution. No positive root proof, obligation closure,
audit completion, or theorem completion is claimed. The recorded vector stays
`[H1, M3, R3]`; `M5` is only the proposed diagnosis for the erroneous formal
encoding.

The prerequisite obligation-tree item is still provisional `[_]`, not
master-accepted `[x]`. Its conditional branch composer remains valid only when
given endpoint and sharpness premises and cannot produce the false sharpness
branch. The statement receipt also lacks normalized elaborated-expression and
mutation-test evidence, while `scope-map.md` incorrectly says domain
nonemptiness is unnecessary. The support encoding uses
`Function.support phi subset Omega`, rather than the usual
`tsupport phi subset Omega`, without a checked equivalence to the claimed
compact-support-inside-domain class.

## Validation

All checks ran in this worker clone against the existing pinned artifacts. No
`lake update`, `lake build`, dependency clone/fetch, network access, or `.lake`
mutation was used. The automation-provided untracked `.lake` symlink makes the
result nonrelease blocker evidence.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1277` | 0 | Rank 328; lifecycle `planned`; legacy artifacts unaccepted; theorem incomplete |
| `python3 Stage1_Instances/THM-M-1277/check_obligation_tree.py` | 0 | `PASS`: 24 obligations, 48 typed edges, denominator `e17739e989327c1dcc2a43ec26c2d83e43a62bdf8448246f530a84f65af60575`; root open `M3` |
| Fresh temporary-olean recipe below | 0 | Statement and proof elaborated; exact countertheorem observed; every one of 13 printed axiom sets was exactly `propext`, `Classical.choice`, and `Quot.sound` |
| Three independent read-only target audits | 0 | Each confirmed the exact statement, fatal regularity mismatch, counterproof chain, and lack of a lawful positive proof route; one separately replayed the trust-zero elaboration |
| `lake env lean --version` from `Formalizations/Lean` | 0 | Lean 4.29.0 commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD^{commit} HEAD^{tree}` | 0 | Mathlib `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b` |
| `rg -n '\b(sorry\|admit\|sorryAx)\b\|^[[:space:]]*(axiom\|unsafe)\b' Stage1_Instances/THM-M-1277 --glob '*.lean'` | 1, expected | No prohibited placeholder, declared axiom, generated placeholder constant, or unsafe declaration |
| `test ! -e .stage1-worker-selftest.json` | 0 | No positive proof self-test manifest was written |

Fresh Lean recipe, run from the workspace root:

```bash
set -u
ROOT=$PWD
LEAN_ROOT="$ROOT/Formalizations/Lean"
TMP=$(mktemp -d /tmp/thm-m-1277-proof-7a05a580-slot35.XXXXXX)
trap 'rm -rf "$TMP"' EXIT
cd "$LEAN_ROOT"
BASE=$(timeout --foreground --kill-after=5s 60 lake env printenv LEAN_PATH)
LEAN_NUM_THREADS=1 timeout --foreground --kill-after=5s 300 \
  lake env lean --trust=0 -t0 --root=../.. \
  -o "$TMP/Statement.olean" \
  ../../Stage1_Instances/THM-M-1277/Statement.lean \
  >"$TMP/statement.out" 2>&1
S=$?
if [ "$S" -ne 0 ]; then cat "$TMP/statement.out"; exit "$S"; fi
LEAN_NUM_THREADS=1 LEAN_PATH="$TMP:$BASE" \
  timeout --foreground --kill-after=5s 300 \
  lake env lean --trust=0 -t0 --root=../.. \
  -o "$TMP/Proof.olean" \
  ../../Stage1_Instances/THM-M-1277/Proof.lean \
  >"$TMP/proof.out" 2>&1
P=$?
if [ "$P" -ne 0 ]; then cat "$TMP/proof.out"; exit "$P"; fi
sha256sum "$TMP/Statement.olean" "$TMP/Proof.olean" \
  "$TMP/statement.out" "$TMP/proof.out"
```

The SHA-256 values were
`84f541c01763ee25facdce4cfc28cc3380e52a5f55d9c3c295c0cefe99159e63`
for `Statement.olean`,
`fe8744f2d174c01c443bc4c34ce0f9ed934e5e39b7bba12eed53b718b24c0e91`
for `Proof.olean`,
`593f08c48172c08e242b8073f6550e2d3f100806c26d98d9ddb387dc8a1fb3a8`
for statement output, and
`2f47380b9e5a682199aa7e433ad923111d99b9612a1d9bb3a050fa4f8c10d9c8`
for proof output. The temporary directory was removed.

## Retry condition

Reopen `S56-M-1277-STATEMENT`, replace the analytic order with the intended
smooth order `((top : ENat) : WithTop ENat)`, reconcile nonempty-domain and
support semantics, add exact-expression and mutation evidence, and regenerate
the obligation registry, typed graphs, and validation specifications for the
new statement fingerprint. Only after those prerequisite nodes are accepted
can a new proof attempt begin.

This is durable current-base blocker evidence. It does not satisfy
`S56-M-1277-PROOF` and makes no provisional, accepted, validation, release, or
theorem-completion claim. Repeated blocker artifact counts do not establish
scheduler tick identity; the master must reconcile its private attempt ledger
and redirect the target after five actual unresolved proof ticks.
