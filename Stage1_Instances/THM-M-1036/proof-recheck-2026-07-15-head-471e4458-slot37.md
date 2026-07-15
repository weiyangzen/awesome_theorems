# THM-M-1036 proof-phase recheck at `471e4458` (slot37)

Item: `S56-M-1036-PROOF`

Date: `2026-07-15` (`Asia/Shanghai`)

Base revision: `471e4458269351ee096972776c478d019941b679`.

Base tree: `e30e1cefce39148420ccc4525b726d57f58ee94b`.

Packet owner and attestor: Stage1 worker slot37 local process. This is unsigned,
nonrelease, provisional blocker evidence pending independent master review. It
was validated at `2026-07-15T20:19:12+08:00` and must be reviewed before any
acceptance, statement repair, proof retry, or downstream validation. Changes to
the repository tree, target/graph/validation artifacts, toolchain/dependencies,
trust policy, task state, or upstream source status make it stale. The incident
path is master reconciliation of the five-tick split rule followed by statement
repair or counterexample/barrier redirection. Full support, supersession,
revocation, and invalidation metadata is in the paired JSON packet.

## Verdict

`blocked`. No legal positive proof body can inhabit the exact frozen target.
The tracked, placeholder-free declaration

```text
Stage1Instances.THM_M_1036.Counterexample.not_sdeExistenceUniquenessTarget :
  Not Stage1Instances.THM_M_1036.SdeExistenceUniquenessTarget.{0}
```

kernel-checks at trust level zero. `IntegralSemantics` supplies arbitrary
`timeIntegral` and `itoIntegral` operations, while `standard_time_integral`
and `standard_ito_integral` are bare propositions imposing no laws on either
operation. The target nevertheless quantifies over every such semantics and
concludes strong existence after receiving proofs of those propositions.

`Counterexample.lean` makes both propositions true, uses `Unit` with its Dirac
probability measure, state dimension one and noise dimension zero, and defines
`timeIntegral f _ omega = f 0 omega + 1`. At `t = 0`, the required integral
equation yields `x = x + 1` in coordinate zero. Any positive proof of the
universe-polymorphic target would therefore contradict its checked
universe-zero specialization.

This refutes the frozen Lean encoding, not the classical SDE theorem. Proving a
repaired, strengthened, or narrower statement here would substitute the
assigned theorem. The existing `root_of_existence_and_uniqueness` declaration
is only conditional assembly: it assumes complete existence and uniqueness
packages and supplies neither.

The item remains `[ ]`. No positive proof body, proof receipt, provisional
state, audit completion, validation completion, release, theorem completion,
or master acceptance is claimed. Its prerequisite obligation-tree item is
still worker-provisional `[_]`, not master-accepted `[x]`.

## Failed Gate And Retry

The first failed gate is
`S56-5.1-EXACT-TARGET-CONSISTENCY / M1036-X-INTEGRAL-SEMANTICS`. The minimal
decisive inconsistency/repair cut is `M1036-X-INTEGRAL-SEMANTICS`; its
invalidated/open chain continues through limit construction and existence
assembly to `M1036-ROOT`.

The frozen registry projects `[H2, M3, R3]`. This recheck proposes machine
classification `M5`, so `[H2, M3, R3] -> [H2, M5, R3]`, without changing
accepted state. `H2` stays unchanged because the countermodel diagnoses the
formal encoding rather than the human mathematical theorem.

Replace the two bare semantic flags with a source-faithful, law-bearing
standard time/Ito integral construction or exact sufficient laws. Then publish
a new statement fingerprint and freshly freeze and master-accept the statement,
anchor audit, obligation registry, and typed graphs before proof work resumes.
An explicit redirect to the checked counterexample/barrier target is the other
legal route.

This directory already contained 47 `proof-recheck-*.json` records and 48
structured blockers when `proof-blocker.json` was included, while the DAG still
records proof `attempts: 0` and no children. File counts do not prove distinct
scheduler ticks, but the master must reconcile them and apply the five-tick
split rule. Another unchanged positive-proof retry is not useful.

## Validation

