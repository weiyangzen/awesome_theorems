# Current-base proof recheck

Item: `S56-M-1419-PROOF`

Theorem: `THM-M-1419`

Base revision: `3a40b1969f841e07036db5c4d7f03e97c7c57949`

Base tree: `404cccc598c2d4c8831d55138df788f0438ddce8`

Attempt date: `2026-07-15` (`Asia/Shanghai`)

Worker: Stage1 rev-5.6 automation clone `slot64`

## Verdict

`blocked`; the assigned proof phase remains `[ ]`. No proof body, axiom,
placeholder, weakened theorem, dependency, or frozen authority artifact was
added or changed. No worker self-test manifest is emitted.

## First failed gate

Exact-target fidelity fails before proof implementation. The frozen target
quantifies a plain equivalence `T : Ω ≃ Ω`. Its
`MeasurePreserving T mu mu` and `Ergodic T mu` hypotheses provide
`Measurable T`, but they do not provide `Measurable T.symm`. Mathlib's theorem
`Ergodic.symm` instead requires `T : Ω ≃ᵐ Ω`.

This missing inverse-measurability premise matters to the selected two-sided
splitting theorem. The substantive external candidate
`ErgodicTheory.oseledets_splitting` also requires a measurable equivalence, and
the prior structured audit records a Bernoulli-shift obstruction to recovering
the desired measurable equivariant splitting from forward measurability alone.
Because that obstruction has not been kernel-formalized, the accepted root
classification remains `[H2, M3, R3]`; this worker does not promote it to `M5`.

The exact statement must first be reopened, changed to use `MeasurableEquiv`
or an explicit `Measurable T.symm` hypothesis, and re-elaborated. That change
requires a new normalized statement fingerprint and obligation-registry
version plus fresh statement, source, anchor, and obligation-tree acceptance.
A proof worker must not silently repair this prerequisite by strengthening the
theorem it was assigned.

## Proof frontier after prerequisite repair

Even after repairing the statement, no exact placeholder-free root body is in
the pinned closure. The frozen registry has 13 machine-required obligations;
12 lack terminal proof-body IDs. The current
`target_of_construction_package` declaration merely returns a premise that is
definitionally the entire target and does not consume the four proof children
recorded for assembly.

The repository-local `THM-M-1057` Kingman declarations are real checked
analytic inputs, correcting the older prose blocker's claim that no Kingman
body exists. They do not construct exterior-power processes, forward/backward
flags, measurable splitting, equivariance, or vector-growth limits, so no
`THM-M-1419` obligation is newly closed here.

The external Oseledets candidate at
`marcmorningstar/lean4-ergodic-theory@ed3fa6b8a30594eeb791160563942ba115581aa0`
is not in the pinned dependency closure. It targets Lean `4.30.0-rc2` and
mathlib `34f7a6cd...`; the repository uses Lean `4.29.0` and mathlib
`8a178386...`. A read-only scratch compatibility attempt has only 17 of 62
modules elaborated and first fails in `ErgodicTheory.Lyapunov.ExteriorNorm.Basic`.
Its theorem additionally needs checked transports for almost-everywhere versus
pointwise assumptions, Pi versus Euclidean norms, cocycle order, measurable
subspaces, direct sums, positive finrank, equivariance, and output indexing.

## Validation evidence

All commands ran from this worker clone. No `lake update`, `lake build`, clone,
fetch, or dependency mutation was run. The automation-provided `.lake` symlink
was reused read-only. During this attempt, `lake env` became unavailable because
the shared pinned `flt-regular` checkout had an unresolved `HEAD`; the same
pinned Lean executable and existing package oleans were therefore invoked
directly with an explicit read-only `LEAN_PATH`. Temporary outputs were removed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique ordered targets, ranks 1 through 1546, passed |
| `python3 scripts/stage1_target.py show THM-M-1419` | 0 | rank 688; planned; rework required; theorem incomplete |
| Obligation-tree checker | 0 | 14 obligations and 41 typed edges passed; denominator `ad691633...5999`; root remains open `M3` |
| `lake env lean --version` from `Formalizations/Lean` | 1 | shared `flt-regular` checkout could not resolve `HEAD`; no repair or fetch attempted |
| `/home/sansha-2/.elan/toolchains/leanprover--lean4---v4.29.0/bin/lean --version` | 0 | Lean `4.29.0`, commit `98dc76e3...716fb04` |
| Disposable trust-zero statement/wrapper replay | 0 | exact target elaborated; wrapper axioms were the accepted three; olean hashes `f5222f72...3a9169`, `4fd543d8...50a6` |
| Disposable guarded inverse-measurability probe | 0 | stronger derivations were rejected; `hT.measurable` gives only `Measurable T`, and `Ergodic.symm` requires `MeasurableEquiv` |
| Scoped input/pin diff from `4e4f31e4` to `HEAD` | 0 | no target, architecture, manifest, toolchain, dependency, or `THM-M-1057` proof input changed |
| Token-anchored prohibited-device scan | 1 | expected no-match exit: no proof placeholder or unsafe injection token occurs |

## Retry condition and boundary

Reopen and accept the repaired statement and a new registry version first.
Then compatibly port or locally implement the complete Oseledets closure,
prove every exact transport, and replace the identity wrapper with a checked
composer that consumes all four required children. This current-base blocker is
negative nonrelease evidence only: it does not satisfy the proof item, close an
obligation or root, change scheduler state, establish audit/theorem completion,
or claim master acceptance.
