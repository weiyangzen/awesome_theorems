# THM-M-1277 proof-phase recheck at current base

Item: `S56-M-1277-PROOF`

Date: `2026-07-15` (`Asia/Shanghai`)

Base revision: `71bcc40e66b043742dafd4e66c6a868ff2b2a6ad`

Base tree: `741fca489134e06814154a72672b15212ec28c19`

Worker slot: `55`

## Verdict

`blocked`. No legal positive proof body can inhabit the exact frozen target:
the tracked, placeholder-free declaration

```text
Stage1Rev56.THMM1277.not_statement :
  Not Stage1Rev56.THMM1277.Statement
```

kernel-checks at trust level zero against a freshly emitted
`Statement.olean`. Independent proof review and a separate fresh Lean replay
reproduced the declaration type, axiom report, and generated output hashes.

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
an illegal substitution. The dossier's recorded vector remains
`[H1, M3, R3]`; `M5` is only the proposed machine diagnosis for the exact
statement mismatch. No positive proof receipt, obligation closure, audit
completion, or theorem completion is claimed. The pre-existing negative
proof body is retained as real blocker evidence; no proof source changed in
this run.

The statement prerequisite also lacks the required normalized elaborated-
expression fingerprint and mutation-test evidence. In addition,
`scope-map.md` says nonemptiness is unnecessary while the formal target,
statement record, and README require it because sharpness is false on the
empty domain. The existing positive obligation registry and typed graphs
predate the refutation. Their structural validator reports an open `M3` root;
its checked conditional branch composer cannot supply the false sharpness
premise.

Independently, the assigned proof node's prerequisite
`S56-M-1277-OBLIGATION_TREE` is still provisional `[_]`, not master-accepted
`[x]`. Dependency-ordered acceptance is therefore unavailable.

Before this run, the target contained 21 proof-recheck JSON files, 22
proof-recheck Markdown files, and one separate structured `proof-blocker.json`.
Those counts prove repeated unresolved rechecks, not scheduler tick identity;
the authoritative DAG still records zero proof attempts. The master must
reconcile its private tick ledger against the five-unresolved-tick split rule.
Retrying the unchanged positive proof node cannot succeed; it needs upstream
statement repair or explicit redirection to the checked refutation.

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
| `git status --short` (before edits) | 0 | Only the automation-provided untracked `Formalizations/Lean/.lake` symlink was present; the owned path and root self-test path were clean |
| `python3 Stage1_Instances/THM-M-1277/check_obligation_tree.py` | 0 | `PASS`: 24 obligations and 48 typed edges; denominator `e17739e...f60575`; stale positive root open `M3` |
| Fresh temporary-olean recipe below | 0 | `Statement : Prop` and `not_statement : Not Statement` elaborated at trust level zero; every printed axiom set was exactly `propext`, `Classical.choice`, and `Quot.sound` |
| Independent fresh trust-zero replay by a read-only worker | 0 | Reproduced the exact countertheorem, axiom report, and all three generated hashes |
| `rg -n '\b(sorry|admit|sorryAx)\b\|^[[:space:]]*(axiom\|unsafe)\b' Stage1_Instances/THM-M-1277 --glob '*.lean'` | 1, expected | No prohibited placeholder, declared axiom, generated placeholder constant, or unsafe declaration |
| `/home/sansha-2/.elan/toolchains/leanprover--lean4---v4.29.0/bin/lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD^{commit} HEAD^{tree}` | 0 | Pinned mathlib `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b` |
| `python3 -m json.tool <current-blocker> >/dev/null` plus `jq -e <blocker-invariants> <current-blocker> >/dev/null` | 0 | The structured blocker is valid JSON and records this item/base, blocked state, noncompletion, and self-test absence |
| `git diff --no-index --check /dev/null <new-artifact>` for each new JSON/Markdown file | 1 per file, expected | Both commands reported only added-file status and produced no whitespace diagnostic |
| `test ! -e .stage1-worker-selftest.json` | 0 | No positive proof self-test manifest was written |

Exact Lean recipe, run from `Formalizations/Lean`:

```bash
set -u
TMP=$(mktemp -d /tmp/thm-m-1277-current-head.XXXXXX)
cleanup(){ rm -rf "$TMP"; }
trap cleanup EXIT
BASE=$(lake env printenv LEAN_PATH)
lake env lean --trust=0 -t0 --root=../.. \
  -o "$TMP/Statement.olean" \
  ../../Stage1_Instances/THM-M-1277/Statement.lean \
  >"$TMP/statement.out" 2>&1
s1=$?
if [ "$s1" -eq 0 ]; then
  LEAN_PATH="$TMP:$BASE" lake env lean --trust=0 -t0 --root=../.. \
    ../../Stage1_Instances/THM-M-1277/Proof.lean \
    >"$TMP/proof.out" 2>&1
  s2=$?
else
  s2=99
fi
printf 'TMP_BASENAME=%s\nSTATEMENT_EXIT=%s\nPROOF_EXIT=%s\n' \
  "$(basename "$TMP")" "$s1" "$s2"
printf '%s\n' '--- statement output ---'
cat "$TMP/statement.out"
printf '%s\n' '--- proof output ---'
cat "$TMP/proof.out" 2>/dev/null || true
printf '%s\n' '--- hashes ---'
sha256sum "$TMP/Statement.olean" "$TMP/statement.out" "$TMP/proof.out" \
  2>/dev/null || true
exit "$s2"
```

The fresh output hashes were
`84f541c01763ee25facdce4cfc28cc3380e52a5f55d9c3c295c0cefe99159e63`
for `Statement.olean`,
`593f08c48172c08e242b8073f6550e2d3f100806c26d98d9ddb387dc8a1fb3a8`
for statement output, and
`2f47380b9e5a682199aa7e433ad923111d99b9612a1d9bb3a050fa4f8c10d9c8`
for proof output. The temporary directory was removed.

## Retry Condition

The first failed gate is exact canonical statement correctness. Reopen
`S56-M-1277-STATEMENT`, use the intended smooth order unambiguously as
`((top : ENat) : WithTop ENat)` (scoped notation `infinity`), reconcile the
nonempty-domain scope text, rerun exact-expression identity and mutation
tests, and publish a versioned obligation registry, typed graphs, and
validation specifications for the new fingerprint before another proof
attempt.

The remaining root cut set is `S56-M-1277-STATEMENT`. Because the assigned
positive proof phase is not genuinely self-tested as complete,
`.stage1-worker-selftest.json` is deliberately absent and the item remains
`[ ]`.
