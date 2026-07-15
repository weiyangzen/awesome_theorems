# THM-M-0120 proof-phase recheck at base `b98f9f43`

Item: `S56-M-0120-PROOF`

Intent: `prove`

Recheck date: 2026-07-15 (Asia/Shanghai)

Base revision: `b98f9f4368d78fd9f600d1619f36d55ed0d6f751`

Base tree: `166b9e92bfa134dcffd9b1c707f1e26cad247239`

## Verdict

`blocked`. No positive proof body can inhabit the exact frozen proposition. The existing
placeholder-free declaration

```text
Stage1Instances.THMM0120.Proof.not_moriConeTheoremTarget :
  Not (Stage1Instances.THMM0120.MoriConeTheoremTarget.{0, 0, 0, 0})
```

was freshly recompiled from `Statement.lean` and `Proof.lean` with Lean trust level zero. It supplies
a concrete countermodel to the universal target. The proper morphism is the identity on
`Spec (AlgebraicClosure Rat)`, and every explicit proposition hypothesis is true, but the statement
leaves its numerical data independent: `N1 = Real`, `moriCone = {-1}`, `canonicalPairing =
LinearMap.id`, and `RationalCurve = Empty`. The required decomposition of `-1` then produces a
nonnegative component that is both `-1` and nonnegative, a contradiction.

Refutation at universe specialization `{0, 0, 0, 0}` rules out a universe-polymorphic positive
proof. This refutes the current abstract Lean encoding, not the mathematical Mori cone theorem.
Replacing the target, narrowing its binders, or assuming `Conclusion` or any required output package
would be substitution or circularity and is outside this proof item's ownership. The item therefore
remains `[ ]`; no proof receipt, provisional state, audit completion, theorem completion, release
decision, or master acceptance is claimed. The predecessor obligation-tree item is only provisional
`[_]`, and the authoritative root remains `H2 / M3 / R4`; this attempt proposes `H5 / M5 / R4` only
for integration review.

## First Failed Gate And Retry

The first failed gate is `S56-5.1-EXACT-TARGET-CONSISTENCY`, at obligations `M0120-S-DATA` and
`M0120-S-BOUNDARY`. `S56-M-0120-STATEMENT` must be reopened. Its numerical curve space, effective
cone, canonical pairing, rational curves, and contractions must be defined intrinsically or tied to
the projective klt pair by noncircular semantic laws. After that repair, the integration lane must
freeze and accept a new expression fingerprint and obligation registry, then rerun the anchor audit
and proof work.

Before this recheck, the dossier contained 27 structured and 37 readable proof recheck artifacts,
plus two structured and two readable proof blocker artifacts, while the authoritative execution DAG
still recorded `attempts: 0` and no children. The master must reconcile whether and how those
artifacts map to execution ticks; if at least five do, section 10.2 requires splitting or redirecting
the task rather than scheduling another identical proof retry. This worker does not edit scheduler
authority.

## Scoped Validation

All commands ran in this worker clone against the existing pinned dependency artifacts. No
`lake update`, `lake build`, clone, fetch, network operation, or dependency mutation was performed.
The automation-provided untracked `Formalizations/Lean/.lake` symlink makes this nonrelease evidence.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0120` | 0 | rank 39; planned; L0/rework-required; legacy artifacts unaccepted; theorem incomplete |
| `python3 Stage1_Instances/THM-M-0120/check_statement.py` | 0 | expression SHA-256 `074d45c3...d88cfd`; all three structural mutations differed; pinned Lean 4.29.0 and mathlib `8a178386...a95` agreed |
| `python3 Stage1_Instances/THM-M-0120/check_anchor_audit.py` | 0 | immutable candidates, clean pinned mathlib, eight Lean probes, and the `M3` boundary agreed |
| `python3 Stage1_Instances/THM-M-0120/check_obligation_tree.py` | 0 | 25 obligations and 62 typed edges passed; denominator `69152b16...63081b1`; root remains `M3` |
| isolated pinned-mathlib `lake env lean --trust=0 -t0` recipe below | 0 | exact statement and countermodel elaborated; axiom report `[propext, Classical.choice, Quot.sound]` |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` | 0 | revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`; tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b` |
| `test -z "$(git -C Formalizations/Lean/.lake/packages/mathlib status --porcelain)"` | 0 | pinned mathlib worktree clean |
| placeholder scan below | 1 | no matches; exit 1 is ripgrep's no-match result |
| artifact JSON and blocker-invariant check | 0 | identity, hashes, fail-closed state, exact cut set, empty receipts, scheduler finding, and self-test absence agreed |
| temporary-index `git diff --check` over both new artifacts | 0 | no whitespace errors in either new owned-path artifact |
| `test ! -e .stage1-worker-selftest.json` | 0 | completion self-test manifest deliberately absent |

