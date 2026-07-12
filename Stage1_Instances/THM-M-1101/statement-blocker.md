# THM-M-1101 statement-phase blocker

## Decision

`S56-M-1101-STATEMENT` is blocked and is not self-tested as a completed
statement phase. No canonical Lean target has been created, and no statement,
proof, audit completion, or theorem completion is claimed.

The repository claim is only "the basic algorithm of MCMC". It does not select
a truth-valued result from Hastings (1970), and the accepted intake explicitly
leaves open the source equation/result, target and proposal representation,
support and zero-ratio convention, rejection mass, and conclusion. Choosing
detailed balance, invariance, convergence, or estimator correctness without
inspecting the primary source would broaden or substitute the unidentified
claim. A generic theorem saying that an already reversible kernel is invariant
would also assume away the Metropolis-Hastings construction.

## Primary-source access check

The publisher deposit identifies the version-of-record article as W. K.
Hastings, "Monte Carlo Sampling Methods Using Markov Chains and Their
Applications", *Biometrika* 57(1) (1970), pages 97-109, DOI
`10.1093/biomet/57.1.97`. The publisher PDF endpoint returned an HTTP 403 HTML
page in this environment rather than the article. OpenAlex reports the work as
closed access, with no repository full text. Semantic Scholar likewise reports
`openAccessPdf.status = CLOSED`. Consequently the exact numbered equation or
result, its ordered assumptions, boundary conventions, proof context, and
errata could not be inspected here.

This is the first failed rev-5.6 gate: exact source proposition selection. The
next valid action is to provide or inspect a stable copy of Hastings (1970),
record the exact section/equation/page and assumptions, and obtain the required
source-mapping review. Only then can the statement phase freeze and elaborate
the corresponding Lean expression.

## Validation record

Commands were run in the worker clone on 2026-07-12 at base revision
`c83a05a429c195d51008196099c68c42b7fd9ec1`. The repository-provided untracked
`Formalizations/Lean/.lake` link was not modified.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Standard check passed: 15 assurance groups and 1546 uniform-L0 Lean 4 targets. |
| `python3 scripts/stage1_target.py check` | 0 | Manifest check passed: 1546 unique targets, ranks 1..1546, all L0/rework-required. |
| `python3 scripts/stage1_target.py show THM-M-1101` | 0 | Confirmed rank 541, planned lifecycle, unaccepted legacy artifacts, and `theorem_complete: false`. |
| `curl -L --max-time 30 -o /tmp/hastings1970.pdf -w '%{http_code} %{content_type} %{size_download}' 'https://academic.oup.com/biomet/article-pdf/57/1/97/23940249/57-1-97.pdf'` | 0 | Transfer completed but response was `403 text/html; charset=UTF-8 5548`, not a PDF. |
| `curl -L --max-time 20 -s 'https://api.openalex.org/works/https://doi.org/10.1093/biomet/57.1.97'` | 0 | Metadata reports `is_oa: false`, `oa_status: closed`, and no repository full text. |
| `curl -L --max-time 20 -s 'https://api.semanticscholar.org/graph/v1/paper/DOI:10.1093/biomet/57.1.97?fields=title,year,openAccessPdf,url,externalIds'` | 0 | Metadata identifies the paper and reports the open-access PDF status as `CLOSED`. |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`; the pinned elaborator is available, but there is no exact target to elaborate. |

Status boundary: this artifact records a source-selection blocker only. The
assigned phase remains open, so no `.stage1-worker-selftest.json` is emitted.
