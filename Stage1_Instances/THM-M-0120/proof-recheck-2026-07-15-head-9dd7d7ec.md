# THM-M-0120 proof-phase recheck at base `9dd7d7ec`

Item: `S56-M-0120-PROOF`

Intent: `prove`

Recheck date: 2026-07-15 (Asia/Shanghai)

Base revision: `9dd7d7ec7d399cdac6abb2a51d3ea55ed5f4b8ca`

Base tree: `af8d932b6def693afe67a997e2be4c6e813036f2`

## Verdict

`blocked`. No positive proof body can truthfully inhabit the exact frozen proposition. The existing
placeholder-free declaration

```text
Stage1Instances.THMM0120.Proof.not_moriConeTheoremTarget :
  Not (Stage1Instances.THMM0120.MoriConeTheoremTarget.{0, 0, 0, 0})
```

was recompiled from fresh copies of `Statement.lean` and `Proof.lean` with Lean trust level zero.
It supplies a concrete countermodel to the universal target. The proper morphism is the identity on
`Spec (AlgebraicClosure Rat)`, and every explicit proposition hypothesis is true, but the numerical
data are independent: `N1 = Real`, `moriCone = {-1}`, `canonicalPairing = LinearMap.id`, and
`RationalCurve = Empty`. The required decomposition of `-1` then produces a nonnegative component
that is both `-1` and nonnegative, a contradiction.

Refuting the target at universe specialization `{0, 0, 0, 0}` rules out a universe-polymorphic
positive proof. This refutes the frozen abstract Lean encoding, not the mathematical Mori cone
theorem. Replacing the target, narrowing its binders, or adding `Conclusion` or any output package
as an assumption would be a substituted or circular repair and is outside this proof item. The item
therefore remains `[ ]`; no proof receipt, provisional state, audit completion, theorem completion,
release decision, or master acceptance is claimed.

## Failed Gate And Retry

The first failed gate is exact-target consistency at `M0120-S-DATA` and
`M0120-S-BOUNDARY`. `S56-M-0120-STATEMENT` must be reopened so that the numerical curve space,
effective cone, canonical pairing, rational curves, and contractions are defined intrinsically or
connected to the projective klt pair by noncircular semantic laws. Positive proof execution may
resume only after the repaired target has a new accepted expression fingerprint, anchor audit, and
obligation-registry version. The prerequisite obligation-tree item is currently only provisional
`[_]`, not master-accepted.

## Scoped Validation

All successful checks used this worker clone and the existing pinned Lean artifacts. No
`lake update`, build, clone, fetch, dependency mutation, or network operation was performed. The
automation-provided untracked `Formalizations/Lean/.lake` symlink points at the canonical pinned
artifacts, so this is dirty, nonrelease blocker evidence.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0120` | 0 | rank 39; lifecycle planned; L0/rework-required; legacy artifacts unaccepted; theorem incomplete |
| `python3 Stage1_Instances/THM-M-0120/check_anchor_audit.py` | 0 | immutable local candidates, clean pinned mathlib, eight Lean probes, and the `M3` boundary agreed |
| `python3 Stage1_Instances/THM-M-0120/check_obligation_tree.py` | 0 | 25 obligations and 62 typed edges passed; denominator `69152b16...63081b1`; root remains `M3`; substantive packages remain open |
| isolated `lake env lean --trust=0 -t0` recipe below | 0 | exact statement and countermodel elaborated; axiom report `[propext, Classical.choice, Quot.sound]` |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` | 0 | revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`; tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b` |
| `test -z "$(git -C Formalizations/Lean/.lake/packages/mathlib status --porcelain)"` | 0 | pinned mathlib worktree clean |
| placeholder scan below | 1 | no matches; exit 1 is ripgrep's no-match result |
| JSON parse and artifact invariant check below | 0 | identity, base/tree, source hashes, fail-closed state, direct Lean exits, exact cut set, empty receipts, and self-test absence agreed |
| scoped tracked and no-index whitespace checks | 0 / 1 / 1 | no whitespace errors; the JSON and Markdown no-index checks each returned exit 1 only because the new file differs from `/dev/null` |
| `test ! -e .stage1-worker-selftest.json` | 0 | completion self-test manifest deliberately absent |

Exact Lean countermodel recipe:

```bash
set -u
repo_root=$PWD
target=$repo_root/Stage1_Instances/THM-M-0120
lean_root=$repo_root/Formalizations/Lean
tmp=$(mktemp -d /tmp/thm-m-0120-proof-head9dd7d7ec.XXXXXX)
log=$(mktemp /tmp/thm-m-0120-proof-head9dd7d7ec-log.XXXXXX)
trap 'rm -rf "$tmp" "$log"' EXIT HUP INT TERM
cp "$target/Statement.lean" "$tmp/Statement.lean"
cp "$target/Proof.lean" "$tmp/Proof.lean"
cd "$lean_root"
base=$(lake env printenv LEAN_PATH)
LEAN_NUM_THREADS=1 timeout --foreground 300 \
  lake env lean --trust=0 -t0 --root="$tmp" \
    -o "$tmp/Statement.olean" "$tmp/Statement.lean" >"$log" 2>&1
statement_status=$?
proof_status=125
if [ "$statement_status" -eq 0 ]; then
  LEAN_PATH="$tmp:$base" LEAN_NUM_THREADS=1 timeout --foreground 300 \
    lake env lean --trust=0 -t0 --root="$tmp" \
      -o "$tmp/Proof.olean" "$tmp/Proof.lean" >>"$log" 2>&1
  proof_status=$?
fi
printf 'STATEMENT_EXIT=%s\nPROOF_EXIT=%s\n' \
  "$statement_status" "$proof_status" >>"$log"
cat "$log"
sha256sum "$tmp/Statement.olean" "$tmp/Proof.olean"
test "$statement_status" = 0
test "$proof_status" = 0
```

