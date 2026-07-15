# THM-M-1277 proof-phase recheck at current base

Item: `S56-M-1277-PROOF`

Date: `2026-07-15` (`Asia/Shanghai`)

Base revision: `3862149a6bcf2a64e19fabdced9dd80a706f288e`

Base tree: `d3e57e661c2326a97c8b48580abe1f4a3797cd98`

Worker slot: `35`

## Verdict

`blocked`. No legal positive proof body can inhabit the exact frozen target.
The tracked, placeholder-free declaration

```text
Stage1Rev56.THMM1277.not_statement :
  Not Stage1Rev56.THMM1277.Statement
```

kernel-checks at trust level zero against a freshly emitted
`Statement.olean`. Independent proof review and a separate fresh Lean replay
reproduced the declaration type, axiom report, and all generated hashes.

The defect is in `SmoothCompactIn`. Its `ContDiff Real top` order is
mathlib's analytic order `omega`, not smooth order `infinity`, which is the
coerced top of `ENat`. Analytic uniqueness makes every compactly supported
approximant identically zero. Consequently `ZeroBoundarySobolev` forces its
scalar field to vanish almost everywhere, and every admissible exponential
integral equals `volume Omega` for every exponent. On the bounded open unit
ball, the supercritical clause with `C = volume Omega` then requires
`volume Omega < volume Omega`.

This refutes only the frozen Lean encoding, not the mathematical
Moser-Trudinger theorem. Correcting the target during this proof item would be
an illegal substitution. The recorded vector remains `[H1, M3, R3]`; `M5`
is only the proposed diagnosis for the exact statement mismatch. No positive
proof receipt, obligation closure, audit completion, or theorem completion is
claimed. The pre-existing negative proof body is retained as real blocker
evidence; no proof source changed in this run.

The statement prerequisite also lacks the required normalized elaborated-
expression fingerprint and mutation-test evidence. In addition,
`scope-map.md` says nonemptiness is unnecessary while the formal target,
statement record, and README require it because sharpness is false on the
empty domain. `SmoothCompactIn` also uses `Function.support u subset Omega`
while the intake says compact support in `Omega`; the intended
`tsupport`/`support` boundary has no checked equivalence. The existing
positive obligation registry and typed graphs predate the refutation. Their
structural validator reports an open `M3` root; its conditional branch
composer cannot supply the false sharpness premise.

Independently, the assigned proof node's prerequisite
`S56-M-1277-OBLIGATION_TREE` is still provisional `[_]`, not master-accepted
`[x]`. Dependency-ordered acceptance is unavailable.

Before this run, the target contained 40 proof-recheck JSON files and 41
proof-recheck Markdown files. Those counts prove repeated unresolved
rechecks, not scheduler tick identity; the authoritative DAG still records
zero proof attempts. The master must reconcile its private tick ledger
against the five-unresolved-tick split rule. Retrying the unchanged positive
proof node cannot succeed; it needs upstream statement repair or explicit
redirection to the checked refutation.

## Validation

