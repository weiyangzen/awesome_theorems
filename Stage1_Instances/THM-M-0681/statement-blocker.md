# Exact-statement gate: blocked

Item: `S56-M-0681-STATEMENT`  
Theorem: `THM-M-0681`  
Base revision: `dd6b82c28776722313b4c880fe7f45e1135d2b09`

## Decision

The exact Lean 4 target cannot be truthfully selected or elaborated from the authoritative
repository material. Its complete mathematical wording is `微分闭域的公理化`
("axiomatization of differentially closed fields"), attributed to Abraham Robinson in 1959.
This names a theorem family rather than one proposition. It does not identify the original
Robinson axiom scheme, a later Blum-style one-variable differential-polynomial criterion, an
existential-closedness characterization, or an equivalence between two of these presentations.

Those alternatives require materially different domains, ordered binders, side conditions, and
conclusions. In particular, the record does not freeze the differential-polynomial syntax, number
of differential indeterminates, rankings and orders, initials or separants, equations and
inequations, extension embeddings, or the precise semantics of existential closedness. Choosing a
familiar modern `DCF_0` criterion would substitute an unselected later formulation. Defining an
opaque `DifferentiallyClosed` predicate by that criterion and proving a reflexive equivalence would
instead assume away the requested axiomatization.

The intake identifies Robinson's 1959 paper only as a discovery anchor. The dossier contains no
accepted immutable edition, theorem/page pinpoint, exact transcription, errata review,
binder-by-binder assumption crosswalk, or independently checked bridge from Robinson's formulation
to a modern criterion. Therefore the section 5 statement-identity gate fails before a canonical
human proposition, exact Lean expression, expression hash, checked alternate transport, or
meaningful removed-hypothesis, changed-domain, binder-scope, and boundary mutations can be frozen.

## Pinned Lean boundary

`IntakeProbe.lean` uses the single direct import
`Mathlib.FieldTheory.Differential.Basic`. With the pinned environment it elaborates only the
independent substrate `Differential`, `Differential.deriv`, `DifferentialAlgebra`, `Derivation`, and
`CharZero`. A case-insensitive search of pinned mathlib found no occurrence of "differentially
closed", "differential polynomial", or `DCF` and hence no theorem-specific target or
differential-polynomial interface. The probe declares no theorem, axiom, proxy predicate, or proof,
so it receives no exact-statement credit.

The reused environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. The `lean-toolchain` and `lake-manifest.json` SHA-256
values are respectively `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`
and `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`. The existing pinned
`.lake` artifacts were reused read-only; no update, build, clone, or fetch was performed.

## Validation evidence

Commands ran from this worker clone on 2026-07-12 (Asia/Shanghai).

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0681` | 0 | rank 722, planned, legacy artifacts unaccepted, theorem incomplete |
| `rg` inspection of the repository source rows | 0 | located only the short wording, Robinson attribution, 1959 date, and untrusted `已验证` label |
| pinned-mathlib `rg` search for differential closedness, differential polynomials, and `DCF` | 0 | no matching interface or declaration |
| `cd Formalizations/Lean && lake env lean --version && lake --version && sha256sum lean-toolchain lake-manifest.json` | 0 | produced the pinned versions and hashes recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | produced the pinned mathlib revision recorded above |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0681/IntakeProbe.lean` | 0 | all five substrate declarations elaborated and printed their types |

## Gate result

First failed gate: exact canonical-claim/source identity, before Lean target elaboration. Machine
status remains `M4`; no statement acceptance, proof credit, audit completion, or theorem completion
is claimed. Retry requires an accountable source reviewer to pin and inspect one exact primary
formulation, transcribe it, freeze every convention and side condition above, and approve its
crosswalk to the repository claim. Only then can a statement run implement the missing
differential-polynomial and existential-closedness surfaces, minimize imports, fingerprint the
exact expression, compile any credited transport, and run structural mutations.

Because the assigned statement phase is blocked rather than self-tested complete, no
`.stage1-worker-selftest.json` is emitted.
