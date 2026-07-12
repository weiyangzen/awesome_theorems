# Statement-phase blocker

Item: `S56-M-1256-STATEMENT`  
Base revision: `c00bc6793b3d4c186b81b80bbaf165b32e125b58`

## Verdict

`blocked`: the repository does not identify an exact mathematical proposition from which an exact
Lean 4 target can truthfully be elaborated. No `Statement.lean` was created, because selecting one
of the inequivalent formulations below would broaden or substitute the source claim.

The only repository source wording is "solvability of constant-coefficient PDE", attributed to
Lars Hormander in 1955. It does not fix:

- the scalar field, dimension, polynomial symbol, or treatment of the zero operator;
- local versus global solvability or the domain quantifiers;
- the datum and solution spaces (smooth functions, distributions, or another class);
- support or growth conditions;
- whether the conclusion is direct solvability `P(D) u = f` or existence of a distributional
  fundamental solution.

These choices produce different propositions. The adjacent `THM-M-1255` inventory entry separately
names the Malgrange-Ehrenpreis fundamental-solution theorem, so silently using that theorem is not
a justified disambiguation. The existing intake crosswalk also explicitly forbids that
substitution without primary-source evidence and checked implications.

## Validation evidence

Commands were run from the repository root on 2026-07-12.

| Command | Exit | Exact result summary |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-1256` | 0 | rank 434; `L0`; `rework_required: true`; lifecycle `planned`; `theorem_complete: false` |
| `sed -n '9178,9200p' Docs/researches/math_theorems.md` | 0 | located only the title, attribution/date, and the wording `constant-coefficient PDE solvability`; no definitions, quantifiers, or citation |
| `sed -n '34170,34235p' Docs/Stage0_Blueprint.md` | 0 | all exact definitions, assumptions, equivalent formulations, axioms, and machine artifacts remain `to be supplemented` |
| `rg -n 'Hormander\|Hörmander\|1256' ...` over repository sources | 0 | found this inventory material and unrelated subelliptic/Fourier-integral-operator targets; found no exact source statement for `THM-M-1256` |

`lake env lean` was deliberately not run: there is no canonical expression to put before the Lean
elaborator. Elaborating an invented surrogate would not validate this statement node.

## First failed gate and retry condition

The first failed gate is exact source-statement identification (rev-5.6 target-freeze gate). To
retry, provide or locate a primary source with edition/article, theorem number and pages, exact
quantifiers and function/distribution spaces, assumptions, and errata status. The next statement
run must crosswalk that text to a canonical Lean expression, settle the boundary cases above, and
then run `lake env lean` with the minimal pinned imports.

No statement receipt or worker self-test manifest is emitted. Root status remains `[H4, M4, R4]`;
neither audit completion nor theorem completion is claimed.
