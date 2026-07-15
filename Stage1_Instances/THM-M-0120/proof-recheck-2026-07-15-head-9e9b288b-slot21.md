# THM-M-0120 proof-phase recheck at base `9e9b288b`

Item: `S56-M-0120-PROOF`

Intent: `prove`

Recheck date: 2026-07-15 (Asia/Shanghai)

Base revision: `9e9b288bc68d49399b5213338febc717e7624b76`

Base tree: `4af7553f47b9d96ae14915b2a728e9f0298be5cc`

## Verdict

`blocked`. No positive proof body can truthfully inhabit the exact frozen proposition. The existing
placeholder-free declaration

```text
Stage1Instances.THMM0120.Proof.not_moriConeTheoremTarget :
  Not (Stage1Instances.THMM0120.MoriConeTheoremTarget.{0, 0, 0, 0})
```

was freshly recompiled with Lean trust level zero. It gives a concrete countermodel to the universal
target. The proper morphism is the identity on `Spec (AlgebraicClosure Rat)`, and every explicit
proposition hypothesis is true, but the statement leaves its numerical data independent:
`N1 = Real`, `moriCone = {-1}`, `canonicalPairing = LinearMap.id`, and `RationalCurve = Empty`.
The required decomposition of `-1` then produces a nonnegative component that is both `-1` and
nonnegative, a contradiction. Refutation at universe specialization `{0, 0, 0, 0}` rules out a
universe-polymorphic positive proof.

This refutes the current abstract Lean encoding, not the mathematical Mori cone theorem. Replacing
the target, narrowing its binders, or adding `Conclusion` or any required output package as a
hypothesis would be substitution or circularity and is outside this proof item's ownership. The item
therefore remains `[ ]`; no proof receipt, provisional state, audit completion, theorem completion,
release decision, or master acceptance is claimed. The predecessor graph remains authoritatively
`H2 / M3 / R4`; this proof attempt only proposes `H5 / M5 / R4` for integration review.

## Failed Gate And Retry

The first failed gate is exact-target consistency at `M0120-S-DATA` and
`M0120-S-BOUNDARY`. `S56-M-0120-STATEMENT` must be reopened so that the numerical curve space,
effective cone, canonical pairing, rational curves, and contractions are defined intrinsically or
connected to the projective klt pair by noncircular semantic laws. Positive proof execution may
resume only after the repaired target has a new accepted expression fingerprint and obligation
registry, followed by a fresh anchor audit and proof execution. The prerequisite obligation-tree
item is currently only provisional `[_]`, not master-accepted.

## Scoped Validation

All successful checks ran in this worker clone using the existing pinned dependency artifacts. No
`lake update`, `lake build`, clone, fetch, dependency mutation, or network operation was performed.
The automation-provided untracked `Formalizations/Lean/.lake` symlink makes this dirty, nonrelease
blocker evidence.

The root `Formalizations/Lean` Lake environment is incomplete: its pinned `flt-regular` checkout has
`HEAD` set to `refs/heads/.invalid` and no checked-out worktree. Consequently the root-level
`check_statement.py` recipe fails before invoking Lean. The narrow theorem replay instead ran
`lake env lean` from the pinned mathlib checkout with `LEAN_PATH` explicitly set to its already-built
pinned dependency directories. This fallback was read-only and successfully checked the exact
statement and countermodel.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0120` | 0 | rank 39; planned lifecycle; L0/rework-required; legacy artifacts unaccepted; theorem incomplete |
| `python3 Stage1_Instances/THM-M-0120/check_statement.py` | 1 | root Lake environment rejected `flt-regular` because its `HEAD` cannot resolve to a commit; no dependency repair or mutation was attempted |
| `python3 Stage1_Instances/THM-M-0120/check_anchor_audit.py` | 0 | immutable local candidates, clean pinned mathlib, eight Lean probes, and the `M3` boundary agreed |
| `python3 Stage1_Instances/THM-M-0120/check_obligation_tree.py` | 0 | 25 obligations and 62 typed edges passed; denominator `69152b16...63081b1`; root remains `M3`; substantive packages remain open |
| isolated pinned-mathlib `lake env lean --trust=0 -t0` recipe below | 0 | exact statement and countermodel elaborated; axiom report `[propext, Classical.choice, Quot.sound]` |
| `/home/sansha-2/.elan/toolchains/leanprover--lean4---v4.29.0/bin/lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| placeholder scan below | 1 | no matches; exit 1 is ripgrep's no-match result |
| JSON parse and blocker-invariant check | 0 | current-base structured blocker identity, hashes, failed gate, retry condition, empty receipts, and self-test absence agreed |
| scoped tracked/no-index whitespace checks | 0 | no whitespace errors in owned-path content |
| `test ! -e .stage1-worker-selftest.json` | 0 | completion self-test manifest deliberately absent |

