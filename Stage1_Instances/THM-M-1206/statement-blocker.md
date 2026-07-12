# Exact-statement gate: blocked

Item: `S56-M-1206-STATEMENT`  
Theorem: `THM-M-1206`  
Base revision: `446f3e80e7a93deeca70150fa80d9ee079ee0586`

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the available source record. The
Stage0 content is only "weak-convergence measure representation," while the intake selects J. M.
Ball, "A version of the fundamental theorem for young measures," *PDEs and Continuum Models of
Phase Transitions*, Lecture Notes in Physics 344 (1989), pp. 207-215, DOI
`10.1007/BFb0024945`, Theorem 2.1 as a candidate. The repository contains neither an authoritative
copy nor an exact quotation of that theorem and its referenced definitions. The publisher page
and bibliographic APIs confirm the chapter metadata but do not expose the theorem text.

Consequently the source has not fixed the domain measure space, target space and topology,
sequence hypotheses, precise no-escape/coercivity condition, subsequence encoding, measurable
parametrized-measure formulation, admissible integrands, integrability assumptions, convergence
mode, or treatment of null and non-tight cases. These choices materially change the proposition.
Choosing them from a secondary formulation or convenience would broaden or substitute the unknown
root, contrary to the exact-statement gate.

The target therefore remains `[H2, M4, R4]`. There is no canonical expression fingerprint,
minimal-import claim, checked transport, or meaningful removed-hypothesis/domain/binder-scope/
boundary mutation suite. No statement acceptance, audit completion, or theorem completion is
claimed.

## Lean boundary

`StatementCandidateProbe.lean` elaborates against the existing pinned environment with the single
import `Mathlib.Probability.Kernel.Defs`. It confirms that mathlib represents a measurable family
of measures by `ProbabilityTheory.Kernel` and expresses probability-valued kernels using
`ProbabilityTheory.IsMarkovKernel`. This is only an encoding probe: it neither encodes extraction
of a subsequence nor the source's convergence formula, and receives no exact-statement or proof
credit. Minimal imports cannot be determined for a source target that is not yet identified.

## Required unblock

An accountable reviewer must inspect a stable authoritative copy of Ball's chapter and record the
verbatim theorem, page and theorem number, all referenced definitions, ordered assumptions,
conclusion, and errata. The source-to-Lean crosswalk must then freeze every choice listed above.
Only then can a statement worker encode the exact proposition, minimize pinned imports, serialize
its elaborated expression and environment, check alternate transports, and run the four required
mutation classes.

## Narrow validation evidence

Commands ran from this worker clone on 2026-07-12. Lean used only the existing pinned `.lake`
artifacts; no update, build, clone, fetch, or dependency mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1206` | 0 | rank 399, planned, legacy artifacts unaccepted, theorem incomplete |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1206/StatementCandidateProbe.lean` | 0 | kernel, kernel measurability, Markov-kernel, and measure declarations elaborated |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `git diff --check -- Stage1_Instances/THM-M-1206` | 0 | no output |

Known failures are canonical source identity, exact Lean elaboration, expression fingerprint,
checked transports, and mutation tests. The assigned deliverable is therefore not genuinely
self-tested, so no `.stage1-worker-selftest.json` is emitted.
