# Exact-statement gate: blocked

Item: `S56-M-0717-STATEMENT`  
Theorem: `THM-M-0717`  
Base revision: `3a479c703900e8096e6b239e7bf5b0da25472b8a`

## Decision

The exact Lean 4 target cannot be elaborated truthfully from the authoritative repository record.
Its complete mathematical wording is the topic label `图灵机` ("Turing machine") and the gloss
`图灵机的计算模型` ("the computational model of a Turing machine"). This identifies a mathematical
object or theory, not a proposition with ordered binders, hypotheses, and a conclusion. Stage0
also leaves the exact definitions, assumptions, proof process, axioms, and formal artifacts open.

Several inequivalent targets remain compatible with the wording: defining a single-tape machine
and its deterministic step semantics, proving a simulation between machine variants, exhibiting a
machine that computes a particular function, or characterizing Turing-computable functions. They
differ in alphabet and blank-symbol conventions, state and finiteness conditions, tape or stack
representation, input/output encodings, halting and divergence semantics, ordered binders, and
conclusions. The neighboring universal-machine and recognizable-language records are separately
owned targets and cannot fill this gap. Selecting any of these readings would therefore invent or
substitute mathematics.

There is consequently no canonical expression to elaborate or hash, no sound minimal-import claim,
and no meaningful removed-hypothesis, changed-domain, binder-scope, or boundary-case mutation. The
rev-5.6 exact-statement gate fails before anchor or proof evidence may receive credit. Machine state
remains `M4`; the root remains `[H3, M4, R4]`; audit and theorem completion remain false.

## Pinned Lean boundary

Pinned mathlib does provide `TM0`, `TM1`, `TM2`, and `FinTM2` APIs. The existing
`IntakeProbe.lean` imports `Mathlib.Computability.TuringMachine.Computable` and checks representative
machine, configuration, transition, evaluation, support, output, and computability declarations.
It was re-elaborated to distinguish a usable pinned environment from the missing mathematical
statement. It is not a canonical target and receives no statement or proof credit.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. Existing canonical `.lake` artifacts were used read
only. No update, build, dependency clone, or fetch was run.

## Validation evidence

Commands ran in this worker clone on 2026-07-12 (Asia/Shanghai).

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0717` | 0 | rank 756, planned, legacy artifacts unaccepted, theorem incomplete |
| repository `rg` search for the theorem ID, Chinese/English label, and gloss | 0 | found only the topic/gloss, open Stage0 fields, intake records, and separately owned related targets; no exact proposition |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0 at the commit above |
| `cd Formalizations/Lean && lake --version` | 0 | Lake version above |
| `cd Formalizations/Lean && sha256sum lean-toolchain lake-manifest.json` | 0 | hashes `651c8a...1d2` and `321626...d81`, recorded in the JSON blocker |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | pinned mathlib revision above |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0717/IntakeProbe.lean` | 0 | all 12 representative Turing-machine API checks elaborated |

## Retry condition

An accountable source reviewer must preserve and hash an immutable primary-source edition, select
and transcribe one exact proposition with all incorporated definitions and assumptions, dispose of
errata, and independently approve the mapping. Only then can a statement worker encode that same
claim, establish genuinely minimal pinned imports, fingerprint the elaborated expression, check
alternate transports, and run all four mutation classes.

This is the first failed gate, not completion of the statement node or any later node. The assigned
phase is not genuinely self-tested, so no `.stage1-worker-selftest.json` is emitted.
