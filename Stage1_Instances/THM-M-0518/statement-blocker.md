# Statement-phase blocker

Item: `S56-M-0518-STATEMENT`  
Theorem: `THM-M-0518`  
Worker base revision: `e9252b1cfdc99a094324c8a10d260769df2eca15`

## Gate decision

The exact Lean 4 target cannot yet be elaborated without substituting abstract propositions for
the mathematics. The human statement is identified as Wiles 1995, Theorem 0.4: every semistable
elliptic curve over `Q` is modular. The pinned Lean environment does not, however, provide the two
global arithmetic boundaries needed to translate that sentence faithfully.

First, `WeierstrassCurve.HasGoodReduction R W` and `HasMultiplicativeReduction R W` concern one
chosen discrete valuation ring `R`. They do not quantify over all finite places of `Q`, choose and
transport compatible integral/minimal models, or establish model independence. Second, the
available `ModularForm` and `CuspForm` APIs are analytic function spaces. No pinned API found here
attaches a rational elliptic curve to a normalized weight-two newform at the curve's conductor by
equality of L-series, compatible Galois representations, or another source-equivalent relation.

The legacy `S1_M_064.lean` boundary confirms rather than fills this gap: its semistability,
L-function compatibility, conductor compatibility, and Galois compatibility fields are abstract
`Prop` values, and its own documentation disclaims a semistable modularity theorem. Reusing that
shape would make the intended arithmetic content trusted input and would violate the exact-target
gate. The later theorem that every rational elliptic curve is modular, a local reduction statement,
or a residual-representation modularity-lifting theorem would likewise be a substituted target.

Consequently there is no exact expression to serialize, no expression hash to record, and no sound
removed-hypothesis, changed-domain, changed-binder-scope, or boundary mutation suite. Section 5.1
of the rev-5.6 blueprint fails before proof evidence may be inspected. `IntakeProbe.lean` was
re-elaborated only as evidence that the pinned environment and nearby ingredients are available; it
is not the canonical target and earns no statement or proof credit.

## Exact validation record

Validation date: `2026-07-12` (`Asia/Shanghai`). The pre-existing canonical `.lake` artifacts were
used read-only. No dependency update, build, fetch, clone, or other `.lake` mutation was run.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups; 1546 uniform-L0 Lean 4 targets; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets; ranks 1..1546; all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0518` | 0 | rank 891; planned; legacy artifacts unaccepted; theorem_complete false |
| `rg -n -C 8 'THM-M-0518\|模性提升定理\|半稳定椭圆曲线的模性' Docs/researches/math_theorems.md Docs/Stage0_Blueprint.md Docs/Stage1_Blueprint_Applicable_Theorems.md` | 0 | located the exact repository record; Stage0 says precise definitions and prerequisites remain open |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | mathlib `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `git -C Formalizations/Lean/.lake/packages/flt-regular rev-parse HEAD` | 0 | flt-regular `56161b6eb5281fbfe9c38f2bcec0f429ebc11a27` |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0518/IntakeProbe.lean)` | 0 | nine pinned API checks and the local reduction disjunction elaborated; no global target asserted |
| `rg -n -i 'semistab\|modular elliptic\|elliptic.*modular\|modularity' Formalizations/Lean/.lake/packages/mathlib/Mathlib Formalizations/Lean/.lake/packages/flt-regular` | 0 | only unrelated modularity text and a bibliographic Wiles citation; no terminal theorem or global predicate |
| `rg -n '\\b(sorry\|admit)\\b\|^[[:space:]]*axiom\\b' Stage1_Instances/THM-M-0518 -g '*.lean'` | 1 | expected no-match exit; no prohibited placeholder or axiom in owned Lean source |
| `python3 -m json.tool Stage1_Instances/THM-M-0518/statement-blocker.json` | 0 | blocker record is valid JSON |

## Required unblocker and status boundary

The retry condition is to implement or immutably pin the missing all-finite-places semistability,
conductor/newform, and arithmetic attachment interfaces; audit their conventions against the
primary source; and only then elaborate and mutation-test the exact implication with minimal
imports.

This statement node remains `[ ]`, blocked at `M3`. The root remains `[H1, M3, R4]`, with
`audit_complete: false` and `theorem_complete: false`. No worker self-test manifest is emitted,
because the assigned statement deliverable did not pass its completion gate.
