# THM-M-0113 proof-phase result

Item: `S56-M-0113-PROOF`

## Verdict

The requested positive proof body cannot truthfully be implemented because
the exact frozen proposition is false. `Proof.lean` gives a kernel-checked
counterexample at universes `(0,0,0,0)` and proves
`not_hodgeDecompositionTarget` without `sorry`, declarations of new axioms, or
unsafe code.

The countermodel is the zero-dimensional compact complex manifold
`Fin 0 -> Complex`. Its `HodgeData` sets `isKahler := True`, every cohomology
space to `Complex`, and every Hodge piece to bottom. All structure fields and
conjugation laws hold, but the degree-zero spanning conclusion would say the
bottom submodule of `Complex` is top, contradicting `one_ne_zero`.

This exposes a statement-level defect: `HodgeData.isKahler` is an arbitrary
`Prop` and has no relationship to `cohomology` or `hodgePiece`. The intended
theorem cannot quantify over every `HodgeData` realization unless those fields
are canonically constructed from the manifold or the necessary analytic laws
are added as hypotheses. Merely proving the intended mathematical Hodge
theorem cannot establish this broader proposition.

## Validation

Base revision: `00e1e30ff33e4399bb3fdf46894103a5f67be8ab`.

Run from `Formalizations/Lean` using the existing pinned toolchain and
artifacts. The first command materializes only the target-local import object;
the cleanup removes it after elaboration.

```bash
cp ../../Stage1_Instances/THM-M-0113/Statement.lean Statement.lean
lake env lean -o .lake/build/lib/lean/Statement.olean Statement.lean
lake env lean ../../Stage1_Instances/THM-M-0113/Proof.lean
rm -f Statement.lean .lake/build/lib/lean/Statement.olean
```

Result: exit `0`. Lean printed
`Stage1Instances.THMM0113.not_hodgeDecompositionTarget` and reported only the
standard axioms `[propext, Classical.choice, Quot.sound]`; it reported no
`sorryAx`. This command uses the already-present untracked `.lake` link into
the canonical pinned artifacts; it neither updates nor otherwise mutates the
dependency checkout.

Additional checks:

```bash
python3 Docs/tools/check_stage1_standard.py
python3 scripts/stage1_target.py check
python3 scripts/stage1_target.py show THM-M-0113
python3 Stage1_Instances/THM-M-0113/check_obligation_tree.py
git diff --check -- Stage1_Instances/THM-M-0113
```

The standard and manifest checks passed; `show` continued to report rank 25,
`planned`, `L0 / rework_required`, and `theorem_complete: false`. The frozen
obligation-tree validator passed with 26 obligations and 49 typed edges, while
correctly retaining root state M4. The whitespace check passed.

## Status boundary

No proof-phase self-test manifest is emitted: this phase is blocked rather
than complete. The first failed gate is exact-target truth. The remaining root
cut set is the statement repair itself, followed by a new statement receipt,
anchor audit, and obligation-registry version before any positive proof work.
No theorem completion, M0 closure, validation completion, release evidence, or
master acceptance is claimed.
