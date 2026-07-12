# Exact-statement gate: blocked

Item: `S56-M-0739-STATEMENT`  
Theorem: `THM-M-0739`  
Base revision: `3159849a5319960dea505779c7c20894ea30487c`

## Decision

The authoritative repository record supplies only the topic label `深度受限电路` and the gloss
`电路深度的下界` ("lower bounds on circuit depth"). It does not identify one proposition or an
immutable primary-source passage. Consequently no exact Lean 4 target can be elaborated without
inventing or substituting mathematics.

Materially inequivalent readings remain compatible with the record, including a polynomial-size
`AC^0` lower bound for parity, a logarithmic depth lower bound for bounded-fan-in circuits, and a
size-depth tradeoff for a named function and gate basis. These readings require different circuit
grammars, fan-in rules, size constraints, uniformity conventions, function families, quantifier
orders, and conclusions. An unrestricted gate basis can even contain the target function as one
primitive gate, showing why the missing model is mathematically decisive rather than cosmetic.

There is therefore no canonical expression to serialize or hash, no justified minimal import for
that expression, and no sound removed-hypothesis, changed-domain, changed-binder-scope, or boundary
mutation test. Section 5.1 of the rev-5.6 blueprint fails before proof evidence may be inspected.
The intake probe was re-elaborated only to distinguish a functioning pinned Lean environment from
a missing mathematical statement. It establishes generic finite Boolean-function APIs, not a
circuit definition or theorem, and receives no statement or proof credit.

## Validation evidence

Commands ran in this worker clone on `2026-07-12` (`Asia/Shanghai`). The canonical `.lake` path is
a link to the existing pinned artifacts and was used read-only. No update, build, clone, fetch, or
dependency mutation was run.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups; 1546 uniform-L0 Lean 4 targets; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0739` | 0 | rank 775, planned, legacy artifacts unaccepted, theorem incomplete |
| repository `rg` search for the theorem ID and Chinese/English label and gloss | 0 | found only the underspecified source metadata, generated inventory entries, and this target's intake records; no exact proposition or primary-source locator |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `(cd Formalizations/Lean && lake --version)` | 0 | Lake `5.0.0-src+98dc76e` |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | hashes `651c8a...1d2` and `321626...d81`, recorded in `statement-blocker.json` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | pinned mathlib `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| pinned-mathlib `rg` search for Boolean-circuit, circuit-depth, bounded-fan-in, `AC^0`, and circuit/parity terms | 0 | only unrelated lexical false positives such as identifiers ending in `ac0`; no relevant circuit model or lower-bound declaration was identified |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0739/IntakeProbe.lean)` | 0 | all seven generic finite Boolean-function API/type checks elaborated; no canonical theorem target asserted |
| `python3 -m json.tool Stage1_Instances/THM-M-0739/instance.json` | 0 | valid intake JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-0739/task-dag.json` | 0 | valid open task DAG JSON |
| `rg -n '\b(sorry\|admit)\b\|^[[:space:]]*axiom\b' Stage1_Instances/THM-M-0739 -g '*.lean'` | 1 | expected no-match exit; no prohibited placeholder or axiom in owned Lean files |

## Retry condition and status boundary

An accountable source reviewer must preserve and hash an immutable primary or authoritative source
edition, select and transcribe one exact lower-bound theorem, record its theorem/page and errata,
fix all circuit and asymptotic conventions, and independently approve the mapping to this target.
A later statement run can then encode that same claim, minimize imports, fingerprint the elaborated
expression, check credited alternate transports, and execute all four required mutation classes.

This is the first failed gate. The statement node remains `[ ]`; the root remains
`[H3, M4, R4]`, with `audit_complete: false` and `theorem_complete: false`. The assigned phase is
not genuinely self-tested, so no `.stage1-worker-selftest.json` is emitted.
