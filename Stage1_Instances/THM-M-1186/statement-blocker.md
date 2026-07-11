# Exact-statement gate: blocked

Item: `S56-M-1186-STATEMENT`  
Base revision: `f36169f19d5994091ea3dc506080032ff3f5321b`

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the repository source record. The
complete mathematical wording is `最优传输的存在性` ("existence of optimal transport"), under the
label "McCann theorem" and a 1995 date. It does not determine a unique proposition. In particular,
the record does not identify:

- whether the conclusion concerns an optimal coupling, an optimal transport map, displacement
  interpolation, or McCann's displacement-convexity principle;
- the source and target spaces, their topology and measurable structure, or compactness/Radon/
  Polish assumptions;
- the admissible measures, mass normalization, finite-moment conditions, and cost;
- the regularity, measurability, lower-semicontinuity, boundedness, or finiteness hypotheses;
- the exact minimization functional and whether infinite-valued costs or nonunique minimizers are
  allowed.

These choices give inequivalent theorems. McCann's named work is especially ambiguous here: the
intake crosswalk identifies his 1997 displacement-convexity paper, while existence of a minimizing
coupling is ordinarily a Kantorovich existence result. Choosing either family, or the convenient
compact-metric coupling statement in the legacy Lean file, would invent missing mathematics rather
than elaborate the exact repository claim.

The Stage0 record independently marks all precise definitions and premises as `待补充` (to be
supplied). Its metadata value `已验证` is neither a source pinpoint nor kernel evidence. The intake
therefore correctly leaves source identity at `H3` and the Lean target at `M4`. This phase fails at
canonical human-claim identity, before minimal imports, expression serialization, checked
transports, or meaningful removed-hypothesis/domain/binder/boundary mutations can be established.

## Legacy Lean boundary

`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_151.lean` was checked only as discovery input. Its
`StatementShapeCompactMetric` selects compact metric Borel spaces and asserts `StatementShape`,
which requires `Nonempty (OptimalTransportExistenceData mu nu c)`. That data structure includes not
only an optimal coupling but also tightness and lower-semicontinuity fields. The file itself says
this is a conservative scope decision and not a closed McCann/Kantorovich theorem.

The module elaborates in the pinned environment with five broad direct imports. This establishes
that the historical candidate is syntactically and type-correct; it cannot establish fidelity to
an unidentified source theorem or minimal imports for an exact target. No legacy declaration is
credited as the rev-5.6 canonical statement.

## Required unblock

An accountable source reviewer must first identify a stable primary source by edition,
theorem/page, and exact wording. The review must freeze the theorem family, spaces, measures,
admissible plans or maps, cost and regularity assumptions, functional, conclusion, and degenerate
cases. A later statement worker can then encode that claim, minimize pinned imports, serialize the
elaborated expression and environment, compile all credited transports, and run the four required
structural mutations.

## Narrow validation evidence

Commands were run from this worker clone on 2026-07-12. The existing `.lake` directory is a
worker-clone symlink to canonical pinned artifacts. No update, build, dependency fetch, or mutation
of `.lake` was performed.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1186` | exit 0; rank 151, planned, legacy artifacts unaccepted, theorem incomplete |
| `(cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_151.lean)` | exit 0; historical candidate elaborated and printed its audit probes |
| `(cd Formalizations/Lean && lake env lean --version)` | exit 0; Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | exit 0; `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | exit 0; `651c8acc...b1d2` and `321626c8...2d81` |

First failed gate: exact source-statement identity. Known failures are the canonical Lean target,
minimal-import determination, expression fingerprint, checked transports, and mutation tests. The
assigned phase is not self-tested or complete, so no `.stage1-worker-selftest.json` is emitted. No
theorem completion or downstream-node credit is claimed.
