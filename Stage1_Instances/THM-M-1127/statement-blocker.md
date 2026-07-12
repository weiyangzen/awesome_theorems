# S56-M-1127-STATEMENT blocker

Item: `S56-M-1127-STATEMENT`  
Theorem: `THM-M-1127` (d'Alembert formula)  
Base revision: `540de1f8d50dd82b5695b80f6568f470b21233a4`

## Verdict

The rev-5.6 exact-statement gate is blocked. No canonical Lean target, elaborated-expression
fingerprint, checked transport, mutation receipt, or statement acceptance is claimed. The intake
dependency is provisionally self-tested, but it deliberately records that the repository's source
scope is insufficient to select an exact proposition.

The authoritative repository record supplies only the Chinese gloss "the general solution of the
one-dimensional wave equation", attribution to d'Alembert, and the year 1746. It supplies no
primary-source edition, theorem/page locator, exact wording, translation, surrounding definitions,
or errata review. In particular, it does not determine:

- whether the target is the traveling-wave representation `u(x,t) = F(x-c*t) + G(x+c*t)`, the
  Cauchy-data integral formula, or a theorem proving their equivalence;
- whether "general solution" requires construction, necessity, uniqueness, or both directions;
- the domains of `x` and `t`, and whether the result is global on `Real x Real`;
- the scalar field, regularity class, and classical, weak, or distributional solution notion;
- the normalization and sign of the wave equation, or the positivity and treatment of wave speed;
- the initial displacement and velocity hypotheses, integral orientation/base point, and boundary
  or decay assumptions; and
- the behavior at `c = 0`, negative speed, zero data, bounded or periodic domains, and endpoints.

These alternatives change the domains, ordered binders, hypotheses, conclusion, and degenerate
cases. Choosing the familiar traveling-wave formula merely from its name would silently weaken a
two-way general-solution theorem if that is intended; choosing the initial-value formula would be a
different theorem and introduces division by the wave speed. Either choice would invent missing
mathematics and violate the no-broadened-or-substituted-target rule.

Consequently there is no truthful expression on which to run the required removed-hypothesis,
changed-domain, binder-scope, and boundary-case mutations. No `Statement.lean`, theorem, proof,
axiom, bodyless declaration, `sorry`, placeholder, or abstract interface assuming the desired PDE
claim was introduced. The root vector remains `[H4, M4, R4]`; theorem completion remains false.

## Pinned environment and scoped search

- Validation date: 2026-07-12 (Asia/Shanghai).
- Lean toolchain: `leanprover/lean4:v4.29.0`; Lean 4.29.0, commit
  `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- Lake: `5.0.0-src+98dc76e`.
- Pinned mathlib revision: `8a178386ffc0f5fef0b77738bb5449d50efeea95`.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

All commands ran in this worker clone. Existing `.lake` artifacts were read only; no update,
build, clone, or fetch command was run.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-1127` | 0 | rank 332; planned; L0/rework-required; legacy artifacts unaccepted; theorem incomplete |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean version and commit recorded above |
| `cd Formalizations/Lean && lake --version` | 0 | Lake version recorded above |
| `cd Formalizations/Lean && sha256sum lean-toolchain lake-manifest.json` | 0 | hashes match the environment fingerprint above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | pinned mathlib revision recorded above |
| `rg -n -i "d.?alembert\|one[- ]dimensional wave\|wave equation\|traveling wave\|travelling wave" Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'` | 1 | no matching theorem-specific declaration in pinned mathlib |
| `rg -n -i "d.?alembert\|general solution of the one-dimensional wave equation\|one-dimensional wave equation" Docs Formalizations/Lean/AwesomeTheorems --glob '*.md' --glob '*.json' --glob '*.lean'` | 0 | only underspecified metadata and unrelated d'Alembertian keywords; no source-frozen proposition |

There is no applicable `lake env lean <target>.lean` check: an exact target does not exist.
Elaborating a remembered specialization or a predicate parameter that assumes the wave equation
would be fake statement evidence rather than the assigned deliverable.

## Retry condition

Provide an immutable primary-source edition (and translation if used) with an exact theorem/page
locator, surrounding definitions, and errata status. An accountable source review must then freeze
the formula family, quantifier direction, domains, equation convention, speed, regularity and
solution notions, initial/boundary data, and degenerate cases. A later statement run can encode that
exact proposition with minimal imports, serialize its elaborated expression, check any alternate
transport, and run structural mutations.

Section 5/5.1 source identity is the first failed gate. Because this assigned phase is blocked
rather than genuinely self-tested, no `.stage1-worker-selftest.json` is emitted.
