# Exact-statement gate: blocked

Item: `S56-M-0327-STATEMENT`  
Theorem: `THM-M-0327`  
Base revision: `8014740e5a37eff82745f6fd2bc69f0ee45e67c9`

## Decision

No exact Lean 4 target can be truthfully elaborated from the repository source record. Its entire
mathematical wording is `弱紧算子的特征` ("characterization of weakly compact operators"). The
record supplies no source locator, domains, ordered binders, hypotheses, conclusion, or definition
of weak compactness, and Stage0 explicitly leaves the exact definitions and assumptions open.

The accepted intake identifies two materially different readings that remain compatible with this
metadata: a uniform-integrability characterization of relatively weakly compact subsets of an
`L^1` space, and an operator characterization involving bounded linear maps and weak compactness.
Related formulations using weakly convergent sequences or the Dunford-Pettis property are not
definitionally interchangeable with either reading. They require different scalar, Banach-space,
measure-space, boundedness, closure, topology, unit-ball, sequence/net, and equivalence
hypotheses. Selecting one from the theorem name would substitute invented mathematics for the
repository claim.

Consequently there is no canonical human proposition from which to derive a minimal import set,
an elaborated expression fingerprint, checked transports, or meaningful removed-hypothesis,
changed-domain, binder-scope, and boundary mutations. This fails the rev-5.6 exact-statement gate
before formal-anchor or proof evidence may receive credit. Machine state remains `M4`; statement
and theorem completion are false.

## Pinned Lean boundary

`IntakeProbe.lean` was re-elaborated using the existing pinned artifacts. It checks that mathlib
provides `WeakSpace`, `IsCompactOperator`, `MeasureTheory.Lp`, both uniform-integrability
predicates, and `IsCompact`. These are possible encoding ingredients only. In particular,
`IsCompactOperator` uses the topology already installed on its codomain and does not select the
intended weak topology or theorem variant. A narrow pinned-mathlib search found uniform-
integrability infrastructure but no declaration named for Dunford-Pettis and no matching weakly
compact-operator characterization. Neither the probe nor the search identifies a canonical target.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. The existing canonical `.lake` artifacts were used
read-only; no update, build, clone, fetch, or dependency mutation was run.

## Validation evidence

Commands ran in this worker clone on 2026-07-12 (Asia/Shanghai).

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0327` | 0 | rank 821, planned, legacy artifacts unaccepted, theorem incomplete |
| `rg -n -i 'Dunford.?Pettis\|邓福德.?佩蒂斯\|弱紧算子的特征' ...` over repository sources | 0 | only the underspecified title/gloss, open Stage0 fields, generated projections, and the intake dossier were found |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean version and commit recorded above |
| `cd Formalizations/Lean && lake --version` | 0 | Lake version recorded above |
| `cd Formalizations/Lean && sha256sum lean-toolchain lake-manifest.json` | 0 | `651c8acc...b1d2` and `321626c8...6d81` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | pinned mathlib revision recorded above |
| pinned-mathlib `rg` search for Dunford-Pettis, uniform integrability, and weakly compact operators | 0 | uniform-integrability definitions and uses found; no exact Dunford-Pettis or weakly compact-operator theorem found |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0327/IntakeProbe.lean` | 0 | all six substrate declarations elaborated; no canonical theorem asserted |

## Retry condition

An accountable source reviewer must preserve and hash an immutable primary-source edition, select
and transcribe one exact theorem, record its locator and errata disposition, freeze all incorporated
definitions and assumptions, and independently approve its mapping to the repository label. A
later statement run can then encode that same claim, minimize imports, fingerprint the elaborated
expression, check alternate transports, and execute all four required mutation classes.

This is the first failed gate, not completion of the statement node or any later node. The assigned
phase is not genuinely self-tested, so no `.stage1-worker-selftest.json` is emitted.
