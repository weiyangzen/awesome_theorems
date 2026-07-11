# THM-M-1073 rev-5.6 intake

This directory is the `planned` intake for the repository label "Poisson process" (`泊松过程`).
The only source claim, "a basic model of a counting process" (`计数过程的基本模型`), describes a
mathematical object and its role; it is not a truth-valued proposition. It gives no rate, index set,
probability space, process axioms, hypotheses, or conclusion. Intake therefore preserves the source
boundary instead of silently choosing one of the many inequivalent theorems about Poisson processes.

The structured scope is in `intake.json`, the field-by-field source comparison is in
`source_statement_crosswalk.md`, and `task-dag.json` records the dependent work left open.

## Scope map

| Surface | Source supplies | Boundary at intake |
|---|---|---|
| Named object | Poisson process | Neither a definition nor a theorem is specified |
| Informal role | Basic model of a counting process | This is descriptive, not a conclusion with a truth value |
| Parameters | none | Rate/intensity, time index, state space, and initial value are open |
| Probability structure | none | Sample space, filtration, measurability, and law are open |
| Candidate characterizations | none selected | Independent stationary increments, exponential interarrival times, and finite-dimensional Poisson laws require an equivalence theorem and hypotheses |
| Candidate results | none selected | Existence, uniqueness in law, increment distributions, martingale properties, and limit laws are distinct targets |
| Lean surface | Lean 4 is the queue backend | No declaration or expression can be selected without inventing the root claim |
| Human source | attribution to Simeon Poisson and year 1837 only | A theorem-bearing primary or authoritative modern source with a pinpoint statement is required |
| Machine status | untrusted metadata says `已验证` | No exact target, formal artifact, or kernel evidence is identified |

## Intake verdict

Lifecycle is `planned`; the conservative root vector is `[H5, M4, R4]`. Here `H5` classifies the
current record as ill-posed as a theorem, not the mathematical topic as false. The first failed gate
is exact human statement identification. Recovery requires an authoritative exact proposition and
then a source decision fixing all parameters, binders, assumptions, and conclusion. No statement,
proof, audit, or theorem completion is claimed.

## Validation

The commands and exact results in `validation.md` establish target membership, repository-standard
consistency, JSON syntax, and dossier-local intake invariants only. There is no eligible Lean
expression to elaborate during this phase.