All successful Lean checks used the existing pinned artifacts read-only via
`lake env lean`. No `lake update`, `lake build`, dependency clone/fetch,
network access, or `.lake` mutation was performed. The automation-provided
untracked `Formalizations/Lean/.lake` symlink makes this nonrelease blocker
evidence.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1277` | 0 | Rank 328; lifecycle `planned`; legacy artifacts unaccepted; theorem incomplete |
| `git status --short` before edits | 0 | Only the automation-provided untracked `Formalizations/Lean/.lake` symlink was present |
| `python3 Stage1_Instances/THM-M-1277/check_obligation_tree.py` | 0 | `PASS`: 24 obligations and 48 typed edges; denominator `e17739e...f60575`; stale positive root open `M3` |
| Fresh temporary-olean recipe below | 0 | `Statement : Prop` and `not_statement : Not Statement` elaborated at trust level zero; all 13 axiom reports were exactly `propext`, `Classical.choice`, and `Quot.sound` |
| Independent fresh trust-zero replay by a read-only worker | 0 | Reproduced the exact countertheorem, axiom report, and all four generated hashes |
| `rg -n '\b(sorry\|admit\|sorryAx)\b\|^[[:space:]]*(axiom\|unsafe)\b' Stage1_Instances/THM-M-1277 --glob '*.lean'` | 1, expected | No prohibited placeholder, declared axiom, generated placeholder constant, or unsafe declaration |
| `lake env lean --version` from `Formalizations/Lean` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD^{commit} HEAD^{tree}` | 0 | Pinned mathlib `8a178386...eea95`, tree `bdc39a31...2c19e5c2b` |
| `python3 -m json.tool Stage1_Instances/THM-M-1277/proof-recheck-2026-07-15-head-3862149a-slot35.json` plus the exact `jq -e` predicate recorded in the structured artifact | 0 | The blocker is valid JSON and binds this item/base, blocked state, noncompletion, empty accepted receipts, and self-test absence |
| `git diff --no-index --check /dev/null Stage1_Instances/THM-M-1277/proof-recheck-2026-07-15-head-3862149a-slot35.{json,md}` expanded to two paths | 1 per file, expected | Both commands reported added-file status and no whitespace diagnostic |
| `test ! -e .stage1-worker-selftest.json` | 0 | No positive proof self-test manifest was written |

Exact Lean recipe, run from `Formalizations/Lean`:

```bash
set -u
TMP=$(mktemp -d /tmp/thm-m-1277-proof-3862149a-slot35.XXXXXX)
cleanup(){ rm -rf "$TMP"; }
trap cleanup EXIT
BASE=$(timeout --foreground --kill-after=5s 60 lake env printenv LEAN_PATH)
LEAN_NUM_THREADS=1 timeout --foreground --kill-after=5s 300 \
  lake env lean --trust=0 -t0 --root=../.. \
  -o "$TMP/Statement.olean" \
  ../../Stage1_Instances/THM-M-1277/Statement.lean \
  >"$TMP/statement.out" 2>&1
s1=$?
if [ "$s1" -ne 0 ]; then
  cat "$TMP/statement.out"
  exit "$s1"
fi
LEAN_NUM_THREADS=1 LEAN_PATH="$TMP:$BASE" \
  timeout --foreground --kill-after=5s 300 \
  lake env lean --trust=0 -t0 --root=../.. \
  -o "$TMP/Proof.olean" \
  ../../Stage1_Instances/THM-M-1277/Proof.lean \
  >"$TMP/proof.out" 2>&1
s2=$?
cat "$TMP/statement.out"
cat "$TMP/proof.out"
sha256sum "$TMP/Statement.olean" "$TMP/Proof.olean" \
  "$TMP/statement.out" "$TMP/proof.out"
exit "$s2"
```

The replay began at `2026-07-15T16:57:10+08:00` and ended at
`2026-07-15T16:59:57+08:00`. Fresh hashes were:

| Output | SHA-256 |
|---|---|
| `Statement.olean` | `84f541c01763ee25facdce4cfc28cc3380e52a5f55d9c3c295c0cefe99159e63` |
| `Proof.olean` | `fe8744f2d174c01c443bc4c34ce0f9ed934e5e39b7bba12eed53b718b24c0e91` |
| statement output | `593f08c48172c08e242b8073f6550e2d3f100806c26d98d9ddb387dc8a1fb3a8` |
| proof output | `2f47380b9e5a682199aa7e433ad923111d99b9612a1d9bb3a050fa4f8c10d9c8` |

The temporary directory was removed.

## Retry Condition

The first failed gate is exact canonical statement correctness. Reopen
`S56-M-1277-STATEMENT`, use the intended smooth order unambiguously as
`((top : ENat) : WithTop ENat)` (scoped notation `infinity`), reconcile the
nonempty-domain scope text and the `Function.support` versus `tsupport`
meaning of compact support in `Omega`, add any required checked equivalence,
rerun exact-expression identity and mutation tests, and publish a versioned
obligation registry, typed graphs, and validation specifications for the new
fingerprint before another proof attempt.

The remaining root cut set is `S56-M-1277-STATEMENT`. Because the assigned
positive proof phase is not genuinely self-tested as complete,
`.stage1-worker-selftest.json` is deliberately absent and the item remains
`[ ]`.
