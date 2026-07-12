# Statement-phase blocker

Item: `S56-M-0365-STATEMENT`  
Theorem: `THM-M-0365`  
Worker base revision: `b8a117cd19ae3b30b59087d7bc9c8071ee7212ab`

## Gate decision

The exact Lean 4 target cannot be elaborated truthfully from the repository source record. The
record gives only the family name `Tb theorem` and the gloss `singular integrals under
nondegeneracy conditions`. Stage0 leaves the precise definitions and assumptions, proof path,
equivalent formulations, axiom profile, and machine artifact unfilled. The intake therefore
correctly has a null canonical statement and a gate state of
`blocked_pending_variant_and_primary_source_statement_selection`.

Several inequivalent results remain compatible with this metadata: global versus local Tb,
doubling versus non-homogeneous settings, one accretive function versus a dual pair, and
accretive versus para-accretive testing data. The record also omits the ambient measure space,
kernel and truncation conventions, weak boundedness and testing hypotheses, adjoint convention,
and exact boundedness conclusion. Selecting any one formulation would broaden or substitute the
source claim. There is consequently no canonical expression to fingerprint and no sound removed-
hypothesis, changed-domain, changed-scope, or boundary-case mutation suite. The rev-5.6 section
5.1 statement gate fails before proof evidence may be inspected.

A narrow search found none of the terms `Tb theorem`, `para-accretive`, `Calderon-Zygmund`, or
`weak boundedness property` in the pinned mathlib Lean sources. That observation is only a
statement-surface check, not the assigned later anchor audit. No Lean source was invented: an
elaborating proposition chosen without a source decision would not validate this theorem.

## Exact validation record

Validation date: `2026-07-12` (`Asia/Shanghai`). The canonical pinned `.lake` artifacts were read
only. No dependency update, build, fetch, or clone was run. The untracked `.lake` path pre-existed
this work and was not modified.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups; 1546 uniform-L0 Lean 4 targets; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets; ranks 1..1546; all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0365` | 0 | rank 857; planned; legacy artifacts unaccepted; theorem_complete false |
| `rg -n -C 10 'THM-M-0365|Tb定理|非退化条件下的奇异积分' Docs/researches/math_theorems.md Docs/Stage0_Blueprint.md Docs/Stage1_Targets_rev-5.6.json` | 0 | only the family name/gloss and explicitly open Stage0 fields identify the claim |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `(cd Formalizations/Lean && lake --version)` | 0 | Lake `5.0.0-src+98dc76e` |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | hashes `651c8acc...b1d2` and `321626c8...5b2d` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | mathlib `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `rg -n -i '\\bTb theorem\\b|para.?accretive|Calder[oó]n.?Zygmund|weak boundedness propert' Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'` | 1 | expected no-match exit; no candidate declaration was found by this narrow term search |

## Required unblocker and status boundary

The first unblocker is an immutable, independently inspected primary-source passage selecting one
exact Tb result, including its definitions, ordered binders, hypotheses, conclusion, quantitative
constants, boundary cases, and errata disposition. Only then can the minimal imports and fixed Lean
context be selected, the elaborated kernel expression serialized, alternate forms transported, and
the four mandatory mutation classes checked.

This statement node remains `[ ]` and blocked at `M4`. The root remains `[H1, M4, R4]` with
`audit_complete: false` and `theorem_complete: false`. No worker self-test manifest is emitted,
because the assigned statement deliverable did not pass its gate. Master acceptance of the
provisional intake dependency also remains outstanding.
