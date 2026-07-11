# Statement gate blocker

Item: `S56-M-0443-STATEMENT`  
Theorem: `THM-M-0443`  
Verdict: blocked; no exact canonical Lean target is claimed.

## First failed gate

The repository source record does not identify a unique mathematical proposition. It gives only
the title "Mazur-Tate theorem", the gloss "the p-adic L-function of an elliptic curve", the year
1973, and an untrusted `已验证` label. Those fields do not select among materially different claims,
including:

1. existence and interpolation of an elliptic-curve p-adic L-function;
2. the Mazur-Tate-Teitelbaum exceptional-zero leading-term formula; and
3. statements about Mazur-Tate elements or refined Birch-Swinnerton-Dyer conjectures.

These alternatives have different objects, reduction hypotheses, character families,
normalizations, and conclusions. The source record supplies no bibliographic reference, theorem
number, page, prime or reduction condition, period convention, Euler factor, conductor convention,
or interpolation/leading-term formula. The intake crosswalk identifies candidate publications but
explicitly records that their exact statements and proof status have not been inspected. Choosing
one candidate would therefore invent or substitute mathematics rather than elaborate the exact
manifest target. Under rev-5.6 sections 2 and 5, unknown statement identity and the absence of an
exact expression fingerprint fail closed.

The legacy discovery module
`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_089.lean` does not resolve this ambiguity. Its
`MazurTateStatementData.interpolationFormula` is an unconstrained `Prop`, and its `StatementShape`
quantifies over arbitrary such records before returning that field from two other abstract
proposition fields. It is an interface sketch, not an encoding of any candidate source formula.
Its own comments label the reduction condition, normalization, p-adic L-function, critical values,
and interpolation formula as placeholders. Crediting that shape would broaden the target into an
opaque proxy predicate, which the assigned gate forbids.

Consequently the ordered binders, exact hypotheses, conclusion, normalized elaborated expression,
expression hash, checked transports, and meaningful mutation tests cannot truthfully be produced.
The machine state remains `M4`: no exact formal target has been identified. No `sorry`, axiom,
placeholder declaration, or substituted theorem was added.

## Environment fingerprint

- Repository base revision: `a8aa34a03ae0ed5279f951be889c5fec4af35ef6`.
- Validation date: 2026-07-12 (Asia/Shanghai).
- Lean toolchain file: `leanprover/lean4:v4.29.0`; Lean `4.29.0`, commit
  `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- Checked mathlib revision: `8a178386ffc0f5fef0b77738bb5449d50efeea95`.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- Lake manifest SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.
- Legacy discovery module SHA-256:
  `b84f7b5f8920f58cf57e0428139fa74e54bd8eb1fdaac776203e53233ee8c831`.
- The clone's `Formalizations/Lean/.lake` is a pre-existing symlink to the canonical pinned Lake
  artifacts. No dependency mutation command was run.

## Validation evidence

Commands ran inside this worker clone. Lean used only the existing pinned Lake environment; no
update, build, clone, or fetch command was used.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0443` | 0 | rank 89, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |
| `cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_089.lean` | 0 | legacy interface module elaborated with no output; this checks only the interface sketch, not an exact Mazur-Tate target |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `rg -n -i 'Mazur[- ]?Tate\|Mazur[- ]?Tate[- ]?Teitelbaum\|p-adic L-function\|padic L-function' Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'` | 1 | no matching declaration or source text in pinned mathlib; this is discovery evidence only, not the later anchor audit |
| `rg -n '\\bsorry\\b\|\\badmit\\b\|sorryAx\|\\baxiom\\b' Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_089.lean` | 1 | no textual proof placeholder in the legacy module; its abstract proposition fields still make it ineligible as the exact target |
| `git diff --check -- Stage1_Instances/THM-M-0443` | 0 | no whitespace errors |

## Retry condition

Provide an immutable primary-source edition/page and theorem or proposition label selecting one
exact proved claim, together with all referenced definitions and assumptions. For an interpolation
claim this must fix the curve domain, prime and reduction hypotheses, character family, periods,
Euler factors, conductors, coefficient fields and embeddings, and the equality being asserted. For
an exceptional-zero claim it must additionally fix the Tate period, p-adic logarithm, L-invariant,
derivative order, and normalization. For a Mazur-Tate-element claim it must instead fix the group
rings, augmentation filtration, specialization maps, and modular-symbol coefficients.

Once that source identity is fixed, a later statement run can encode and elaborate the complete
claim with minimal pinned imports, fingerprint the explicit expression, and mutation-test its
hypotheses and boundary cases. Until then, statement acceptance and theorem completion are false.
Because the assigned phase is not self-tested to its completion gate, no
`.stage1-worker-selftest.json` is emitted.
