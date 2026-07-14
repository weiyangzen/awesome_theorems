# THM-M-0120 proof-phase recheck at base `3f555cfc`

Item: `S56-M-0120-PROOF`

Intent: `prove`

Recheck date: 2026-07-15 (Asia/Shanghai)

Base revision: `3f555cfc0879cb7c42e83d6bcf7b9e3e09997e58`

Base tree: `e8837f7e0722548e2b35e901d9d974797097635e`

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

This refutes the current abstract Lean encoding, not the mathematical Mori cone theorem. Replacing
the target, narrowing its binders, or adding `Conclusion` (or any output package) as an assumption
would be a substitution or a circular repair and is outside this proof item's ownership. The item
therefore remains `[ ]`; no proof receipt, provisional state, audit completion, theorem completion,
release decision, or master acceptance is claimed.

## Failed Gate And Retry

The first failed gate is exact-target consistency at `M0120-S-DATA` and
`M0120-S-BOUNDARY`. `S56-M-0120-STATEMENT` must be reopened so that the numerical curve space,
effective cone, canonical pairing, rational curves, and contractions are defined intrinsically or
connected to the projective klt pair by noncircular semantic laws. Positive proof execution may
resume only after the repaired target has a new accepted expression fingerprint, anchor audit, and
obligation-registry version.

## Scoped Validation

All checks used this worker clone and the existing pinned Lean artifacts. No `lake update`, build,
clone, fetch, dependency mutation, or network operation was performed. The automation-provided
untracked `Formalizations/Lean/.lake` symlink points at the canonical pinned artifacts, so this is
dirty, nonrelease blocker evidence.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0120` | 0 | rank 39; lifecycle planned; L0/rework-required; legacy artifacts unaccepted; theorem incomplete |
| `python3 Stage1_Instances/THM-M-0120/check_statement.py` | 0 | canonical expression SHA-256 `074d45c3...d88cfd`; removed-klt, absolute-base, and no-contractions mutations all differed |
| `python3 Stage1_Instances/THM-M-0120/check_anchor_audit.py` | 0 | immutable local candidates, clean pinned mathlib, eight Lean probes, and the `M3` boundary agreed |
| `python3 Stage1_Instances/THM-M-0120/check_obligation_tree.py` | 0 | 25 obligations and 62 typed edges passed; denominator `69152b16...63081b1`; root remains `M3`; substantive packages remain open |
| isolated `lake env lean --trust=0 -t0` recipe below | 0 | exact statement and countermodel elaborated; axiom report `[propext, Classical.choice, Quot.sound]` |
| `lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `test -z "$(git -C Formalizations/Lean/.lake/packages/mathlib status --porcelain)"` | 0 | pinned mathlib worktree clean |
| placeholder scan below | 1 | no matches; exit 1 is ripgrep's no-match result |
| artifact JSON validation and blocker-invariant check | 0 | JSON parsed; identity, base/tree, hashes, blocked state, empty receipts, failed gate, retry condition, and self-test absence agreed |
| scoped tracked and no-index whitespace checks | 0 | no whitespace errors; each no-index check returned its expected content-difference exit 1 |
| `test ! -e .stage1-worker-selftest.json` | 0 | completion self-test manifest deliberately absent |

Exact artifact invariant check:

