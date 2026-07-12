# Statement gate blocker

Item: `S56-M-0150-STATEMENT`  
Theorem: `THM-M-0150`  
Verdict: blocked; no exact canonical Lean target is claimed.

## First failed gate

The intake freezes the human claim as finite generation of

`R(X,K_X) = direct_sum_{m >= 0} H^0(X, O_X(mK_X))`

for a smooth projective variety of general type over the complex numbers. The pinned mathlib
snapshot has schemes and scheme-morphism predicates including smoothness and properness, but its
algebraic-geometry tree has no definitions for the canonical sheaf or canonical divisor of a
variety, tensor/reflexive powers of that object, the resulting graded section ring, or general
type. It also has no theorem or declaration matching the Hacon-McKernan/BCHM canonical-ring result.
Consequently the conclusion and one essential hypothesis cannot be represented by the pinned API.

Defining local opaque predicates named `IsOfGeneralType` or `CanonicalRing`, or taking those
predicates as parameters, would merely encode an uninterpreted proxy. It would not elaborate the
exact mathematical target, and would violate the rev-5.6 prohibition on placeholder and substituted
statements. Replacing projectivity by properness or replacing the canonical ring by an arbitrary
graded algebra would also weaken or broaden the claim. Therefore no canonical declaration,
expression hash, checked transport, or mutation tests can truthfully be emitted in this phase.

`StatementInfrastructure.lean` checks only the available, noncontroversial substrate. Its local
`SmoothProper` conjunction is a probe and is explicitly not the target: properness is not accepted
as a checked encoding of projectivity here. No theorem, axiom, `sorry`, proxy canonical-ring
definition, or proof claim was introduced. The machine state remains `M4` and theorem completion
is false.

## Environment fingerprint

- Repository base revision: `18e5e2e7f79baaa12f66c2b1214a9c5fe5bf3b5b`.
- Validation date: 2026-07-12 (Asia/Shanghai).
- Lean toolchain file: `leanprover/lean4:v4.29.0`.
- Checked mathlib revision: `8a178386ffc0f5fef0b77738bb5449d50efeea95`.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- Lake manifest SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Validation evidence

Commands ran from this worker clone using only the existing pinned `.lake` artifacts. No update,
build, fetch, or clone command was used.

| Command | Exit | Result |
|---|---:|---|
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0150/StatementInfrastructure.lean` | 0 | Scheme, smooth/proper morphism, and algebra finite-type substrate elaborated; four expected types printed |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `rg -n -i 'Hacon|McKernan|log canonical ring|general type|canonical (sheaf|divisor)' Formalizations/Lean/.lake/packages/mathlib/Mathlib/AlgebraicGeometry --glob '*.lean'` | 1 | No matching pinned algebraic-geometry source declaration |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0150` | 0 | Rank 324, planned, L0/rework-required, theorem incomplete |
| `git diff --check -- Stage1_Instances/THM-M-0150` | 0 | No whitespace errors |

## Retry condition

Add pinned, kernel-checkable definitions for varieties over `C`, projectivity, the canonical
sheaf/divisor and its powers, global sections and their graded multiplication, finite generation of
that graded algebra, and general type, with checked bridges to the selected BCHM specialization.
The next statement run can then elaborate the exact ordered target and mutation-test the base field,
smoothness, projectivity, general-type hypothesis, and canonical-ring conclusion.

Until then the statement gate is blocked. Because the assigned phase is not genuinely self-tested
to its completion gate, no `.stage1-worker-selftest.json` is emitted.
