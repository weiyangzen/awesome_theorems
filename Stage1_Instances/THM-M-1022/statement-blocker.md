# Exact-statement gate: blocked

Item: `S56-M-1022-STATEMENT`  
Theorem: `THM-M-1022`  
Base revision: `aaeade67ccb391b2d10e50e766d54427324b3090`

## Decision

No exact Lean 4 target can be truthfully elaborated from the frozen intake record. The intake
deliberately leaves the primary-source theorem/page and exact conclusion strength open. Its
provisional claim says that a continuous, even real function, normalized at zero, tending to zero
at positive infinity, and convex on the nonnegative half-line is a characteristic function, but it
also explicitly says that the source conclusion concerning a density or atoms remains unchecked.

The cited discovery candidate is Georg Polya, "Remarks on Characteristic Functions",
*Proceedings of the Berkeley Symposium on Mathematical Statistics and Probability* (1949), pages
115--123. OpenAlex record `W1562638189` confirms that bibliographic range and points to Project
Euclid record `euclid.bsmsp/1166219202`. This is metadata, not an inspected theorem statement. The
Project Euclid endpoints available in this run returned an anti-automation HTML page rather than
the article, so the theorem wording and definitions could not be checked.

The unresolved choices are proposition-changing rather than cosmetic:

- whether Polya assumes continuity separately or obtains it from other conditions;
- whether convexity is ordinary `ConvexOn` on the closed half-line, midpoint convexity, or a
  source-specific difference condition;
- whether nonnegativity, monotonicity, or integrability is assumed, derived, or absent;
- whether the limit is at positive infinity or in absolute value and how endpoint behavior at zero
  is stated;
- whether the conclusion gives only a probability distribution, an absolutely continuous law, a
  density formula, or allows an atom, and whether symmetry is stated or derived;
- the Fourier sign and normalization convention used by the conclusion.

Pinned mathlib does provide the relevant representation primitives: `MeasureTheory.charFun` is
defined in `Mathlib.MeasureTheory.Measure.CharacteristicFunction.Basic`, and real characteristic
functions use `integral x, exp (t * x * I)`. It also provides `ConvexOn` and probability measures.
Those APIs do not resolve which human proposition the source selects. Writing a declaration with
one guessed combination would invent or substitute mathematics, even if Lean accepted its type.

Accordingly no `Statement.lean`, canonical expression hash, minimal-import claim, transport,
mutation suite, or Lean elaboration receipt is emitted. No `sorry`, axiom, assumed characteristic
function, weakened special case, or broadened theorem was introduced. Machine state remains `M4`;
statement acceptance and theorem completion are false.

## Pinned environment and checks

- Validation date: 2026-07-12 (Asia/Shanghai).
- Lean toolchain: `leanprover/lean4:v4.29.0`; Lean 4.29.0, commit
  `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- Lake: `5.0.0-src+98dc76e`.
- Pinned mathlib revision: `8a178386ffc0f5fef0b77738bb5449d50efeea95`.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

Commands ran inside this worker clone. The canonical `.lake` tree was only read through the
existing worker symlink; no update, build, clone, or fetch command was used.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1022` | 0 | rank 498, planned, L0/rework-required, theorem incomplete |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0 at the commit recorded above |
| `cd Formalizations/Lean && lake --version` | 0 | Lake version recorded above |
| `cd Formalizations/Lean && sha256sum lean-toolchain lake-manifest.json` | 0 | produced the two hashes recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | produced the pinned mathlib revision recorded above |
| focused repository search for Polya and convex characteristic-function statements | 0 | found only the metadata entry and this intake dossier; no source-frozen proposition or Lean target for `THM-M-1022` |
| focused pinned-mathlib search for Polya or a convexity-to-`charFun` theorem | 1 | no theorem-specific match (`rg` exit 1 means no match) |
| pinned-mathlib inspection of `CharacteristicFunction/Basic.lean` | 0 | confirmed `charFun` and the real convention `exp (t * x * I)` |
| OpenAlex API lookup of `W1562638189` | 0 | confirmed author, year, pages 115--123, and Project Euclid identifier; no full text |
| Project Euclid landing/PDF/JSON/XML endpoint probes for `1166219202` | 0 | HTTP 200 responses contained about 1 KB of anti-automation HTML, not the article |

There is no applicable `lake env lean <target>.lean` command: the exact source proposition needed
to create that target is the failed gate. Elaborating a guessed type would not be valid statement
evidence.

## Retry condition

An accountable source review must inspect an immutable copy of the primary article, select the
exact theorem/page, check definitions and errata, and freeze every assumption and conclusion choice
listed above. The subsequent statement run can then crosswalk those components to
`MeasureTheory.charFun`, `ProbabilityMeasure` (or `Measure` plus `IsProbabilityMeasure`), and the
selected convexity encoding; minimize imports; fingerprint the elaborated expression; and run
removed-hypothesis, changed-domain, binder-scope, and boundary mutation tests.

The assigned phase is not genuinely self-tested to its completion gate, so no
`.stage1-worker-selftest.json` is emitted.
