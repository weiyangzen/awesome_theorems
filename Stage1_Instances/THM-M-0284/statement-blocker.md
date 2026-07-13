# THM-M-0284 exact-statement gate: blocked

Item: `S56-M-0284-STATEMENT`

Base revision: `a75b2f3ac5b8b7d34eb73435734edfeecc41bd40` (tree
`66a22e1dc2e1c14c27bd01396a99826ab2536bf1`).

## Decision

The statement item remains `[ ]`. The catalog says only that tail events have a zero-one property.
It does not select independent random variables or sub-sigma-algebras; an index type, order, and tail
direction; ordinary probability, finite measure, kernel, or conditional assumptions; an exact tail
sigma-algebra encoding; event measurability; a conclusion encoding; or boundary cases. These are
proposition-changing choices, not notation that a Lean file may silently fill in.

The intake identifies Kolmogorov's 1933 *Grundbegriffe der Wahrscheinlichkeitsrechnung* and its
later English translation only as a source family. No lawful immutable edition, theorem or page,
exact passage, incorporated definition chain, translation and errata audit, or independent review
has been admitted. Accordingly, `instance.json` deliberately leaves the canonical human statement,
Lean expression, expression hash, and canonical-target environment fingerprint null. Selecting a
familiar modern formulation now would invent missing mathematics.

The first failed gate is exact source-statement identity and variant selection. Without a canonical
expression there is no target-specific minimal-import result, checked alternate transport, or
meaningful removed-hypothesis, changed-domain, changed-binder-scope, or boundary-case mutation. The
provisional intake classification remains `[H1, M3, R4]`; lifecycle remains `planned`;
`audit_complete` and `theorem_complete` remain false.

The predecessor intake appears as provisional `[_]` in the authoritative execution DAG. Its worker
receipt has `accepted=false` and is neither content-addressed nor master-accepted. That dependency
state independently prevents an accepted statement transition, although it does not prevent this
fail-closed preparation.

## Pinned Lean boundary

Pinned mathlib contains a strong exact-topic candidate in the ordinary probability-measure form:

```lean
import Mathlib.Probability.Independence.ZeroOne

#check ProbabilityTheory.measure_zero_or_one_of_measurableSet_limsup_atTop
```

It takes an ordinary measure satisfying `iIndep s μ` (hence a probability measure) and states the
`atTop` law for an independent family of sub-sigma-algebras indexed by a nonempty no-max
semilattice-sup type: a set measurable in `Filter.limsup s Filter.atTop` has measure zero or one.
The same module also exposes an `atBot` variant and kernel and conditional variants. The source
record selects none of these, nor does it select the common random-variable formulation and its
generated-sigma-algebra transport.

The existing `IntakeProbe.lean` re-elaborates all eight recorded interfaces through its sole direct
import, `Mathlib.Probability.Independence.ZeroOne`. This authenticates the pinned candidate surface,
not the target statement. That import cannot be certified minimal for an absent canonical target.
The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided `.lake` symlink and pinned
artifacts were used read-only. No update, build, clone, fetch, or dependency mutation was run.

## Validation record

Commands ran on 2026-07-13 in `Asia/Shanghai`; commands without a stated working directory ran at
the worker-clone root.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0284` | 0 | rank 1290; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git rev-parse HEAD 'HEAD^{tree}'` and pre-edit `git status --short --untracked-files=all` | 0 | base identity shown above; only the automation-provided `Formalizations/Lean/.lake` symlink was untracked |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | Lean 4.29.0 at `98dc76e3...`; Lake `5.0.0-src+98dc76e` |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` and `rev-parse HEAD 'HEAD^{tree}'` | 0 | clean package status; pinned revision and tree shown above |
| `(cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0284/IntakeProbe.lean)` | 0 | eight pinned APIs elaborated; stdout SHA-256 `0e974f6d4668a227f6524037cc73face6bfc6d5329adc98d0c19b7a785b55e55`; no canonical target or wrapper declared |
| `python3 -B Stage1_Instances/THM-M-0284/check_intake.py` | 1 | historical intake checker expects authoritative intake state `[ ]` and attempts 0; integration now records provisional `[_]` and attempts 1, so the stale assertion was preserved and recorded rather than edited |
| `rg -n -e '\bsorry\b' -e '\badmit\b' -e '\bsorryAx\b' -e '\baxiom\b' -e '\bconstant\b' -e '\bopaque\b' -e '\bunsafe\b' Stage1_Instances/THM-M-0284 --glob '*.lean'` | 1 (expected no match) | no prohibited declaration token in the API-only probe |
| `python3 -m json.tool Stage1_Instances/THM-M-0284/statement-blocker.json` | 0 | blocker parsed as valid JSON |
| `python3 -c "$(python3 -c 'import json; print(next(row[\"argv\"][2] for row in json.load(open(\"Stage1_Instances/THM-M-0284/statement-blocker.json\"))[\"commands_and_results\"] if row[\"argv\"][:2] == [\"python3\", \"-c\"]))')"` | 0 | replays the exact recorded `python3 -c` assertion program and prints `statement blocker invariants: ok`; the program checks item/base identity, blocked open state, null target fields, unchanged `H1/M3/R4`, four undefined mutations, false completion fields, exact changed paths, empty accepted receipts, and no self-test |
| `git diff --check -- Stage1_Instances/THM-M-0284` | 0 | no tracked whitespace diagnostics |
| `git diff --no-index --check /dev/null Stage1_Instances/THM-M-0284/statement-blocker.json` and the same command for `statement-blocker.md` | 1 each (expected new-file difference) | empty diagnostic output; neither new file has a whitespace error |
| `test ! -e .stage1-worker-selftest.json` | 0 | self-test manifest is absent because the statement completion gate did not pass |

The machine-readable blocker records the exact hashes, null target fields, unresolved choices,
candidate boundary, mutation status, retry conditions, and remaining root cut set.

## Retry condition and status boundary

An accountable source owner must preserve and hash one lawful immutable source edition, select and
independently approve an exact theorem passage and proof boundary, and freeze every incorporated
definition, ordered binder, hypothesis, conclusion, translation, correction, erratum, and boundary
case. The selection must decide the independent-object model, generated-sigma-algebra transport,
index and tail conventions, ambient measurable space, measure contract, event measurability, and
conclusion encoding. A later statement run can then encode that same claim, minimize its pinned
imports, serialize its elaborated expression and environment, compile checked transports, and run
all four required mutation classes.

This is a truthful blocker for the assigned phase, not completion of the statement node or a
downstream node. No statement receipt, worker `[_]`, accepted state, statement fingerprint, proof
credit, audit completion, theorem completion, or master acceptance is claimed. Because the assigned
phase did not pass its completion gate, `.stage1-worker-selftest.json` is intentionally absent.
