# Exact-statement gate: blocked

Item: `S56-M-1330-STATEMENT`  
Theorem: `THM-M-1330`  
Base revision: `b1720c87b4674563b995fad5e6dd9828348b7230`

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the available authoritative material.
The repository source wording is only `负曲率流形的谱` (spectrum of negatively curved
manifolds). The accepted intake dependency identifies Harold Donnelly and Peter Li's 1979 paper,
but deliberately leaves its numbered theorem, page, assumptions, and operator conventions open.
Its familiar summary, that sectional curvature tending to minus infinity implies pure point or
discrete Laplace spectrum, is explicitly provisional rather than a source transcription.

Crossref corroborates the authors, title, journal, volume, issue, date, DOI, and Project Euclid
location. It contains no theorem text. The Project Euclid article and download endpoints returned
an access-control HTML response rather than the paper. The download response was 1164 bytes with
SHA-256 `3f6708f4ad27d212928037934fa1b1c6e29272da2a2c483823f1f4f53df5462c`;
it is not primary-source evidence and was not added to the dossier.

The missing choices alter the proposition rather than merely its notation:

- manifold dimension, connectedness, boundary, smoothness, and completeness;
- the quantifiers and uniformity in "sectional curvature tends to minus infinity at infinity";
- the Laplacian sign, Hilbert space, operator domain, and self-adjoint realization;
- whether "pure point" means compact resolvent, isolated finite-multiplicity eigenvalues, a complete
  eigenbasis, or another source-specific formulation;
- any multiplicity, accumulation, exceptional-set, or end hypotheses in the actual theorem.

Selecting conventional answers would manufacture a nearby theorem. Encoding the conclusion as an
opaque predicate or assumption would instead be a placeholder. Both are forbidden. Consequently
there is no canonical expression on which minimal imports, an expression hash, checked transports,
or meaningful removed-hypothesis, changed-domain, changed-binder-scope, and boundary mutations can
be established. Machine debt remains `M4`; no statement or theorem completion is claimed.

## Lean boundary

The existing pinned Lean environment is usable, but repository search found no historical Lean
candidate for this target. A pinned-mathlib source search under `sectional curvature`,
`Laplace-Beltrami`, `pure point spectrum`, `discrete spectrum`, and `compact resolvent` found no
matching API. This is limited feasibility evidence, not an anchor audit and not a replacement for
the missing source statement. There is no applicable `lake env lean <canonical-target>.lean`
command because the proposition that file would contain has not been identified.

## Validation record

Commands ran from this worker clone on 2026-07-12 (Asia/Shanghai). The canonical `.lake` artifacts
were read only; no update, build, clone, fetch, or dependency mutation was run.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1330` | 0 | rank 492, planned, legacy artifacts unaccepted, theorem incomplete |
| repository `rg` search for the theorem ID, name, paper title, and discovery wording | 0 | only underspecified catalogue metadata and this intake dossier; no exact proposition or Lean candidate |
| Crossref DOI API query | 0 | bibliographic metadata and Project Euclid URL found; no theorem statement |
| Project Euclid article/download retrieval | 0 transport exit | returned a 1164-byte `text/html` access-control page, not the paper |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `cd Formalizations/Lean && lake --version` | 0 | Lake `5.0.0-src+98dc76e` |
| `cd Formalizations/Lean && sha256sum lean-toolchain lake-manifest.json` | 0 | hashes `651c8a...1d2` and `321626...d81` recorded in the JSON blocker |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| pinned-mathlib `rg` API search | 1 | no matches for the five theorem-specific geometry/spectral terms |

## Retry condition

An accountable reviewer must preserve a lawful immutable primary-source copy, record its content
hash, transcribe the exact numbered theorem and relevant definitions with page locators, audit
errata, and independently approve the crosswalk. The statement phase can then freeze all ordered
binders and conventions, implement the real Lean substrate, minimize imports, serialize and hash
the elaborated expression, check alternate transports, and run all four mutation classes.

This records the first failed gate and does not complete the statement node or any later node. The
assigned phase is not genuinely self-tested, so no `.stage1-worker-selftest.json` is emitted.
