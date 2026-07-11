# Statement gate blocker

Item: `S56-M-0436-STATEMENT`  
Theorem: `THM-M-0436`  
Base revision: `108284d893a06f2c566f9a7958581e78cbb50d02`

## Verdict

The exact-statement gate is blocked and remains `M4`. The repository identifies only the broad
historical topic "Shimura lifting" and a likely primary paper, G. Shimura, *On modular forms of
half integral weight*, Annals of Mathematics 97 (1973), 440-481. It contains no immutable copy,
theorem/page selection, or exact transcription of the relevant result. The paper contains a family
of results whose weights, levels, characters, admissible squarefree index, cusp/eigenform
hypotheses, coefficient normalization, and exceptional cases cannot be inferred from the metadata
without inventing mathematics. Section 5 of the rev-5.6 standard makes that ambiguity a hard
statement blocker.

Consequently this phase does not publish a canonical `Statement.lean`, expression hash,
environment fingerprint for an alleged root, checked alternate transport, or successful worker
self-test receipt. The retry condition is an immutable primary-source copy plus an independently
reviewed selection and transcription of the precise theorem/corollary intended by `THM-M-0436`.

## Rejected legacy candidate

The historical declaration
`AwesomeTheorems.Stage1.S1_M_085.StatementShape` is not an exact encoding. Its source object stores
the transformation law, cuspidality, plus-space membership, and Hecke eigenform status as unrelated
`Prop` fields. Its target stores the coefficient formula, Hecke compatibility, and L-function
compatibility as unconstrained `Prop` fields, with no required truth proofs in the root.

`StatementAudit.lean` mutation-tests this boundary using a field-for-field local expansion of the
legacy source record, target record, and `StatementShape`. It constructs the target for every input
using the zero ordinary cusp form and fills the compatibility fields with `True`, proving that
expanded shape regardless of all four input hypotheses. This kernel result is evidence that
promoting the legacy declaration would substitute a vacuous existence wrapper for Shimura's
theorem. It receives no theorem-proof credit.

## Commands and results

Commands ran in this worker clone. Lean commands ran from `Formalizations/Lean` and reused the
canonical pinned `.lake` symlink; no dependency update, build, clone, or fetch was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets validated |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546 |
| `python3 scripts/stage1_target.py show THM-M-0436` | 0 | rank 85, planned, L0/rework-required, theorem incomplete |
| `lake env lean AwesomeTheorems/Stage1/S1_M_085.lean` | 0 | historical discovery module elaborated against pinned artifacts |
| `lake env lean ../../Stage1_Instances/THM-M-0436/StatementAudit.lean` | 0 | local expansion and vacuity mutation elaborated; printed `legacyStatementShape_is_vacuous : LegacyStatementShape` |
| `lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `sha256sum lean-toolchain lake-manifest.json` | 0 | `651c8acc...85b1d2` and `321626c8...2d81`; manifest pins mathlib `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| forbidden declaration scan of `StatementAudit.lean` | 1 | no `sorry`, `admit`, or `axiom` token; 1 is ripgrep's no-match exit |
| `git diff --check -- Stage1_Instances/THM-M-0436` | 0 | no whitespace errors |

## Status boundary

This artifact identifies and checks a concrete failure of the legacy statement candidate. It does
not freeze the human claim, elaborate the exact Shimura-lifting target, prove any case of Shimura
lifting, or advance the anchor, obligation, proof, validation, or release phases. No
`.stage1-worker-selftest.json` is emitted because the assigned statement phase did not pass.