All checks ran in this worker clone. The scheduler-provided untracked
`Formalizations/Lean/.lake` symlink was treated as read-only. No `lake update`,
`lake build`, dependency clone/fetch, network action, or deliberate `.lake`
mutation occurred. Generated Lean output stayed under `/tmp` and was removed.
The untracked cache symlink makes this nonrelease evidence.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and all 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required`. |
| `python3 scripts/stage1_target.py show THM-M-1036` | 0 | Rank 229; planned; legacy artifacts unaccepted; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1036/check_statement.py` | 0 | Statement elaborated; three mutations differed; fingerprint `3717483261012dabe49b9787ad1336001262cbdf7791dfd1094c217298ac8954`; mathlib pin matched. |
| `python3 Stage1_Instances/THM-M-1036/check_obligation_tree.py` | 0 | 18 obligations and 47 typed edges passed; denominator `7e425556f1efaf61324a9d453d76aa833189110b116824aaf32c2f390b328e69`; root open at M3. |
| `cd Formalizations/Lean && timeout --foreground 60 lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`. |
| Isolated trust-zero Lean replay below | 0 | `Statement.lean` and `Counterexample.lean` elaborated. Both negative declarations reported exactly `[propext, Classical.choice, Quot.sound]`; output SHA-256 `4b11faa31e8ad2a6401448d63176322e46bf814ff423c23016d4c7bfea426a55`. |
| Prohibited-device scan over owned `*.lean` | 1 | Expected no-match exit: no `sorry`, `admit`, axiom declaration, unsafe/opaque/extern escape, `sorryAx`, `implemented_by`, or `native_decide`. |
| `python3 -m json.tool` plus packet invariant assertions | 0 | Structured blocker JSON parsed and all identity, hash, state, axiom, completion, and self-test-absence invariants agreed. |
| Scoped `git diff --check` and the exact new-file no-index wrapper below | 0 | Tracked check returned 0. Each raw no-index command returned expected new-file-difference exit 1 with no whitespace diagnostic; the wrapper required those results and returned 0. |
| `test ! -e .stage1-worker-selftest.json` | 0 | The completion-only self-test manifest is absent. |

The narrow kernel replay used the repository's existing pinned Lake closure:

```bash
set -euo pipefail
root=$PWD
target=$root/Stage1_Instances/THM-M-1036
cd "$root/Formalizations/Lean"
tmp=$(mktemp -d /tmp/thm-m-1036-proof-head-471e4458-slot37.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
cp "$target/Statement.lean" "$tmp/Statement.lean"
cp "$target/Counterexample.lean" "$tmp/Counterexample.lean"
LEAN_NUM_THREADS=1 nice -n 15 timeout --foreground 900 lake env lean \
  --trust=0 -t0 --root="$tmp" -o "$tmp/Statement.olean" \
  "$tmp/Statement.lean" >"$tmp/statement.out" 2>&1
lean_path=$(lake env printenv LEAN_PATH)
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" nice -n 15 \
  timeout --foreground 900 lake env lean --trust=0 -t0 --root="$tmp" \
  "$tmp/Counterexample.lean" >"$tmp/counterexample.out" 2>&1
cat "$tmp/statement.out" "$tmp/counterexample.out" >"$tmp/kernel-output.txt"
sha256sum "$tmp/kernel-output.txt" "$tmp/Statement.olean"
```

Exact environment and pinned-dependency probes were:

```bash
root=$PWD
( cd "$root/Formalizations/Lean" && \
  timeout --foreground 60 lake env lean --version && \
  lake --version && lake env which lean )
git -C "$root/Formalizations/Lean/.lake/packages/mathlib" rev-parse HEAD
git -C "$root/Formalizations/Lean/.lake/packages/mathlib" rev-parse HEAD^{tree}
git -C "$root/Formalizations/Lean/.lake/packages/flt-regular" rev-parse HEAD
git -C "$root/Formalizations/Lean/.lake/packages/flt-regular" rev-parse HEAD^{tree}
lean_bin=$(cd "$root/Formalizations/Lean" && lake env which lean)
sha256sum "$lean_bin"
printf '%s\n' "$(readlink "$root/Formalizations/Lean/.lake")" | sha256sum
```

The exact prohibited-device scan (raw exit 1, expected no match) was:

```bash
rg -n --pcre2 \
  '^\s*(?:sorry|admit|axiom)(?:\s|$)|\bsorryAx\b|^\s*(?:unsafe|opaque|extern)\s|\bimplemented_by\b|\bnative_decide\b' \
  Stage1_Instances/THM-M-1036 --glob '*.lean'
```

It ran from `2026-07-15T20:18:27+08:00` through
`2026-07-15T20:19:12+08:00`. Statement and counterexample outputs hashed
`052c267144c1dc46129f5c40f97db91627a3025fea97d86a001e8ee1bd004673`
and `e5e5d6a071019cdb10d072baefb1e7f05d0da040dcd61a457458decb0d897cfe`.
The generated `Statement.olean` hashed
`a3ec6b23bd506207b3cd0aff4175153a56fc3aa87f37cfc0466d3fe46a4812e4`.
The paired JSON packet binds all source, environment, object, and output hashes.

Final structured and whitespace checks used this exact wrapper (the invariant
script is included rather than represented by a label):

```bash
python3 -m json.tool \
  Stage1_Instances/THM-M-1036/proof-recheck-2026-07-15-head-471e4458-slot37.json \
  >/dev/null
python3 - <<'PY'
import hashlib, json, os, subprocess
p = 'Stage1_Instances/THM-M-1036/proof-recheck-2026-07-15-head-471e4458-slot37.json'
d = json.load(open(p))
assert d['schema_version'] == 'stage1-proof-blocker/1.1'
assert d['item_id'] == 'S56-M-1036-PROOF'
assert d['theorem_id'] == 'THM-M-1036'
assert d['base_revision'] == subprocess.check_output(
    ['git', 'rev-parse', 'HEAD'], text=True).strip()
assert d['base_tree'] == subprocess.check_output(
    ['git', 'rev-parse', 'HEAD^{tree}'], text=True).strip()
assert d['verdict'] == 'blocked' and d['state'] == '[ ]'
assert d['canonical_statement_fingerprint'] == \
    '3717483261012dabe49b9787ad1336001262cbdf7791dfd1094c217298ac8954'
assert d['countermodel_exact_type'] == \
    'Not Stage1Instances.THM_M_1036.SdeExistenceUniquenessTarget.{0}'
for name, want in d['source_hashes'].items():
    prefix = ('Formalizations/Lean/' if name in
              {'lean-toolchain', 'lake-manifest.json'} else
              'Stage1_Instances/THM-M-1036/')
    got = hashlib.sha256(open(prefix + name, 'rb').read()).hexdigest()
    assert got == want, (prefix + name, got, want)
assert d['kernel_recheck']['reported_axioms'] == \
    ['propext', 'Classical.choice', 'Quot.sound']
for field in ['proof_body_added', 'positive_root_proof_exists',
              'proof_phase_complete', 'root_closed', 'audit_complete',
              'theorem_complete', 'selftest_manifest_written']:
    assert not d[field]
for field in ['accepted_receipt_ids', 'content_addressed_recipe_ids',
              'content_addressed_receipt_ids']:
    assert d[field] == []
assert not os.path.exists('.stage1-worker-selftest.json')
assert all(os.path.exists(x) for x in d['changed_paths'])
PY
git diff --check -- Stage1_Instances/THM-M-1036
for f in \
  Stage1_Instances/THM-M-1036/proof-recheck-2026-07-15-head-471e4458-slot37.json \
  Stage1_Instances/THM-M-1036/proof-recheck-2026-07-15-head-471e4458-slot37.md; do
  if git diff --no-index --check /dev/null "$f" \
      >/tmp/thm-m-1036-noindex-check.out 2>&1; then
    code=0
  else
    code=$?
  fi
  test "$code" -eq 1
  test ! -s /tmp/thm-m-1036-noindex-check.out
done
rm -f /tmp/thm-m-1036-noindex-check.out
test ! -e .stage1-worker-selftest.json
```

## Status Boundary

This current-base packet is durable blocker evidence, not a proof receipt. It
does not satisfy `S56-M-1036-PROOF` or support any completion claim. Because
the assigned proof phase is not genuinely self-tested complete,
`.stage1-worker-selftest.json` is deliberately absent.
