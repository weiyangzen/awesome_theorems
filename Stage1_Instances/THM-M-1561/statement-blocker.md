# Exact-statement gate: blocked

Item: `S56-M-1561-STATEMENT`  
Theorem: `THM-M-1561`  
Base revision: `b5768b55f94197ed20d70d350ea6d4def3c3a667`

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the authoritative repository record.
The complete mathematical wording is only `随机矩阵与可积系统的联系` ("the connection between
random matrices and integrable systems"). It supplies no ensemble, observable, integrable
hierarchy or equation, normalization, hypotheses, ordered quantifiers, or conclusion. The
metadata value `已验证` is explicitly untrusted under rev-5.6 and is not a source receipt.

The accepted intake names two discovery anchors, but they represent inequivalent theorem families:

- Adler and van Moerbeke (1995) concerns matrix integrals, Toda symmetries, tau functions, and
  orthogonal polynomials.
- Tracy and Widom (1994) concerns level-spacing distributions, the Airy kernel, Fredholm
  determinants, and integrable equations, and may overlap the separately scheduled Tracy-Widom
  target.

Neither citation has an approved exact theorem or displayed identity, page locator, definition
crosswalk, assumptions, or errata audit. Selecting one family because it is convenient to encode
would substitute mathematics rather than elaborate the source target. The proposition-changing
choices still include the matrix field and symmetry class, size and probability law, potential,
observable, deformation variables, base measure, normalization, finite-size versus limiting
regime, hierarchy or equation conventions, branch and boundary data, and degenerate cases.

Consequently this phase fails at canonical human-claim identity, before minimal imports, an
elaborated expression fingerprint, checked alternate transports, or meaningful removed-hypothesis,
changed-domain, binder-scope, and boundary-case mutations can be established. No Lean declaration,
axiom, assumed interface, broadened connection claim, or convenient special case was introduced.
Machine debt remains `M4`; statement acceptance, audit completion, and theorem completion remain
false.

## Pinned environment and scoped search

Commands were run inside this worker clone on 2026-07-12 (Asia/Shanghai). Existing `.lake`
artifacts were read only; no update, build, clone, fetch, or dependency mutation was performed.

- Lean toolchain: `leanprover/lean4:v4.29.0`; Lean 4.29.0, commit
  `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- Lake: `5.0.0-src+98dc76e`.
- Pinned mathlib revision: `8a178386ffc0f5fef0b77738bb5449d50efeea95`.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1561` | 0 | Rank 572, planned, legacy artifacts unaccepted, theorem incomplete |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean version and commit recorded above |
| `cd Formalizations/Lean && lake --version` | 0 | Lake version recorded above |
| `cd Formalizations/Lean && sha256sum lean-toolchain lake-manifest.json` | 0 | Produced the two hashes recorded above |
| `git -C "$(readlink -f Formalizations/Lean/.lake/packages/mathlib)" rev-parse HEAD` | 0 | Produced the pinned mathlib revision recorded above |
| repository `rg` search for the theorem ID, Chinese title/gloss, English title, and both candidate paper titles | 0 | Found only underspecified catalogue metadata, this intake, and distinct related targets; no source-frozen proposition or target-specific Lean declaration |
| pinned-mathlib `rg` search for random matrices, matrix integrals, Toda hierarchies/lattices, tau functions, Painleve equations, Airy kernels, and Fredholm determinants | 1 | No matching Lean source under the searched terms |
| `python3 -m json.tool Stage1_Instances/THM-M-1561/statement-blocker.json` | 0 | Blocker receipt is valid JSON |
| `git diff --check -- Stage1_Instances/THM-M-1561` | 0 | No whitespace errors |

There is no applicable `lake env lean <canonical-target>.lean` elaboration check because no exact
expression exists. Elaborating a proposition selected from either candidate family, or an abstract
interface that assumes the desired connection, would be fake statement evidence.

## Retry condition

An accountable source review must preserve an immutable primary-source edition, select an exact
theorem or displayed identities with page locators, audit definitions and errata, and independently
approve a row-by-row crosswalk. It must freeze every ensemble, observable, normalization,
integrable-system, hypothesis, quantifier, conclusion, limiting, and boundary choice listed above.
A later statement run can then encode the exact Lean expression, minimize pinned imports,
fingerprint the elaboration and environment, check alternate transports, and execute all four
required mutation classes.

This records the first failed gate and does not complete this or any downstream node. The assigned
phase is not genuinely self-tested, so no `.stage1-worker-selftest.json` is emitted.
