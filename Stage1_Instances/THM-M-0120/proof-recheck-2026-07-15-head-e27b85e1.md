# THM-M-0120 proof-phase recheck at base `e27b85e1`

Item: `S56-M-0120-PROOF`

Intent: `prove`

Recheck date: 2026-07-15 (Asia/Shanghai)

Base revision: `e27b85e1503047c5e4bd8d5410b6fba5c4dda896`

Base tree: `29c625431b9c241bce6286123205defcbd1e7f7e`

## Verdict

`blocked`. No legal positive proof body exists for the exact frozen proposition. The existing
placeholder-free declaration

```text
Stage1Instances.THMM0120.Proof.not_moriConeTheoremTarget :
  Not (Stage1Instances.THMM0120.MoriConeTheoremTarget.{0, 0, 0, 0})
```

kernel-checks at trust level zero. Its countermodel uses the proper identity morphism on
`Spec (AlgebraicClosure Rat)` and makes every proposition premise of the target true. The statement
does not connect those premises to its numerical data, so the same model may set `N1 = Real`,
`moriCone = {-1}`, `canonicalPairing = LinearMap.id`, and `RationalCurve = Empty`.

The forward direction of the required decomposition equivalence sends `-1` to an element `z0` of
the nonnegative part. Membership in the declared cone gives `z0 = -1`, while membership in the
nonnegative part gives `0 <= z0`, a contradiction. Refutation at universe specialization
`{0, 0, 0, 0}` rules out a universe-polymorphic positive proof of the canonical target.

This is a counterexample to the frozen abstract encoding, not to the mathematical Mori cone
theorem. A repaired, narrowed, or circularly strengthened proposition cannot replace the assigned
target. The item remains `[ ]`; no positive proof body, provisional receipt, audit completion,
theorem completion, release, or master acceptance is claimed. The predecessor graph remains
authoritatively `H2 / M3 / R4`; this proof attempt only proposes the blocker classification
`H5 / M5 / R4` for integration review.

## Failed Gate And Retry

The first failed gate is exact-target consistency at `M0120-S-DATA` and
`M0120-S-BOUNDARY`. `S56-M-0120-STATEMENT` must be reopened, and the disconnected proposition and
numerical-data stand-ins must be replaced by intrinsic definitions or noncircular laws connecting
the projective klt pair to its numerical curve space, effective cone, canonical pairing, rational
curves, and contractions. Assuming `Conclusion`, its decomposition branch, or any other required
output package would be circular.

Positive proof work may resume only after the repaired target receives a new accepted expression
fingerprint and obligation-registry version, followed by a fresh anchor audit and proof execution.
The generated checklist currently projects the prerequisite obligation-tree item as provisional
`[_]`, while the target-local task DAG has no accepted states; it is not master-accepted.

## Scoped Validation

All successful checks ran in this worker clone with the existing pinned Lean closure. No
`lake update`, `lake build`, fetch, clone, or dependency mutation was performed. The
automation-provided untracked `Formalizations/Lean/.lake` symlink makes this nonrelease evidence.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0120` | 0 | rank 39; planned lifecycle; L0/rework-required; legacy artifacts unaccepted; theorem incomplete |
| `python3 Stage1_Instances/THM-M-0120/check_statement.py` | 0 | three structural mutations killed; expression SHA-256 `074d45c3...d88cfd`; pinned toolchain and mathlib revision matched |
| `python3 Stage1_Instances/THM-M-0120/check_anchor_audit.py` | 0 | immutable local candidates, clean pinned mathlib, eight Lean probes, and the `M3` boundary agreed |
| `python3 Stage1_Instances/THM-M-0120/check_obligation_tree.py` | 0 | 25 obligations and 62 typed edges passed; denominator `69152b16...63081b1`; root remains `M3` |
| isolated `lake env lean --trust=0 -t0` recipe below | 0 | exact statement and countermodel elaborated; axiom report `[propext, Classical.choice, Quot.sound]` |
| `/home/sansha-2/.elan/toolchains/leanprover--lean4---v4.29.0/bin/lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| placeholder scan below | 1 | no matches; exit 1 is ripgrep's no-match result |
| `python3 -m json.tool Stage1_Instances/THM-M-0120/proof-recheck-2026-07-15-head-e27b85e1.json` | 0 | current-base structured blocker is valid JSON |
| tracked diff check plus `git diff --no-index --check /dev/null <new-file>` for both new files | 0 | no whitespace errors in tracked or newly added owned-path content; each no-index check returned its expected clean-diff exit 1 |
| `test ! -e .stage1-worker-selftest.json` | 0 | completion self-test manifest deliberately absent |

Exact Lean recipe, run from the repository root:

```bash
set -euo pipefail
repo_root=$PWD
target=$repo_root/Stage1_Instances/THM-M-0120
tmp=$(mktemp -d /tmp/stage1-m0120-proof.XXXXXX)
trap 'rm -rf "$tmp"' EXIT HUP INT TERM
cp "$target/Statement.lean" "$target/Proof.lean" "$tmp/"
cd "$repo_root/Formalizations/Lean"
base=$(lake env printenv LEAN_PATH)
LEAN_NUM_THREADS=1 timeout --foreground 300 \
  lake env lean --trust=0 -t0 --root="$tmp" \
    -o "$tmp/Statement.olean" "$tmp/Statement.lean"
LEAN_PATH="$tmp:$base" LEAN_NUM_THREADS=1 timeout --foreground 300 \
  lake env lean --trust=0 -t0 --root="$tmp" "$tmp/Proof.lean"
printf 'LEAN_RECHECK_EXIT=0\n'
```

The relevant output was:

```text
def Stage1Instances.THMM0120.MoriConeTheoremTarget.{u, uK, uN, uC} : Prop :=
forall (D : Stage1Instances.THMM0120.ConeTheoremData.{u, uK, uN, uC}),
  @AlgebraicGeometry.IsProper.{u} D.X D.S D.f ->
    D.definedOverBaseField -> D.projective -> D.normal -> D.qFactorial -> D.klt -> D.Conclusion
'Stage1Instances.THMM0120.Proof.not_moriConeTheoremTarget' depends on axioms:
[propext, Classical.choice, Quot.sound]
LEAN_RECHECK_EXIT=0
```

Exact placeholder scan:

```bash
rg -n --pcre2 '\b(?:sorry|admit|axiom)\b|sorryAx|unsafe' \
  Stage1_Instances/THM-M-0120/Proof.lean
```

The unchanged source inputs have these SHA-256 values: statement
`69eabc83cd8b7fe8fa34d598c9de890eea09d8ee8357d551abf3e7727444fd6b`, proof witness
`e5c342e97885f6a533fada4b928685ea4c2e888baa5e21699a454049f02f29ab`, registry
`cd24f57d66422f500f17b348bed362dddcdf032447861f2560518f95c1a48a2d`, typed graphs
`9ca86f175b3413edd03fec0971bb165c9dd0396ade874a0b0c0c674ac861e23f`, and anchor audit
`71ff1889e55e0f4387697db69ff7acae110f0530f94879ef68ae06370475090d`.

No `.stage1-worker-selftest.json` is written because the assigned positive proof phase is blocked
rather than genuinely self-tested as complete.
