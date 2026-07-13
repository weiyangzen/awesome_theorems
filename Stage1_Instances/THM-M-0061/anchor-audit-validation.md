# THM-M-0061 Anchor-Audit Validation

Item: `S56-M-0061-ANCHOR_AUDIT`

Base revision: `eb9c2192f79a480deff66d2c0f8e31032bcc2d9f`

Base tree: `57b76c2fceacd8819b0ec8b9abcd42cfcc74b8e2`

Validation date: `2026-07-13` (`Asia/Shanghai`)

## Result

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`,
`Subgroup.card_subgroup_dvd_card` proves `Nat.card H ∣ Nat.card G` for every multiplicative group,
without requiring finiteness. The audit wrapper keeps the frozen `[Finite G]` binder and inhabits
the literal finite-group root. Lean elaborates the wrapper and reports only `propext`,
`Classical.choice`, and `Quot.sound`.

The theorem's printed body reduces divisibility to
`Subgroup.card_eq_card_quotient_mul_card_subgroup`. That bridge uses `Nat.card_prod`,
`Nat.card_congr`, and `Subgroup.groupEquivQuotientProdSubgroup`. The additive theorem is a generated
domain-changing duplicate, while quotient-product and index formulations are support paths rather
than additional proof bodies. No separate candidate was found in the other materialized pinned
dependencies. A bounded public repository search located two instructional group-theory projects,
but neither yielded an admitted Lagrange closure at its immutable revision.

The pinned route is a provisional `M0-W` candidate with local `E2` checking. The accepted root
remains `H1/M3/R4` until proof, composition, full transitive trust/provenance, and master-acceptance
gates provide accepted evidence. Neither `AUDIT-Z` nor theorem completion is claimed.

## Commands And Results

All local validation ran in this worker clone against the automation-provided canonical `.lake`
symlink read-only. No `lake update`, `lake build`, dependency clone/fetch, or `.lake` mutation ran.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | standard structure, execution skill, and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique ordered targets passed |
| `python3 scripts/stage1_target.py show THM-M-0061` | 0 | rank 1093; planned; L0/rework-required; theorem incomplete |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | exact revision `8a1783...ea95`, tree `bdc39a...5c2b` |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | 0 | empty output; dependency worktree clean |
| scoped repo-local, pinned-mathlib, and materialized non-mathlib dependency searches | 0 | exact mathlib candidate and visible body chain classified; no separate pinned external candidate located |
| anonymous GitHub repository/API searches at the recorded cutoff | 0 | exact-topic queries returned zero; broad query's two immutable repository heads were classified; authenticated code search and grep.app remained unavailable |
| `lake env lean ../../Stage1_Instances/THM-M-0061/AnchorAudit.lean` from `Formalizations/Lean` | 0 | exact candidate, direct bridge, additive duplicate, proof bodies, four axiom reports, adapter, and explicit root elaborated; stdout SHA-256 `ea79a8bf...00dc` |
| `python3 -B Stage1_Instances/THM-M-0061/check_anchor_audit.py` | 0 | authority item, statement fingerprint, pins, blobs, source hashes, bodies, history ancestry, inventory, receipt, packet, and narrow Lean replay agreed |
| `python3 -m json.tool` on both anchor JSON artifacts and root packet | 0 | all structured artifacts parsed |
| scoped prohibited-construct scan over `AnchorAudit.lean` | 1 (expected no match) | no proof gap, axiom declaration, unsafe/opaque body, or placeholder |
| `git diff --check -- Stage1_Instances/THM-M-0061 .stage1-worker-selftest.json` plus per-new-file checks | 0 | no whitespace diagnostics |

## External Search Boundary

Anonymous GitHub exact-topic repository searches returned zero matches. A broader `lean4 group
theory` query returned two small instructional repositories, which were frozen by commit/tree and
classified in `anchor-audit.json`. GitHub code search returned HTTP 401, grep.app returned HTTP 429,
and raw retrieval of one public Lean file timed out. These are bounded results and access failures,
not evidence of global absence or discovery saturation.

## Status Boundary

This phase supplies provisional self-tested anchor evidence pending master acceptance. The
obligation registry, canonical proof-phase composition, full transitive trust/TCB closure,
primary-source and readable reconstruction review, hermetic and independent validation,
deterministic release bundle, `AUDIT-Z`, and theorem completion remain open.
