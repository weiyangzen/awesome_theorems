# Anchor audit

Item: `S56-M-1356-ANCHOR_AUDIT`. Discovery protocol frozen at 2026-07-13
03:02; audit cutoff 03:08 (`Asia/Shanghai`).

## Frozen discovery inventory

Before the bounded search, the inventory fixed this order: repo-local Lean;
pinned mathlib; public Lean 4 projects and indexes; statement collections; and
the already identified mathematical sources. The aliases were `Routh-Hurwitz`,
`Routh Hurwitz`, `RouthHurwitz`, `routh_hurwitz`, `Hurwitz matrix`,
`hurwitzMatrix`, `Hurwitz determinant`, `hurwitzDeterminant`, `Hurwitz
criterion`, `Hermite-Biehler`, `Lienard-Chipart`, and `stable polynomial`.
Local searches used `rg`/`git grep`; external searches used unauthenticated
GitHub repository and code APIs, Sourcegraph's public Lean index with forks and
archives included, and grep.app. Expected negative evidence was an exact
no-match exit or a timestamped API result; access failures were retained rather
than converted into absence claims.

The immutable local environment is repository commit
`7a489588a59dbd7cca44de7e3b8c3bafcb7448f5` (tree
`54d558bf8ed3ea71536ff6a7e6ac7ee67cccfe98`), Lean `v4.29.0` commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, and clean pinned mathlib commit
`8a178386ffc0f5fef0b77738bb5449d50efeea95` (tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`). No dependency was fetched,
installed, or mutated.

The captured discovery responses are dated, bounded evidence rather than
immutable source snapshots: no external candidate was found to resolve to a
revision. Their response hashes preserve the observed payloads; rerunning an
index may legitimately change trace metadata or results.

## Repo-local and pinned mathlib result

The complete repo-local Lean scan outside this target found no Routh-Hurwitz
proof, wrapper, or statement. The only `Hurwitz` hit was an unrelated Hurwitz
zeta module name. The canonical local declaration
`Stage1Instances.THM_M_1356.RouthHurwitzTarget` is an exact proposition
definition and has no proof body, so it remains statement evidence only.

The scan of all 7,871 pinned `Mathlib/**/*.lean` files found no declaration for
Routh-Hurwitz, a Hurwitz matrix or determinant criterion, Hermite-Biehler,
Lienard-Chipart, or stable-polynomial root/minor equivalence. Mathlib's
`docs/1000.yaml` contains only the title `Routh-Hurwitz theorem` under
`Q4455015`; at pinned blob `3e681315f501e3487e117071b1ec8710e7d95176`
that row has no module or declaration and is a wishlist/catalog entry, not a
formal candidate.

`AnchorAudit.lean` kernel-checks the nearest useful polynomial construction,
root transport, real-to-complex embedding, finite-index embedding, submatrix,
and determinant declarations. They support the target's interface but supply
neither implication of the criterion. In particular, generic
`Polynomial.IsRoot.map` and `Matrix.det` do not connect root real parts to
positivity of leading Hurwitz minors. They receive no terminal proof credit.

## External Lean 4 result

Sourcegraph queries covering all frozen name variants, with `lang:Lean`,
`fork:yes`, and `archived:yes`, completed with `matchCount=0`. Two final grouped
responses had SHA-256 values
`0e0a2b2b579f987073660c21ee2932f6273db5fdb23c0401c00558d073c35246`
and `4643b2d46e36e90582b985ccfae75cfa573f402243f9b56122678add9b0c6fd3`.
A broad `Hurwitz` search found only unrelated Riemann-Hurwitz, Radon-Hurwitz,
and Hurwitz-zeta material, so those were rejected by statement normalization.

GitHub repository-metadata searches for the quoted theorem name, spaced name,
Hurwitz matrix, and `RouthHurwitz language:Lean` each returned
`total_count=0` and `incomplete_results=false`; the captured quoted-name
response SHA-256 is
`08c082fdf7ca87ba911a2aabb0f0cf2d3e482a6feeaac9713e4578c20b2600b2`.
GitHub code search was unavailable without authentication/rate allowance, and
grep.app returned a security checkpoint instead of a search result. Neither
blocked lane is counted as negative evidence. These bounded public-index
results do not establish global discovery saturation.

No external Lean 4 repository, immutable revision, module, declaration, or
terminal proof body was discovered. Consequently there is no candidate whose
dependency closure, axioms, placeholders, license, toolchain, or adapter could
be checked, and no moving dependency was fetched merely to manufacture an
immutable pin.

## Mathematical-source boundary and classification

Barkovsky, arXiv:0802.1805v1, printed pages 6 and 18-19, matches the frozen
strict-stability and finite leading-minor formulation. Hurwitz's 1895 pages
273-274 corroborate it. Holtz, arXiv:math/0512591v1, uses ascending
coefficients and an infinite-matrix positive factorization, so it is a useful
human-source route but not an exact Lean candidate. These publications are
mathematical sources, not kernel proof bodies.

The root stays `[H1, M3, R4]`: the exact Lean interface exists, but no local,
pinned-mathlib, or external Lean 4 closure is known. The next phase must model
the missing proof rather than treating generic polynomial/matrix APIs or a
catalog title as terminal anchors. Reopen the candidate inventory when a
concrete Lean 4 proof appears at an immutable revision; acceptance would then
require exact-type transports, pinned integration, transitive parser-aware
placeholder/axiom/unsafe review, and a local kernel check.

This self-tested phase closes only the bounded anchor inventory pending master
acceptance. It does not claim exhaustive discovery, `H0`, proof closure,
obligation-tree closure, `R0`, audit completion, or theorem completion.
