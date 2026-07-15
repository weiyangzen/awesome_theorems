# THM-M-1277 proof-phase recheck at current base

Item: `S56-M-1277-PROOF`

Date: `2026-07-15` (`Asia/Shanghai`)

Base revision: `d44ed2b11fb201a761afad9b133caa8bc97fd710`

Base tree: `9602084a1c32fa6685f1c60eff540528226decff`

Worker slot: `36`

## Verdict

`blocked`. No legal positive proof body can inhabit the exact frozen target.
A fresh trust-level-zero replay at this base checks the tracked,
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
the bounded open unit ball, the supercritical clause with
`C = volume Omega` demands `volume Omega < volume Omega`.

This refutes only the frozen formal encoding, not the mathematical
Moser-Trudinger theorem. Editing the statement or proving a corrected theorem
inside this proof item would be an illegal target substitution. No positive
root proof, proof-node receipt, obligation closure, audit completion, or
theorem completion is claimed. The recorded vector remains `[H1, M3, R3]`;
`M5` is only the proposed machine diagnosis for this exact statement mismatch.

The assigned node is also not dependency-legal for acceptance: its prerequisite
`S56-M-1277-OBLIGATION_TREE` remains provisional `[_]`, not master-accepted
`[x]`. The structurally valid obligation registry predates the refutation; its
conditional branch composer cannot provide the false sharpness premise and
its root remains open `M3`. Independently, `statement.json` lacks a normalized
elaborated-expression fingerprint and mutation-test evidence, while
`scope-map.md` conflicts with the formal target about the nonempty-domain
condition. The raw-support encoding also lacks a checked crosswalk to the
usual compact-support-inside-domain condition.

Before this run, the owned path already contained 46 proof-recheck JSON files
and 47 proof-recheck Markdown files. Those files are repeated blocker evidence,
not authoritative scheduler attempts. The DAG still records zero proof
attempts; only the master may reconcile its private tick ledger and the
five-unresolved-tick split rule. Retrying the unchanged positive proof node
cannot succeed.

## Validation

All Lean checks used the existing pinned artifacts read-only through
`lake env lean`. No `lake update`, `lake build`, dependency clone/fetch,
network access, or `.lake` mutation was performed. The automation-provided
untracked `Formalizations/Lean/.lake` symlink makes this nonrelease blocker
evidence.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1277` | 0 | Rank 328; lifecycle `planned`; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all` before edits | 0 | Only the automation-provided untracked `Formalizations/Lean/.lake` symlink was present |
| `python3 Stage1_Instances/THM-M-1277/check_obligation_tree.py` | 0 | `PASS`: 24 obligations and 48 typed edges; denominator `e17739e...f60575`; root open `M3` |
| Fresh temporary-olean recipe below | 0 | Statement and proof elaborated at trust level zero; exact countertheorem observed; all 13 axiom reports were exactly `propext`, `Classical.choice`, and `Quot.sound` |
| Two independent read-only proof analyses and fresh trust-zero replays | 0 | Both reproduced the exact countertheorem, axiom report, and stable output hashes |
| `lake env lean --version` from `Formalizations/Lean` | 0 | Lean 4.29.0 commit `98dc76e...fab16740` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD^{commit} HEAD^{tree}` | 0 | Mathlib `8a178386...eea95`, tree `bdc39a31...2c19e5c2b` |
| `rg -n '\\b(sorry\|admit\|sorryAx)\\b\|^[[:space:]]*(axiom\|unsafe)\\b' Stage1_Instances/THM-M-1277 --glob '*.lean'` | 1, expected | No prohibited placeholder, declared axiom, generated placeholder constant, or unsafe declaration |
| Current-base structured invariant/hash checks and added-file whitespace checks | 0 | Blocker is valid and base-bound; recorded input hashes agree; both new artifacts have no whitespace diagnostics |
| `test ! -e .stage1-worker-selftest.json` | 0 | No positive proof self-test manifest was written |

Exact Lean recipe, run from `Formalizations/Lean`:

```bash
set -u
TMP=$(mktemp -d /tmp/thm-m-1277-proof-d44ed2b1-slot36.XXXXXX)
cleanup(){ rm -rf "$TMP"; }
trap cleanup EXIT
BASE=$(timeout --foreground --kill-after=5s 60 lake env printenv LEAN_PATH)
LEAN_NUM_THREADS=1 timeout --foreground --kill-after=5s 300 \
  lake env lean --trust=0 -t0 --root=../.. \
  -o "$TMP/Statement.olean" \
  ../../Stage1_Instances/THM-M-1277/Statement.lean \
  >"$TMP/statement.out" 2>&1
LEAN_NUM_THREADS=1 LEAN_PATH="$TMP:$BASE" \
  timeout --foreground --kill-after=5s 300 \
  lake env lean --trust=0 -t0 --root=../.. \
  -o "$TMP/Proof.olean" \
  ../../Stage1_Instances/THM-M-1277/Proof.lean \
  >"$TMP/proof.out" 2>&1
sha256sum "$TMP/Statement.olean" "$TMP/Proof.olean" \
  "$TMP/statement.out" "$TMP/proof.out"
```

The replay began at `2026-07-15T19:20:11+08:00` and ended at
`2026-07-15T19:20:45+08:00`. Fresh SHA-256 values were
`84f541c01763ee25facdce4cfc28cc3380e52a5f55d9c3c295c0cefe99159e63`
for `Statement.olean`,
`fe8744f2d174c01c443bc4c34ce0f9ed934e5e39b7bba12eed53b718b24c0e91`
for `Proof.olean`,
`593f08c48172c08e242b8073f6550e2d3f100806c26d98d9ddb387dc8a1fb3a8`
for statement output, and
`2f47380b9e5a682199aa7e433ad923111d99b9612a1d9bb3a050fa4f8c10d9c8`
for proof output. The temporary directory was removed.

## Retry condition

The first failed gate is exact canonical statement correctness. Reopen
`S56-M-1277-STATEMENT`, replace the analytic order with the intended smooth
order `((top : ENat) : WithTop ENat)`, reconcile the nonempty-domain scope
text, audit or replace the raw-support condition, run exact-expression identity
and mutation gates, and publish a new version of the obligation registry,
typed graphs, and validation specifications for the changed fingerprint before
another proof attempt.

The remaining root cut set is `S56-M-1277-STATEMENT`. Because the assigned
positive proof phase is not genuinely self-tested as complete,
`.stage1-worker-selftest.json` is deliberately absent and the item remains
`[ ]`.