Exact Lean countermodel recipe:

```bash
set -u
repo_root=$PWD
target=$repo_root/Stage1_Instances/THM-M-0120
mathlib=$repo_root/Formalizations/Lean/.lake/packages/mathlib
tmp=$(mktemp -d /tmp/thm-m-0120-proof-head-b98f9f43-slot12.XXXXXX)
log=$(mktemp /tmp/thm-m-0120-proof-head-b98f9f43-slot12-log.XXXXXX)
trap 'rm -rf "$tmp" "$log"' EXIT HUP INT TERM
cp "$target/Statement.lean" "$target/Proof.lean" "$tmp/"
paths=$(find "$repo_root/Formalizations/Lean/.lake/packages" \
  -path '*/.lake/build/lib/lean' -type d -print | sort | paste -sd: -)
cd "$mathlib"
LEAN_PATH="$paths" LEAN_NUM_THREADS=1 timeout --foreground 300 \
  lake env lean --trust=0 -t0 --root="$tmp" \
    -o "$tmp/Statement.olean" "$tmp/Statement.lean" >"$log" 2>&1
statement_status=$?
proof_status=125
if [ "$statement_status" -eq 0 ]; then
  LEAN_PATH="$tmp:$paths" LEAN_NUM_THREADS=1 timeout --foreground 300 \
    lake env lean --trust=0 -t0 --root="$tmp" \
      -o "$tmp/Proof.olean" "$tmp/Proof.lean" >>"$log" 2>&1
  proof_status=$?
fi
cat "$log"
printf 'STATEMENT_EXIT=%s\nPROOF_EXIT=%s\n' "$statement_status" "$proof_status"
sha256sum "$log" "$tmp/Statement.olean" "$tmp/Proof.olean"
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

The displayed arrows were normalized to ASCII. The complete captured output had SHA-256
`19d53d6a657e000a6c2cfd7f6cf0a5e34ffb70112eca7beb74a243e2b472cc59`.
The temporary `Statement.olean` had SHA-256
`f0a4ec2437554ebd1dbb7790e87258f56104c31916b9cb1462e189def53b3d16`, and the temporary
`Proof.olean` had SHA-256
`cbc71754bd5c087c618b35ed31902741ef312d1be2f6adc7ddfbb0306e8be3ec`, before cleanup.

Exact placeholder scan:

```bash
rg -n --pcre2 '\b(?:sorry|admit|axiom)\b|sorryAx|unsafe|\bopaque\b|\bextern\b|implemented_by|native_decide' \
  Stage1_Instances/THM-M-0120 -g '*.lean'
```

Exact blocker-invariant check:

```bash
python3 - <<'PY'
import hashlib, json, pathlib, subprocess
root = pathlib.Path('.')
p = root / 'Stage1_Instances/THM-M-0120/proof-recheck-2026-07-15-head-b98f9f43-slot12.json'
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
assert d['statement_recheck']['current_mutation_replay_executed'] is True
assert d['remaining_root_cut_set'] == ['M0120-S-DATA', 'M0120-S-BOUNDARY']
assert d['scheduler_reconciliation']['required'] is True
for name, expected in d['source_hashes'].items():
    base = ('Formalizations/Lean' if name in {'lake-manifest.json', 'lean-toolchain'}
            else 'Stage1_Instances/THM-M-0120')
    q = root / base / name
    assert hashlib.sha256(q.read_bytes()).hexdigest() == expected, name
link_text = (root / 'Formalizations/Lean/.lake').readlink().as_posix().encode()
assert hashlib.sha256(link_text).hexdigest() == \
    d['input_worktree']['link_target_text_sha256']
assert not (root / '.stage1-worker-selftest.json').exists()
print('PASS: current-base blocker identity, hashes, fail-closed state, scheduler finding, and self-test absence agree')
PY
```

The unchanged content inputs at this base are: statement SHA-256
`69eabc83cd8b7fe8fa34d598c9de890eea09d8ee8357d551abf3e7727444fd6b`, countermodel proof
SHA-256 `e5c342e97885f6a533fada4b928685ea4c2e888baa5e21699a454049f02f29ab`, registry SHA-256
`cd24f57d66422f500f17b348bed362dddcdf032447861f2560518f95c1a48a2d`, typed graphs SHA-256
`9ca86f175b3413edd03fec0971bb165c9dd0396ade874a0b0c0c674ac861e23f`, and anchor audit SHA-256
`71ff1889e55e0f4387697db69ff7acae110f0530f94879ef68ae06370475090d`.

No `.stage1-worker-selftest.json` is written because the assigned positive proof deliverable is
blocked rather than genuinely self-tested as complete.
