# Statement-phase blocker

Item: `S56-M-0386-STATEMENT`  
Theorem: `THM-M-0386`  
Attempt date: `2026-07-12` (`Asia/Shanghai`)  
Worker base revision: `562c428c3d520ab42bba305174b7cad9409d7c0b`

## Verdict

`blocked`: the repository does not contain an exact mathematical statement that can be translated
without invention. The only source wording is `多项式在格点上的取值` ("values of a polynomial on
grid points"), together with the theorem name, authors, and year. As already frozen by the accepted
intake, this identifies a theorem family rather than a unique proposition.

The materially different candidates include the 2012 structural theorem for algebraic surfaces
with many Cartesian-product points and later quantitative incidence bounds. They differ in base
field, polynomial/surface hypotheses, finite-set cardinality regime, exceptional loci, constants
and exponents, and the precise group-like alternative. Choosing any of these from the gloss would
broaden or substitute the requested theorem.

Consequently no canonical Lean declaration or expression, normalized elaboration hash, checked
alternate transport, or required mutation suite can truthfully be produced. `IntakeProbe.lean`
continues to establish only the availability of possible encoding APIs. It is not a theorem
statement. The root remains `[H3, M4, R4]`; no proof, audit completion, or theorem completion is
claimed.

## First failed gate and retry condition

The first failed gate is Stage1 rev-5.6 section 5 / 5.1: freeze an exact canonical claim and map it
to a metavariable-free, pinned Lean expression. The hard-stop condition in the execution skill also
applies: the source statement cannot be identified without inventing missing mathematics.

Retry only after an immutable primary-source edition and exact theorem locator have been supplied
and independently reviewed. The review must freeze the ordered quantifiers, domains, every
hypothesis, conclusion, definitions, exceptional and degenerate cases, and any errata. A later
refinement may be selected only with an explicit source decision and a checked crosswalk, not by
silently treating it as the 2012 theorem.

## Validation evidence

The pre-existing canonical `.lake` link/artifacts were used read-only. No dependency update, build,
clone, or fetch was run.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0386` | exit 0; rank 873, planned, legacy artifacts unaccepted, theorem_complete false |
| `git status --short` | exit 0; only pre-existing untracked `Formalizations/Lean/.lake` was reported before this artifact was added |
| `git rev-parse HEAD` | exit 0; `562c428c3d520ab42bba305174b7cad9409d7c0b` |
| `rg -n -C 12 'THM-M-0386\|Elekes-Szab[oó]\|多项式在格点' Docs/researches Docs/Stage0_Blueprint.md Formalizations -g '*.md' -g '*.lean' -g '*.json'` | exit 0; found only the ambiguous repository gloss and Stage0 metadata; no exact statement or theorem-specific formal artifact |
| `(cd Formalizations/Lean && lake env lean --version)` | exit 0; Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | exit 0; mathlib `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0386/IntakeProbe.lean)` | exit 0; six polynomial/evaluation/finite-product API checks elaborated; this does not satisfy the statement gate |
| `rg -n '\b(Elekes\|Szab[oó])\b' Formalizations/Lean/.lake/packages/mathlib/Mathlib Formalizations/Lean -g '*.lean'` | exit 1; no matching Lean declaration (bounded local search only, not the later anchor audit) |
| `rg -n '\b(sorry\|admit)\b\|^[[:space:]]*axiom\b' Stage1_Instances/THM-M-0386 -g '*.lean'` | exit 1, expected no-match result; no prohibited placeholder or axiom found |

This phase is not self-tested as complete. Per the worker contract, no
`.stage1-worker-selftest.json` is emitted.
