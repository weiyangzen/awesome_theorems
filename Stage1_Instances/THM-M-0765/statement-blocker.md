# Exact-statement gate: blocked

Item: `S56-M-0765-STATEMENT`

Theorem: `THM-M-0765`

Base revision: `2226f559136f12fde46b1bf73cdf629043b8a648` (tree
`33cb254ed06b1391379b8e7f88c5e23188957b62`)

Attempt date: 2026-07-13 (`Asia/Shanghai`)

## Decision

The assigned statement node remains `[ ]`. The repository source record gives only the title
`图灵机可识别语言`, the gloss `递归可枚举语言`, an Alan Turing attribution, and the year 1936.
It supplies no truth-valued proposition, bibliography, source passage, definition chain, ordered
binders, hypotheses, conclusion, or proof boundary. Stage0 repeats the gloss while explicitly
leaving the precise definitions and premises open. The integrated intake therefore correctly
freezes a concept family at `[H5, M4, R4]`, not a theorem statement.

At least four materially different roots remain compatible with the record:

1. a definition of Turing recognition;
2. an equivalence between Turing recognition and recursive enumerability;
3. a characterization by the domain of a partial computable function or semidecision procedure;
4. a characterization by the range of a total or partial enumerator.

Those readings require choices that are not mere notation: alphabet and finite-word encoding;
language representation; deterministic or nondeterministic machine model; program validity;
initial configuration; acceptance, rejection, halting, and divergence semantics; the meaning of
recursive enumerability; and the direction of every implication. Enumerator variants also differ
on duplicates, malformed outputs, partiality, and the empty-language case. Selecting a familiar
equivalence, or defining the two sides to coincide, would invent or substitute proposition-changing
mathematics.

The prerequisite intake is only provisional `[_]`. Its worker receipt has `accepted: false` and
contains no accepted receipt ID; master acceptance therefore also remains open. Even apart from
that workflow boundary, the intake's null canonical statement and explicit source-identity blocker
make section 5.1 of the rev-5.6 standard impossible to satisfy truthfully.

Consequently there is no canonical expression to elaborate, no import set that can honestly be
called minimal for the target, and no expression or environment fingerprint. There is likewise no
credited alternate encoding for a checked transport. The required removed-hypothesis,
changed-domain, changed-binder-scope, and boundary-case mutations are not runnable without first
inventing the missing binders and conclusion. These mutation results are undefined, not passed.

## Pinned Lean boundary

The existing `IntakeProbe.lean` was re-elaborated from `Formalizations/Lean` with the existing
pinned Lake environment. Its sole direct import is
`Mathlib.Computability.TuringMachine.ToPartrec`, and all ten checks of adjacent `REPred`, partial
recursive code, and partial-recursive-to-`TM2` simulation interfaces passed. Probe stdout has
SHA-256 `4173c3e8a8b372ef140edd9c38c64cfbbfb47b2e09d24e7bcfdc0bb6b0b5a90b`.

This probe declares no canonical target, checked transport, or proof body. In particular,
`REPred` selects one predicate-level definition, while `Turing.PartrecToTM2.tr_eval` checks one
computation simulation. Neither identifies the catalog's alphabet, language encoding, recognition
semantics, root direction, or source claim. The probe import is therefore not claimed to be a
minimal import for an absent target and receives no statement or proof credit.

A bounded case-insensitive search of repo-local Lean and pinned mathlib found no declaration named
for a Turing-recognizable-language or recursively-enumerable-language equivalence. This is scoped
feasibility evidence only, not the downstream anchor audit and not a proof of global absence.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided `.lake` symlink and canonical
artifacts were used read-only. No update, build, clone, fetch, or dependency mutation was run.

## Validation record

All commands ran inside this worker clone on 2026-07-13.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0765` | 0 | rank 1351; `planned`; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` (pre-edit) | 0 | only the automation-provided `Formalizations/Lean/.lake` symlink was untracked; base revision and tree appear above |
| source record, Stage0 projection, neighboring-topic, and source-history inspection | 0 | confirmed that the catalog provides only six sparse fields from commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`; no proposition or source locator is present |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | Lean 4.29.0 at commit `98dc76e3...1740`; Lake `5.0.0-src+98dc76e` |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short`; `git -C ... rev-parse HEAD 'HEAD^{tree}'` | 0 | package status empty; pinned revision `8a178386...eea95` and tree `bdc39a...5e2b` |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0765/IntakeProbe.lean` | 0 | ten adjacent pinned interfaces elaborated; no target or proof body declared; stdout hash shown above |
| bounded exact-topic `rg` over repo-local Lean and pinned mathlib | 1 (expected no match) | no explicitly named Turing-recognizable/recursively-enumerable language equivalence was found |
| `python3 -B Stage1_Instances/THM-M-0765/check_intake.py` | 1 | the historical intake-only checker expects intake state `[ ]`; integration now records `[_]`, so its stale state assertion fails closed and is not statement evidence |
| `rg -n --glob '*.lean' '\b(sorry\|admit)\b\|\bsorryAx\b\|^[[:space:]]*(axiom\|constant\|opaque\|unsafe)[[:space:]]' Stage1_Instances/THM-M-0765` | 1 (expected no match) | no prohibited proof escape or bodyless declaration |
| `python3 -m json.tool Stage1_Instances/THM-M-0765/statement-blocker.json` plus scoped JSON invariant assertions | 0 | blocker identity, null target fields, four unrunnable mutations, unchanged vector, false completion fields, and no-self-test policy agree |
| `git diff --check -- Stage1_Instances/THM-M-0765`; per-new-file `git diff --no-index --check /dev/null <file>` | 0 | no whitespace diagnostics; each no-index exit 1 is only the expected new-file difference |
| `test ! -e .stage1-worker-selftest.json` | 0 | root worker self-test manifest was absent at final validation because the assigned statement gate did not pass |

The stale intake checker is bound to intake-time authoritative state and inventory. It was neither
edited nor represented as statement-phase evidence.

## Retry condition and status boundary

An accountable source owner must lawfully preserve and hash one immutable primary or approved
authoritative source, select one exact proposition, transcribe all incorporated definitions,
ordered binders, hypotheses, conclusion, proof boundary, translation, and correction status, and
obtain independent approval of the mapping to `THM-M-0765`. That decision must also fix the word,
language, machine, program, execution, acceptance, recursive-enumerability, implication-direction,
and degenerate-case contracts listed above.

A later statement run can then encode that same claim, minimize its pinned imports, serialize and
hash its elaborated expression and environment, compile every credited transport, and run all four
required mutation classes. Master acceptance of the intake dependency remains required before an
accepted statement transition.

This blocker is the assigned phase's truthful result, not completion of the statement node or a
receipt. Lifecycle remains `planned`; the root remains `[H5, M4, R4]`; `audit_complete: false` and
`theorem_complete: false`. No `.stage1-worker-selftest.json`, worker `[_]`, statement fingerprint,
proof credit, accepted state, audit completion, theorem completion, or master acceptance is
claimed.
