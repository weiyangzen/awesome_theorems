# THM-M-0120 proof phase blocked at base `6bf9ee93`

Item: `S56-M-0120-PROOF`

Intent: `prove`

Recheck date: 2026-07-16 (Asia/Shanghai)

Base revision: `6bf9ee93a322e7d25cf9249226222095f95d1cff`

Base tree: `24acf86e69ab2e6fca9480c6269b6429874ba295`

## Verdict

`blocked`. No positive proof body can truthfully inhabit the exact frozen
proposition. The existing placeholder-free declaration

```text
Stage1Instances.THMM0120.Proof.not_moriConeTheoremTarget :
  Not (Stage1Instances.THMM0120.MoriConeTheoremTarget.{0, 0, 0, 0})
```

was freshly recompiled with Lean trust level zero. It supplies a concrete
countermodel to the universal target. The proper morphism is the identity on
`Spec (AlgebraicClosure Rat)`, and all six explicit input premises hold. The
statement nevertheless leaves its numerical data independent:
`N1 = Real`, `moriCone = {-1}`, `canonicalPairing = LinearMap.id`, and
`RationalCurve = Empty`. The required decomposition of `-1` produces a
component in the nonnegative part that is both `-1` and nonnegative, a
contradiction.

Refutation at universe specialization `{0, 0, 0, 0}` rules out a
universe-polymorphic positive proof. It refutes the current abstract Lean
encoding, not the mathematical Mori cone theorem. Replacing or narrowing the
target, or assuming `Conclusion` or a required output package, would be theorem
substitution or circularity.

The required v2 dependency audit was also performed before proof work. The
target has no admitted hard parents, transitive ancestors, incoming hard edges,
reuse hints, or shared groups. The new
`dependency-reuse-ledger.json` records this empty audited closure against graph
SHA-256 `73e99d22...40eca` and context SHA-256 `068170c7...c5c`.
An empty admitted context is not a claim that the proof is mathematically
independent.

The item remains `[ ]`. No proof receipt, provisional completion state, audit
completion, theorem completion, release decision, or master acceptance is
claimed. Its obligation-tree dependency is only provisional `[_]`.

## Failed Gate And Retry

The first failed gate is `S56-5.1-EXACT-TARGET-CONSISTENCY`, at obligations
`M0120-S-DATA` and `M0120-S-BOUNDARY`. `S56-M-0120-STATEMENT` must be reopened
so that the numerical curve space, effective cone, canonical pairing, rational
curves, and contractions are intrinsic or connected to the projective klt pair
by noncircular semantic laws. Proof execution may resume only after the
repaired target has a new accepted expression fingerprint, anchor audit,
obligation registry, and typed graphs.

The dossier already contains many repeated blocker/recheck artifacts while the
authoritative execution DAG records zero attempts and no child nodes. The
master should reconcile the attempt history and redirect work to statement
repair or bounded child nodes before scheduling another identical proof retry.
This worker does not edit scheduler authority.

## Scoped Validation

