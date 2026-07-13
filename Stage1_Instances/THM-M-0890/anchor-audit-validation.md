# Anchor-audit validation

Item: `S56-M-0890-ANCHOR_AUDIT`

Base revision: `a1c9974d7fb28cd680e6494b968544bf801a93a2` (tree
`1fa287bc821355aca2ca9e3ce107830a3eb58e64`). Validation date: 2026-07-13
(`Asia/Shanghai`).

## Result

The exact positive-degree regular-graph proposition elaborates, but the bounded immutable audit
found no repo-local, pinned-mathlib, or external Lean 4 proof body for Hoffman's independence-number
ratio bound. Pinned mathlib provides useful independent-set, regular adjacency-matrix, Hermitian
eigenvalue, and positive-semidefinite interfaces only. Those interfaces support a future proof; they
do not state the quotient inequality.

Atlas is genuinely spectral-graph-adjacent at immutable commit `34ffed396...`. Its expander module
defines ordered adjacency eigenvalues and states second-largest-eigenvalue expansion estimates, but
those estimates contain `sorry` and do not match the least-eigenvalue independence bound. The only
declaration named `matching_ratio_bound` concerns counts of partial bipartite matchings, is also a
placeholder, and is unrelated. The immutable Formal Conjectures tree contains adjacent
`Independence`, `Cvetkovic`, and `LovaszTheta` definitions, but no Hoffman ratio-bound declaration.

All five frozen candidate groups are classified. No eligible external integration task exists; the
remaining machine debt is a real proof-formalization obligation. Root status stays
`[H1, M3, R4]`. This is a bounded node self-test pending master acceptance, not an exhaustive-public-
search claim, full audit completion, or theorem completion.

## Immutable inventory

- Repository base: commit `a1c9974d...`, tree `1fa287bc...`.
- Lean: `4.29.0`, commit `98dc76e3...`; Lake: `5.0.0-src+98dc76e`.
- Mathlib: commit `8a178386...`, tree `bdc39a31...`; 8,374 tracked Lean files; clean
  dependency worktree; Apache-2.0.
- `flt-regular`: commit `56161b6e...`, tree `32c9eace...`; 32 tracked Lean files; clean.
- Atlas: commit `34ffed39...`, tree `c12fe231...`; complete 2,860-entry tree response; Lean
  `4.29.0`; same mathlib pin; CC BY-NC 4.0 plus a no-training rider.
- Formal Conjectures: commit `b2e608fc...`, tree `40d17fde...`; complete 1,204-entry tree
  response; Lean `4.27.0`; mathlib `a3a10db0...`; Apache-2.0.

The automation-provided canonical `Formalizations/Lean/.lake` symlink and already materialized
packages were used read-only. No `lake update`, `lake build`, dependency clone/fetch, checkout, or
other `.lake` mutation was performed. External archives and index responses in `/tmp` were
discovery evidence only, not installed dependencies.

## Commands and exact outcomes

Commands ran from the repository root unless another working directory is shown.

| Command | Exit | Outcome |
|---|---:|---|
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base commit/tree `a1c9974d...` / `1fa287bc...` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and `status --short` | 0 | pinned commit/tree `8a178386...` / `bdc39a31...`; empty status |
| `git -C Formalizations/Lean/.lake/packages/flt-regular rev-parse HEAD 'HEAD^{tree}'` and `status --short` | 0 | pinned commit/tree `56161b6e...` / `32c9eace...`; empty status |
| complete repo-local, 8,374-file mathlib, 32-file `flt-regular`, and locally stored mathlib history/ref searches for aliases and independence/eigenvalue co-occurrences | 1 expected / 0 | no exact or equivalent terminal theorem; only unrelated local/history hits; result hashes recorded in `anchor-audit.json` |
| immutable mathlib source inspection | 0 | support APIs identified in `Finite.lean:304`, `Clique.lean:927`, `AdjMatrix.lean:311`, `LapMatrix.lean:51`, `Spectrum.lean:56`, and both matrix `PosDef.lean` modules; no ratio-bound declaration |
| complete Atlas tree and source inspection at `34ffed396f376454c1a9b297f3fd74c5c801fb50` | 0 | 2,860 entries, tree response SHA-256 `3a6c23e...`; adjacent `Expanders.lean` SHA-256 `3b29aa...`; no matching theorem; adjacent statements use placeholders |
| complete Formal Conjectures tree/source inspection at `b2e608fc52d765510915a244bb69b1a2741acc3c` | 0 | 1,204 entries, tree response SHA-256 `76fa3f96...`; no Hoffman/ratio path; three adjacent files classified, none a terminal candidate |
| Sourcegraph exact aliases and independence/eigenvalue query families | 0 | exact/related queries completed with zero matches; broad `Hoffman` returned only three Atlas Hoffman-Wielandt occurrences; response hashes recorded in `anchor-audit.json` |
| GitHub REST repository searches | 0 | three bounded queries returned `total_count=0`, `incomplete_results=false`; repository metadata only |
| GitHub REST code search | blocked | anonymous API rate limit; response SHA-256 `1db366...`; no negative evidence credited |
| grep.app queries | blocked | Vercel Security Checkpoint; response hashes recorded; no negative evidence credited |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0890/AnchorAudit.lean)` | 0 | 12 pinned support declarations elaborated; eight axiom reports contained only `propext`, `Classical.choice`, and `Quot.sound`; stdout SHA-256 `a6dd4cce...` |

Final packet-level JSON, checker, prohibited-construct, and whitespace checks are recorded by the
node receipt and root worker packet, which are maintained separately from this validation note.

## Status boundary

No exact external declaration, wrapper, or terminal body was found, so nothing can honestly be
classified `M1` or `M0-*`. A later discovery reopens the inventory and must be frozen to an
immutable revision, type-compared against the positive-degree target, locally integrated, and
audited for dependencies, placeholders, axioms, trust, and licensing before receiving proof credit.

The obligation registry, proof architecture, proof body, composition, full provenance/TCB closure,
primary-source `H0`, independently reviewed `R0`, hermetic and independent validation,
deterministic release evidence, `AUDIT-Z`, master acceptance, and theorem completion remain open.
