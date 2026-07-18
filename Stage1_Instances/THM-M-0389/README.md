# THM-M-0389 Intake Dossier

## Status boundary

This is a retained `planned` intake instance at `L0 / rework_required`. It contains no accepted proof state, no Lean closure, and no theorem-completion claim. The repository label `已验证` is explicitly untrusted metadata.

## Scope map

The repository supplies only the phrase `x²+y²+z²=3xyz的整数解`, naturally identifying the integer Markov equation

`x^2 + y^2 + z^2 = 3*x*y*z`.

It does not state a proposition about those solutions. In particular, it does not choose among existence, complete classification, generation from a base triple by permutations and Vieta moves, positivity/nonnegativity, or a uniqueness assertion. The intended binder order, sign policy, zero cases, ordering convention, and quotient by permutations are also absent. Therefore intake preserves the wording and records `M3` statement debt rather than inventing a broader or more convenient theorem.

The target domain is provisionally `ℤ` because the source explicitly says integer solutions. A later statement phase must not silently replace this with positive naturals; any such encoding needs a source-backed exact claim and checked transports.

## Source-statement crosswalk

| Source node | Recorded text/metadata | Formal consequence at intake | Debt |
|---|---|---|---|
| `Docs/Stage0_Blueprint.md`, THM-M-0389 | `x²+y²+z²=3xyz的整数解`; proposer Andrey Markov; status `已验证` | Identifies equation and integer domain only | No exact conclusion, hypotheses, or primary citation; H4/M3 |
| `Docs/Stage1_Blueprint.md`, S1-M-020 | Same wording; Lean 4 + mathlib lane; historical `closed` bucket | Discovery and scheduling provenance only | Legacy status grants no proof credit |
| `Docs/Stage1_Target_Membership_v2.json`, rank 20 | Membership, discovery metadata, planned lifecycle, uniform L0 baseline | Identifies this frozen Stage1 member | Does not establish mathematical fidelity, focus eligibility, or closure |
| `Docs/Stage1_Blueprint_v2.md`, S56-M-0389 nodes | Current identity and state for intake followed by statement, audit, graph, integration, validation, release | Sole requirements and task-state boundary | All later nodes remain open/blocked |

No primary mathematical source is cited in the repository records. Primary-source theorem/page identification and the choice of exact classification statement belong to the subsequent statement/source audit work and are not claimed here.

## Provisional statement artifact

The statement phase freezes the standard complete-classification reading in
`Statement.lean`: every integer Markov triple is zero or an even-sign variant
of a triple generated from `(1,1,1)` by permutations and Vieta mutations. The
target elaborates with only `Init`; its explicit expression, environment, and
four structural mutations are recorded in `statement.json` and
`statement-validation.md`.

This is self-tested statement evidence pending master acceptance, not a proof
or a human-source fidelity upgrade. The absence of a repository primary-source
theorem/page remains explicit debt for the source/anchor audit.

## Validation record

Base revision: `a8d6489fd935cd71fa4499f2f3f5b051998203f4`.

Preflight commands on 2026-07-12:

- `python3 Docs/tools/check_stage1_standard.py` -> exit 0; `ok` with 15 assurance groups, 1546 uniform-L0 targets, and execution skill present.
- `python3 scripts/stage1_target.py check` -> exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required.
- `python3 scripts/stage1_target.py show THM-M-0389` -> exit 0; rank 20, planned, theorem_complete false.
- `git status --short` -> exit 0; empty before dossier creation.

The smallest intake validation is JSON parsing plus repository structural validation and whitespace checking. Exact commands/results are refreshed in `validation.txt`. No Lean command is appropriate yet because the source does not determine a canonical proposition; fabricating one merely to elaborate would violate the exact-statement gate.
