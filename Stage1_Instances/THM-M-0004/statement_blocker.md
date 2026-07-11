# Statement-phase blocker

## Verdict

`S56-M-0004-STATEMENT` is blocked at the exact-statement selection gate. No canonical Lean
declaration has been added, and this artifact does not claim worker completion.

The target metadata supplies only “Relation between homology groups and tensor product/Hom
groups.” This does not determine a single theorem. In particular, it does not choose between the
homological tensor/Tor short exact sequence and the cohomological Hom/Ext short exact sequence, nor
does it specify the base ring, module handedness, chain/cochain convention, boundedness or
projectivity assumptions, degree shifts, comparison maps, naturality scope, or splitting claim.
The repository also contains a distinct universal-coefficient entry, `THM-M-0531`, worded as a
relation between homology and cohomology. That second entry makes silently interpreting
`THM-M-0004` as the cohomological theorem especially unsafe.

The intake record correctly leaves `statement_selection` open and its exact expression and
environment fingerprints null. Under sections 5 and 5.1 of the rev-5.6 standard, unresolved
statement ambiguity is a hard blocker. Selecting a branch or supplying omitted assumptions here
would invent mathematics not fixed by the source record. The historical
`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_099.lean` cannot resolve this: its
`Stage1.THMM0004.StatementShape` quantifies over an abstract output package whose mathematical term
identifications are merely fields, so it is discovery material rather than either classical UCT
statement.

## Smallest real validation

Base revision: `9e3fd02a2a952da7031bb1dd61387443dd4c1cc7`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Standard, execution skill, and 1546-target projection are consistent. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique uniform-L0 targets with ranks 1 through 1546. |
| `python3 scripts/stage1_target.py show THM-M-0004` | 0 | Rank 99; lifecycle `planned`; legacy artifacts unaccepted; theorem incomplete. |
| `lake env lean AwesomeTheorems/Stage1/S1_M_099.lean` from `Formalizations/Lean` | 0 | The historical discovery module elaborates, but its output confirms only API probes and abstract statement shapes; it does not provide an exact terminal UCT target. |
| `lake env lean --version` from `Formalizations/Lean` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`. |
| `git -C .lake/packages/mathlib rev-parse HEAD` from `Formalizations/Lean` | 0 | Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`. |

The canonical source file has SHA-256
`1c848c84f99b8753b7a77e83e1851697910e4fcaa009441d631cd25de39f8f93`, but that hash identifies
the historical discovery artifact, not an accepted exact statement. The pinned toolchain and
mathlib are available, so missing build infrastructure is not the blocker.

## Unblocking condition

An authority for the theorem scope must select one branch and pin a primary-source edition,
theorem/page, and complete assumptions. It must also decide whether `THM-M-0531` owns the
cohomological branch. Once that decision is recorded in the intake contract, this phase can encode
the exact source terms and maps, minimize imports, elaborate with fixed universes/options, compute
the expression and environment fingerprints, and run the four required statement mutations.

Until then the root vector remains `[H3, M3, R3]`, the first failed gate is exact-statement
selection, and theorem completion remains false.
