# Exact-statement gate: blocked

Item: `S56-M-1151-STATEMENT`  
Theorem: `THM-M-1151`  
Base revision: `4fe80223f9834108bda5b71558952837bf8bdba2`

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the repository source record. The
entire mathematical claim is `混合边值问题` ("mixed boundary-value problem") under the title
"Robin problem". The record gives Victor Robin and 1886 as metadata, but supplies no bibliography,
edition, theorem/page, exact wording, or errata review. The `已验证` label is untrusted screening
metadata under rev-5.6, not statement or kernel evidence.

This wording does not identify a proposition. In particular, it leaves unresolved:

- the differential operator, equation, dimension, scalar field, and domain;
- the domain and boundary regularity assumptions and the solution concept;
- whether "mixed" denotes a Robin linear combination on one boundary, distinct condition types
  on separate boundary pieces, or another convention;
- the Robin coefficient, forcing and boundary data, sign convention, and function spaces;
- the compatibility, ellipticity, boundedness, positivity, or coercivity hypotheses;
- whether the conclusion is existence, uniqueness, an estimate, regularity, or a combination;
- the treatment of zero coefficients, empty boundary pieces, disconnected domains, and the pure
  Dirichlet or Neumann limiting cases.

These choices yield inequivalent theorems. Selecting a conventional Laplace or elliptic problem
such as `-Delta u = f` with `partial_n u + alpha * u = g` would therefore substitute newly chosen
mathematics for the received claim. A generic record whose fields assume the desired analytic
facts would likewise be only an interface, not the exact theorem.

Section 5 consequently fails at canonical human-claim identity. There is no honest canonical Lean
expression, minimal import set, expression hash, checked alternate encoding, or meaningful suite
of removed-hypothesis, changed-domain, binder-scope, and boundary-case mutations. No Lean
declaration, axiom, placeholder, weakened special case, or broadened theorem was introduced.
Machine debt remains `M4`; statement acceptance, audit completion, and theorem completion remain
false. In addition, the intake task is only provisional (`[_]`) and has no master-accepted state in
the dossier, so this node cannot receive dependency-legal master acceptance in this worker lane.

## Repository and pinned-environment inspection

Repository-wide searches for the Chinese and English title, target ID, and Robin/mixed-boundary
phrases found only the metadata and accepted-intake-boundary records for this target; no source-
frozen theorem or Lean candidate was identified. A search of the pinned local mathlib sources for
`Robin boundary`, `Robin problem`, `Robin condition`, and `mixed boundary` returned no matches.
This negative search does not prove that no formalization exists; it records only the narrow local
inspection appropriate before the later anchor-audit phase.

Validation ran on 2026-07-12 (Asia/Shanghai) inside this worker clone using the existing canonical
Lake artifacts read-only. No `lake update`, build, dependency clone/fetch, or `.lake` mutation was
performed.

- Toolchain: `leanprover/lean4:v4.29.0`; Lean 4.29.0, commit
  `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- Lake: `5.0.0-src+98dc76e`.
- Pinned mathlib: `8a178386ffc0f5fef0b77738bb5449d50efeea95`.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1151` | 0 | rank 356, planned, no accepted legacy artifact, theorem incomplete |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean version and commit recorded above |
| `cd Formalizations/Lean && lake --version` | 0 | Lake version recorded above |
| `cd Formalizations/Lean && sha256sum lean-toolchain lake-manifest.json` | 0 | produced the two hashes recorded above |
| `cd Formalizations/Lean && git -C .lake/packages/mathlib rev-parse HEAD` | 0 | produced the pinned mathlib revision above |
| repository search for `Robin问题`, `Robin problem`, `THM-M-1151`, and related boundary phrases | 0 | only underspecified metadata and this dossier; no exact proposition |
| pinned-mathlib search for Robin/mixed-boundary phrases | 1 | no matching Lean source; no candidate declaration identified |

## Required unblock

An accountable source reviewer must identify an immutable primary-source edition and exact
theorem/page, check relevant errata, and freeze every operator, domain, boundary, coefficient,
data, solution-space, hypothesis, conclusion, and degenerate-case choice listed above. The intake
node must also receive master acceptance. A later statement worker can then encode the claim
without substitution, minimize pinned imports, serialize the elaborated expression and environment
fingerprint, check alternate encodings, and run all four required mutation classes.

First failed substantive statement gate: exact source-statement identity. The assigned phase is
not genuinely self-tested or complete, so `.stage1-worker-selftest.json` is intentionally absent.
