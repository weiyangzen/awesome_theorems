# Exact-statement gate: blocked

Item: `S56-M-1354-STATEMENT`

Theorem: `THM-M-1354`

Base revision: `8c50139eafcb1c2e29e7ca69379648590820bf53` (tree
`84cd63b08ff977c1b895e0299927df8b6d6bc8ae`).

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the authoritative repository record.
That record supplies only the title `特征指数` (characteristic exponent), Gaston Floquet, 1883,
and the gloss `周期系统的特征值` (eigenvalues of periodic systems). It provides no cited
truth-valued proposition, definitions, ordered binders, hypotheses, conclusion, proof boundary, or
boundary cases. Stage0 explicitly leaves the precise definitions and premises, proof route,
equivalent statements, axioms, machine status, and artifact links open. The catalog value `已验证`
is untrusted metadata under rev-5.6.

The title and gloss do not select the same spectral object unambiguously. At least these materially
different roots remain possible:

- characteristic multipliers `rho`, defined as eigenvalues of a one-period monodromy matrix;
- characteristic exponents `mu` satisfying `exp(T * mu) = rho`, with nonunique logarithm branches;
- eigenvalues of a constant exponent matrix in a Floquet decomposition;
- a theorem relating the multiplier and exponent encodings, with multiplicity and base-time rules;
- a Floquet solution representation `exp(mu * t) * p(t)`; or
- a stability criterion using multiplier moduli or exponent real parts.

The inspected source-family material confirms this separation but cannot select a target. Floquet's
1883 paper was identified only through Numdam and Crossref bibliographic metadata; the catalog does
not cite it and no exact passage was admitted. Teschl, *Ordinary Differential Equations and
Dynamical Systems*, Section 3.6, separately describes monodromy multipliers, characteristic
exponents, their exponential relation, and a later stability corollary. The catalog does not cite
Teschl either. Neither discovery lead supplies an accepted immutable proposition, incorporated
definitions, assumption and conclusion crosswalk, proof boundary, errata disposition, or
independent review.

The missing choices are proposition-changing: periodic-system model, scalar field, dimension,
coefficient regularity, positive or minimal period, solution-matrix normalization and base time,
monodromy orientation, multiplier versus exponent, logarithm and branch policy, algebraic versus
geometric multiplicity, repeated or defective spectrum, exact conclusion, binder order, and the
zero-dimensional, scalar, zero-period, identity-monodromy, unit-circle, purely imaginary, real-log,
complexification, period-doubling, and generalized-eigenvector cases. Selecting a familiar variant
would invent or substitute mathematics. Assuming the desired monodromy, exponent relation, Floquet
representation, or stability conclusion as data would merely hide the same gap.

