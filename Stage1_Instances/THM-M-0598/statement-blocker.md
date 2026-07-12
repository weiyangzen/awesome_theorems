# Exact-statement gate: blocked

Item: `S56-M-0598-STATEMENT`  
Theorem: `THM-M-0598`  
Base revision: `a1bd625c34bac608d64b423cf1ca0c9b6db6adb0`

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the authoritative repository record.
The complete mathematical wording is only "the topology of manifolds and the critical points of
smooth functions", under the label "Morse theory". This denotes a theory and a family of results,
not one proposition. The accepted intake therefore freezes only a provisional family and explicitly
leaves selection of the exact sourced root to this phase.

The intake names Morse's 1934 monograph and Milnor's 1963 monograph as bibliographic discovery
anchors, but no immutable edition, theorem/page, exact wording, incorporated definitions, errata,
or independent source review is present. Choosing the familiar sublevel-set theorem from memory
would invent the choices that the source record omits:

- whether the manifold is compact, closed, has boundary, or is noncompact with a proper function;
- the finite-dimensional smoothness and scalar conventions for the manifold and function;
- regular-value and endpoint conventions, and compactness of the critical band;
- whether a band has no critical points, one critical point, or one critical value containing
  several points;
- the Hessian, nondegeneracy, and Morse-index definitions;
- whether the conclusion is diffeomorphism, deformation retraction, homotopy equivalence, CW-cell
  attachment, or smooth handle attachment, including the attachment map and corner conventions;
- behavior at empty bands, extrema of index zero or full dimension, and boundary critical points.

These choices change the domains, binders, hypotheses, and conclusion. They also distinguish the
regular-interval theorem from the critical-level attachment theorem; silently conjoining both
would broaden the target. Morse inequalities (`THM-M-0599`), the Morse lemma (`THM-M-0600`), and a
general handle-decomposition theorem are separately scheduled claims and cannot substitute for
this root.

Consequently the phase fails at canonical human-claim identity, before a canonical Lean
expression, minimal imports, expression fingerprint, checked transports, or meaningful
removed-hypothesis, changed-domain, binder-scope, and boundary mutations can be established. No
Lean declaration, axiom, assumed attachment field, weakened special case, or broadened theorem was
introduced. Machine state remains `M4`; statement acceptance and theorem completion are false.

## Pinned environment and search

Commands ran inside this worker clone on 2026-07-12 (Asia/Shanghai). The existing canonical `.lake`
artifacts were read only; no update, build, clone, fetch, or dependency mutation was used.

- Lean toolchain: `leanprover/lean4:v4.29.0`; Lean 4.29.0, commit
  `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- Lake: `5.0.0-src+98dc76e`.
- Checked mathlib revision: `8a178386ffc0f5fef0b77738bb5449d50efeea95`.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0598` | 0 | Rank 636, planned, legacy artifacts unaccepted, theorem incomplete |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean version and commit recorded above |
| `cd Formalizations/Lean && lake --version` | 0 | Lake version recorded above |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | Produced the two hashes recorded above |
| `git -C "$(readlink -f Formalizations/Lean/.lake/packages/mathlib)" rev-parse HEAD` | 0 | Produced the pinned mathlib revision recorded above |
| repository `rg` search for the theorem ID, Chinese and English titles, gloss, and handle-attachment terminology | 0 | Found underspecified catalogue metadata and this intake dossier, but no source-frozen proposition or theorem-specific Lean target |
| pinned-mathlib `rg` search for Morse theory/functions/index, handle attachment, critical sublevels, and critical values | 0 | The only Morse-function API found concerns Galois groups of polynomials; no differential-topological Morse or handle-attachment target was identified |

There is no applicable `lake env lean <canonical-target>.lean` elaboration check because no exact
expression exists. Elaborating a remembered textbook variant or an abstract interface that assumes
the desired topological change would be fake statement evidence, not the assigned deliverable.

## Retry condition

An accountable source review must select an immutable primary-source edition and exact
theorem/page, dispose of corrections and errata, and freeze every manifold, function,
critical-band, nondegeneracy, index, attachment/equivalence, endpoint, and degenerate-case choice
listed above. A later statement run can then crosswalk that claim row by row, encode the exact Lean
expression, minimize pinned imports, fingerprint the elaboration and environment, check alternate
transports, and execute the four required mutation classes.

The assigned phase is not genuinely self-tested to its completion gate, so no
`.stage1-worker-selftest.json` is emitted. No downstream-node or theorem-completion credit is
claimed.
