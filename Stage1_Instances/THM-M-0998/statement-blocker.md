# Exact-statement gate: blocked

Item: `S56-M-0998-STATEMENT`  
Theorem: `THM-M-0998`  
Base revision: `ac680cc80e4b42c3cb2c59fc038ab8c5c5fb5e16`

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the repository source record. The
complete mathematical wording available for this probability-category entry is `方差的上界`
("an upper bound on variance"), under the name Poincare inequality. This identifies a theorem
family, but it does not determine one proposition. In particular, the record does not fix:

- the state space, probability measure, or normalization;
- the admissible real-valued functions and their measurability, integrability, or regularity;
- the Dirichlet/gradient energy, derivative structure, or boundary conditions;
- the Poincare constant, its quantification, normalization, finiteness, or positivity;
- whether the intended result is Gaussian, Euclidean, manifold, Markov-chain, graph, or another
  inequivalent variance-energy inequality;
- the centering convention and treatment of constant or zero-energy functions.

The Stage0 record explicitly marks precise definitions and hypotheses as `待补充` (to be supplied),
and the research note repeats only the same one-line gloss. The historical `已验证` value is
untrusted metadata under rev-5.6, not a theorem-level source or a statement receipt. The intake
therefore correctly leaves the canonical formal target null with root vector `[H4, M4, R4]`.

Choosing a familiar formulation would broaden or substitute the source claim. In particular, the
finite reversible Markov-chain formulation and the abstract user-supplied energy predicate in the
legacy Lean module are possible models, not checked encodings of the unspecified root. Consequently
this phase fails at canonical human-claim identity, before a minimal import, elaborated expression
fingerprint, alternate-form transport, or meaningful removed-hypothesis/domain/binder/boundary
mutation suite can exist. The intake dependency is also only provisional (`[_]`) pending master
acceptance; this worker does not promote it.

## Legacy Lean discovery check

`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_278.lean` imports
`Mathlib.Probability.Moments.Variance` and elaborates in the existing pinned environment. Its
`PoincareInequality` quantifies over an arbitrary `EnergyFunctional`, while
`FiniteReversibleMarkovChainPoincareStatement` selects a finite-chain model. The module itself says
these are predicate/statement boundaries and does not claim the full Poincare theorem. Successful
elaboration establishes only that these legacy declarations are type-correct; it cannot establish
source identity or minimal imports for an exact rev-5.6 target.

## Required unblock

An accountable source reviewer must identify an immutable primary source by edition and exact
theorem/page, then freeze its carrier, measure, admissible functions, variance convention, energy,
constant convention, quantifier order, boundary/centering assumptions, and degenerate cases. A
later statement worker can then encode exactly that claim, minimize imports in the pinned closure,
serialize and hash the elaborated expression and environment, check any credited transports, and
run all four required mutation classes.

## Narrow validation evidence

Commands were run from this worker clone on 2026-07-12. No dependency update, build, clone, fetch,
or `.lake` mutation was performed.

| Command | Exit | Exact result or scope |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0998` | 0 | rank 278; planned; L0/rework-required; legacy artifacts unaccepted; theorem incomplete |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release |
| `(cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_278.lean)` | 0 | legacy module elaborated and printed declaration types; discovery check only |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`; `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81` |

First failed gate: exact source-statement identity. Known failures are exact target elaboration,
minimal-import determination, expression/environment fingerprinting, checked transports, and the
four semantic mutation classes. The assigned phase is not self-tested or complete, so no
`.stage1-worker-selftest.json` is emitted. No proof, theorem completion, downstream phase, or
master-acceptance credit is claimed.