Exact Lean recipe, with the long package path list abbreviated here as `<pinned-paths>`:

```bash
repo_root=$PWD
target=$repo_root/Stage1_Instances/THM-M-0120
mathlib=$repo_root/Formalizations/Lean/.lake/packages/mathlib
tmp=$(mktemp -d /tmp/thm-m-0120-slot21-lake.XXXXXX)
trap 'rm -rf "$tmp"' EXIT HUP INT TERM
cp "$target/Statement.lean" "$target/Proof.lean" "$tmp/"
cd "$mathlib"
LEAN_PATH=<pinned-paths> LEAN_NUM_THREADS=1 \
  lake env lean --trust=0 -t0 --root="$tmp" \
    -o "$tmp/Statement.olean" "$tmp/Statement.lean"
LEAN_PATH="$tmp:<pinned-paths>" LEAN_NUM_THREADS=1 \
  lake env lean --trust=0 -t0 --root="$tmp" \
    -o "$tmp/Proof.olean" "$tmp/Proof.lean"
```

`<pinned-paths>` was the colon-separated sequence of `.lake/build/lib/lean` directories for `Cli`,
`batteries`, `Qq`, `aesop`, `proofwidgets`, `importGraph`, `LeanSearchClient`, `plausible`, and
`mathlib`, all beneath the automation-provided pinned package closure.

The relevant output was:

```text
def Stage1Instances.THMM0120.MoriConeTheoremTarget.{u, uK, uN, uC} : Prop :=
forall (D : Stage1Instances.THMM0120.ConeTheoremData.{u, uK, uN, uC}),
  @AlgebraicGeometry.IsProper.{u} D.X D.S D.f ->
    D.definedOverBaseField -> D.projective -> D.normal -> D.qFactorial -> D.klt -> D.Conclusion
STATEMENT_EXIT=0
'Stage1Instances.THMM0120.Proof.not_moriConeTheoremTarget' depends on axioms:
[propext, Classical.choice, Quot.sound]
PROOF_EXIT=0
```

The captured output SHA-256 was
`b5d5bafd2f6d5f7d0d409896e75060d49c38081debaa0dbfecef5e19897f5bda`.
The temporary statement and proof oleans had SHA-256 values
`f0a4ec2437554ebd1dbb7790e87258f56104c31916b9cb1462e189def53b3d16` and
`cbc71754bd5c087c618b35ed31902741ef312d1be2f6adc7ddfbb0306e8be3ec` before cleanup.

Exact placeholder scan:

```bash
rg -n --pcre2 '\b(?:sorry|admit|axiom)\b|sorryAx|unsafe' \
  Stage1_Instances/THM-M-0120 -g '*.lean'
```

The unchanged source inputs have these SHA-256 values: statement
`69eabc83cd8b7fe8fa34d598c9de890eea09d8ee8357d551abf3e7727444fd6b`, countermodel proof
`e5c342e97885f6a533fada4b928685ea4c2e888baa5e21699a454049f02f29ab`, registry
`cd24f57d66422f500f17b348bed362dddcdf032447861f2560518f95c1a48a2d`, typed graphs
`9ca86f175b3413edd03fec0971bb165c9dd0396ade874a0b0c0c674ac861e23f`, and anchor audit
`71ff1889e55e0f4387697db69ff7acae110f0530f94879ef68ae06370475090d`.

No `.stage1-worker-selftest.json` is written because the assigned positive proof phase is blocked
rather than genuinely self-tested as complete.
