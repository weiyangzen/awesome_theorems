# Quillen-Suslin Port Provenance

The complete Lean import closure of the terminal theorem `quillenSuslin` is vendored from:

- Repository: <https://github.com/mbkybky/QuillenSuslin>
- Revision: `51ed173b17b274e61f759556ab3e1c090267d1bd`
- Source tree: `264c487a24b2158bf8432459fd0b1e326acdf1eb`
- Immutable archive SHA-256:
  `ad8bd7662861ddf984f6c244f3b1d3eabbe4b0fd9b33f51dd85e2918d737babf`
- Upstream environment: Lean `v4.28.0-rc1`, mathlib
  `9543d5047cb12a05abd2d9b9bc2ea2a604b3be87`
- Target environment: Lean `v4.29.0`, mathlib
  `8a178386ffc0f5fef0b77738bb5449d50efeea95`

Every production source in the immutable archive declares Apache-2.0 in its header, but the archive
contains no root `LICENSE`, `COPYING`, or `NOTICE`. `Vendor/LICENSE` therefore supplies the standard
Apache 2.0 text locally. It is not represented as a byte copy from the upstream archive.

The closure contains eight modules, seven internal imports, 5,079 newline-terminated source lines,
and 260,645 vendored bytes. `UnimodularVector/BivariatePolynomial.lean` is byte-identical to
upstream. Seven files carry a port notice and the compatibility edits below. All changes are
mechanically inverted by `build_vendor_manifest.py`, which then verifies the exact upstream hashes.

| Source path under `Vendor` | Upstream SHA-256 | Vendored SHA-256 |
|---|---|---|
| `QuillenSuslin/FiniteFreeResolution/Basic.lean` | `fa821f42aa065af060d0af552d449946c1424f90ba28c5cd27836c07605652b2` | `02b95a0fe71a78f534257fe3507f414e49a2e46e33ff4f4e6a1a25b8b742eb13` |
| `QuillenSuslin/FiniteFreeResolution/Polynomial.lean` | `01eb31ded76f6a9e6d853516fc9f23d54f2a388b295f95582c75824c3e1a8744` | `0e1f11a4825cc5889a581d9ddb446352e308da5c58a7e4d7f8412d79e5785d0a` |
| `QuillenSuslin/FiniteFreeResolution/StablyFree.lean` | `27bf1423baec49d61042b1670ddb681d88a6cb1343273b37b107e736f10b4a6d` | `0bcd23fdbc28137cfd0468dc589131a509ade25f2a5672b169915f1f9b0f9a8a` |
| `QuillenSuslin/MainTheorem.lean` | `55b82438fd10a2f3598b52d51c59257b86850ac873d3359c5c540b54434c4f7f` | `7f41f50c1ad55c9e07583cf220c69431f1af95dfe0df5ccd717f050b147f5e50` |
| `QuillenSuslin/UnimodularVector/Basic.lean` | `3a17838ebaa14eb1d45423309b4e581d60d82717bdce7ba41d7d24fd26843af0` | `e6213033db01359e42e1e4bdd177937e3e15cc690a5e20f98bbf50276c37a123` |
| `QuillenSuslin/UnimodularVector/BivariatePolynomial.lean` | `d1f142dec441dd9ecdaf51a99076eff69c9683f06fa6e94e2112c0fe5a0e2f72` | `d1f142dec441dd9ecdaf51a99076eff69c9683f06fa6e94e2112c0fe5a0e2f72` |
| `QuillenSuslin/UnimodularVector/PID.lean` | `b623f1ec9e5391e296c9b96092267496eac79b72e46372dbd5d5ab8df7062d4b` | `aea2cf9c890e3ea4c562464b9e626585159a1c49442ff6263fb1fef1b7f2b1b1` |
| `QuillenSuslin/UnimodularVector/SuslinMonicPolynomialThm.lean` | `d083e52e23c83700888fbbfd1333fbd227d7620a7226c6ec5865d0cbd3fde688` | `0037a897bfc635d4e453bdf804e78a63ec89fafd3f6702872c7dd77ea6e00964` |

## Compatibility Edits

- All seven upstream sibling imports are qualified with the target-local module prefix. This avoids
  collisions while leaving imported declarations and proof terms unchanged.
- `FiniteFreeResolution/Basic.lean` uses the current `Module.Free.iff_of_equiv` name in six places
  and replaces two brittle `simpa [hinst]` transports with an explicit `rw` followed by `exact`.
- `FiniteFreeResolution/Polynomial.lean` proves one definitionally equal module-action equality by
  `rfl` rather than an obsolete simplifier expansion.
- `UnimodularVector/Basic.lean` supplies the polynomial divisor argument now expected by two
  `modByMonic_eq_sub_mul_div` applications.
- `UnimodularVector/PID.lean` makes a finite-sum erasure rewrite explicit, composes the resulting
  equality directly, gives the exact simplifier set, and uses `rw [mul_sum]` where the old
  simplifier invocation no longer fires.
- `UnimodularVector/SuslinMonicPolynomialThm.lean` supplies a quotient nontriviality instance in the
  prime-height branch, uses current bivariate swap lemmas in place of obsolete simp behavior and a
  local induction, and makes the final swap simplification explicit.

These are API and elaboration compatibility changes only. No theorem statement, hypothesis, proof
branch, or mathematical conclusion is removed or weakened. The exact normalized operation-ledger
SHA-256 is `c76174fb78f391ceb00fc57df79829ef3af99c0dc43b477f444c61085ed02fe3`.
The path-normalized semantic-diff SHA-256, after removing port notices and reversing only import
localization, is `372acc2ec8f1f0921b9ffe63fda67f4ec40487840d8379af091a7297047d0d19`.
Both are recomputed and checked by `build_vendor_manifest.py`.
