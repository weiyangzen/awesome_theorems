# THM-M-0012 Intake Dossier

`THM-M-0012` is a rev-5.6 `planned` instance for the fundamental theorem of algebra:
every nonconstant univariate complex polynomial has a complex root. The repository wording is
recognizable and stable enough to freeze that human scope, but it supplies no pinpoint primary
source, definition of nonconstant, formal expression, or accepted evidence.

## Intake boundary

- Manifest rank: 1062; legacy slot: none.
- Lane: `hard_statement_first_partial_verification`; baseline: `L0 / rework_required`.
- Lifecycle: `planned`; accepted proof/task state: none.
- Root vector: `H1 / M4 / R4`.
- Audit complete: false; theorem complete: false.

Pinned mathlib contains the close candidate `Complex.exists_root`, together with
`Complex.isAlgClosed` and the generic `IsAlgClosed.exists_root` API. The scoped Lean probe confirms
only that these names and types elaborate at the recorded pin. The canonical target, checked
transports, proof-body provenance, trust closure, and source fidelity belong to later phases and
receive no intake credit.

## Open execution route

| Task | Required output | State |
|---|---|---|
| `S56-M-0012-STATEMENT` | Independently review a source, elaborate the exact target, and mutation-test its scope | open |
| `S56-M-0012-ANCHOR_AUDIT` | Audit formal candidates, bodies, revisions, imports, and trust boundaries | open; depends on statement |
| `S56-M-0012-OBLIGATION_TREE` | Freeze obligations and typed graphs before closure metrics | open; depends on audit |
| `S56-M-0012-PROOF` | Implement or integrate genuine proof bodies | open; depends on tree |
| `S56-M-0012-VALIDATION` | Run hermetic kernel, provenance, trust, and independent gates | open; depends on proof |
| `S56-M-0012-RELEASE` | Independently reconcile audit and theorem completion | open; depends on validation |

The first retry condition is a reviewed source-to-Lean choice among positive degree, exclusion of
constants, `IsRoot`, evaluation equality, and algebraic closedness, followed by exact elaboration
and the required statement mutations.

## Validation boundary

The recorded validation checks manifest consistency, dossier invariants, JSON structure, the
discovery-only Lean probe, prohibited constructs, and whitespace. It reuses the automation-provided
canonical `.lake` artifacts read-only; no update, build, fetch, or dependency mutation was run.
This is provisional worker self-test evidence for intake only, not an accepted receipt or theorem
completion claim.
