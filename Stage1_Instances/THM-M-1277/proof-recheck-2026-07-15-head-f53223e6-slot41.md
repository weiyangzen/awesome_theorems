# THM-M-1277 proof-phase recheck at current base

Item: `S56-M-1277-PROOF`

Date: `2026-07-15` (`Asia/Shanghai`)

Base revision: `f53223e6746df4856b00068d3e8723264dfd044a`

Base tree: `bb293e5342b6501791d40c7464d150820aafe441`

Worker slot: `41`

## Verdict

`blocked`. No legal positive proof body can inhabit the exact frozen target.
A fresh trust-level-zero replay through the required `lake env lean` interface
checks the tracked, placeholder-free countertheorem

```text
Stage1Rev56.THMM1277.not_statement :
  Not Stage1Rev56.THMM1277.Statement
```

The defect is in `SmoothCompactIn`. Its `ContDiff Real top` order elaborates
to mathlib's analytic order `omega`, not smooth order `infinity` (the coerced
top of `ENat`). Analytic uniqueness makes every compactly supported
approximant identically zero. Consequently `ZeroBoundarySobolev` forces its
scalar field to vanish almost everywhere, and every admissible exponential
integral equals `volume Omega` for every exponent. On the bounded open unit
ball, the supercritical clause with `C = volume Omega` then requires
`volume Omega < volume Omega`.

This refutes only the frozen Lean encoding, not the mathematical
Moser-Trudinger theorem. Correcting the target during this proof item would be
an illegal substitution. The recorded vector remains `[H1, M3, R3]`; `M5`
is only the proposed machine diagnosis for this exact statement mismatch. No
positive proof receipt, obligation closure, audit completion, or theorem
completion is claimed. The pre-existing negative proof body is retained as
real blocker evidence; no proof source changed in this run.

The statement prerequisite also lacks the required normalized elaborated-
expression fingerprint and mutation-test evidence. In addition,
`scope-map.md` says nonemptiness is unnecessary while the formal target,
statement record, and README require it because sharpness is false on the
empty domain. The intake phrase compactly supported in `Omega` is also
ambiguous between the selected `Function.support u subset Omega` convention
and the stronger `tsupport u subset Omega` convention; the selected meaning
lacks an explicit source-statement crosswalk. The existing positive obligation
registry and typed graphs predate the refutation. Their structural validator
reports an open `M3` root; its conditional branch composer cannot supply the
false sharpness premise.

Independently, the assigned proof node's prerequisite
`S56-M-1277-OBLIGATION_TREE` is still provisional `[_]`, not master-accepted
`[x]`. Dependency-ordered acceptance is unavailable.

Before this run, the target contained 42 proof-recheck JSON files and 43
proof-recheck Markdown files. Those counts prove repeated unresolved rechecks,
not scheduler tick identity; the authoritative DAG still records zero proof
attempts. The master must reconcile its private tick ledger against the
five-unresolved-tick split rule. Retrying the unchanged positive proof node
cannot succeed; it needs upstream statement repair or explicit redirection to
the checked refutation.

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
| `git status --short --untracked-files=all` before edits | 0 | Only the automation-provided untracked `Formalizations/Lean/.lake` symlink was present |
| `python3 Stage1_Instances/THM-M-1277/check_obligation_tree.py` | 0 | `PASS`: 24 obligations and 48 typed edges; denominator `e17739e...f60575`; stale positive root open `M3` |
| Fresh temporary-olean recipe below | 0 | `Statement : Prop` and `not_statement : Not Statement` elaborated at trust level zero; all 13 axiom reports were exactly `propext`, `Classical.choice`, and `Quot.sound` |
| Independent read-only inspection | 0 | Three reviewers independently confirmed the false frozen target, legal blocker disposition, and artifact requirements; a separate replay elaborated `Statement.lean`, while its Proof process was killed under unrelated shared-host memory pressure and is not validation evidence |
| `rg -n '\b(sorry\|admit\|sorryAx)\b\|^[[:space:]]*(axiom\|unsafe)\b' Stage1_Instances/THM-M-1277 --glob '*.lean'` | 1, expected | No prohibited placeholder, declared axiom, generated placeholder constant, or unsafe declaration |
| `lake env lean --version` from `Formalizations/Lean` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD^{commit} HEAD^{tree}` | 0 | Pinned mathlib `8a178386...eea95`, tree `bdc39a31...2c19e5c2b` |
| `git diff --check -- Stage1_Instances/THM-M-1277` before artifacts | 0 | Existing target tree had no whitespace errors |
| Structured JSON predicate and syntax check | 0 | The blocker binds this item/base, blocked state, noncompletion boundary, exact countertheorem, empty accepted receipts, two changed paths, and self-test absence |
| Scoped added-file whitespace checks | 1 per file, expected | Both commands report only added-file status and no whitespace diagnostic |
| `test ! -e .stage1-worker-selftest.json` | 0 | No positive proof self-test manifest was written |

Exact Lean recipe, run from `Formalizations/Lean`:

```bash
set -u
START=$(date --iso-8601=seconds)
TMP=$(mktemp -d /tmp/thm-m-1277-proof-f53223e6-slot41.XXXXXX)
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
END=$(date --iso-8601=seconds)
cat "$TMP/statement.out"
cat "$TMP/proof.out"
sha256sum "$TMP/Statement.olean" "$TMP/Proof.olean" \
  "$TMP/statement.out" "$TMP/proof.out"
exit "$s2"
```

The replay began at `2026-07-15T17:59:16+08:00` and ended at
`2026-07-15T17:59:59+08:00`. Fresh hashes were:

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
nonempty-domain scope text, explicitly crosswalk the selected
`Function.support` convention against the source meaning of compact support in
`Omega`, rerun exact-expression identity and mutation tests, and publish a
versioned obligation registry, typed graphs, and validation specifications for
the new fingerprint before another proof attempt.

The remaining root cut set is `S56-M-1277-STATEMENT`. Because the assigned
positive proof phase is not genuinely self-tested as complete,
`.stage1-worker-selftest.json` is deliberately absent and the item remains
`[ ]`.
