# Exact-statement gate: blocked

Item: `S56-M-1297-STATEMENT`  
Theorem: `THM-M-1297`  
Base revision: `3bb2bb303df87d54d8d5dfafcee61ad3c329e278`

## Decision

No exact Lean 4 target can be truthfully elaborated from the authoritative repository record. The
complete mathematical content supplied for this target is the title "Sobolev space interpolation"
and the phrase "Besov spaces and Triebel-Lizorkin spaces." The record has no formula, primary-source
pinpoint, inspected theorem text, definitions, or errata record. The two books listed by intake are
explicitly discovery candidates only; neither has been selected or inspected as the canonical
source statement.

Those phrases describe several inequivalent theorem families. In particular, they do not fix:

- real versus complex interpolation, or the interpolation parameter and fine index;
- homogeneous versus inhomogeneous Sobolev/Bessel-potential, Besov, or Triebel-Lizorkin spaces;
- the ambient Euclidean, periodic, bounded, or extension domain and scalar field;
- smoothness and integrability indices, endpoint exclusions, or quasi-Banach restrictions;
- equality with equivalent norms versus one-way continuous embedding; or
- quotient conventions, zero-function behavior, and other boundary cases.

Each choice changes domains, ordered binders, hypotheses, or the conclusion. Selecting a familiar
Sobolev log-convexity inequality, an abstract interpolation-space theorem, or one particular
Besov/Triebel-Lizorkin identity would therefore substitute a nearby theorem rather than elaborate
the exact catalog claim. Encoding an API whose fields assume the desired identity would be fake
statement evidence.

Rev-5.6 sections 0.1 and 5 require a hard stop when the source statement cannot be identified
without inventing missing mathematics. The canonical human claim fails before minimal imports,
normalized expression fingerprinting, checked transports, and removed-hypothesis, changed-domain,
binder-scope, and boundary-case mutations can be meaningful. No Lean declaration, axiom,
placeholder, weakened special case, or broadened target was introduced. Machine debt remains `M4`;
statement acceptance, audit completion, and theorem completion remain false.

## Pinned environment and scoped checks

Commands ran in this worker clone on 2026-07-12 (Asia/Shanghai). The pre-existing
`Formalizations/Lean/.lake` symlink points to the canonical pinned artifacts and was used read-only.
No Lake update, build, dependency clone, fetch, or `.lake` mutation was performed.

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
| `python3 scripts/stage1_target.py show THM-M-1297` | 0 | rank 465, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0 at the commit recorded above |
| `cd Formalizations/Lean && lake --version` | 0 | Lake version recorded above |
| `cd Formalizations/Lean && sha256sum lean-toolchain lake-manifest.json` | 0 | produced the two hashes recorded above |
| `git -C "$(readlink -f Formalizations/Lean/.lake/packages/mathlib)" rev-parse HEAD` | 0 | produced the pinned mathlib revision recorded above |
| repository `rg` search for the target ID, Chinese title/content, English title, and candidate books | 0 | found only underspecified metadata, intake artifacts, the execution schedule, and a neighboring independent target; no source-frozen proposition |
| pinned-mathlib `rg` search for Besov, Triebel-Lizorkin, and Sobolev interpolation terms | 1 | no matching Lean declaration or function-space API (`rg` exit 1 means no match) |

There is no applicable `lake env lean <target>.lean` command because no exact expression exists.
Elaborating an arbitrarily chosen interpretation would be false evidence rather than the assigned
deliverable.

## Retry condition

An accountable source review must select an immutable primary-source edition and exact
theorem/page, inspect errata, and freeze the interpolation functor, every space and normalization,
domain, scalar field, indices, endpoint restrictions, ordered quantifiers, hypotheses, conclusion,
and boundary conventions. It must also explain how the selected root corresponds to both the
"Sobolev space interpolation" title and the Besov/Triebel-Lizorkin content phrase. A later statement
run can then encode that exact proposition with minimal pinned imports, serialize its elaborated
expression and environment, compile all credited transports, and execute the four required mutation
classes.

The assigned phase is not genuinely self-tested to its completion gate, so no
`.stage1-worker-selftest.json` is emitted.
