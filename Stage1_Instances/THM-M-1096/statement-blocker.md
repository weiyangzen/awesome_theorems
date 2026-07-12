# Exact-statement gate: blocked

Item: `S56-M-1096-STATEMENT`  
Theorem: `THM-M-1096`  
Base revision: `67664ce109cd6d2cb390a1bab66d3f84f38a8e35`

## Decision

No exact Lean 4 target can be truthfully elaborated from the authoritative repository material.
The record supplies only "ergodicity of diffusion processes." The intake identifies Khasminskii's
1960 article by DOI, but no numbered theorem, page, definitions, hypotheses, or errata have been
inspected. Direct access to the publisher article and PDF returned an HTTP 403 HTML challenge, and
OpenAlex classifies the work as closed with no available full text.

The phrase describes several inequivalent claims. It does not decide between almost-sure time
averages, convergence in probability or distribution, transition-kernel convergence, existence or
uniqueness of an invariant measure, or stabilization of the parabolic Cauchy problem. Nor does it
fix the diffusion model, recurrence class, regularity and non-explosion assumptions, invariant
measure normalization, admissible observables, convergence topology, exceptional sets, or initial
state quantifiers. These choices change the proposition's domains, binders, hypotheses, and
conclusion.

Selecting a generic Birkhoff theorem, assuming ergodicity or the limit as structure data, choosing
a positive-recurrent specialization, or asserting an abstract diffusion interface would invent or
substitute mathematics. Therefore the first failed gate is `exact_source_statement`. There is no
canonical expression to elaborate, no meaningful minimal import set, and no valid removed-
hypothesis, changed-domain, binder-scope, or boundary mutation to run. Machine status remains `M4`;
statement acceptance and theorem completion are false.

## Validation record

Commands ran from this worker clone on 2026-07-12 (Asia/Shanghai). The existing `.lake` symlink and
pinned artifacts were read only; no update, build, clone, or fetch command was used.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1096` | 0 | rank 536, planned, legacy artifacts unaccepted, theorem incomplete |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `cd Formalizations/Lean && lake --version` | 0 | Lake `5.0.0-src+98dc76e` |
| `cd Formalizations/Lean && sha256sum lean-toolchain lake-manifest.json` | 0 | hashes recorded in `statement-blocker.json` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| repository `rg` search for Khasminskii, the paper title, and the repository gloss | 0 | only underspecified metadata and the existing intake were found; no exact source-frozen proposition or historical Lean target exists |
| pinned-mathlib `rg` search for diffusion-process and recurrent-diffusion/ergodicity terms | 1 | no matching Lean source; scoped negative search only, not anchor-audit completion |
| `curl -L --max-time 30 -s -o /tmp/khas.pdf -w '%{http_code} %{content_type} %{size_download}' 'https://epubs.siam.org/doi/pdf/10.1137/1105016'` | 0 | HTTP 403, `text/html`, 5495 bytes; no article text obtained |
| `curl -L --max-time 30 -s 'https://api.openalex.org/works/https://doi.org/10.1137/1105016'` | 0 | work `W1999897837`; closed access, `has_fulltext=false`, no PDF URL |

There is no applicable `lake env lean <canonical-statement>.lean` check. Creating a declaration
without the missing source statement would be fake statement evidence rather than the assigned
deliverable.

## Retry condition

An accountable reviewer must preserve and inspect an immutable primary-source edition, select an
exact theorem and page, audit its definitions, every hypothesis, translation differences, and
errata, and crosswalk each component to ordered Lean binders. A later statement run can then choose
minimal pinned imports, elaborate and serialize the exact expression, check alternate transports,
and execute all four required mutation classes.

This artifact records a blocker only. It does not accept the statement node, alter the execution
DAG, or claim audit or theorem completion. The phase is not genuinely self-tested, so no
`.stage1-worker-selftest.json` is emitted.
