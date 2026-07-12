# THM-M-1544 statement-phase blocker

Item: `S56-M-1544-STATEMENT`  
Base revision: `6afdcb2c5487434cce7acf7aeb8ed471faf92666`

## Verdict

The exact Lean 4 target cannot yet be truthfully frozen or elaborated. The accepted intake bounds
the human claim as an ADHM classification/construction of framed anti-self-dual connections, but
it deliberately leaves open the gauge group, instanton-charge convention, framing point,
regularity class, presentation of the ADHM data, real equation, stability/nondegeneracy condition,
quotient group, and whether the conclusion is a set-level bijection or a stronger moduli-space
equivalence. These choices change the proposition, its ordered binders, and its boundary cases.
The repository's source record supplies only the phrase "the algebraic-geometric construction of
instantons" and the bibliographic anchor to the 1978 paper; it contains no reviewed exact theorem
transcription, premise map, convention crosswalk, or errata decision from which those choices can
be recovered without inventing mathematics.

The legacy module `Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_203.lean` elaborates in the
pinned environment, but it is negative boundary evidence rather than an exact target. Its
`StatementShape` quantifies over an arbitrary field and arbitrary finite-dimensional spaces, while
`ADHMHypotheses` stores the real moment-map condition, rank/charge condition, and complex-base
condition as proposition fields accompanied by proofs. Its conclusion is merely
`Nonempty (ADHMConstructionPackage D)`, and that package stores the absent bundle, connection,
anti-self-duality, rank/charge, and equivalence conclusions as fields. It neither defines framed
ASD connections and gauge equivalence nor states the intake-selected classification between their
moduli classes and ADHM-data classes. Wrapping or copying it would therefore substitute a coarse
interface for the assigned theorem.

First failed gate: rev-5.6 section 5 exact source-statement identification, before canonical Lean
elaboration. The statement node remains open at `M4`; there is no canonical declaration,
expression fingerprint, minimal exact-target import list, checked alternate transport, or valid
four-class mutation suite. Retry only after an immutable primary-source statement (supplemented by
a pinned detailed treatment if the short paper does not fix the conventions) is independently
reviewed and freezes every choice above, including charge-zero and empty-moduli behavior. No
statement acceptance, proof credit, audit completion, or theorem completion is claimed.

## Commands and results

All commands ran in this worker clone. The Lean check reused the existing canonical `.lake`
artifacts through the worker link. No update, build, fetch, or dependency mutation was run.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Standard projection passed: 15 assurance groups and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | 0 | Manifest passed: 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1544` | 0 | Rank 203, planned, `hard_mathlib_anchor_and_wrapper`, legacy artifacts unaccepted, theorem incomplete |
| `cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_203.lean` | 0 | Legacy boundary module elaborated; this does not elaborate the exact ADHM classification target |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_203.lean` | 0 | SHA-256 values `651c8a...b1d2`, `321626...2d81`, and `126f5d...af5` respectively |
| `rg -n -i 'ADHM\|Atiyah.*Hitchin.*Drinfeld.*Manin\|Construction of instantons' . --glob '!Formalizations/Lean/.lake/**' --glob '!Stage1_Instances/THM-M-1544/**'` | 0 | Found only the terse repository source record, generated metadata, legacy boundary module, and neighboring references; no exact reviewed source transcription |

No `.stage1-worker-selftest.json` is emitted because the assigned statement phase is blocked rather
than genuinely self-tested.
