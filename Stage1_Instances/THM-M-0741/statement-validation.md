# THM-M-0741 statement validation

Item: `S56-M-0741-STATEMENT`

Base revision: `d05520867fab3367a9b61b9544c3e12241204f54`

Base tree: `fb2cfc62077d5b53e9938632cd6361dd60872067`

## Frozen target

`Stage1Instances.THM_M_0741.HaltingProblemUndecidable` is the conventional
arbitrary-program/arbitrary-input reading of the repository claim. Programs are
`Nat.Partrec.Code`, inputs are natural numbers, halting is definedness of the universal partial
evaluator, and effective decidability is `ComputablePred`. Thus the target asks for one uniform
total effective Boolean decision procedure over every code/input pair and negates its existence.

The target-bearing catalog gives only the short gloss "the halting problem is undecidable." The
repository's fuller computability catalog explicitly gives the arbitrary-machine/given-input
reading, and the statement phase selects mathlib's standard computability-complete code model for
it. This is a machine-statement freeze at `H1`, not an accepted translation of Turing's 1936
terminology. The immutable primary passage, historical definition transport, correction/errata
review, and independent source review remain open.

The sole direct import is `Mathlib.Computability.Halting`. That module defines `ComputablePred` and
publicly imports `PartrecCode`; changing the import to `Mathlib.Computability.PartrecCode` makes
`ComputablePred` unknown. The canonical target has a checked definitional iff to its expanded
form. Four mutations change the effective-decider contract, code/input domain, input binder scope,
or self-input boundary. Lean rejects exact-type interchange and their fully explicit expression
fingerprints differ. This tests statement identity; it does not assert logical inequivalence of
every mutation.

## Commands and results

All commands ran in this worker clone on 2026-07-13. Lean reused the automation-provided canonical
pinned `.lake` symlink read-only. No update, build, clone, fetch, or dependency mutation was run.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required`. |
| `python3 scripts/stage1_target.py show THM-M-0741` | 0 | Rank 1329, planned, legacy artifacts unaccepted, theorem incomplete. |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`. |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0741/Statement.lean` | 0 | Canonical and expanded targets, checked iff, four expected exact-type rejections, two execution boundaries, axiom report, and explicit expression elaborated; output SHA-256 `497f631d...79e`. |
| `cd Formalizations/Lean && python3 -B ../../Stage1_Instances/THM-M-0741/check_statement.py` | 0 | Expression SHA-256 `1a96ad27...18c`; all mutations distinguished; minimal-import negative probe, source/record/receipt/packet hashes, base identity, and dependency pins passed. |
| minimal import negative probe replacing `Mathlib.Computability.Halting` with `Mathlib.Computability.PartrecCode` | 1 | Expected failure: `ComputablePred` is unknown. |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | 0 | Empty output; pinned dependency worktree stayed clean. |
| scoped prohibited-construct scan over owned Lean sources | 1 | Expected no-match exit: no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration. |
| JSON validation and scoped whitespace checks | 0 | Structured artifacts are valid and no whitespace diagnostics were emitted. |

The checked iff reports `propext`, `Classical.choice`, and `Quot.sound`; no custom axiom or
`sorryAx` appears. The two boundary witnesses establish that the zero code halts on every input
and that unbounded search for a zero of successor diverges on every input. They authenticate the
selected semantics only and are not a proof of undecidability.

## Status boundary

This is a provisional worker-self-tested statement proposal. The intake dependency is itself only
provisional, so acceptance must remain dependency ordered. Primary-source H0, alternate
Turing-machine transport, anchor and terminal-body audit, obligation registry, proof,
composition/trust/readability closure, hermetic replay, independent verification, release, and
master acceptance all remain open. No audit completion or theorem completion is claimed.
