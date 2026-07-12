# Exact-statement gate: blocked

Item: `S56-M-1093-STATEMENT`  
Base revision: `388f85443db876842b04fb42b0e5a952f22f66d9`

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the repository source record. The
mathematical source wording for this target is only `概率密度的演化方程` ("evolution equation for a
probability density"). A second repository research list gives the displayed formula
`partial_t p = -partial_x (A p) + partial_xx (B p)` and the dates 1914/1917, but neither record
identifies an edition, page, equation, stochastic model, or theorem with hypotheses and a
conclusion.

In particular, the records do not determine:

- whether the target is the displayed PDE identity, a derivation from a diffusion, a classical or
  weak existence theorem, a uniqueness theorem, or a law/semigroup evolution theorem;
- whether the diffusion coefficient is `B` as displayed or a variance coefficient `a = 2 B`, which
  changes whether the second-order term has coefficient `1` or `1/2`;
- the time and state domains, initial and boundary conditions, and treatment of nonnegative time;
- coefficient measurability, ellipticity/degeneracy, growth, and regularity assumptions;
- the solution class, density existence, differentiability and integrability conditions;
- probability normalization, nonnegativity, mass preservation, uniqueness, or the conclusion's
  quantifier strength.

Those choices yield inequivalent propositions. The intake therefore correctly labels its
one-dimensional existence-and-uniqueness formulation provisional at `[H3, M3, R3]` and says that
the statement phase must first decide among a PDE identity, an SDE/Markov derivation, and an
existence-and-uniqueness theorem. It does not provide source authority for making that decision.
Consequently the phase fails at canonical human-claim identity, before an exact expression hash,
minimal imports, checked alternate transports, or meaningful mutations can be established.

## Historical Lean boundary

`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_217.lean` was checked only as discovery input. Its
`StatementShape` asserts existence of `FokkerPlanckDensityEvolution` for every package satisfying
several unconstrained `Prop` fields. The result bundles a classical equation, a selected weak
equation, probability normalization for every real time, initial trace, law agreement, generator
compatibility, and uniqueness. These are substantial additions to the source gloss, not a direct
encoding of it. The module itself says it is a conservative boundary for a future formalization and
does not prove the terminal theorem.

The historical module elaborates in the pinned environment, but that establishes only that its
candidate definitions are type-correct. Its nine direct imports are not evidence of minimal imports
for an exact target, because the source does not identify an exact target. Adopting
`StatementShape`, or replacing it with the bare pointwise PDE predicate, would substitute a chosen
theorem for the missing source theorem and is forbidden by this gate.

## Required unblock

An accountable source reviewer must freeze a stable source by edition, theorem/equation and page,
exact wording, and assumptions. The review must select the coefficient convention, domain,
initial/boundary data, solution notion and regularity, and whether the conclusion is an identity,
derivation, existence, preservation, or uniqueness claim. A later statement worker can then encode
that claim, minimize pinned imports, print and hash the elaborated expression, check any alternate
encoding transport, and mutation-test its hypotheses, domains, binder scopes, and boundary cases.

## Narrow validation evidence

Commands ran inside this worker clone on 2026-07-12. No Lake update, build, dependency fetch, or
mutation of `.lake` was performed.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1093` | exit 0; rank 217, planned, `L0/rework_required`, legacy artifacts unaccepted, theorem incomplete |
| `(cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_217.lean)` | exit 0; historical candidate declarations elaborated and printed; no exact-statement credit |
| `(cd Formalizations/Lean && lake env lean --version)` | exit 0; Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | exit 0; `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | exit 0; `651c8acc...b1d2` and `321626c8...2d81` |

First failed gate: exact source-statement identity. Known failures are the canonical Lean target,
minimal-import determination, expression and environment fingerprint for that target, checked
transports, and mutation tests. The assigned phase is not self-tested or complete, so no
`.stage1-worker-selftest.json` is emitted. No theorem completion or downstream-node credit is
claimed.
