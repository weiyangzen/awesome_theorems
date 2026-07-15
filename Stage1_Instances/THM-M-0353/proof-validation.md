# THM-M-0353 proof-phase validation

Item: `S56-M-0353-PROOF`

Base revision: `48fb6596b1844f4183c411142415d872ff21e842`

Verdict: `no_state_change`; provisional worker self-test, pending master acceptance.

## Exact proof body

`Proof.lean` proves the unchanged
`Stage1Instances.THM_M_0353.HermiteCompletenessTarget`. It transports a proved real Hermite
development to the target's literal complex-valued functions, constructs their complex `Lp`
representatives, proves orthonormality, reduces complex completeness to the real and imaginary
parts, and packages the family with `HilbertBasis.mkOfOrthogonalEqBot`. The final declaration
`hermiteCompletenessTarget_proof` consumes the exact frozen `HermiteMemLpPackage` and
`HermiteBasisPackage` through `root_of_hermite_packages`; it does not substitute a weaker target.

The analytic bodies are a byte-identical Apache-2.0 source from
`mrdouglasny/gaussian-field` at commit
`d63a28568a75d99f6cb27af1f888a49a69855a66`, tree
`7b2c1a97a992cacee49dcbd347a9d78d59fdc383`. The source, Git blob, and license are bound in
`vendor-manifest.json` and `VENDOR_PROVENANCE.md`. The upstream file targets Lean 4.30/mathlib
`c5ea0035...`; the unchanged bytes also elaborate under this repository's pinned Lean 4.29/mathlib
`8a178386...` environment. Its header contains stale prose saying that key properties are axioms,
but the actual declarations have proof bodies and the executable-code scanner finds no axiom or
placeholder declaration.

## Frozen graph mapping

The exact package and root declarations provisionally map `M0353-P-MEMLP`, `M0353-P-BASIS`,
`M0353-T-ASSEMBLE`, and `M0353-ROOT`. The adapter also supplies concrete anchors for the complex
`Lp` vectors, normalization, orthonormality, orthogonal-complement completeness, complexification,
and Hilbert-basis construction. The vendored source supplies all-index integrability, Gaussian
Hermite orthogonality, polynomial/moment reduction, Fourier uniqueness, and real completeness.

This is nevertheless not an accepted per-node graph rewrite. Several frozen internal nodes have
only planned prose signatures, and the vendored completeness route uses Gaussian moments and
Fourier uniqueness rather than the weighted-space density route suggested by the frozen graph.
No individual planned internal obligation or composition edge receives accepted closure credit in
this worker packet. Source review, full trust/provenance acceptance, validation, and release remain
separate downstream gates.

## Validation ledger

All Lean checks use disposable files under `/tmp`, the existing pinned toolchain, and prebuilt
canonical dependency artifacts. No `lake update`, `lake build`, dependency clone/fetch, or `.lake`
mutation was performed. `check_proof.sh` resolves the Lean binary and pinned dependency path with
`lake env`, then invokes Lean directly with the disposable directory first, preventing a stale
project `.olean` from shadowing the copied modules.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required. |
| `python3 scripts/stage1_target.py show THM-M-0353` | 0 | rank 846, lifecycle planned, `theorem_complete=false`. |
| `python3 -I -B Stage1_Instances/THM-M-0353/check_statement.py` | 0 | frozen statement SHA-256 and four structural mutations passed. |
| `python3 -I -B Stage1_Instances/THM-M-0353/check_obligation_tree.py` | 0 | 16 obligations, 76 typed edges, denominator `4516c92f...`; historical accepted root remains open. |
| `python3 -I -B Stage1_Instances/THM-M-0353/build_vendor_manifest.py --check` | 0 | one byte-identical 99,106-byte source module and its license matched the immutable manifest. |
| `bash Stage1_Instances/THM-M-0353/check_proof.sh` | 0 | isolated `--trust=0 -t0` replay elaborated Statement, ObligationTree, vendor, and Proof; six declarations were sorry-free. |
| `python3 -I -B Stage1_Instances/THM-M-0353/check_proof.py` | 0 | source lexer, provenance, frozen graph, receipt, packet, and pinned-environment checks passed. |
| `python3 -m json.tool Stage1_Instances/THM-M-0353/vendor-manifest.json` | 0 | JSON valid. |
| `python3 -m json.tool Stage1_Instances/THM-M-0353/proof-receipt.json` | 0 | JSON valid. |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | 0 | empty output; pinned mathlib worktree clean. |
| `git diff --check -- Stage1_Instances/THM-M-0353 .stage1-worker-selftest.json` plus no-index checks for new files | 0 | no whitespace errors. |

The six diagnostic declarations are
`hermiteFunction_memLp`, `hermiteFunction_orthonormal`, `hermiteFunction_complete`,
`hermiteMemLpPackage_proof`, `hermiteBasisPackage_proof`, and
`hermiteCompletenessTarget_proof`. Every `#print sorries` result was
`Declarations are sorry-free!`; every `#print axioms` result was exactly
`[propext, Classical.choice, Quot.sound]`. The comment/string-aware scan rejects executable
`sorry`, `admit`, `sorryAx`, bodyless `axiom`/`constant`, `opaque`, `unsafe`, `extern`,
`implemented_by`, and `native_decide`.

## Status boundary

This packet proposes an `M0-P` candidate for the exact root after provenance, trust, graph
reconciliation, and dependency-ordered master review. Accepted state remains at the weaker intake
boundary `[H1, M4, R4]`; the frozen graph separately records root `M3`, a pre-existing discrepancy
left for the master. Accepted obligation closure is empty. H0, R0, release-grade E1, full transitive
TCB closure, hermetic empty-cache/offline replay, independent verification, validation, release,
`AUDIT-Z`, `THEOREM-Z`, audit completion, and theorem completion are all unclaimed.
