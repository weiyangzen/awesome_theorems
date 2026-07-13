# Exact-statement gate: blocked

Item: `S56-M-0763-STATEMENT`

Theorem: `THM-M-0763`

Base revision: `444860f481e8bbf64a3357008fd4d01a52006f08` (tree
`dee24a14497f877ebd81712a99d2da08de62d7ad`)

Attempt date: 2026-07-13 (`Asia/Shanghai`)

## Decision

The assigned statement node remains `[ ]`. The repository record gives only the title
`乔姆斯基层次`, the gloss `形式语言的分类`, the Noam Chomsky attribution, and the year 1956. It
contains no truth-valued proposition, bibliography, incorporated definitions, ordered binders,
hypotheses, conclusion, proof boundary, correction record, or reviewer. Stage0 repeats the gloss
while explicitly leaving its precise definitions and premises open. The integrated intake
therefore correctly freezes a theorem family at `[H5, M4, R4]`, not an exact statement.

At least five materially different roots remain compatible with the record:

1. Chomsky's 1956 three-class comparison of finite-state, derivable, and terminal languages;
2. definitions of the modern four grammar types and their generated-language classes;
3. the weak inclusion chain from regular through recursively enumerable languages;
4. strictness of the inclusions, including explicit separating languages;
5. equivalences with finite automata, pushdown automata, linear-bounded automata, and Turing
   machines.

The inspected 1956 Theorem (27) is not the familiar modern four-level theorem: it includes
incomparability between finite-state and derivable languages. The separate Stage0-only
`THM-C-0151` record makes a modern four-level reading plausible, but it is outside the rev-5.6
target set and has no accepted duplicate-identity or source-transfer decision. Selecting either
reading, one inclusion edge, or a conjunction assembled from neighboring targets would invent or
substitute proposition-changing mathematics.

The prerequisite intake is only provisional `[_]`. Its worker receipt says `accepted: false` and
contains no accepted receipt ID, so master acceptance also remains open. Independently of that
workflow boundary, the intake deliberately leaves the canonical mathematical statement and Lean
target null. Section 5 of the rev-5.6 standard makes statement ambiguity and a missing expression
fingerprint hard blockers.

Consequently there is no canonical expression to elaborate and no import set that can truthfully
be called minimal for the target. There is no expression or canonical-environment fingerprint and
no credited alternate encoding. Removed-hypothesis, changed-domain, changed-binder-scope, and
boundary-case mutations are undefined until a source owner selects the missing binders and
conclusion; they are not passed.

## Pinned Lean boundary

`IntakeProbe.lean` was re-elaborated from `Formalizations/Lean` using the existing pinned Lake
environment. Its imports expose `Language`, `Language.IsRegular`, context-free grammar and
language interfaces, and generic computability and recursively-enumerable predicates. All nine
checks passed; stdout has SHA-256
`723b5c8d93c6aa2bb100d72a4fc3ecffe24d863d24b408021a08177822a5417c`.

That probe declares no canonical target, checked transport, or proof body. In particular, the
available regular and context-free predicates do not select or prove the complete hierarchy. A
bounded exact-topic search over repo-local Lean and pinned mathlib found no explicitly named
Chomsky-hierarchy, context-sensitive-grammar, unrestricted-grammar, or type-0/type-1/type-2/type-3
classification declaration. The only match was the probe's own disclaimer. This is scoped
feasibility evidence, not the downstream anchor audit or a global absence proof. Probe imports are
therefore not claimed minimal for the absent target and receive no statement or proof credit.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided `.lake` symlink and pinned
artifacts were used read-only. No update, build, clone, fetch, or dependency mutation was run.

## Validation record

All commands ran inside this worker clone on 2026-07-13.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0763` | 0 | rank 1349; `planned`; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` (pre-edit) | 0 | only the automation-provided `Formalizations/Lean/.lake` symlink was untracked; base revision and tree appear above |
| source record, Stage0 projections, intake crosswalk, neighboring-target, git-blame, and blob inspection | 0 | confirmed that the catalog has only six sparse fields originating at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`; no exact proposition is present |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | Lean 4.29.0 at commit `98dc76e3...1740`; Lake `5.0.0-src+98dc76e` |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short`; `git -C ... rev-parse HEAD 'HEAD^{tree}'` | 0 | package status empty; pinned revision `8a178386...eea95` and tree `bdc39a...5e2b` |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0763/IntakeProbe.lean` | 0 | nine adjacent interfaces elaborated; no target or proof body declared; stdout hash shown above |
| bounded exact-topic `rg` over repo-local Lean and pinned mathlib | 0 | only the intake probe disclaimer matched; no exact-topic declaration was found in the searched roots |
| `python3 -B Stage1_Instances/THM-M-0763/check_intake.py` | 1 | the historical intake-only checker fingerprints the pre-integration DAG entry; integration changed intake from `[ ]` to `[_]`, so its stale assertion fails closed and is not statement evidence |
| prohibited-construct `rg` over owned Lean files | 1 (expected no match) | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| `python3 -m json.tool Stage1_Instances/THM-M-0763/statement-blocker.json` plus scoped invariant assertions | 0 | blocker identity, dependency state, null target fields, unchanged vector, four undefined mutations, false completion fields, exact two-file scope, and no-self-test policy agree |
| scoped `git diff --check` plus per-new-file no-index whitespace checks | 0 | no whitespace diagnostics; each no-index exit 1 was only the expected new-file difference |
| `test ! -e .stage1-worker-selftest.json` | 0 | root worker self-test manifest remained absent because the statement gate did not pass |

The historical intake checker is bound to intake-time authority and inventory. It was neither
edited nor represented as statement-phase evidence.

## Retry condition and status boundary

An accountable source owner must first preserve and hash one lawful immutable primary or approved
authoritative source, select and independently approve one exact truth-valued proposition, map
every incorporated definition, ordered binder, hypothesis, conclusion, proof boundary,
translation, correction, and erratum, decide between the 1956 and modern readings, and reconcile
`THM-C-0151` plus the neighboring theorem boundaries. The decision must freeze alphabet, word,
grammar, generated-language, production-restriction, effectiveness, machine, inclusion,
strictness, witness, and degenerate-case contracts.

A later statement run can then encode exactly that claim, minimize its pinned imports, serialize
and hash its elaborated expression and environment, compile every credited transport, and run all
four required mutation classes. Master acceptance of the intake dependency remains required before
an accepted statement transition.

This blocker is the assigned phase's truthful result, not completion of the statement node or a
receipt. Lifecycle remains `planned`; the root remains `[H5, M4, R4]`; `audit_complete: false` and
`theorem_complete: false`. No `.stage1-worker-selftest.json`, worker `[_]`, statement fingerprint,
proof credit, accepted state, audit completion, theorem completion, or master acceptance is
claimed.
