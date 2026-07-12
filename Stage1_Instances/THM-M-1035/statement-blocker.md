# Exact-statement gate: blocked

Item: `S56-M-1035-STATEMENT`  
Base revision: `81c766970d38b9ae3179b58cc75a46425a624c6e`

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the repository source record. The
complete mathematical wording is `另一种随机积分定义` ("another definition of stochastic
integral"), under the name "Stratonovich integral". This names a family of constructions rather
than one proposition and does not determine:

- the probability space, filtration, time domain, or class of integrands and integrators;
- the partition model, tags, midpoint convention, and limiting refinement;
- the convergence mode (pathwise, in probability, in an `L^p` space, or another topology);
- the hypotheses that make the limit exist, such as semimartingale and integrability conditions;
- whether the intended root is a definition, an existence theorem, an Ito-Stratonovich conversion
  formula, or the Stratonovich chain rule;
- the equality convention, normalization, initial/terminal times, and degenerate cases.

These choices give inequivalent statements. Selecting one would broaden or substitute the source
claim rather than elaborate it exactly. The Stage0 entry independently marks precise definitions,
hypotheses, proof details, axioms, and machine artifacts as `待补充` (to be supplied). Its metadata
label `已验证` is explicitly untrusted under rev-5.6 and is not a source or kernel receipt.

The intake dependency preserves this ambiguity with root vector `[H3, M3, R3]` and a null canonical
statement. Consequently the phase fails at canonical human-claim identity, before a minimal import,
an elaborated expression fingerprint, checked transports, or meaningful removed-hypothesis,
changed-domain, binder-scope, and boundary mutations can be fixed.

## Legacy Lean boundary

`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_228.lean` was inspected and elaborated only as
legacy discovery input. Its finite sum uses `Nat`-indexed real-valued functions. Its
`StratonovichIntegralData` then stores the stochastic-basis, semimartingale, integrability,
mesh-limit, midpoint-convergence, Ito-conversion, and chain-rule requirements as unconstrained
`Prop` fields. `StatementShape` assumes several of those fields and asks for a conclusion structure
that repeats them alongside additional obligations. It is therefore an abstract interface package,
not a formalization crosswalked to an identified Stratonovich definition or theorem.

The legacy file elaborates with five broad direct imports in the existing pinned environment. This
establishes only that the old interface and its substrate wrappers are type-correct. It neither
identifies the exact target nor establishes minimal imports for one, and it receives no rev-5.6
statement credit.

## Required unblock

An accountable source reviewer must identify an authoritative source by stable edition,
theorem/definition number or page, and exact wording. The review must freeze the process classes,
filtration and time model, partitions and midpoint convention, topology of convergence, all
existence/integrability assumptions, precise conclusion, normalization, and boundary cases. A
later statement worker can then encode that claim without substitution, minimize pinned imports,
serialize and hash its elaborated expression, add checked transports, and run the four required
mutation classes.

## Narrow validation evidence

Commands were run from this worker clone on 2026-07-12. The existing `.lake` path is a symlink to
the canonical pinned artifacts; no `lake update`, build, fetch, clone, or `.lake` mutation was
performed.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1035` | exit 0; rank 228, planned, `L0/rework_required`, legacy artifacts unaccepted, theorem incomplete |
| `(cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_228.lean)` | exit 0; legacy abstract interface and substrate wrappers elaborated; no exact Stratonovich target checked |
| `(cd Formalizations/Lean && lake env lean --version)` | exit 0; Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | exit 0; `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | exit 0; `651c8acc...b1d2` and `321626c8...2d81` |

First failed gate: exact source-statement identity. Known failures are canonical target selection,
minimal-import determination, expression fingerprinting, checked transports, and mutation tests.
The assigned phase is not self-tested or complete, so no `.stage1-worker-selftest.json` is emitted.
No theorem completion or downstream-node credit is claimed.
