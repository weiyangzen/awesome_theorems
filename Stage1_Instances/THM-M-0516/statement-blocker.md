# Statement-phase blocker

## Verdict

`S56-M-0516-STATEMENT` is blocked at the exact-source gate. The repository gives the title
"Iwasawa theory" and only the gloss "p-adic L-functions of cyclotomic fields". This does not
determine a proposition, so it cannot determine an exact Lean expression. No canonical target,
checked transport, expression hash, or statement-phase receipt is claimed.

This is not merely a missing Lean definition. At least the following mutually non-equivalent
readings remain compatible with the supplied metadata:

1. existence of a Kubota-Leopoldt p-adic L-function;
2. a particular interpolation formula, with source-dependent Euler factors and normalizations;
3. uniqueness or a measure/power-series formulation of that construction;
4. a structural or growth theorem for an Iwasawa module in a cyclotomic tower.

The adjacent target `THM-M-0517` separately names the Iwasawa main conjecture. Substituting that
claim, a complex Dirichlet L-series theorem, a theorem only about cyclotomic fields, or a convenient
special case would broaden or replace this target and is therefore prohibited.

## First failed gate and retry condition

The first failed gate is statement identity: no immutable primary-source edition and exact theorem
passage has been selected. The retry must provide an authoritative edition, theorem/page or unique
passage, exact assumptions and conclusion, and decisions for the prime, character and conductor,
coefficient field, embeddings, normalization, interpolation range, Euler factors, exceptional
zeros, and finite-layer versus tower conventions. Only then can ordered Lean binders, boundary
cases, an elaborated expression, checked transports, and mutation tests be frozen.

## Validation evidence

Validation was run from repository base
`e9252b1cfdc99a094324c8a10d260769df2eca15` on 2026-07-12. The existing untracked
`Formalizations/Lean/.lake` is the canonical pinned artifact reused by the worker; it was not
modified or fetched.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`; 15 assurance groups and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | 0 | `ok`; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0516` | 0 | rank 890, lifecycle `planned`, theorem completion false |
| `rg -n -C 8 '岩泽理论\|Iwasawa\|分圆域的p-adic' Docs/researches/math_theorems.md Docs/Stage0_Blueprint.md` | 0 | the only positive target wording is the topic gloss; Stage0 leaves exact definitions and prerequisites open |
| `rg -n -i 'p-adic l\|padic.*lfunction\|lfunction.*padic\|kubota\|leopoldt\|iwasawa' Formalizations/Lean/.lake/packages/mathlib/Mathlib -g '*.lean'` | 0 | the only implemented Iwasawa-named module found is the unrelated group-action simplicity criterion; no result resolves source identity |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0516/IntakeProbe.lean)` | 0 | pinned APIs for cyclotomic fields, p-adics, Dirichlet characters, and complex L-series elaborate; these are ingredients, not the missing target |
| `git diff --check -- Stage1_Instances/THM-M-0516` | 0 | no whitespace errors before this evidence file was added |

The Lean command is a narrowly scoped environment/API check, not canonical-statement validation.
Because the exact proposition is unavailable, there is no truthful statement self-test to run and
no `.stage1-worker-selftest.json` is emitted. Root status remains `[H3, M4, R4]`; audit and theorem
completion remain false.