The relevant observed output was:

```text
def Stage1Instances.THMM0120.MoriConeTheoremTarget.{u, uK, uN, uC} : Prop :=
forall (D : Stage1Instances.THMM0120.ConeTheoremData.{u, uK, uN, uC}),
  @AlgebraicGeometry.IsProper.{u} D.X D.S D.f ->
    D.definedOverBaseField -> D.projective -> D.normal -> D.qFactorial -> D.klt -> D.Conclusion
'Stage1Instances.THMM0120.Proof.not_moriConeTheoremTarget' depends on axioms:
[propext, Classical.choice, Quot.sound]
STATEMENT_EXIT=0
PROOF_EXIT=0
```

The arrows above are shown as ASCII; Lean printed the corresponding Unicode arrows. The temporary
`Proof.olean` had SHA-256
`cbc71754bd5c087c618b35ed31902741ef312d1be2f6adc7ddfbb0306e8be3ec` before cleanup. The execution
harness did not return the transient log hash or `Statement.olean` hash, so this receipt does not
claim either hash for this run.

Exact placeholder scan:

```bash
rg -n --pcre2 '\b(?:sorry|admit|axiom)\b|sorryAx|unsafe' \
  Stage1_Instances/THM-M-0120 -g '*.lean'
```

Exact artifact invariant check:

```bash
python3 - <<'PY'
import hashlib, json, pathlib, subprocess
root = pathlib.Path('.')
p = root / 'Stage1_Instances/THM-M-0120/proof-recheck-2026-07-15-head-9dd7d7ec.json'
d = json.loads(p.read_text())
assert d['item_id'] == 'S56-M-0120-PROOF'
assert d['theorem_id'] == 'THM-M-0120'
assert d['base_revision'] == subprocess.check_output(
    ['git', 'rev-parse', 'HEAD'], text=True).strip()
assert d['base_tree'] == subprocess.check_output(
    ['git', 'rev-parse', 'HEAD^{tree}'], text=True).strip()
assert d['verdict'] == 'blocked' and d['state'] == '[ ]'
for key in ('proof_body_added', 'positive_root_proof_exists', 'root_closed',
            'audit_complete', 'theorem_complete', 'selftest_manifest_written'):
    assert d[key] is False, key
for key in ('accepted_receipt_ids', 'content_addressed_recipe_ids',
            'content_addressed_receipt_ids'):
    assert d[key] == [], key
assert d['kernel_recheck']['statement_exit_code'] == 0
assert d['kernel_recheck']['proof_exit_code'] == 0
assert d['remaining_root_cut_set'] == ['M0120-S-DATA', 'M0120-S-BOUNDARY']
for name, expected in d['source_hashes'].items():
    if name in {'lake-manifest.json', 'lean-toolchain'}:
        q = root / 'Formalizations/Lean' / name
    else:
        q = root / 'Stage1_Instances/THM-M-0120' / name
    assert hashlib.sha256(q.read_bytes()).hexdigest() == expected, name
assert not (root / '.stage1-worker-selftest.json').exists()
print('PASS: current-base blocker identity, hashes, fail-closed state, and self-test absence agree')
PY
```

The unchanged content inputs at this base are: statement SHA-256
`69eabc83cd8b7fe8fa34d598c9de890eea09d8ee8357d551abf3e7727444fd6b`, countermodel proof
SHA-256 `e5c342e97885f6a533fada4b928685ea4c2e888baa5e21699a454049f02f29ab`, registry SHA-256
`cd24f57d66422f500f17b348bed362dddcdf032447861f2560518f95c1a48a2d`, typed graphs SHA-256
`9ca86f175b3413edd03fec0971bb165c9dd0396ade874a0b0c0c674ac861e23f`, and anchor audit SHA-256
`71ff1889e55e0f4387697db69ff7acae110f0530f94879ef68ae06370475090d`.

An auxiliary `python3 Stage1_Instances/THM-M-0120/check_statement.py` mutation replay was interrupted
during severe shared-host memory and swap contention and is not credited. This does not weaken the
direct check above: `Statement.lean` itself elaborated successfully, printed the frozen exact target,
and the exact negative theorem imported that fresh olean and kernel-checked. The statement source
hash also matches the frozen statement record.

No `.stage1-worker-selftest.json` is written because the assigned positive proof deliverable is
blocked rather than genuinely self-tested as complete.
