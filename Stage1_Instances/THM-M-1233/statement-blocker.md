# Exact-statement gate: blocked

Item: `S56-M-1233-STATEMENT`  
Theorem: `THM-M-1233`  
Base revision: `854537bcbb10ad4c68b5a61f06171fffcec64961`

## Decision

The exact Lean 4 target cannot yet be truthfully elaborated. The intake identifies the original
Beale-Kato-Majda paper and its whole-space, three-dimensional incompressible-Euler scope, but the
repository does not contain a pinned copy or exact transcription of Theorem 1. A direct retrieval
attempt on 2026-07-12 reached the publisher's bot-challenge HTML rather than the paper. Bibliographic
APIs confirm the DOI, title, journal, volume, issue, and pages, but report that the full text is
closed; they do not expose the theorem statement.

This missing source text is material. The current intake deliberately leaves unresolved:

- the exact Sobolev regularity index and all decay/integrability conditions on the initial data;
- the paper's precise solution class and the interval on which its regularity is asserted;
- whether the root is phrased as finite-time breakdown, continuation, or both, and the exact
  quantifier order connecting a maximal time to the vorticity integral;
- the maximum-norm convention for vorticity and the endpoint/improper-integral convention;
- the hypotheses under which the continuation and breakdown formulations are equivalent.

Choosing values for these fields from a modern textbook formulation would substitute a nearby
theorem. Encoding them as unconstrained predicate parameters would only elaborate an assumed
interface, not the exact BKM claim. Consequently no `Statement.lean`, declaration/expression hash,
checked alternate-form transport, or mutation suite is emitted. Machine state remains `M4`; the
statement phase and theorem completion remain false. No `sorry`, axiom, placeholder, weakened
special case, or broadened target was introduced.

## Pinned environment and search

- Validation date: 2026-07-12 (Asia/Shanghai).
- Lean toolchain: `leanprover/lean4:v4.29.0`; Lean 4.29.0, commit
  `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- Lake: `5.0.0-src+98dc76e`.
- Pinned mathlib revision: `8a178386ffc0f5fef0b77738bb5449d50efeea95`.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.
- Primary bibliographic identity: J. T. Beale, T. Kato, A. Majda, *Remarks on the breakdown of
  smooth solutions for the 3-D Euler equations*, Communications in Mathematical Physics 94 (1984),
  no. 1, 61-66, DOI `10.1007/BF01212349`.

Commands ran inside this worker clone. Existing `.lake` artifacts were read only; no update, build,
clone, or fetch command was used.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1233` | 0 | rank 418, planned, legacy artifacts unaccepted, theorem incomplete |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean version and commit recorded above |
| `cd Formalizations/Lean && lake --version` | 0 | Lake version recorded above |
| `cd Formalizations/Lean && sha256sum lean-toolchain lake-manifest.json` | 0 | produced the two hashes recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | produced the pinned mathlib revision recorded above |
| `cd Formalizations/Lean && rg -n -i 'Beale.Kato\|Kato.Majda\|vorticity\|incompressible Euler\|Euler equations\|EulerEquation' .lake/packages/mathlib/Mathlib .lake/packages/mathlib/Archive` | 1 | no BKM or incompressible-Euler theorem API found (`rg` exit 1 means no match) |
| `rg -n -i 'Beale.Kato\|Kato.Majda\|vorticity\|incompressible Euler\|Euler equations' --glob '!Stage1_Instances/THM-M-1233/**' ../..` | 0 | only metadata and a distinct two-dimensional Yudovich formalization found; no exact BKM proposition |
| `curl -L --fail --max-time 30 -o /tmp/bkm.pdf <Project-Euclid-DOI-PDF-URL> && file /tmp/bkm.pdf` | 0 | returned a 1050-byte HTML bot-challenge, not a PDF; therefore it is not source evidence |
| `curl -L --fail --max-time 30 'https://api.openalex.org/works/https://doi.org/10.1007/BF01212349'` | 0 | confirmed the bibliographic record and pages 61-66; reported closed access and no full-text URL |
| `curl -L --fail --max-time 30 'https://api.semanticscholar.org/graph/v1/paper/DOI:10.1007/BF01212349?fields=title,openAccessPdf,externalIds'` | 0 | confirmed the bibliographic identity; reported `openAccessPdf.status = CLOSED` |
| `git diff --check -- Stage1_Instances/THM-M-1233` | 0 | no whitespace errors in the owned artifact |

There is no applicable `lake env lean <target>.lean` check because the source-frozen expression does
not exist. Elaborating a guessed regularity class or an abstract implication would create fake
statement evidence rather than satisfy the assigned deliverable.

## Retry condition

An accountable source review must provide an immutable copy of the original paper, record its hash,
and transcribe Theorem 1 with its preceding definitions and assumptions. The review must freeze the
regularity index, data and solution spaces, maximal-time semantics, vorticity norm, integral endpoint,
and logical direction, and dispose of corrections or errata. A later statement run can then encode
those exact fields, minimize pinned imports, preserve the elaborated expression and environment
fingerprints, compile checked transports, and run all four structural mutation tests.

The assigned phase is not genuinely self-tested to its completion gate, so no
`.stage1-worker-selftest.json` is emitted.
