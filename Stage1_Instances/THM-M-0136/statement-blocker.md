# Statement gate blocker

Item: `S56-M-0136-STATEMENT`  
Theorem: `THM-M-0136`  
Verdict: blocked; no exact canonical Lean target is claimed.

## First failed gate

The accepted intake and source crosswalk do not identify a proposition that can be frozen. The
repository supplies only the subject label "Kac-Moody algebras" and the gloss "classification of
infinite-dimensional Lie algebras." It supplies no primary-source theorem/page, exact
transcription, coefficient field, index-set restrictions, Cartan-matrix conditions, equivalence
notion, ordered binders, or conclusion. In particular, it does not decide whether the intended
result is a construction or presentation theorem, the finite/affine/indefinite classification of
generalized Cartan matrices, a classification preserving a Cartan subalgebra or distinguished
generators, or an assertion about abstract Lie algebra isomorphisms. These are inequivalent claims.

The provisional intake candidate asks whether an equivalence of Serre-constructed Lie algebras
recovers symmetrizable indecomposable generalized Cartan matrices up to reindexing. That candidate
is explicitly unsourced. Selecting it as canonical would invent mathematics absent from the
manifest rather than elaborate the exact target. It also leaves essential choices open, including
the coefficient domain and which structure the Lie equivalence must preserve.

The legacy declaration
`AwesomeTheorems.Stage1.S1_M_052.StatementShape` elaborates in the pinned environment, but it does
not resolve the blocker. Its own documentation calls it a candidate and allows an arbitrary
commutative coefficient ring and an abstract `LieEquiv`; no primary-source crosswalk establishes
that this is the repository claim. Its two imports therefore cannot be certified as the minimal
imports of an exact target. The checked Serre-construction and finite-root-system declarations in
that module are adjacent boundaries, not alternate encodings of a classification theorem.

Consequently the exact human claim, canonical Lean expression, expression hash, meaningful
removed-hypothesis/domain/binder-scope/boundary mutations, and checked alternate transports
required by rev-5.6 section 5.1 cannot truthfully be produced. Machine status remains `M4`, and no
statement acceptance, proof credit, audit completion, or theorem completion is claimed.

## Environment fingerprint

- Repository base revision: `de9509a9b807a45e9fb1511465a7b957788afc54`.
- Validation date: 2026-07-12.
- Lean toolchain: `leanprover/lean4:v4.29.0`; Lean `4.29.0`, commit
  `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- mathlib Lake pin and checked revision:
  `8a178386ffc0f5fef0b77738bb5449d50efeea95`.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- Lake manifest SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.
- Legacy module SHA-256:
  `9bcc528e6ebe745ed1a2934441fc0bfe89624d9c83d5d00dabac44ce7511620e`.

## Validation evidence

All commands ran in this worker clone. The Lean commands used the existing pinned `.lake`
artifacts. No update, build, fetch, clone, or other dependency mutation was run.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | standard projection passed: 15 assurance groups and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | manifest passed: 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0136` | 0 | rank 52, planned, legacy artifacts unaccepted, theorem incomplete |
| `cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_052.lean` | 0 | legacy candidate and adjacent boundaries elaborated; this is negative boundary evidence, not exact-statement credit |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_052.lean` | 0 | hashes match the environment fingerprint above |
| repo-local `rg` search for Kac-Moody, generalized-Cartan, and classification terms outside this dossier and `.lake` | 0 | found the legacy candidate and neighboring coarse artifacts, but no exact primary-source transcription |

## Retry condition

The authoritative lane must identify an immutable primary source and pinpoint one theorem with its
exact assumptions, conclusion, equivalence structure, conventions, branch restrictions, and errata
status. It must explicitly decide whether Cartan data, generators, grading, or triangular
decomposition is preserved. Only then can this node encode the claim, determine minimal imports,
fingerprint the elaborated expression, and run the four required mutation classes.

Because the assigned exact-statement phase is blocked rather than genuinely self-tested to its
completion gate, no `.stage1-worker-selftest.json` is emitted.
