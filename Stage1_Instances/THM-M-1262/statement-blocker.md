# Exact-statement gate: blocked

Item: `S56-M-1262-STATEMENT`  
Theorem: `THM-M-1262`  
Base revision: `9144fc9aa3522671a4cda7de9d460d01f382367a`

## Decision

No exact Lean 4 target can be truthfully elaborated from the authoritative repository record. The
record gives only the field name "microlocal analysis", attributes it to Lars Hormander in the
1970s, and glosses it as "local and frequency analysis of PDEs". It supplies no proposition,
primary-source edition, theorem number, page, assumptions, quantifiers, or conclusion. The accepted
intake therefore correctly keeps `canonical_claim` null and classifies statement selection as the
first open cut.

The label covers inequivalent theorem families, including smoothness characterized by an empty
wavefront set, wavefront-set functoriality, microlocal elliptic regularity, and statements about
pseudodifferential operators. Choosing any one of them would require inventing at least the
following source information:

- the base space (Euclidean open set or manifold), scalar field, and distribution space;
- the cotangent/frequency space and deleted-zero-section convention;
- the definition and normalization of wavefront set or singular support;
- any differential or pseudodifferential operator and its symbol class;
- ellipticity, proper-support, regularity, or characteristic-set hypotheses;
- binder order, boundary and degenerate cases, and the exact equality or inclusion concluded.

These choices change the domains, hypotheses, and conclusion, so a generic abstract record, an
assumed target predicate, a convenient Fourier theorem, or one selected candidate family would be
a broadened or substituted theorem. No such declaration, axiom, placeholder, or weakened special
case was introduced.

The statement gate consequently fails before minimal imports, a canonical expression hash,
checked alternate transports, or meaningful removed-hypothesis, changed-domain, binder-scope, and
boundary mutations can be produced. Machine state remains `M4`; no statement acceptance, proof
credit, audit completion, or theorem completion is claimed.

## Pinned environment and evidence

Commands ran in this worker clone on 2026-07-12 (Asia/Shanghai). The canonical `.lake` directory
was used read-only; no update, build, clone, or fetch was run.

- Lean toolchain: `leanprover/lean4:v4.29.0`; Lean 4.29.0, commit
  `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- Lake: `5.0.0-src+98dc76e`.
- Pinned mathlib revision: `8a178386ffc0f5fef0b77738bb5449d50efeea95`.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1262` | 0 | Rank 439, planned, legacy artifacts unaccepted, theorem incomplete |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0 at the commit recorded above |
| `cd Formalizations/Lean && lake --version` | 0 | Lake version recorded above |
| `cd Formalizations/Lean && sha256sum lean-toolchain lake-manifest.json` | 0 | Produced the two hashes recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | Produced the pinned mathlib revision recorded above |
| repository `rg` search for the title and English/Chinese gloss | 0 | Found only underspecified catalog metadata and this intake dossier; no source-frozen proposition |
| pinned-mathlib `rg` search for microlocal, wavefront, pseudodifferential, and singular-support terms | 1 | No matching Lean source declaration (`rg` exit 1 means no match) |

There is no applicable `lake env lean <target>.lean` command: no exact proposition exists to put in
a target file. Elaborating a fabricated interface would be fake statement evidence rather than the
assigned deliverable.

## Retry condition

An accountable source review must select an immutable primary-source edition and exact
theorem/page, quote or transcribe the proposition and definitions, inspect errata, and justify why
that theorem rather than the other microlocal-analysis families is the intended catalog claim. It
must freeze every domain, convention, hypothesis, binder, and boundary case listed above. A later
statement run can then encode that claim, minimize pinned imports, preserve its elaborated
expression and environment fingerprint, add checked transports, and run all four required mutation
classes.

The assigned phase is not genuinely self-tested to its completion gate, so no
`.stage1-worker-selftest.json` is emitted.
