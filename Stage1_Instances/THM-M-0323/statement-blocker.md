# Statement-phase blocker

Item: `S56-M-0323-STATEMENT`  
Base revision: `d41c33c7ad196cf30c996231fabd214f4d9f5248`

## Decision

The exact Lean target cannot truthfully be frozen from the available source material. The
repository supplies only the Chinese label "Schauder basis theorem" and the phrase "existence of a
basis in Banach spaces". It supplies no theorem locator, space, scalar field, basis system, index
order, norm, or endpoint convention. The accepted intake already records these omissions and makes
primary-source proposition selection the first blocker for this node.

The universal reading is not admissible: not every Banach space has a Schauder basis. In
particular, a countably indexed Schauder basis makes the space separable, while nonseparable Banach
spaces exist; the adjacent repository item `THM-M-0324` also explicitly records Enflo's stronger
counterexample. Replacing the wording by Haar in an unspecified `L^p` space, or by the
Faber-Schauder system in an unspecified continuous-function space, would select a different theorem
without source authority.

`StatementCheck.lean` elaborates the literal universal reading solely as a rejected candidate. It
uses the minimal pinned module that defines `SchauderBasis`; it does not declare that expression to
be canonical and supplies no proof. This preserves a machine-checkable representation of precisely
what was rejected without using `sorry`, an axiom, or a substituted theorem.

## First failed gate

Rev-5.6 section 5's target-freeze gate fails at source identity: no exact primary-source edition,
theorem/page locator, statement, or assumption crosswalk identifies which mathematical proposition
the metadata denotes. Consequently the canonical claim, ordered binders, boundary cases, canonical
Lean expression, and expression fingerprint remain unset (`M3`).

## Unblocking condition

Provide or approve a stable primary-source proposition and record its exact locator and wording.
The statement phase can then freeze its function space, scalar field, norm, Haar/Faber-Schauder
enumeration and normalization, exponent/endpoints where applicable, and elaborate that exact target.

## Scoped validation

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-0323` | exit 0; rank 679, L0/rework_required, planned, theorem_complete false |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0323/StatementCheck.lean` | exit 0; rejected candidate and three representation types elaborated |
| `git diff --check -- Stage1_Instances/THM-M-0323` | exit 0; no output |

This node is blocked rather than self-tested complete. No `.stage1-worker-selftest.json` is emitted,
and no statement, audit, or theorem completion is claimed.
