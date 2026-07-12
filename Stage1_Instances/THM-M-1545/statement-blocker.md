# Exact-statement gate: blocked

Item: `S56-M-1545-STATEMENT`  
Theorem: `THM-M-1545`  
Base revision: `6afdcb2c5487434cce7acf7aeb8ed471faf92666`

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the accepted intake and the repository
source record. The source phrase is only "Nahm transform" / "construction of monopoles". The intake
explicitly leaves charge, interval and endpoint conventions, pole residues, gauge group, framing,
base geometry, analytic function spaces, regularity, and the intended result form unresolved. It
also records that the source could mean a construction in one direction or a correspondence modulo
gauge. These choices produce inequivalent propositions, so selecting them in this phase would
invent missing mathematics.

The discovery citations do not resolve the ambiguity. Nahm (1980) and Hitchin (1983) are listed
without an accepted theorem/page, exact statement, assumption map, immutable source receipt, or
errata audit. The intake requires those facts to be extracted rather than inferred. Consequently
the phase fails at canonical human-claim identity, before an exact expression fingerprint, minimal
import set, checked alternate-encoding transport, or meaningful removed-hypothesis, changed-domain,
binder-scope, and boundary mutation suite can be established.

No statement receipt, machine-proof credit, audit completion, or theorem completion is claimed.
The root remains at least `M3`, and the legacy source is discovery material only.

## Historical Lean boundary

`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_204.lean` elaborates in the pinned environment, but
its `StatementShape` is not exact-statement evidence. The file expressly calls itself a conservative
statement boundary and says that it is not a terminal Nahm-transform proof. Its model makes
substantive unresolved choices and assumptions:

- it uses bounded continuous Hilbert operators while noting that the analytic transform uses
  unbounded differential operators on Sobolev completions;
- `NahmTransformHypotheses` contains an unexplained `True` conjunct and packages unresolved reality,
  spectral, gauge-preservation, and charge/framing predicates as fields;
- `NahmTransformConclusion` assumes a preselected `MonopoleData` output and asks for a nonempty
  `NahmTransformPackage`, whose fields already include the kernel construction, transformed fields,
  Bogomolny result, regularity, and finite energy;
- the file has eleven direct mathlib imports supporting its broader audit surface, so elaborating it
  cannot establish minimal imports for an unidentified canonical target.

Thus the successful legacy elaboration shows only that this abstract API is compatible with the
pinned Lean environment. Reusing it as the exact target would substitute a conditional package
interface for the source theorem and would violate the rev-5.6 freeze gate.

## Required unblock

An accountable source reviewer must select one stable primary-source theorem-level claim and record
the edition/version, theorem or proposition and page range, exact wording, surrounding definitions,
assumptions, corrections, and errata. The selection must freeze the charge, interval, endpoint and
residue conventions, gauge group and quotient/framing convention, base three-manifold, Nahm data
regularity and reality conditions, Dirac operator and Sobolev domains, kernel-rank hypotheses,
output bundle/connection/Higgs regularity, finite-energy condition, ordered binders, and whether the
conclusion is construction, uniqueness, or equivalence. A later statement worker can then encode
that proposition without substitution, minimize its imports, print and hash its elaborated
expression, check transports, and run structural mutations.

## Narrow validation evidence

Commands were run in this worker clone on 2026-07-12. Lean reused the existing canonical pinned
`.lake` symlink; no dependency update, build, clone, or fetch was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1545` | 0 | rank 204, planned, legacy artifacts unaccepted, theorem incomplete |
| `cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_204.lean` | 0 | historical abstract module elaborated and printed its audit checks; not exact-statement evidence |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | mathlib `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | toolchain `651c8acc...b1d2`; manifest `321626c8...2d81` |

Known failures are exact canonical claim identity, minimal imports, expression fingerprint, checked
transports, and mutation tests. The assigned deliverable is therefore not self-tested or complete,
so no `.stage1-worker-selftest.json` is emitted. Master acceptance remains outstanding, and this
artifact does not modify the generated checklist or execution DAG.
