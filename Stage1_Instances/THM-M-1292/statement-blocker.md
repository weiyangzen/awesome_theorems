# Statement-phase blocker

Item: `S56-M-1292-STATEMENT`

Verdict: `blocked`. No canonical Lean target can be truthfully frozen from the available source
record.

## First failed gate

The exact mathematical claim is not identified. The complete repository source record gives only
the label "Struwe compactness lemma", Michael Struwe, the year 1984, and the description "an
alternative to the Palais-Smale condition". It supplies no publication, title, theorem or lemma
number, page, quotation, definition reference, assumptions, or errata. These fields are required by
the rev-5.6 exact-statement gate and cannot be inferred from a name shared by inequivalent variants
of Struwe's monotonicity method.

In particular, the record does not determine the ambient function space, parameter interval,
functional family, min-max class, monotonicity convention, differentiability assumptions,
quantifier order, exceptional-set notion, bounded Palais-Smale conclusion, or a compactness
conclusion. Choosing values for these fields would broaden or substitute the theorem rather than
elaborate the exact target.

## Legacy Lean probe

`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_172.lean` elaborates in the pinned environment,
but it is not eligible as the canonical target. Its declaration
`AwesomeTheorems.Stage1.S1_M_172.StatementShape` selects an abstract monotonicity-trick interface
and assumes the central variational work through proposition-valued fields such as
`monotoneParameterFamily`, `minmaxGeometry`, and `deformationEstimate`. The module's own
`statementNormalizationNote` says that this is not a terminal Struwe proof. Successful elaboration
therefore establishes only that the legacy candidate is syntactically usable discovery input; it
does not establish source fidelity or clear the statement gate.

No new Lean declaration was created, because any exact-looking declaration would encode choices
absent from the source. No `sorry`, axiom, placeholder, substituted compactness theorem, or proof
claim was introduced.

## Retry condition

Reopen this phase only after a primary publication has been identified and independently checked
with an exact edition/theorem-or-lemma/page/definition/assumption/errata crosswalk. The resulting
record must fix all domains, ordered binders, hypotheses, conclusion, exceptional-set semantics,
and boundary cases before a canonical Lean expression and minimal imports can be frozen and
elaborated.

## Validation evidence

Base revision: `935f676246c95d817740248fb8588e8cea34c00d`.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-1292` | exit 0; rank 172, `L0 / rework_required`, planned, theorem completion false |
| `git status --short` | exit 0; pre-existing untracked `Formalizations/Lean/.lake` symlink only |
| `(cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_172.lean)` | exit 0 in 2.8 seconds; legacy module and audit probes elaborated |

The smallest real Lean check passes for the legacy candidate, while the required exact target
remains undefined. Consequently this statement phase is not self-tested as complete and no
`.stage1-worker-selftest.json` is emitted.
