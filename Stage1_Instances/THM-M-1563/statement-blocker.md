# Statement-phase blocker

Item: `S56-M-1563-STATEMENT`

Base revision: `aa6d10d262275c028256db77ef82b5418d76bc27`.

Validation date: 2026-07-12 (Asia/Shanghai).

## Verdict

The exact-statement gate is blocked. The repository identifies only the topic `KPZ方程` and the
gloss `随机表面生长`; neither is a proposition. The accepted intake dependency has not selected an
immutable primary-source theorem, theorem/page locator, or a conclusion. Its own crosswalk leaves
the theorem conclusion, assumptions, and ordered binders open.

Writing a Lean declaration now would require choosing among inequivalent claims such as definition
of the stochastic model, existence or uniqueness for a particular solution concept, a Cole-Hopf
construction, or approximation and renormalization convergence. It would also require inventing the
dimension, domain, coefficients, noise law, initial data, exceptional-set quantifiers, and boundary
conditions. That would broaden or substitute the target, so no `.lean` target or expression hash is
produced.

Consequently the required statement-gate evidence is absent:

- no canonical human proposition with ordered binders, hypotheses, and conclusion;
- no minimal Lean import can be determined from a nonexistent formal expression;
- no elaborated kernel expression or expression fingerprint;
- no checked alternate encoding or mutation tests;
- no frozen foundation, TCB, or computation profile specific to an exact claim.

The target remains `M4`. This artifact claims neither statement completion nor theorem completion.
No worker self-test manifest is emitted because the assigned phase is not self-tested.

## Smallest real validation

The canonical pinned `.lake` artifacts were read only. No update, build, clone, fetch, or dependency
mutation was performed. The pre-existing untracked `Formalizations/Lean/.lake` link makes these
nonrelease checks.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1563` | 0 | rank 574; lifecycle `planned`; theorem incomplete |
| `rg -n -i 'KPZ\|Kardar\|Parisi.?Zhang\|随机表面生长' --glob '!Formalizations/Lean/.lake/**' --glob '!Stage1_Instances/THM-M-1563/**' .` | 0 | repository sources contain only catalogue metadata and neighboring-target discussion; no exact proposition or local Lean declaration |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git status --short` | 0 | before this artifact, only the pre-existing untracked `Formalizations/Lean/.lake` entry was reported |
| `git rev-parse HEAD` | 0 | `aa6d10d262275c028256db77ef82b5418d76bc27` |

Running `lake env lean` on a fabricated proposition would demonstrate only that the fabrication
elaborates, not that the repository's exact target elaborates. The narrowest truthful Lean check is
therefore the toolchain fingerprint above; canonical elaboration is the failed gate, not a skipped
successful check.

## Retry condition

An accountable intake/source review must select one exact mathematical theorem from an immutable
primary source, provide its theorem/page locator and errata disposition, and approve a row-by-row
mapping of every quantifier, hypothesis, normalization, degenerate case, and conclusion. Once that
identity is accepted, the statement phase can encode it with minimal pinned imports, elaborate it,
preserve its kernel-expression fingerprint, and run the required alternate-form and mutation
checks.
