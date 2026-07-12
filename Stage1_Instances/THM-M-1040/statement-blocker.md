# Exact-statement gate: blocked

Item: `S56-M-1040-STATEMENT`
Base revision: `4633bb122ff00838c72bebefcbb3490430c9e2f3`

## Decision

The exact Lean 4 target cannot yet be truthfully selected or elaborated. The repository source
record says only "Feller semigroup and Markov process." The accepted intake deliberately leaves
the exact primary-source theorem, state-space assumptions, function space, initial-law
quantification, canonical path space, and path regularity open. These choices distinguish
non-equivalent theorems, including:

- a locally compact second-countable Hausdorff state space versus a Polish or general Borel space;
- the Feller action on `C₀(E)` versus bounded continuous functions;
- a conservative versus sub-Markov semigroup, with or without a cemetery state;
- realization for each starting point versus every initial distribution;
- existence of a Markov realization versus a canonical path-space realization; and
- no asserted path regularity, right-continuous paths, or cadlag paths.

The repository contains no inspected stable primary-source transcription fixing these choices.
Its discovery notes name Feller, volume II (1971), and Ethier-Kurtz, Chapter 4 (1986), but record no
exact theorem/page, wording, assumptions, or errata. Selecting one familiar formulation would
therefore substitute an invented target for the metadata-screened claim, contrary to the
rev-5.6 exact-statement gate.

## Lean boundary checked

The pinned mathlib source tree contains no declaration or module matching case-insensitive search
`Feller`. The legacy module
`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_233.lean` elaborates in the pinned environment,
but cannot supply the canonical target. Its `FellerSemigroupData` uses bounded continuous
functions rather than a source-selected `C₀(E)` formulation, while `FellerProcessRealization`
stores the terminal transition-law, Markov-property, and path-regularization propositions together
with proofs as fields. Consequently its `StatementShape` asks for a package already containing the
desired conclusions and does not encode their mathematical definitions. The module itself labels
this as a statement shape and explicitly denies construction of a continuous-time Feller process.

Elaboration of that legacy module is useful only as a pinned API/substrate check. It is not exact
statement identity, a checked transport, or proof evidence for `THM-M-1040`.

## Validation record

Commands were run from this worker clone on 2026-07-12. The Lean command was run from
`Formalizations/Lean` using the existing canonical `.lake` symlink. No update, fetch, clone, or
build was performed.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-1040` | exit 0; rank 233, planned, theorem_complete false |
| `rg -n -i 'Feller' Formalizations/Lean/.lake/packages/mathlib/Mathlib Formalizations/Lean/.lake/packages/mathlib/Mathlib.lean` | exit 1; no matches |
| `lake env lean AwesomeTheorems/Stage1/S1_M_233.lean` | exit 0; legacy declarations elaborated and printed; no canonical target or proof credited |
| `lake env lean --version` | exit 0; Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git diff --no-index --check /dev/null Stage1_Instances/THM-M-1040/statement-blocker.md` | exit 1 solely because the file is new; no whitespace-error output |

Pinned environment: toolchain `leanprover/lean4:v4.29.0`; mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`; `lean-toolchain` SHA-256
`651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`; and
`lake-manifest.json` SHA-256
`321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Gate result and retry condition

First failed gate: section 5/5.1 exact statement identity. Without the source-exact proposition,
there is no honest canonical Lean declaration, elaborated-expression hash, minimal import set,
checked alternate transport, or meaningful removed-hypothesis/domain/binder-scope/boundary
mutation suite. Machine debt remains `M4`.

Retry after an accountable source reviewer records a stable edition, theorem/page, exact wording,
assumptions, conclusion, edge cases, and errata, and freezes the state-space, `C₀`/bounded-
continuous, conservativity, initial-law, path-space, and path-regularity decisions. The subsequent
statement worker must encode the transition laws and Markov/path conclusions concretely rather
than as caller-supplied opaque propositions.

The assigned statement phase is not self-tested as complete, so no
`.stage1-worker-selftest.json` is emitted. No statement acceptance, proof, audit completion, or
theorem completion is claimed.
