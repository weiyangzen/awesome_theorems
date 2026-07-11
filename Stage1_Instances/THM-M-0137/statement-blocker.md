# Statement gate blocker

Item: `S56-M-0137-STATEMENT`  
Theorem: `THM-M-0137`  
Verdict: blocked; no exact canonical Lean target is claimed.

## First failed gate

The repository source record does not identify a mathematical proposition. It supplies only the
title "Kac-Peterson character formula", the gloss "characters of affine Lie algebras", the year
1984, and an untrusted `已验证` label. Those fields do not select between at least two materially
different roots recorded by the intake:

1. the Weyl-Kac alternating-sum character identity for an integrable highest-weight module; and
2. Kac-Peterson modular-transformation formulae for normalized affine characters and string
   functions.

They differ in objects, hypotheses, and conclusions. The source record gives no theorem number,
page, affine type, level condition, normalization, coefficient/completion semantics, or choice of
formal versus analytic equality. Selecting either root would therefore broaden or substitute the
metadata rather than elaborate its exact claim. Under rev-5.6 sections 2 and 5, statement ambiguity
and a missing exact expression fingerprint are hard blockers.

The legacy module `Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_053.lean` cannot repair that
failure. Its `StatementShape` concludes the proposition field
`CharacterEqualsKacPetersonFormula` only after that same field's intended mathematical content has
been left abstract in the input structure. It records useful interface boundaries, but it does not
encode either candidate formula and receives no statement credit. It nevertheless elaborates in
the pinned environment, confirming that the blocker is target identity and missing affine
character infrastructure rather than an unavailable Lean installation.

Consequently the required ordered binders, exact hypotheses, conclusion, normalized expression,
expression hash, checked transports, and meaningful hypothesis/domain mutations cannot truthfully
be produced. The machine state remains `M4`: no exact formal target has been identified. No `sorry`,
axiom, opaque proxy predicate, placeholder theorem, or alternate finite-dimensional character
formula was introduced.

## Environment fingerprint

- Repository base revision: `de9509a9b807a45e9fb1511465a7b957788afc54`.
- Validation date: 2026-07-12 (Asia/Shanghai).
- Lean toolchain: `leanprover/lean4:v4.29.0`; Lean `4.29.0`, commit
  `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- Checked mathlib revision: `8a178386ffc0f5fef0b77738bb5449d50efeea95`.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- Lake manifest SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.
- Legacy discovery module SHA-256:
  `0a16ee0be2a18b0bfb5baff0b686620895995404bb2a83c6da0e3cfdb9c7d184`.

## Validation evidence

Commands ran from this worker clone using only the existing canonical pinned `.lake` artifacts.
No update, build, fetch, or clone command was used.

| Command | Exit | Result |
|---|---:|---|
| `cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_053.lean` | 0 | Legacy interface/discovery module elaborated and printed its checked declarations; it contains no exact formula target |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | Checked mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `rg -n -i 'Kac[- ]?Peterson\|Weyl[- ]?Kac character\|affine (Lie\|Kac.Moody).*character' Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'` | 1 | No matching pinned mathlib source declaration |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0137` | 0 | Rank 53, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |

## Retry condition

Provide an immutable primary-source page and theorem label that selects one exact character
formula, including all referenced definitions and assumptions. If that source selects the modular
formula, pinned Lean definitions are also needed for normalized affine characters, string
functions, theta functions, level, and the modular action. If it selects the Weyl-Kac identity,
pinned definitions are needed for the affine Kac-Moody algebra, integrable highest-weight module,
affine Weyl action, roots and multiplicities, and the completed formal-character ring. The next
statement run can then freeze and elaborate the source-faithful target and mutation-test its
hypotheses and boundary cases.

Until that retry condition is met, statement acceptance and theorem completion are false. Because
the assigned phase is not self-tested to its completion gate, no `.stage1-worker-selftest.json` is
emitted.
