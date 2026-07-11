# THM-M-0388: Pell Equation Intake

## Status

This is a `planned` rev-5.6 instance at `L0 / rework_required`. It records no accepted proof state,
no theorem-completion claim, and no inherited credit from the legacy Stage1 Lean file. The intake
item is `S56-M-0388-INTAKE`; all later execution nodes remain open or dependency-blocked.

## Frozen Source Claim

The repository source at `Docs/researches/math_theorems.md` names **佩尔方程** and states exactly
`x²-Dy²=1的整数解` (integer solutions of `x² - D y² = 1`). The metadata calls the formalization
status `已验证`, but rev-5.6 treats that label as untrusted discovery metadata.

The wording does not specify the domain and side conditions on `D`, whether trivial solutions are
excluded, or whether the requested conclusion is existence, generation, or exhaustive
classification. Those are material differences, so intake deliberately does not manufacture a
canonical Lean proposition. The statement phase must settle them using a primary mathematical
source and checked transports.

## Scope Map

| Surface | Intake boundary |
|---|---|
| Objects | `x, y` are explicitly described as integers; the domain of `D` is unstated. |
| Relation | `x^2 - D*y^2 = 1`. |
| Quantification | Quantifiers and binder order are absent from the source sentence. |
| Parameter conditions | Positivity and nonsquareness of `D` are not stated. |
| Degenerate cases | `D <= 0`, square `D`, `y = 0`, and sign symmetry are not addressed. |
| Conclusion strength | “Solutions” may mean finding some solution or classifying all solutions. |
| Foundation | Lean 4 with the repository's pinned mathlib; exact imports belong to statement phase. |
| Trust/computation | No custom axioms, oracle, or computation is authorized by this intake. |

## Source-Statement Crosswalk

| Source node | Source text | Candidate formal component | Intake result |
|---|---|---|---|
| Name | `佩尔方程` | Pell equation family | Identified, not an exact proposition. |
| Equation | `x²-Dy²=1` | `x ^ 2 - D * y ^ 2 = 1` | Syntactic relation identified; domains remain incomplete. |
| Coordinates | `整数解` | `x y : ℤ` | Supported for solution coordinates. |
| Parameter | implicit `D` | candidate `D : ℤ` | Not source-certified at intake. |
| Side conditions | absent | candidate `0 < D ∧ ¬ IsSquare D` | Legacy/mathlib candidate only; not attributed to the source. |
| Result | `解` | existence or complete generator classification | Ambiguous and intentionally open. |
| Status label | `已验证` | machine-closure claim | Rejected as evidence; no receipt or kernel evidence accompanies it. |

The legacy file `Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_003.lean` combines nontrivial
existence with unique-positive-generator classification for positive nonsquare integer `D`. It is a
useful candidate for later statement and anchor audits, but its stronger interpretation is not
silently substituted for the terse source statement.

## Validation Record

Base revision: `a8d6489fd935cd71fa4499f2f3f5b051998203f4`.

On 2026-07-12 the intake ran the repository preflight commands successfully:

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets)
python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required
python3 scripts/stage1_target.py show THM-M-0388
  exit 0: rank 3, planned, L0, rework_required=true, theorem_complete=false
```

The node-specific structural validation and its exact output are recorded in
`intake-validation.txt`. This is intake evidence only, not Lean elaboration or theorem evidence.
