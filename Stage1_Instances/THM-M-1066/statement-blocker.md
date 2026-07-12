# Exact-statement gate: blocked

Item: `S56-M-1066-STATEMENT`  
Theorem: `THM-M-1066`  
Base revision: `63dd69def57f86f9ff668f657fbd2bbef39b8068`  
Base tree: `b4615edd9544733c053912eb732166270b0bd334`

## Decision

The authoritative repository claim is only "strong approximation of a random walk by Brownian
motion" (`随机游走向布朗运动的强逼近`). It identifies the Komlos-Major-Tusnady theorem family but
does not determine one exact proposition. The intake record correctly leaves the canonical formal
target and its module unset and makes primary-source variant selection a statement blocker.

The discovery citations to Parts I (1975) and II (1976) have not been inspected as immutable
editions and do not provide a theorem/page crosswalk. In particular, the repository record does not
freeze:

- whether increments are identically distributed or only independent, and the exact centering,
  variance, nondegeneracy, and exponential-moment conditions;
- whether the theorem constructs copies on a new probability space or couples an existing random
  walk, and the required marginal-law, independence, and Brownian-motion conditions;
- whether the root is the nonasymptotic exponential tail inequality or its almost-sure
  `O(log n)` consequence;
- the order and ranges of the horizon, deviation, and constant quantifiers, including which data
  the constants may depend on;
- the maximum's index set, logarithm convention, strictness of inequalities, additive terms, and
  treatment of small horizons and degenerate laws;
- whether a scalar partial-sum theorem, a non-identically-distributed extension, or an
  empirical-process result from the KMT paper series is intended.

These alternatives have different domains, binders, hypotheses, and conclusions. Choosing one
would broaden, narrow, or substitute the source claim rather than elaborate it exactly. A generic
Lean interface that assumes the desired coupling or discrepancy estimate would likewise not be an
elaboration of the KMT existence theorem.

Consequently there is no truthful Lean declaration to place in `Statement.lean`: minimal imports,
an expression fingerprint, checked transports, and meaningful removed-hypothesis, changed-domain,
binder-scope, and boundary mutations all depend on a source-exact proposition. No theorem
declaration or proof escape was introduced. The machine state remains `M3`, and statement
acceptance, audit completion, and theorem completion remain false.

## Pinned environment and checks

- Validation date: 2026-07-12 (Asia/Shanghai).
- Lean toolchain: `leanprover/lean4:v4.29.0`; Lean 4.29.0, commit
  `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- Lake: `5.0.0-src+98dc76e`.
- Pinned mathlib revision: `8a178386ffc0f5fef0b77738bb5449d50efeea95`.
- `Formalizations/Lean/lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `Formalizations/Lean/lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

All commands ran in this worker clone. Existing `.lake` artifacts were read only; no update, build,
clone, or fetch command was used.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1066` | 0 | Rank 508, planned, legacy artifacts unaccepted, theorem incomplete |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0 at the commit recorded above |
| `cd Formalizations/Lean && lake --version` | 0 | Lake version recorded above |
| `cd Formalizations/Lean && sha256sum lean-toolchain lake-manifest.json` | 0 | Produced the two hashes recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | Produced the pinned mathlib revision recorded above |
| `rg -n -C 4 'THM-M-1066|KMT定理|随机游走向布朗运动的强逼近' Docs/Stage0_Blueprint.md Docs/Stage1_Targets_rev-5.6.json Stage1_Instances/THM-M-1066` | 0 | Found only the underspecified source metadata and intake discovery records; no source-frozen proposition |
| `rg -n -i 'Koml[oó]s|Major.Tusn[aá]dy|strong approximation|KMT' Formalizations/Lean/.lake/packages/mathlib/Mathlib Formalizations/Lean/.lake/packages/mathlib/Archive` | 1 | No KMT-specific declaration or source statement in pinned mathlib (`1` is the expected no-match result) |

There is no applicable `lake env lean <target>.lean` command because the exact target does not
exist. Elaborating a convenient candidate would be false evidence for the assigned gate.

## Retry condition

An accountable source review must select a content-addressed edition and exact theorem/page from
the KMT papers, record errata status, and crosswalk every premise and conclusion. It must freeze the
increment class, moment assumption, coupling semantics, Brownian normalization, constant
dependencies, tail formula, quantifier order, and all boundary conventions above. A later statement
run can then encode that proposition with minimal pinned imports, preserve its elaborated
expression and environment fingerprints, and execute the required structural mutations.

The assigned phase is not genuinely self-tested to its completion gate, so no
`.stage1-worker-selftest.json` is emitted.
