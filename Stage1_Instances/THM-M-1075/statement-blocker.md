# Exact-statement gate: blocked

Item: `S56-M-1075-STATEMENT`

Theorem: `THM-M-1075`

Base revision: `1a19c121b34bfc2825a510958326294a95c9deb9`

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the authoritative repository record.
The complete supplied mathematical wording is the title "renewal process" (`更新过程`) and the
content phrase "renewal theory" (`更新理论`). These name an object and a subject containing many
results; they do not assert a truth-valued proposition.

In particular, the record does not determine:

- an ordinary, delayed, terminating, arithmetic, or continuous-time renewal model;
- the probability space or the independence, identical-distribution, positivity, finiteness,
  moment, or nonarithmetic assumptions on interarrival times;
- definitions and endpoint conventions for renewal epochs `S_n`, the counting process `N(t)`, and
  the renewal measure or function;
- whether the conclusion is a construction, measurability result, renewal equation, expectation
  identity, almost-sure limit, expectation asymptotic, or distributional assertion; or
- the ordered binders and treatment of time zero, zero interarrivals, defective laws, and infinite
  means.

These choices produce inequivalent propositions. Selecting a definition, renewal equation,
elementary renewal theorem, or asymptotic result would substitute an unstated theorem rather than
elaborate the catalogue claim. Smith's key renewal theorem (`THM-M-1076`) and Blackwell's renewal
theorem (`THM-M-1077`) are separately scheduled targets and cannot supply this target's statement.

The accepted intake dependency records the same fail-closed boundary and provisional vector
`[H5, M4, R4]`. The source status `已验证` is untrusted metadata and supplies neither statement nor
kernel evidence. Consequently this phase fails at canonical human-claim identity, before minimal
imports, an elaborated-expression fingerprint, checked transports, or meaningful removed-
hypothesis, changed-domain, binder-scope, and boundary-case mutations can be established. No Lean
declaration, axiom, abstract structure containing a desired conclusion, weakened special case, or
broadened theorem was introduced.

## Pinned environment and scoped search

Commands were run inside this worker clone on 2026-07-12 (Asia/Shanghai). The canonical `.lake`
directory was read through its existing symlink only; no update, build, clone, fetch, or dependency
mutation command was run.

- Lean toolchain: `leanprover/lean4:v4.29.0`; Lean 4.29.0, commit
  `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- Lake: `5.0.0-src+98dc76e`.
- Checked mathlib revision: `8a178386ffc0f5fef0b77738bb5449d50efeea95`.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1075` | 0 | Rank 517, planned, legacy artifacts unaccepted, theorem incomplete |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean version and commit recorded above |
| `cd Formalizations/Lean && lake --version` | 0 | Lake version recorded above |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | Produced the two hashes recorded above |
| `git -C "$(readlink -f Formalizations/Lean/.lake/packages/mathlib)" rev-parse HEAD` | 0 | Produced the pinned mathlib revision recorded above |
| repository `rg` search for the ID, Chinese wording, and English translations | 0 | Found only underspecified catalogue metadata and related separately owned dossiers; no source-frozen proposition or Lean target |
| pinned-mathlib `rg` search for renewal process, renewal theory/theorem/function, and interarrival terminology | 1 | No matches; `rg` exit 1 means no occurrence |

There is no applicable `lake env lean <target>.lean` elaboration check because no exact expression
exists. Elaborating a conveniently chosen renewal theorem or an abstract interface that assumes a
desired result would be fake statement evidence, not the assigned deliverable.

## Retry condition

An accountable source review must preserve an immutable theorem-bearing primary source, identify
and transcribe one exact theorem with page and definitions, dispose of errata, freeze every model,
assumption, convention, binder, conclusion, and boundary choice listed above, and independently
approve the crosswalk. A later statement run can then encode the claim using real Lean definitions,
minimize pinned imports, serialize and hash the elaborated expression and environment, check any
alternate transports, and execute all four required mutation classes.

This records the first failed gate and does not complete the statement node or any later node. The
assigned phase is not genuinely self-tested to its completion gate, so no
`.stage1-worker-selftest.json` is emitted.
