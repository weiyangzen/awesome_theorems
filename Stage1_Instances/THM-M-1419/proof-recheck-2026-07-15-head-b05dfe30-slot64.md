# Current-base proof recheck

Item: `S56-M-1419-PROOF`

Theorem: `THM-M-1419`

Base revision: `b05dfe30bf9c4067039b9414912ec94f3153bb0b`

Base tree: `a0ccbad8cb36717f11ac16baef9a640aed04457e`

Attempt date: `2026-07-15` (`Asia/Shanghai`)

Worker: Stage1 rev-5.6 automation clone `slot64`

## Verdict

`blocked`; the proof phase remains `[ ]`. No proof body, axiom, placeholder,
weakened theorem, dependency, frozen authority artifact, receipt, or task state
was added or changed. Because this phase is not genuinely self-tested, no
`.stage1-worker-selftest.json` is emitted.

## First failed gate

Exact-target fidelity fails before proof implementation. The canonical target
quantifies `T : Omega Equiv Omega`. `Ergodic T mu` extends
`MeasurePreserving T mu mu`, which supplies forward measurability, but none of
the frozen hypotheses supplies `Measurable T.symm`. Pinned mathlib's
`Ergodic.symm` requires `T : Omega MeasurableEquiv Omega`, whose structure
stores forward and inverse measurability separately.

This is material because the selected target is the conventional invertible,
two-sided splitting theorem and its frozen architecture explicitly builds the
backward filtration over `T.symm`. The substantive external candidate,
`ErgodicTheory.oseledets_splitting`, also requires a measurable equivalence.
The evidence establishes a statement-to-proof-route mismatch; it does not
establish a kernel-checked countermodel to the entire root. The root therefore
stays `[H2, M3, R3]` rather than being promoted to `M5`.

A proof worker cannot silently add the missing premise. The statement phase
must be reopened and changed to a measurable equivalence or given an explicit
`Measurable T.symm` hypothesis. That requires a new statement fingerprint and
obligation-registry version followed by fresh source, mutation, anchor, and
obligation-tree acceptance.

The direct prerequisite `S56-M-1419-OBLIGATION_TREE` remains provisionally
self-tested rather than master accepted. Section 10.2 of the rev-5.6 standard
also requires the repeatedly unresolved proof item to be split after five
execution ticks. Master reconciliation must reopen the prerequisite statement
and version/split the proof work; this worker may not edit the master DAG.

## Proof frontier after repair

No exact placeholder-free root body exists in the pinned closure. The registry
has 13 machine-required obligations and 12 have no terminal proof-body ID.
`target_of_construction_package` merely returns a premise definitionally equal
to the whole target, consuming none of the four frozen proof children. It earns
no substantive proof credit.

Repo-local `THM-M-1057` contains checked Kingman limit theorems, but they do not
construct exterior-power limits, forward/backward filtrations, the measurable
splitting, equivariance, or vector growth required here.

The external candidate at
`marcmorningstar/lean4-ergodic-theory@ed3fa6b8a30594eeb791160563942ba115581aa0`
is absent from the pinned Lake closure and targets Lean `4.30.0-rc2` with
mathlib `34f7a6cd...`, not this repository's Lean `4.29.0` and mathlib
`8a178386...`. The existing compatibility scratch contains 49 of 62 module
oleans but no terminal `SplittingAssembly.olean`; it is not proof evidence.
Even a compatible terminal port would still require checked transports for
the base, almost-everywhere versus pointwise matrix assumptions, Pi versus
Euclidean norms, cocycle order, measurable-subspace APIs, direct sums,
positive finrank, equivariance, and output indexing.

## Fresh validation

All commands ran in this worker clone. No `lake update`, `lake build`, clone,
fetch, dependency repair, or `.lake` mutation was performed. The
automation-provided `.lake` symlink was reused read-only.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique ordered targets, ranks 1 through 1546, passed |
| `python3 scripts/stage1_target.py show THM-M-1419` | 0 | rank 688; planned; rework required; theorem incomplete |
| `python3 Stage1_Instances/THM-M-1419/check_obligation_tree.py` | 0 | 14 obligations and 41 typed edges passed; denominator `ad691633...5999`; root remains open `M3` |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3...` |
| disposable `lake env lean --trust=0 -t0` replay of `OseledetsStatement.lean` | 0 | elaborated; source SHA-256 `22081e4a...04b2`; olean SHA-256 `f5222f72...9169` |
| disposable `lake env lean --trust=0 -t0` replay of `ObligationTree.lean` | 0 | elaborated; axioms exactly `propext`, `Classical.choice`, `Quot.sound`; source SHA-256 `607366cd...0bc1`; olean SHA-256 `4fd543d8...50a6` |
| pinned mathlib API and external candidate inspection | 0 | `Ergodic.symm` and the external theorem require `MeasurableEquiv`; the target has plain `Equiv` |
| scoped proof-input/pin diff from `21798c9c...` to `HEAD` | 0 | empty; no target, architecture, Kingman, toolchain, manifest, or dependency proof input changed |
| token-anchored prohibited-device scan | 1 | expected no-match exit; no prohibited proof device occurs in target Lean files |

The disposable replay copied both target modules to a fresh temporary
directory, obtained `LEAN_PATH` through the existing pinned Lake environment,
compiled fresh oleans with `LEAN_NUM_THREADS=1`, `timeout 300`, `--trust=0`,
and `-t0`, hashed the source/log/output artifacts, and removed the temporary
directory. Cached target oleans were neither used as outputs nor modified.

The exact scoped comparison and prohibited-device commands were:

```bash
git diff --name-status 21798c9c8a9ed9ea40e8df489d9c661b59026564..HEAD -- \
  Stage1_Instances/THM-M-1419/OseledetsStatement.lean \
  Stage1_Instances/THM-M-1419/ObligationTree.lean \
  Stage1_Instances/THM-M-1419/obligation-registry.json \
  Stage1_Instances/THM-M-1419/typed-graphs.json \
  Stage1_Instances/THM-M-1419/anchor-audit.json \
  Stage1_Instances/THM-M-1057 Formalizations/Lean/lean-toolchain \
  Formalizations/Lean/lake-manifest.json

rg -n '^[[:space:]]*(sorry|admit)([[:space:]]|$)|sorryAx|^[[:space:]]*axiom[[:space:]]|^[[:space:]]*unsafe[[:space:]]+(def|theorem)|native_decide|implemented_by|^[[:space:]]*extern[[:space:]]' \
  Stage1_Instances/THM-M-1419 --glob '*.lean'
```

## Retry condition and boundary

Master must reopen and accept the repaired statement and a new registry, split
the oversized proof node, and only then schedule the complete Oseledets
implementation and exact transports. This file is negative nonrelease evidence
only: it does not satisfy the proof item, close an obligation or root, change
scheduler state, establish audit/theorem completion, or claim master
acceptance.