```bash
python3 - <<'PY'
import hashlib, json, pathlib, subprocess
root = pathlib.Path('.')
p = root / 'Stage1_Instances/THM-M-0120/proof-recheck-2026-07-15-head-3f555cfc.json'
d = json.loads(p.read_text())
assert d['item_id'] == 'S56-M-0120-PROOF'
assert d['theorem_id'] == 'THM-M-0120'
assert d['base_revision'] == subprocess.check_output(
    ['git', 'rev-parse', 'HEAD'], text=True).strip()
assert d['base_tree'] == subprocess.check_output(
    ['git', 'rev-parse', 'HEAD^{tree}'], text=True).strip()
assert d['verdict'] == 'blocked' and d['state'] == '[ ]'
assert d['proof_body_added'] is False
assert d['positive_root_proof_exists'] is False
assert d['root_closed'] is False
assert d['audit_complete'] is False
assert d['theorem_complete'] is False
assert d['accepted_receipt_ids'] == []
assert d['content_addressed_recipe_ids'] == []
assert d['content_addressed_receipt_ids'] == []
assert d['selftest_manifest_written'] is False
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

Exact Lean countermodel recipe:

```bash
set -euo pipefail
repo_root=$PWD
target=$repo_root/Stage1_Instances/THM-M-0120
lean_root=$repo_root/Formalizations/Lean
tmp=$(mktemp -d /tmp/thm-m-0120-proof-head3f555cfc.XXXXXX)
log=$(mktemp /tmp/thm-m-0120-proof-head3f555cfc-log.XXXXXX)
trap 'rm -rf "$tmp" "$log"' EXIT HUP INT TERM
cp "$target/Statement.lean" "$tmp/Statement.lean"
cp "$target/Proof.lean" "$tmp/Proof.lean"
cd "$lean_root"
base=$(lake env printenv LEAN_PATH)
set +e
{
  LEAN_NUM_THREADS=1 timeout --foreground 300 \
    lake env lean --trust=0 -t0 --root="$tmp" \
      -o "$tmp/Statement.olean" "$tmp/Statement.lean"
  statement_status=$?
  printf 'STATEMENT_EXIT=%s\n' "$statement_status"
  if [ "$statement_status" -eq 0 ]; then
    LEAN_PATH="$tmp:$base" LEAN_NUM_THREADS=1 timeout --foreground 300 \
      lake env lean --trust=0 -t0 --root="$tmp" \
        -o "$tmp/Proof.olean" "$tmp/Proof.lean"
    proof_status=$?
  else
    proof_status=125
  fi
  printf 'PROOF_EXIT=%s\n' "$proof_status"
} >"$log" 2>&1
set -e
cat "$log"
statement_status=$(sed -n 's/^STATEMENT_EXIT=//p' "$log" | tail -1)
proof_status=$(sed -n 's/^PROOF_EXIT=//p' "$log" | tail -1)
sha256sum "$log"
test -f "$tmp/Statement.olean"
test -f "$tmp/Proof.olean"
sha256sum "$tmp/Statement.olean" "$tmp/Proof.olean"
test "$statement_status" = 0
test "$proof_status" = 0
```

The relevant output was:

```text
def Stage1Instances.THMM0120.MoriConeTheoremTarget.{u, uK, uN, uC} : Prop :=
forall (D : Stage1Instances.THMM0120.ConeTheoremData.{u, uK, uN, uC}),
  @AlgebraicGeometry.IsProper.{u} D.X D.S D.f ->
    D.definedOverBaseField -> D.projective -> D.normal -> D.qFactorial -> D.klt -> D.Conclusion
STATEMENT_EXIT=0
'Stage1Instances.THMM0120.Proof.not_moriConeTheoremTarget' depends on axioms: [propext, Classical.choice, Quot.sound]
PROOF_EXIT=0
```

The arrows above are shown as ASCII; Lean printed the corresponding Unicode arrows.

The complete captured output had SHA-256
`d1c53ea898cc37d74a3c615477e00bc35b4cd8ab287349b05fb107d95fe0721b`; the temporary
`Statement.olean` had SHA-256
`f0a4ec2437554ebd1dbb7790e87258f56104c31916b9cb1462e189def53b3d16`, and the temporary
`Proof.olean` had SHA-256
`cbc71754bd5c087c618b35ed31902741ef312d1be2f6adc7ddfbb0306e8be3ec`, before cleanup.

Exact placeholder scan:

```bash
rg -n --pcre2 '\b(?:sorry|admit|axiom)\b|sorryAx|unsafe' \
  Stage1_Instances/THM-M-0120 -g '*.lean'
```

The unchanged content inputs at this base are: statement SHA-256
`69eabc83cd8b7fe8fa34d598c9de890eea09d8ee8357d551abf3e7727444fd6b`, countermodel
proof SHA-256 `e5c342e97885f6a533fada4b928685ea4c2e888baa5e21699a454049f02f29ab`, registry
SHA-256 `cd24f57d66422f500f17b348bed362dddcdf032447861f2560518f95c1a48a2d`, typed graphs
SHA-256 `9ca86f175b3413edd03fec0971bb165c9dd0396ade874a0b0c0c674ac861e23f`, and anchor audit
SHA-256 `71ff1889e55e0f4387697db69ff7acae110f0530f94879ef68ae06370475090d`.

No `.stage1-worker-selftest.json` is written because the assigned positive proof deliverable is
blocked rather than genuinely self-tested as complete.
