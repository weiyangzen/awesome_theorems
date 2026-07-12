# THM-M-0531 rev-5.6 intake

This `planned` dossier interprets the repository wording, "relation between homology groups and
cohomology groups," as the cohomological universal coefficient theorem for a topological space.
That interpretation is narrower than the generic algebraic UCT family recorded for `THM-M-0004`.
It is still provisional: the metadata does not specify reduced versus unreduced theory, grading,
comparison maps, the degree-zero convention, or whether a splitting is part of the root claim.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Space and chains | A topological space and its integral singular chain complex | Exact Lean model and any hypotheses on the space remain open |
| Homology terms | `H_n(X; Z)` and `H_(n-1)(X; Z)` | Reduced/unreduced convention and the `n = 0` boundary must be frozen |
| Cohomology term | `H^n(X; G)` for an abelian coefficient group `G` | Cochain construction and grading convention remain open |
| UCT conclusion | A natural short exact `Ext -> cohomology -> Hom` sequence | Exact arrows, naturality variables, and splitting strength require source selection |
| Lean substrate | Singular homology and `Ext` APIs from pinned mathlib | The APIs elaborate, but no terminal topological UCT declaration is credited |
| Excluded readings | Tensor/Tor homological UCT, Kunneth, or generic API availability | None may replace the cohomological root merely because it is easier to state |

The structured boundary is in `intake.json`; claim-by-claim source and Lean discovery evidence is in
`source_statement_crosswalk.md`.

## Open phase DAG

`STATEMENT -> ANCHOR_AUDIT -> OBLIGATION_TREE -> PROOF -> VALIDATION -> RELEASE`.
All dependent nodes remain open. Intake supplies no proof credit and does not inherit assurance from
the historical `已验证` label or from the separate `THM-M-0004` artifact.

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H2, M3, R3]`. The first failed gate is exact
statement selection: no immutable source copy, assumption-level source review, normalized Lean root,
expression fingerprint, or checked transport is accepted. The theorem is not complete.

## Validation record

Run from repository root on 2026-07-12 (Asia/Shanghai), base revision
`8cd5bc5a3f94397a9ec5148db97a8631552f37ec`:

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 1546 uniform-L0 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0531` | exit 0; rank 588, planned, L0/rework_required, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-0531/intake.json` | exit 0 |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0531/IntakeProbe.lean` | exit 0; both pinned mathlib substrate declarations elaborated |
| `git diff --check -- Stage1_Instances/THM-M-0531 .stage1-worker-selftest.json` | exit 0 |

The Lean probe validates only candidate API availability. It deliberately contains no theorem body
and is not evidence for the universal coefficient theorem itself.
