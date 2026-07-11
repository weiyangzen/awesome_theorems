# THM-M-0113 anchor-audit validation

Item: `S56-M-0113-ANCHOR_AUDIT`  
Date: 2026-07-12  
Base revision: `0f142dc81233343d6cad44f3c6dfbe9240e15606`

## Decision

The exact repo-local target is a proposition definition without a proof body.
The legacy `S1_M_025.lean` surface is a parameterized statement shape plus
wrappers for nearby facts; it is not exact and receives no inherited rev-5.6
credit. Pinned mathlib at `8a178386ffc0f5fef0b77738bb5449d50efeea95`
provides complex/Riemannian manifold types, exterior derivatives, harmonic
functions, sheaf cohomology, internal-sum notation, and algebraic Kahler
differentials. The twelve `AnchorAudit.lean` probes elaborate those APIs, but
none constructs de Rham/Dolbeault cohomology for compact Kahler manifolds or
proves the bidegree direct sum and conjugation conclusions.

The known Hodge-related project
`lean-dojo/LeanMillenniumPrizeProblems@540da94826f70f3edf4d4fc66ce6cda20e903f61`
was inspected through its complete immutable Git tree and content-hashed raw
sources. It states the different Hodge conjecture over parameterized Hodge
subspaces. Its own immutable source explicitly lists the Hodge-decomposition
isomorphism and harmonic interpretation as not formalized. It uses Lean
`v4.26.0` and mathlib `2df2f0150c275ad53cb3c90f7c98ec15a56a1a67`,
which are not this worker's materialized pinned closure, so it was source-audited
rather than fetched or built.

Bounded Sourcegraph and GitHub repository searches found no further candidate.
GitHub code search required authentication, so that lane is a blocker, not a
negative result. The root is therefore classified `M4`: no exact proof body was
found to integrate. This is a self-tested candidate inventory pending master
acceptance, not a proof, a global nonexistence claim, or audit/theorem completion.

## Commands and results

All commands ran in this worker clone. Lean used the existing pinned `.lake`
artifacts; no dependency update, fetch, clone, or build was performed.

| Command | Exit | Result |
|---|---:|---|
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0113/AnchorAudit.lean` | 0 | Twelve pinned support declarations elaborated and printed |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0113/Statement.lean` | 0 | Frozen target and definitional expansion re-elaborated |
| `python3 Stage1_Instances/THM-M-0113/check_anchor_audit.py` | 0 | Candidate ledger, target boundary, probes, manifest pin, and installed mathlib HEAD agreed |
| `rg -n -i --glob '*.lean' 'HodgeDecomposition\|hodge decomposition\|Dolbeault\|deRhamCohomology\|de Rham cohomology\|KahlerManifold\|KaehlerManifold\|KählerManifold\|HodgeLaplacian\|harmonic representative\|harmonic differential form\|Hodge filtration\|Hodge-to-de Rham' Formalizations/Lean/.lake/packages/mathlib/Mathlib` | 1 | No match in pinned mathlib source; exit 1 is ripgrep's expected no-match status |
| `curl ... sourcegraph.com/.api/search/stream ...` | 0 | `matchCount=0`; response SHA-256 `5d79a5f0fe4bc4d00a3b3878dba66df3a2b8fbcedc8b3b68d86214a513c0a5b0` |
| `curl ... api.github.com/search/repositories ...` | 0 | `total_count=0`, complete response; SHA-256 `08c082fdf7ca87ba911a2aabb0f0cf2d3e482a6feeaac9713e4578c20b2600b2` |
| `curl ... api.github.com/search/code ...` | 0 | Response captured with HTTP 401; SHA-256 `b7dbd173f33b19650f61b1c528737e2037cf768d90076fdfce5d32541765e29e` |
| `curl ... /lean-dojo/LeanMillenniumPrizeProblems/git/trees/540da948...?recursive=1` | 0 | Immutable revision, non-truncated 71-entry tree; SHA-256 `55efcc7d06fd49b41cb09b73118716c52e6512f10fda2811046056d07265906f` |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | rev-5.6 standard and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique ordered targets passed |
| `python3 scripts/stage1_target.py show THM-M-0113` | 0 | Rank 25, planned, legacy artifacts unaccepted, theorem incomplete |
| `git diff --check -- Stage1_Instances/THM-M-0113 .stage1-worker-selftest.json` | 0 | No whitespace errors |

## Reopen condition

Reopen integration when a concrete exact Lean 4 candidate supplies an immutable
repository revision, pinned toolchain and dependencies, module and declaration,
exact-type transport, terminal proof-body provenance, license, trust and
placeholder audits, and a successful repo-local check. Until then, neither an
`M0` class nor theorem-completion credit is valid.
