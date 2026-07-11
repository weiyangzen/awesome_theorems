# THM-M-0401 rev-5.6 statement

Status: `planned`, `L0 / rework_required`. `Statement.lean` freezes and elaborates the exact product-form claim using the pinned Lean 4.29.0 environment. It does not prove Schmidt's theorem or claim source, audit, or release acceptance.

## Scope Map

The selected human claim is Schmidt's simultaneous approximation theorem in product form. For a positive dimension `n`, algebraic reals `alpha_i`, and linear independence of `1, alpha_0, ..., alpha_(n-1)` over `Q`, the positive denominators `q` for which

`product_i ||q * alpha_i|| < q ^ (-1 - epsilon)`

are finite for every positive `epsilon`. Here `||x||` means distance to the nearest integer.

Included: real algebraic inputs, simultaneous rational approximation with one positive common denominator, the product inequality, and finiteness of exceptional denominators.

Excluded or not yet identified with the root: the full number-field Subspace Theorem, quantitative bounds, effective constants, `n = 0`, zero denominators, nonpositive epsilon, and the coordinatewise `-(1/n)-epsilon` formulation except as a prospective corollary requiring a checked bridge.

The canonical declaration is `Stage1Instances.THMM0401.SchmidtSimultaneousApproximationTarget`. Its ordered binders, explicit exclusions, printed normalized expression, source hash, toolchain and lock hashes are recorded in `instance.json` and `normalized-expression.txt`. The legacy module remains discovery input only; the local exact restatement is connected by a checked `iff`.

## Source-Statement Crosswalk

| Source | Pinpoint/status | Mapped content | Intake boundary |
|---|---|---|---|
| W. M. Schmidt, *Simultaneous approximation to algebraic numbers by rationals*, Acta Mathematica 125 (1970), 189-201 | Primary paper identified by title, volume, year, and page span; exact theorem/page and errata not yet independently checked | Product-form simultaneous approximation claim | Bibliographic identification only; cannot establish `H0` |
| W. M. Schmidt, *Diophantine Approximation*, LNM 785, Springer (1980) | The repository's `1980` label is treated as a book pointer; theorem/page/edition and errata remain to audit | Later exposition/context | Does not replace the primary-paper pinpoint |
| `Docs/researches/math_theorems.md` | Repository metadata says “代数数的联立逼近” and “已验证” | Candidate identity and topic | Untrusted metadata; no proof or machine credit |
| `Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_014.lean` | Legacy `CanonicalProductStatementShape` | Proposed Lean encoding of dimension, algebraicity, independence, epsilon, and finite denominator set | No rev-5.6 statement fingerprint or root proof credit |

Current source debt is `H3`: a plausible primary source and claim are identified, but the exact theorem number/page, assumptions, proof boundary, edition relation, and errata require the anchor/source audit. Current machine debt is `M4`: no rev-5.6 exact target or root closure has been accepted. Current readability debt is `R3`: this is an intake map, not a proof reconstruction.

## Statement Gate

The narrow Lean check covers the exact proposition, a definitional transport to the legacy product form, and four negative mutation probes: removal of algebraicity, changing denominators from naturals to integers, moving epsilon outside the dimension binder, and admitting `n = 0`. Each mutated expression is required to fail definitional equality with the canonical target.

The alternate coordinatewise formulation remains uncredited: no checked implication from the product theorem is claimed in this phase. Machine debt stays `M4`, human-source debt stays `H3`, readability debt stays `R3`, and `theorem_complete` remains false.

## Open Task DAG

`ANCHOR_AUDIT -> OBLIGATION_TREE -> PROOF -> VALIDATION -> RELEASE`

Only the statement node is self-tested here. All later nodes remain open, and only the integration lane may accept this provisional result.

## Anchor Audit

The rev-5.6 anchor inventory is recorded in `anchor-audit.json` with readable evidence in
`anchor-audit.md`. At pinned mathlib commit `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the
nearby Diophantine-approximation declarations cover Dirichlet and one-dimensional rational
approximation, not the exact algebraic-vector product-finiteness target. The legacy local artifact
is statement-only (`M3`), and no accessible external search produced an immutable Lean 4 proof
candidate. The exact root therefore remains `M4`; no `M1` or `M0-*` credit is claimed. The primary
1970 paper is bibliographically confirmed, but pinpoint and errata mapping remain open, so
human-source status is conservatively `H1`.

This inventory completes the assigned phase, while the full theorem audit and proof remain open.
External code-search access and fresh Lean replay blockers are described in the audit.

## Obligation Tree

Registry `THM-M-0401-OBLIGATIONS-v1` freezes 14 canonical obligations before proof status is
observed. The 13 required machine obligations explicitly expose the integer-point normalization,
algebraic linear-form construction, height comparison, missing qualitative Subspace-Theorem bridge,
proper-subspace relation extraction, independence-limit argument, finite-union terminal step, and
root trust/provenance boundaries. Separate reciprocal typed graphs prevent source, documentation,
trust, or workflow links from being treated as proof premises.

The coordinatewise alternate formulation is one nonroot informational obligation and is excluded
from all required denominators; it cannot inflate coverage. The frozen denominator projection hash
is `3e0527abbf2146164c691c2e22b29bb7501997a0c80d5e6718b746159e762dcc`. Structural validation is
recorded in `obligation-tree-validation.md`. Zero proof obligations and zero composition
certificates are claimed closed; the exact root remains `M4` and theorem completion remains false.

## Validation Record

Base revision: `ca5213c506afa21d64fb8f2481ac658887786c6e`.

The preflight commands `python3 Docs/tools/check_stage1_standard.py`, `python3 scripts/stage1_target.py check`, and `python3 scripts/stage1_target.py show THM-M-0401` exited 0. The statement command `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0401/Statement.lean)` also exited 0 using the existing canonical `.lake` artifacts; it printed the fully explicit target expression after checking the transport and mutations. Exact commands, hashes, and scope are in `validation.md`.

The owned-artifact self-test commands and exact outcomes are recorded in `.stage1-worker-selftest.json`. No Lean proof validation is claimed by this statement phase.
