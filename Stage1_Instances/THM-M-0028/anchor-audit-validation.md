# THM-M-0028 Anchor-Audit Validation

Item: `S56-M-0028-ANCHOR_AUDIT`

Base revision: `7e54c0fcaf9c0e53fa7afbbeb0a36218152f932c`

Base tree: `80ece87e35401b07ba76abc36ea83440b5fa7f31`

Validation date: `2026-07-13` (`Asia/Shanghai`)

## Result

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the composition of
`isNoetherianRing_iff_ideal_fg` and `monotone_stabilizes_iff_noetherian` closes a literal copy of
the frozen target. The local adapter retains the exact universe, `CommRing` and finite-generation
binders, `Nat ->o Ideal R` carrier, stabilization equality, and zero-ring boundary. Lean prints
both terminal bodies, reports both terminals and the adapter sorry-free, and reports only
`propext`, `Classical.choice`, and `Quot.sound` for the complete adapter.

The immutable Atlas project at `34ffed396f376454c1a9b297f3fd74c5c801fb50` supplies the exact
biconditional `noetherian_fg_iff_acc`; its forward direction matches the target and its full source
elaborates under the identical pinned Lean/mathlib environment. It is outside the dependency
closure, reduces to the same mathlib theorems, and is covered by a restrictive noncommercial and
no-training license. It is therefore `M1 / E2` corroboration, not an integrated `M0-P` candidate.
Its second Noetherian-predicate wrapper is deduplicated. Atlas identifies the corpus as
LLM-autoformalized, so its automated internal report supplies provenance but no independent-human-
review credit.

The exact mathlib route is a self-tested `M0-W / E2` candidate. The accepted root remains
`[H1, M3, R3]` until downstream proof, composition, complete provenance/trust, `E1`, and master
acceptance. Neither `AUDIT-Z` nor theorem completion is claimed.

## Commands And Results

All local validation used the automation-provided canonical `.lake` symlink read-only. No
`lake update`, `lake build`, dependency clone/fetch, or `.lake` mutation ran.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | rev-5.6 standard structure and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique ordered targets passed |
| `python3 scripts/stage1_target.py show THM-M-0028` | 0 | rank 1073; planned; L0/rework-required; theorem incomplete |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | revision `8a178386...ea95`, tree `bdc39a31...5c2b` |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | 0 | empty output; dependency worktree clean |
| bounded `rg` over repository-local Lean and all 11 materialized packages | 0 | pinned mathlib supplied the exact terminal pair; no independent body appeared in the other ten packages |
| anonymous GitHub repository queries for theorem names and aliases | HTTP 200 | four zero-result metadata responses recorded with immutable response hashes |
| GitHub code query for `monotone_stabilizes_iff_noetherian language:Lean` | HTTP 403 | anonymous rate limit exhausted; access limitation, not negative evidence |
| grep.app queries for the two declarations and theorem name | HTTP 429 | Vercel security checkpoint; access limitation, not negative evidence |
| three Sourcegraph global Lean queries | HTTP 200 / curl 0 | exact Atlas names each had one indexed match; generic name had 15 matches across five repos, mostly mathlib consumers; responses hashed |
| `git ls-remote https://github.com/facebookresearch/atlas-lean.git HEAD refs/heads/main` | 0 | immutable Atlas revision `34ffed...fb50` authenticated without clone/fetch |
| immutable GitHub API/CDN reads for Atlas commit, tree, source, pins, and license | 0 | tree/blob/SHA-256 identities, matching Lean/mathlib pins, and restrictive license recorded |
| stream `AffineVarieties.lean` at Atlas revision `34ffed...fb50`, append `#print sorries noetherian_fg_iff_acc` and `#print axioms noetherian_fg_iff_acc`, then pipe to `(cd Formalizations/Lean && lake env lean /dev/stdin)` | 0 | full immutable source elaborated; exact biconditional sorry-free with expected axiom report |
| stream `NoetherianModules.lean` at Atlas revision `34ffed...fb50`, append `#print sorries NoetherianModules.noetherian_ring_iff_acc` and `#print axioms NoetherianModules.noetherian_ring_iff_acc`, then pipe to `(cd Formalizations/Lean && lake env lean /dev/stdin)` | 0 | full immutable source elaborated; secondary wrapper sorry-free with expected axiom report |
| `lake env lean ../../Stage1_Instances/THM-M-0028/AnchorAudit.lean` from `Formalizations/Lean` | 0 | exact terminal types/bodies printed; three sorry-free reports; expected axiom reports; stdout SHA-256 `b099c3dc...223` |
| `python3 -B Stage1_Instances/THM-M-0028/check_anchor_audit.py` | 0 | item identity, pins, hashes, bodies, provenance, classifications, exact expression, and Lean replay matched |
| `python3 -m json.tool` on both anchor JSON artifacts | 0 | both structured artifacts parsed |
| scoped prohibited-construct scan over `AnchorAudit.lean`, pinned mathlib source, and both Atlas sources | 1 (expected no match) | no proof gap, axiom declaration, unsafe/opaque body, or `proof_wanted` marker |
| `git diff --check -- Stage1_Instances/THM-M-0028 .stage1-worker-selftest.json` | 0 | no whitespace diagnostics |

## Search Boundary

The public discovery is bounded, not saturated. GitHub code search and grep.app were inaccessible,
and Sourcegraph omitted 279 forks and 92504 archived repositories by default. Access failures are
recorded as limitations rather than false negative results. The Atlas source was read and checked
at an immutable commit without adding it to the repository or dependency closure.

## Status Boundary

This phase supplies provisional self-tested anchor evidence pending master acceptance. The
obligation registry, proof-phase integration, full transitive trust/TCB closure, primary-source and
readable reconstruction review, hermetic and independent validation, deterministic release bundle,
`AUDIT-Z`, and theorem completion remain open.