The intake therefore correctly leaves the canonical human statement, Lean module and expression,
minimal imports, and expression/environment fingerprints null. Without one canonical target, there
is no meaningful alternate-form transport or removed-hypothesis, changed-domain,
changed-binder-scope, and boundary-case mutation suite. No `Statement.lean`, axiom, placeholder,
weakened special case, or broadened interface was added. The root remains `[H5, M4, R4]`.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` was re-elaborated against the pinned environment. Its six direct
imports expose generic periodicity, integral-curve, matrix-exponential, characteristic-polynomial,
spectrum, and eigenvalue APIs. All eleven checked interfaces elaborate. They do not define a
periodic linear system, fundamental matrix, monodromy, Floquet multiplier, or characteristic
exponent, and the imports cannot be certified minimal for an absent target. The successful check
receives no statement, anchor, or proof credit.

A bounded repo-local and pinned-mathlib search found no exact-topic declaration under the recorded
Floquet, characteristic-exponent, characteristic-multiplier, periodic-fundamental-matrix, or
monodromy terms. This is a local feasibility boundary, not the later immutable anchor audit or a
global absence claim.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib
revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` (tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`). The `lean-toolchain` SHA-256 is
`651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`; the
`lake-manifest.json` SHA-256 is
`321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`; and the probe SHA-256
is `b8be1474907c0abd6c786e48fe0bbfffa7f7b8a9974ac20ff88ce09bcf7bfc6b`.

The automation-provided `Formalizations/Lean/.lake` link to canonical pinned artifacts was used
read-only. No update, build, dependency clone, fetch, or other `.lake` mutation was run.

## Validation Evidence

Commands ran in this worker clone on 2026-07-13 (Asia/Shanghai). Commands ran from the repository
root unless a different working directory is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1354` | 0 | rank 964, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` (pre-edit) | 0 | only the automation-provided `.lake` link was untracked; base revision and tree appear above |
| authority, catalog, Stage0, intake, source-boundary, and neighbor inspection | 0 | found the sparse catalog record, explicit null intake target, and inequivalent multiplier, exponent, decomposition, representation, and stability roots; no source-selected proposition |
| `sha256sum` over authority, intake, probe, toolchain, dependency-lock, and pinned mathlib inputs | 0 | current hashes are recorded in `statement-blocker.json` |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | Lean and Lake match the pinned environment fingerprint above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | revision and tree match the fingerprint above; package worktree is clean |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1354/IntakeProbe.lean)` | 0 | eleven adjacent periodicity, ODE, matrix, exponential, characteristic-polynomial, spectrum, and eigenvalue interfaces elaborated; no target theorem was checked |
| bounded exact-topic `rg` search in repo-local Lean and pinned mathlib | 1 | expected no-match result; no target-specific declaration was located under the recorded terms |
| `python3 -B Stage1_Instances/THM-M-1354/check_intake.py` | 1 | historical intake replay stops at its stale blueprint hash; it also freezes the earlier base, authority state, and intake-only file inventory, so this phase did not rewrite it |
| `python3 -m json.tool Stage1_Instances/THM-M-1354/statement-blocker.json` | 0 | the finalized structured blocker parsed as valid JSON |
| scoped statement-blocker invariant assertions | 0 | IDs, rank, blocked verdict, null target and fingerprints, unchanged `[H5, M4, R4]`, false completion flags, exact changed paths, and absent worker packet agree |
| prohibited Lean construct scan over `Stage1_Instances/THM-M-1354` | 1 | expected no-match result; the API-only probe contains no `sorry`, `admit`, `sorryAx`, axiom, bodyless declaration, or unsafe declaration |
| scoped and per-file whitespace checks for both new blocker artifacts | 0 / 1 per new file | no whitespace diagnostics; each no-index exit is only the expected new-file difference status |
| `test ! -e .stage1-worker-selftest.json` | 0 | the worker packet is absent because the statement completion gate did not pass |

The intake prerequisite itself is only worker-provisional `[_]`, its receipt is not accepted, and
its historical checker freezes pre-integration authority and file inventory. This statement phase
does not rewrite or refresh separately owned intake evidence. That freshness and dependency issue
independently prevents statement-node acceptance.

## Retry Condition

The integration lane must first master-accept refreshed intake evidence. Accountable reviewers must
preserve and hash a lawful immutable primary or authoritative source, select or correct one exact
truth-valued theorem and every incorporated definition with pinpoint locators, audit translation,
corrections and errata, reconcile the neighboring Floquet-theory, fundamental-matrix, and stability
targets, and independently approve the source crosswalk. The selection must fix the periodic system,
field, dimension, regularity, period, fundamental matrix, monodromy, multiplier-versus-exponent and
logarithm-branch convention, multiplicity, ordered binders, exact conclusion, and every boundary
case.

A later statement worker can then encode that same claim using real Lean definitions, minimize its
pinned imports, serialize and hash the elaborated expression and environment, check every credited
transport, and execute all four required mutation classes.

This is the first failed gate, not completion of the statement node or a downstream node. The root
remains `[H5, M4, R4]`, with `audit_complete: false` and `theorem_complete: false`; no debt-vector
change is proposed. The assigned phase is not genuinely self-tested to its completion gate, so no
`.stage1-worker-selftest.json` is emitted and no statement-node or master-acceptance receipt is
claimed.
