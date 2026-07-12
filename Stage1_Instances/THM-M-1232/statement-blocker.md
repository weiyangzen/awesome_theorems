# Exact-statement gate: blocked

Item: `S56-M-1232-STATEMENT`  
Theorem: `THM-M-1232`  
Base revision: `854537bcbb10ad4c68b5a61f06171fffcec64961`

## Decision

The exact Lean 4 target cannot be truthfully elaborated. The screened mathematical source says
only `理想流体的运动方程` ("equations of motion of an ideal fluid"). The related physics inventory
displays `rho (Dv/Dt) = -grad P + rho g`, but does not bind any symbol or assert a
proposition-level conclusion. In particular, the repository does not select:

- compressible or incompressible flow, or the accompanying mass/incompressibility equation;
- spatial dimension, spatial domain, time interval, scalar field, or boundary conditions;
- density and pressure regularity, an equation of state, or the treatment of vacuum;
- a classical, weak, distributional, or other solution concept;
- whether the target asserts a derivation, characterization, existence, uniqueness,
  conservation law, or regularity result.

These choices are not alternate spellings of one theorem. Encoding only the displayed momentum
formula would still require inventing its types and semantics. Taking it as a hypothesis and
returning it would be a tautological wrapper, while choosing an existence or regularity theorem
would broaden or substitute the source claim. The neighboring Beale-Kato-Majda, Yudovich, and
Wolibner records also show that those more specific Euler results are intentionally separate
targets.

Consequently there is no canonical declaration or expression fingerprint, no import set whose
minimality can be established for that declaration, and no meaningful removed-hypothesis,
changed-domain, binder-scope, or boundary-case mutation suite. Machine debt remains `M4`.

## Lean boundary checked

`StatementProbe.lean` uses one pinned mathlib import to elaborate `fderiv`, `HasFDerivAt`, and
`gradient`, calculus primitives that could occur in one modern Euclidean formulation. This checks
only available substrate. It does not define the material derivative, divergence constraint,
fluid domain, or Euler system and is not the target statement.

The environment is Lean `4.29.0` (commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`) with mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, using the existing canonical `.lake` artifacts. No
dependency update, build, clone, or fetch was performed.

## Validation record

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups; 1546 uniform-L0 targets; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1232` | 0 | rank 417; planned; L0/rework-required; theorem incomplete |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1232/StatementProbe.lean` | 0 | `fderiv`, `HasFDerivAt`, and `gradient` elaborated |
| `git diff --check -- Stage1_Instances/THM-M-1232` | 0 | no output |

## Retry condition

Retry after an authoritative source decision fixes one proposition and supplies every regime,
domain, binder, hypothesis, convention, and conclusion needed for a source-to-Lean crosswalk. The
statement phase can then elaborate that exact target, minimize its imports, fingerprint the
expression and environment, check transports, and run the required mutations.

This artifact does not complete the statement node, accept a receipt, or claim audit/theorem
completion. No `.stage1-worker-selftest.json` is emitted because the assigned deliverable is not
genuinely self-tested.
