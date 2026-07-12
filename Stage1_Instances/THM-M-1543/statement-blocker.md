# Exact-statement gate: blocked

Item: `S56-M-1543-STATEMENT`  
Base revision: `a1b16ca3ed65db2ec65e3d478d1680d9c1f5489d`

## Decision

The exact Lean 4 target cannot be frozen truthfully from the accepted intake evidence. The
repository source wording is only `瞬子与代数几何` ("instantons and algebraic geometry"), while
the intake identifies Atiyah and Ward's 1977 paper only as a candidate. It does not identify an
exact numbered result or page within pages 117-124, reproduce the result's hypotheses, or record an
errata review. The paper is not present in the repository. Bibliographic metadata therefore cannot
decide the mathematical choices required by the rev-5.6 statement gate, including:

- the base space and its compactification and orientation conventions;
- the structure group, bundle rank, charge, framing, and reducibility conditions;
- the connection regularity and finite-action hypotheses and gauge equivalence relation;
- the concrete twistor space, real structure, and distinguished-line convention; and
- the holomorphic bundle category, triviality, reality, stability, and isomorphism conditions.

These choices produce non-equivalent correspondence theorems. Selecting them here would invent
missing mathematics or broaden the candidate primary result, contrary to sections 5 and 5.1 of
`Docs/Stage1_Blueprint_rev-5.6.md`. Consequently there is no canonical declaration or expression to
serialize, no honest minimal-import claim, and no meaningful removed-hypothesis, changed-domain,
binder-scope, or boundary mutation suite.

## Legacy Lean boundary

The discovery module
`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_179.lean` elaborates in the pinned environment,
but it is not an exact-statement substitute. In particular, its `StatementShape` quantifies over
user-supplied `TwistorModel`, `GaugeInstantonData`, and `HolomorphicTwistorBundleData`, then asks for
`Nonempty (AtiyahWardCorrespondencePackage T I B)`. The geometric and analytic content occurs as
abstract `Prop` fields, while the package assumes both transforms and their inverse laws as fields.
It therefore packages the desired correspondence instead of stating the selected concrete 1977
result. Its successful elaboration receives no exact-statement or proof credit.

The first failed gate is canonical statement identity. The machine debt remains `M4`; no expression
fingerprint, checked alternate encoding, statement acceptance, proof credit, audit completion, or
theorem completion is claimed. Because the assigned phase is not self-tested to completion, no
`.stage1-worker-selftest.json` is emitted.

## Required unblock

An accountable source reviewer must inspect a stable copy of the candidate primary paper, select
the exact result, and record its page/result identity, complete assumptions and definitions, and
errata outcome. The corresponding base, orientation, gauge, analytic, quotient, twistor-line, and
bundle-reality conventions must then be frozen before a later statement worker encodes the target
and runs the four required mutation classes.

## Narrow validation evidence

Commands ran in this worker clone on 2026-07-12. Lean used the existing pinned `.lake` artifacts;
no update, build, clone, or fetch was performed.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups and 1546 uniform-L0 targets; execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1543` | exit 0; rank 179, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |
| `(cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_179.lean)` | exit 0; the abstract legacy boundary elaborated and printed its audit declarations; this is not canonical-target evidence |
| `(cd Formalizations/Lean && lake env lean --version)` | exit 0; Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |

Known failure: exact source identity and assumptions remain absent. Until they are supplied, target
elaboration, environment/expression fingerprinting, checked transports, and statement mutations
are blocked rather than failed Lean checks.
