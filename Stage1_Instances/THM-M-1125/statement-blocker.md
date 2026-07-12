# Exact-statement gate: blocked

Item: `S56-M-1125-STATEMENT`  
Base revision: `270e3fb34fda8c9a44c27d55bd2b9ac69b3c4945`

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the repository source record. The
record supplies only the title "conformal field theory and SLE" and the gloss "the connection
between CFT and SLE". It gives no exact source proposition, theorem locator, SLE variant, CFT
formalism, normalization, hypotheses, or conclusion. The accepted intake therefore freezes a
theorem family while explicitly leaving the exact result open.

The intake identifies Bauer and Bernard, *Conformal Field Theories of Stochastic Loewner
Evolutions* (2003), and Friedrich and Werner, *Conformal Restriction, Highest-Weight
Representations and SLE* (2003), only as discovery leads. It records that neither immutable
edition was inspected result by result. Selecting a familiar statement from either paper would
invent the missing repository intent, and the papers' martingale and restriction formulations are
not interchangeable.

Within this family, each of the following changes the proposition rather than merely its Lean
encoding:

- chordal, radial, dipolar, multiple, or `SLE(kappa,rho)`, together with the domain and marked
  points;
- the range of `kappa`, half-plane-capacity scale, and Brownian normalization;
- the precise Virasoro module, highest-weight vector, central-charge and conformal-weight
  conventions, and the coefficients of the level-two null vector;
- the chosen correlation or partition-function observable, filtration, lifetime, and collision or
  explosion stopping rule;
- local martingale versus true martingale, including localization and integrability hypotheses;
- algebraic degeneracy implying a stochastic statement, its converse, conformal covariance, or a
  restriction theorem.

The Stage0 entry confirms that precise definitions and prerequisites are `待补充` (to be supplied),
and its `已验证` label is explicitly untrusted under rev-5.6. A repository-local Lean search found
only unrelated mentions of conformal field theory, and pinned mathlib contains no Lean source match
for Schramm-Loewner evolution, conformal field theory, or Virasoro. These searches do not constitute
the later anchor audit; they only confirm that no existing local declaration resolves the source
ambiguity at this gate.

Consequently the phase fails at exact human-claim identity, before ordered binders, minimal
imports, an elaborated expression fingerprint, checked alternate-form transports, or meaningful
removed-hypothesis/domain/binder-scope/boundary mutation tests can be established. Introducing an
abstract structure that assumes the null-vector identity or martingale conclusion would be a
forbidden placeholder and a broadened theorem, not an elaboration of the repository claim.

## Required unblock

An accountable source reviewer must select an immutable primary edition and one exact numbered
theorem or displayed result, inspect its definitions and errata, and freeze all proposition-changing
choices listed above. The source crosswalk must identify the exact observable, quantifier order,
analytic hypotheses, stopping convention, and claimed direction of correspondence. A later
statement worker can then encode that precise claim, minimize the pinned imports, preserve and hash
the elaborated expression, provide checked transports, and run the four required mutation classes.

## Narrow validation evidence

Commands ran in this worker clone on 2026-07-12. The existing canonical `.lake` artifacts were used
read-only; no update, build, clone, fetch, or dependency mutation was performed.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1125` | exit 0; rank 565, planned, `L0/rework_required`, legacy artifacts unaccepted, theorem incomplete |
| `(cd Formalizations/Lean && lake env lean --version)` | exit 0; Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | exit 0; pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | exit 0; `651c8acc...b1d2` and `321626c8...2d81` |
| `rg -n -i 'Schramm.Loewner\|conformal field theor\|Virasoro' Formalizations/Lean --glob '*.lean' --glob '!**/.lake/**'` | exit 0; five unrelated CFT text mentions in `S1_M_177.lean` and `S1_M_181.lean`, no THM-M-1125 declaration or SLE result |
| `rg -n -i 'Schramm.Loewner\|conformal field theor\|Virasoro' Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'` | exit 1; no matches |

First failed gate: exact source-statement identity. Known failures are the canonical Lean target,
minimal-import determination, expression and environment fingerprint, checked transports, and all
four required mutation classes. The assigned phase is therefore not self-tested or complete, and
no `.stage1-worker-selftest.json` is emitted. No statement-node acceptance, downstream credit,
audit completion, or theorem completion is claimed.