All checks used the existing pinned dependency artifacts. No `lake update`,
`lake build`, clone, fetch, dependency mutation, or network operation was
performed. The automation-provided untracked `Formalizations/Lean/.lake`
symlink makes this nonrelease blocker evidence.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0120` | 0 | rank 39; planned; L0/rework-required; legacy artifacts unaccepted; theorem incomplete |
| dependency-ledger validator from `scripts.stage1_execution_cron` with the claimed graph and base revision | 0 | schema 1.1, target identity, graph/context digests, repository revision, and all empty closure lists agreed |
| `timeout --foreground --kill-after=10s 600s env LEAN_NUM_THREADS=1 python3 Stage1_Instances/THM-M-0120/check_statement.py` | 0 | expression SHA-256 `074d45c3...d88cfd`; all three structural mutations differed; pinned Lean 4.29.0 and mathlib revision agreed |
| `timeout --foreground --kill-after=10s 600s env LEAN_NUM_THREADS=1 python3 Stage1_Instances/THM-M-0120/check_anchor_audit.py` | 0 | immutable local candidates, clean pinned mathlib, eight Lean probes, and the M3 boundary agreed |
| `timeout --foreground --kill-after=10s 600s env LEAN_NUM_THREADS=1 python3 Stage1_Instances/THM-M-0120/check_obligation_tree.py` | 0 | 25 obligations and 62 typed edges passed; denominator `69152b16...63081b1`; root remains M3 |
| isolated pinned-mathlib `lake env lean --trust=0 -t0` recipe below | 0 | exact statement and countermodel elaborated; axiom report `[propext, Classical.choice, Quot.sound]` |
| prohibited-token scan below | 0 wrapper, 1 `rg` | no matches; `rg` exit 1 is the expected no-match result |
| `python3 Docs/tools/check_stage1_theorem_dag_v2.py` and `python3 Docs/tools/check_stage1_standard.py` | nonzero/time-limited in the worker clone | the checked-in DAG inventory predates this required new ledger/blocker JSON, so fresh discovery differs; the worker may not regenerate the authoritative DAG, while the fixed graph digest and empty target context passed the dedicated ledger validator |
| `test ! -e .stage1-worker-selftest.json` | 0 | completion self-test correctly absent |

Exact Lean replay:

```bash
set -u
repo_root=$PWD
target=$repo_root/Stage1_Instances/THM-M-0120
mathlib=$repo_root/Formalizations/Lean/.lake/packages/mathlib
tmp=$(mktemp -d /tmp/thm-m-0120-proof-head-6bf9ee93-slot7.XXXXXX)
log=$(mktemp /tmp/thm-m-0120-proof-head-6bf9ee93-slot7-log.XXXXXX)
trap 'rm -rf "$tmp" "$log"' EXIT HUP INT TERM
cp "$target/Statement.lean" "$target/Proof.lean" "$tmp/"
paths=$(find -L "$repo_root/Formalizations/Lean/.lake/packages" \
  -path '*/.lake/build/lib/lean' -type d -print | sort | paste -sd: -)
cd "$mathlib"
LEAN_PATH="$paths" LEAN_NUM_THREADS=1 timeout --foreground --kill-after=10s 600s \
  lake env lean --trust=0 -t0 --root="$tmp" \
    -o "$tmp/Statement.olean" "$tmp/Statement.lean" >"$log" 2>&1
statement_status=$?
proof_status=125
if [ "$statement_status" -eq 0 ]; then
  LEAN_PATH="$tmp:$paths" LEAN_NUM_THREADS=1 \
    timeout --foreground --kill-after=10s 600s \
    lake env lean --trust=0 -t0 --root="$tmp" \
      -o "$tmp/Proof.olean" "$tmp/Proof.lean" >>"$log" 2>&1
  proof_status=$?
fi
cat "$log"
printf 'STATEMENT_EXIT=%s\nPROOF_EXIT=%s\n' \
  "$statement_status" "$proof_status"
sha256sum "$log" "$tmp/Statement.olean" "$tmp/Proof.olean"
test "$statement_status" = 0
test "$proof_status" = 0
```

Relevant output, with arrows normalized to ASCII:

```text
def Stage1Instances.THMM0120.MoriConeTheoremTarget.{u, uK, uN, uC} : Prop :=
forall (D : Stage1Instances.THMM0120.ConeTheoremData.{u, uK, uN, uC}),
  @AlgebraicGeometry.IsProper.{u} D.X D.S D.f ->
    D.definedOverBaseField -> D.projective -> D.normal ->
      D.qFactorial -> D.klt -> D.Conclusion
'Stage1Instances.THMM0120.Proof.not_moriConeTheoremTarget' depends on axioms:
[propext, Classical.choice, Quot.sound]
STATEMENT_EXIT=0
PROOF_EXIT=0
```

The captured output SHA-256 was
`19d53d6a657e000a6c2cfd7f6cf0a5e34ffb70112eca7beb74a243e2b472cc59`.
The temporary statement and proof olean SHA-256 values were respectively
`f0a4ec2437554ebd1dbb7790e87258f56104c31916b9cb1462e189def53b3d16`
and `cbc71754bd5c087c618b35ed31902741ef312d1be2f6adc7ddfbb0306e8be3ec`
before cleanup.

Exact prohibited-token scan:

```bash
rg -n --pcre2 \
  '\b(?:sorry|admit|axiom)\b|sorryAx|unsafe|\bopaque\b|\bextern\b|implemented_by|native_decide' \
  Stage1_Instances/THM-M-0120 -g '*.lean'
```

It returned no output and exit 1, ripgrep's no-match status. No
`.stage1-worker-selftest.json` is written because the assigned positive proof
phase is blocked rather than genuinely self-tested as complete.
