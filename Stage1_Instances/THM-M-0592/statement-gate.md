# Lean 4 statement-gate blocker

Item: `S56-M-0592-STATEMENT`

Theorem: `THM-M-0592`  
Base revision: `a267c059de295b8ec0d71862d466236ec75a5951`

## Gate result

The rev-5.6 Lean statement gate is **blocked**. No Lean declaration or expression was created, and
no statement-elaboration success is claimed.

The repository's entire mathematical wording for this target is the title "Connes cyclic
cohomology" and the gloss "cohomology of noncommutative geometry". These name a theory, not a
proposition. In particular, they determine none of the following statement data required by
section 5 of the blueprint:

- the coefficient ring or field and the associative algebra hypotheses;
- algebraic versus continuous cyclic cochains and unital versus nonunital conventions;
- an ordered binder list, hypotheses, or a conclusion;
- whether the root is the complex construction, an SBI exact sequence, Morita invariance, or a
  K-theory pairing;
- grading, normalization, signs, universes, and boundary cases.

Consequently there is no exact `Prop` against which to select minimal imports, serialize an
elaborated expression, or run the required removed-hypothesis, changed-domain, binder-scope, and
boundary mutations. Choosing any one of the candidate results would broaden or substitute the
repository target. Importing a general module and elaborating a convenient fact would therefore be
false statement evidence.

There is also a dependency-order blocker: the authoritative checklist currently renders
`S56-M-0592-INTAKE` as `[_]`, which means worker evidence exists but master acceptance is pending;
the statement node depends on that intake node.

## Required unblock

The master must first accept a target-correction decision selecting exactly one proposition from an
immutable primary-source edition. That decision must freeze the proposition label and pages,
incorporated definitions, every binder and assumption, the conclusion, exclusions, and errata.
Only then can a statement worker encode the canonical Lean expression, minimize pinned imports,
fingerprint the elaborated expression and environment, and execute the four required mutation
classes.

The root remains `[H5, M4, R4]`; this blocker does not advance any debt axis, lifecycle, checklist
state, audit decision, or theorem-completion decision.

## Validation evidence

Run on 2026-07-12 in the worker automation clone. The pre-existing untracked
`Formalizations/Lean/.lake` canonical cache link was not modified.

| Command | Exact result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0: `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | exit 0: `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0592` | exit 0: rank 632; lifecycle `planned`; baseline `L0`; `rework_required: true`; `theorem_complete: false` |
| `cd Formalizations/Lean && lake env lean --version` | exit 0: `Lean (version 4.29.0, x86_64-unknown-linux-gnu, commit 98dc76e3c0a9b856c9b98726b713fb04fab16740, Release)` |
| `rg -n -C 8 'Connes循环上同调|康内斯循环上同调' Docs/researches/math_theorems.md Docs/Stage0_Blueprint.md` | exit 0; both duplicate records contain only the same theory label/gloss and leave precise definitions and hypotheses open |
| `git diff --check -- Stage1_Instances/THM-M-0592` | exit 0; no output |

There is deliberately no `lake env lean <target-file>` result: without a canonical proposition,
such a file would necessarily be a placeholder, an invented target, or a substituted theorem.
