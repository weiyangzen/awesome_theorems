# Anchor-audit validation record

Item: `S56-M-0508-ANCHOR_AUDIT`  
Base revision: `e9d545372b66f73be63271b2fb408ef134d1d6f7`

## Result

The exact local artifact is only the proposition
`Stage1Instances.THM_M_0508.VinogradovThreePrimesTarget`. Pinned mathlib at
`8a178386ffc0f5fef0b77738bb5449d50efeea95` supplies prime predicates, finite prime sets,
prime counting, infinitude, Chebyshev bounds, and divergence of the prime reciprocal sum. Ten such
declarations elaborate in `AnchorAudit.lean`, but none has an eventual three-prime representation
conclusion. A bounded pinned-source name search also found no Vinogradov/ternary-Goldbach target.

The public search located `TernaryGoldbachConjecture.ternaryGoldbach` in
`google-deepmind/formal-conjectures@b2e608fc52d765510915a244bb69b1a2741acc3c`. Its stronger type
would mathematically imply the eventual target, but its body is literally `by sorry`. The immutable
file has SHA-256 `bf6a587c50ba159af919fbe9afa09f04375608c33c68361ffc52246018a5b447`, so the
candidate is explicitly rejected, not integrated. Other indexed uses of "Vinogradov" were unrelated
prime-counting bounds or the Bombieri-Vinogradov theorem.

Thus the root remains `M4`. This completes only the bounded formal-anchor inventory; it neither
claims global absence nor source fidelity, proof closure, audit completion, or theorem completion.

## Commands and results

Commands ran on 2026-07-12 using existing pinned `.lake` artifacts read-only. No update, build,
dependency clone, or fetch was run.

| Command | Exit | Result |
|---|---:|---|
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0508/AnchorAudit.lean)` | 0 | Ten pinned prime/distribution support declarations elaborated |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0508/Statement.lean)` | 0 | Exact target and checked eventual transport re-elaborated |
| `python3 Stage1_Instances/THM-M-0508/check_anchor_audit.py` | 0 | IDs, negative boundary, probes, rejected placeholder, manifest pin, and installed mathlib HEAD agreed |
| `rg -n -i 'vinogradov|three[- _]?prime|three primes|sum of three primes|ternary goldbach|weak goldbach' Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'` | 1 | Expected no-match exit in pinned mathlib source |
| Sourcegraph global archived/fork Lean query | 0 | 15 matches in four repositories; response SHA-256 `3107b94b...7158a` |
| GitHub repository searches for Vinogradov/weak-Goldbach Lean projects | 0 | Both complete results had count zero; response SHA-256 `08c082fd...ec6cd` |
| GitHub code search for `Vinogradov` in Lean | 0 | Response captured; HTTP 401 blocker; SHA-256 `b7dbd173...e29e` |
| GitHub immutable tree and raw-file inspection for Formal Conjectures | 0 | Non-truncated 1204-entry tree; stronger declaration's literal `sorry` body rejected |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Standard structure and 1546-target uniform-L0 set passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique ranks and manifest invariants passed |
| `python3 scripts/stage1_target.py show THM-M-0508` | 0 | Rank 882, planned, L0/rework-required, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-0508/anchor-audit.json` | 0 | Audit JSON parsed |
| `rg -n '\\b(sorry|admit)\\b|^[[:space:]]*axiom\\b' Stage1_Instances/THM-M-0508 -g '*.lean'` | 1 | Expected no-match exit; owned Lean sources contain no forbidden escape |
| `git diff --check -- Stage1_Instances/THM-M-0508 .stage1-worker-selftest.json` | 0 | No whitespace errors |

## Open integration gate

Retry only with a concrete immutable Lean 4 candidate whose exact type/transport, terminal proof
body, placeholders, axioms, unsafe/oracle boundaries, toolchain, dependencies, and license can be
checked locally. Authenticated GitHub code search remains an explicitly blocked discovery lane.
