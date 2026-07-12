# Exact-statement gate: blocked

Item: `S56-M-1290-STATEMENT`  
Theorem: `THM-M-1290`  
Base revision: `c198d8dd5bd64a4d487ed7455874705d67fd300f`

## Decision

The exact Lean 4 statement cannot be truthfully frozen from the currently available authoritative
material. The repository record gives only the name "Brezis-Nirenberg problem" and the gloss
"critical-growth nonlinear elliptic equation." The intake identifies Brezis and Nirenberg,
"Positive solutions of nonlinear elliptic equations involving critical Sobolev exponents,"
*Communications on Pure and Applied Mathematics* **36** (1983), 437-477, DOI
`10.1002/cpa.3160360405`, but correctly leaves the exact theorem variant and page open.

The bibliographic checks below confirm the article, authors, journal, issue, and page range. They do
not expose its theorem text: OpenAlex marks it closed with no full text, Semantic Scholar reports a
closed empty PDF URL, the Wiley PDF endpoint returns HTTP 403, and the Wiley text-mining endpoint
cannot be used without access credentials. Thus no inspected primary-source theorem fixes the
ordered premises and conclusion.

This matters because the label names a family of non-equivalent propositions. A source review must
choose, rather than conflate:

- existence versus nonexistence, or a precisely sourced conjunction;
- the `n >= 4` regime versus the exceptional `n = 3` regime and any ball-specific threshold;
- the exact bounded-domain regularity and any star-shaped hypothesis;
- open or closed bounds on `lambda` relative to the first Dirichlet eigenvalue;
- positive classical solutions versus nonzero, almost-everywhere-positive weak solutions;
- the normalization of the Laplacian, critical exponent, Sobolev space, trace, and eigenvalue.

Changing any of these changes the domain, binders, hypotheses, boundary cases, or conclusion.
Selecting a convenient general theorem, a ball case, or an abstract structure carrying the desired
existence result would broaden or substitute the unknown root. Consequently there is no honest
canonical Lean expression, minimal import set, expression fingerprint, checked alternate
transport, or removed-hypothesis/domain/binder-scope/boundary mutation suite. Machine state remains
`M4`; statement acceptance and theorem completion are false.

## Pinned environment and validation

Commands ran in this worker clone on 2026-07-12 (Asia/Shanghai). The existing `.lake` artifacts
were read only; no update, build, clone, or fetch was run.

- Lean toolchain: `leanprover/lean4:v4.29.0`; Lean 4.29.0 at commit
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
| `python3 scripts/stage1_target.py show THM-M-1290` | 0 | Rank 461, planned, legacy artifacts unaccepted, theorem incomplete |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean version and commit recorded above |
| `cd Formalizations/Lean && lake --version` | 0 | Lake version recorded above |
| `cd Formalizations/Lean && sha256sum lean-toolchain lake-manifest.json` | 0 | Produced the two hashes recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | Produced the pinned mathlib revision recorded above |
| repository `rg` search for the theorem name, article title, and critical-Sobolev phrases | 0 | Found underspecified metadata and general analysis infrastructure, but no source-frozen proposition for this target |
| Crossref query for DOI `10.1002/cpa.3160360405` | 0 | Confirmed the 1983 article and pages 437-477; supplied no theorem text |
| OpenAlex query for the DOI | 0 | Confirmed metadata; `is_oa=false`, `has_fulltext=false`, no PDF URL |
| Semantic Scholar query for the DOI | 0 | Confirmed metadata; `openAccessPdf.status=CLOSED` with an empty URL |
| Wiley PDF request | 22 | HTTP 403; no primary text obtained |

There is no applicable `lake env lean <target>.lean` command: an exact expression has not been
identified. Elaborating an invented interface or assuming the desired PDE conclusion would be fake
statement evidence, not the assigned deliverable.

## Retry condition

Retry after an accountable reviewer obtains an immutable primary-source copy, selects a pinpoint
theorem and page, checks surrounding definitions and errata, and crosswalks every dimension,
domain, parameter, positivity, solution-space, PDE, and boundary premise into ordered Lean binders.
The statement phase can then select the necessary pinned mathlib interfaces, minimize imports,
serialize the elaborated expression and environment, check alternate transports, and execute all
four required mutation classes.

This artifact records the first failed gate and does not complete the statement node, accept a
receipt, alter the execution DAG, or claim audit/theorem completion. No
`.stage1-worker-selftest.json` is emitted because the assigned phase is not genuinely self-tested.
