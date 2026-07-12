# Exact-statement gate: blocked

Item: `S56-M-1086-STATEMENT`  
Theorem: `THM-M-1086`  
Base revision: `4f1327c0201b7e64bed17be23fe9806cabf547e1`

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the available repository source
record. Its complete mathematical wording is `高斯过程的下界` ("a lower bound for Gaussian
processes"). The intake correctly narrows this to the Sudakov-minoration claim family, but
explicitly leaves the exact primary-source theorem and formal statement open. In particular, the
available evidence does not determine:

- whether entropy is a packing number, internal covering number, or external covering number;
- whether balls are open or closed and whether the radius is `epsilon`, `epsilon / 2`, or another
  convention absorbed into the universal constant;
- whether the theorem is stated for a finite Gaussian vector or a separable process, and the exact
  measurability, boundedness, total-boundedness, and finiteness assumptions;
- whether the left side is `E[sup_t X_t]`, a based increment supremum, `E[sup_t |X_t|]`, or another
  normalized quantity;
- the quantifier scope and normalization of the universal constant, and the permitted positive
  scales;
- the treatment of empty/singleton index sets, zero increment variance, and finite versus infinite
  entropy.

These choices yield different propositions. Choosing a familiar textbook formulation would
therefore substitute an unverified theorem for the assigned exact target. The two bibliography
entries in `source-statement-crosswalk.md` are explicitly discovery candidates without theorem/page
inspection or assumption/errata crosswalk, so they cannot resolve the ambiguity. The historical
metadata label `已验证` supplies neither statement identity nor kernel evidence.

This phase consequently fails at the canonical human-claim identity gate, before a minimal import
set, canonical Lean expression, expression hash, checked transport, or the required removed-
hypothesis/domain/binder-scope/boundary mutation suite can be established.

## Pinned Lean boundary

`StatementProbe.lean` is deliberately not a target declaration. It checks that the existing pinned
mathlib revision provides `ProbabilityTheory.HasGaussianLaw`, Bochner integration,
`Metric.coveringNumber`, `Metric.packingNumber`, and `Metric.IsSeparated`. The probe uses two direct
imports and elaborates, but this establishes only infrastructure availability. It does not choose
an entropy convention, define the canonical increment pseudometric, or encode Sudakov minoration.
Accordingly, the imports are not claimed to be minimal for the still-unidentified exact target.

A repository and pinned-mathlib search for `Sudakov`, `minoration`, and Gaussian/metric-entropy
combinations found no formal declaration capable of settling the statement identity. That search
is only a statement-gate diagnostic, not the downstream anchor audit.

## Required unblock

An accountable source review must inspect a stable primary or selected authoritative edition and
record the exact theorem/page, wording, definitions, all hypotheses, normalization, entropy
convention, constant scope, and errata. It must also decide the finite-versus-separable-process
form and all degenerate cases. A later statement worker can then encode that exact claim, minimize
its pinned imports, serialize and hash the elaborated expression/environment, provide checked
alternate-form transports, and execute all four mutation classes.

## Narrow validation evidence

Commands ran from this worker clone on 2026-07-12. Lean ran through the existing pinned Lake
environment. No `lake update`, build, dependency fetch, or `.lake` mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1086` | 0 | rank 528; planned; `L0/rework_required`; theorem incomplete |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1086/StatementProbe.lean` | 0 | all five pinned infrastructure declarations elaborated |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | `651c8acc...b1d2`; `321626c8...2d81` |

First failed gate: exact source-statement identity. Known failures are the canonical target,
minimal-import proof, expression fingerprint, checked transports, and mutation tests. The assigned
deliverable is therefore blocked rather than self-tested, and no `.stage1-worker-selftest.json` is
emitted. No statement-node acceptance, audit completion, or theorem completion is claimed.
