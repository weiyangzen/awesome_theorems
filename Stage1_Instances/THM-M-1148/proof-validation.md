# THM-M-1148 proof-phase result

Date: 2026-07-12

Item: `S56-M-1148-PROOF`

Base revision: `374f59f3f7c9671f848b5708d8b6787d91aaf98b`

Verdict: blocked; the proof phase is not self-tested as complete and no worker
self-test manifest is emitted.

## Implemented proof body

`Proof.lean` proves the non-circular bridge
`interiorFormula_of_harmonicContOnCl_of_eqOn`. Given a function already
harmonic on the disk, continuous on its closure, and equal to the boundary
data on the circle, it uses the pinned mathlib theorem
`HarmonicContOnCl.circleAverage_poissonKernel_smul` plus
`circleAverage_congr_sphere` to derive the exact interior formula with the
original boundary function `g`.

`dirichletExtension_to_root` then kernel-checks composition of that bridge
with the remaining extension package. Neither declaration assumes the
interior formula being proved, and neither uses `sorry`, `axiom`, or an
unproved local declaration.

## Blocking cut

The target still requires construction, from every continuous `g` on the
circle, of a `u` that is harmonic in the disk, continuous on the closed disk,
and has trace `g`. The installed pinned mathlib module proves Poisson
representation only for an already harmonic and closure-continuous function;
it has no Dirichlet extension theorem. Thus `DirichletExtension` remains an
explicit premise of the composition theorem, not a proved declaration.

This leaves the frozen analytic cut set open, in particular `M1148-C`,
`M1148-L1`, `M1148-B`, and `M1148-N3`. The exact root remains `M4`; no proof,
validation, release, or theorem-completion state is claimed.

## Validation transcript

Working directory for Lean: `Formalizations/Lean`.

Command:

```text
lake env lean ../../Stage1_Instances/THM-M-1148/Proof.lean
```

Exit code: `0`.

Output:

```text
'Stage1Instances.THM_M_1148.Proof.interiorFormula_of_harmonicContOnCl_of_eqOn' depends on axioms: [propext,
 Classical.choice,
 Quot.sound]
'Stage1Instances.THM_M_1148.Proof.dirichletExtension_to_root' depends on axioms: [propext, Classical.choice, Quot.sound]
```

Additional commands, run from the repository root, all exited `0`:

```text
python3 Docs/tools/check_stage1_standard.py
python3 scripts/stage1_target.py check
python3 scripts/stage1_target.py show THM-M-1148
python3 Stage1_Instances/THM-M-1148/check_statement.py
python3 Stage1_Instances/THM-M-1148/check_anchor_audit.py
python3 Stage1_Instances/THM-M-1148/check_obligation_tree.py
git diff --check -- Stage1_Instances/THM-M-1148
```

Structural summaries were respectively: standard OK for 1546 targets; target
manifest OK for ranks 1 through 1546; target shown as L0/rework-required and
not theorem-complete; statement fingerprint and five mutations passed; anchor
audit agreed with pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`; obligation tree passed with 26
obligations and 51 typed edges while reporting the root open at M4; diff
whitespace check produced no output.
