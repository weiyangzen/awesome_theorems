# THM-M-0120 proof-phase recheck at base `b591ad20`

Item: `S56-M-0120-PROOF`

Intent: `prove`

Recheck date: 2026-07-15 (Asia/Shanghai)

Base revision: `b591ad20d93005ec840e569f84d625ef246bd07d`

Base tree: `844da63e73e35787ef60899f9f194dc97006dc8c`

## Verdict

`blocked`. The exact frozen proposition has no positive proof body: the existing
placeholder-free declaration

```text
Stage1Instances.THMM0120.Proof.not_moriConeTheoremTarget :
  Not (Stage1Instances.THMM0120.MoriConeTheoremTarget.{0, 0, 0, 0})
```

was freshly replayed with Lean trust level zero. The countermodel uses the proper identity morphism
on `Spec (AlgebraicClosure Rat)` and makes every explicit proposition hypothesis true, while the
statement permits independent numerical data: `N1 = Real`, `moriCone = {-1}`,
`canonicalPairing = LinearMap.id`, and `RationalCurve = Empty`. The conclusion's decomposition of
`-1` would produce a nonnegative component that is both `-1` and nonnegative, a contradiction.
Refutation at universe specialization `{0, 0, 0, 0}` rules out a universe-polymorphic positive proof.

This refutes only the current abstract Lean encoding, not the mathematical Mori cone theorem. A
narrower theorem, a changed binder domain, or a new assumption supplying `Conclusion` would be a
substitution or circular premise and cannot satisfy this proof item. No proof receipt, provisional
state, audit completion, theorem completion, release decision, or master acceptance is claimed.
The predecessor obligation-tree item is only provisional `[_]`, and the authoritative root remains
`H2 / M3 / R4`; this attempt proposes `H5 / M5 / R4` only for integration review.

## First Failed Gate And Retry

The first failed gate is `S56-5.1-EXACT-TARGET-CONSISTENCY`, at obligations `M0120-S-DATA` and
`M0120-S-BOUNDARY`. `S56-M-0120-STATEMENT` must be reopened. Its numerical curve space, effective
cone, canonical pairing, rational curves, and contractions must be defined intrinsically or tied to
the projective klt pair by noncircular semantic laws. After that repair, the integration lane must
freeze and accept a new expression fingerprint and obligation registry, then rerun the anchor audit
and proof work.

## Scoped Validation

All commands ran in this worker clone against the existing pinned dependency artifacts. No
`lake update`, `lake build`, clone, fetch, network operation, or dependency mutation was performed.
The automation-provided untracked `Formalizations/Lean/.lake` symlink makes this nonrelease evidence.

The project-level statement validator failed before Lean invocation because the pinned
`flt-regular` checkout has an invalid `HEAD` and no worktree. The narrow replay therefore ran
`lake env lean` from the pinned mathlib checkout with `LEAN_PATH` set explicitly to the already-built
shared package directories. A first fallback attempt used package paths below the mathlib checkout;
Lean rejected it with `unknown module prefix 'Batteries'`. The corrected shared-package paths then
checked both exact sources. A second replay with the pinned Lean executable directly produced the
same declarations and olean hashes.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0120` | 0 | rank 39; planned; L0/rework-required; legacy artifacts unaccepted; theorem incomplete |
| `python3 Stage1_Instances/THM-M-0120/check_statement.py` | 1 | root Lake environment rejected `flt-regular`: `could not resolve 'HEAD' to a commit` |
| `python3 Stage1_Instances/THM-M-0120/check_anchor_audit.py` | 0 | immutable candidates, clean pinned mathlib, eight Lean probes, and the `M3` boundary agreed |
| `python3 Stage1_Instances/THM-M-0120/check_obligation_tree.py` | 0 | 25 obligations and 62 typed edges passed; denominator `69152b161a10b5ce6099fb09c48320330d6d35f63a11411ad14ccb84963081b1`; root remains `M3` |
| first isolated fallback with paths below mathlib | 1 | failed with `unknown module prefix 'Batteries'`; no repository or dependency state changed |
| corrected isolated `lake env lean --trust=0 -t0` replay | 0 | statement and countermodel checked; axiom report `[propext, Classical.choice, Quot.sound]` |
| direct pinned-Lean `lean --trust=0 -t0` replay | 0 | independent invocation agreed with the corrected Lake replay and olean hashes |
| `/home/sansha-2/.elan/toolchains/leanprover--lean4---v4.29.0/bin/lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| placeholder scan below | 1 | no matches; exit 1 is ripgrep's no-match result |
| `test ! -e .stage1-worker-selftest.json` | 0 | completion self-test manifest deliberately absent |

The corrected Lean replay copied `Statement.lean` and `Proof.lean` to a fresh temporary directory,
then, from `Formalizations/Lean/.lake/packages/mathlib`, ran:

```bash
LEAN_PATH=<shared-pinned-package-paths> LEAN_NUM_THREADS=1 \
  lake env lean --trust=0 -t0 --root="$tmp" \
    -o "$tmp/Statement.olean" "$tmp/Statement.lean"
LEAN_PATH="$tmp:<shared-pinned-package-paths>" LEAN_NUM_THREADS=1 \
  lake env lean --trust=0 -t0 --root="$tmp" \
    -o "$tmp/Proof.olean" "$tmp/Proof.lean"
```

`<shared-pinned-package-paths>` was the colon-separated set of existing `.lake/build/lib/lean`
directories for `batteries`, `Qq`, `aesop`, `proofwidgets`, `importGraph`, `LeanSearchClient`,
`plausible`, and `mathlib` beneath `Formalizations/Lean/.lake/packages`. The relevant output was:

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

The statement and proof oleans had SHA-256 values
`f0a4ec2437554ebd1dbb7790e87258f56104c31916b9cb1462e189def53b3d16` and
`cbc71754bd5c087c618b35ed31902741ef312d1be2f6adc7ddfbb0306e8be3ec` before cleanup.

Exact placeholder scan:

```bash
rg -n --pcre2 '\b(?:sorry|admit|axiom)\b|sorryAx|unsafe|\bopaque\b|\bextern\b|implemented_by|native_decide' \
  Stage1_Instances/THM-M-0120 -g '*.lean'
```

The unchanged source SHA-256 values are: statement
`69eabc83cd8b7fe8fa34d598c9de890eea09d8ee8357d551abf3e7727444fd6b`, countermodel proof
`e5c342e97885f6a533fada4b928685ea4c2e888baa5e21699a454049f02f29ab`, registry
`cd24f57d66422f500f17b348bed362dddcdf032447861f2560518f95c1a48a2d`, typed graphs
`9ca86f175b3413edd03fec0971bb165c9dd0396ade874a0b0c0c674ac861e23f`, and anchor audit
`71ff1889e55e0f4387697db69ff7acae110f0530f94879ef68ae06370475090d`.

No `.stage1-worker-selftest.json` is written because the assigned positive proof phase is blocked,
not genuinely self-tested as complete.
