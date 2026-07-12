# Exact-statement gate: blocked

Item: `S56-M-1302-STATEMENT`  
Theorem: `THM-M-1302`  
Base revision: `d106a271df55889c00fab33c3ecbdcc7f1d21bd1`

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the authoritative repository record.
Its entire mathematical wording is the title "paradifferential operator" and the gloss "a tool
for nonlinear PDE", attributed to Jean-Michel Bony in 1981. This identifies a construction or
theory, not a proposition with ordered binders, hypotheses, and a conclusion. The historical
`已验证` value is untrusted metadata and supplies neither a mathematical statement nor kernel
evidence.

The intake identifies Bony's 1981 article, *Calcul symbolique et propagation des singularités pour
les équations aux dérivées partielles non linéaires*, only at discovery level. No inspected theorem
or definition-plus-property pinpoint fixes:

- the base domain, Fourier transform normalization, or frequency cutoffs;
- the quantization convention and definition of the operator;
- the symbol class, orders, type estimates, and regularity parameters;
- the source and target function or distribution spaces;
- whether the root is a mapping estimate, symbolic-composition formula, adjoint result,
  ellipticity/parametrix result, or paralinearization theorem;
- endpoint, support, proper-support, or degenerate-case assumptions.

These choices yield materially different propositions. Selecting one convenient boundedness
estimate or symbolic-calculus identity would substitute a narrower theorem for the catalog topic.
Using Bony's paraproduct decomposition would additionally merge this record with the neighboring
target `THM-M-1301`. An abstract structure that stores the desired property would not repair the
identity failure.

Consequently the canonical human claim fails before minimal imports can be determined. There is no
honest Lean declaration or expression to serialize, no elaborated-expression hash, no checked
alternate transport, and no meaningful removed-hypothesis, changed-domain, binder-scope, or
boundary mutation suite. Machine state remains `M4`; statement acceptance and theorem completion
are false. No proof mechanism, assumed target property, weakened special case, or broadened target
was introduced.

## Pinned environment and search

Commands ran in this worker clone on 2026-07-12 (Asia/Shanghai). The canonical `.lake` directory
was read only; no update, build, clone, or fetch command was used.

- Lean toolchain: `leanprover/lean4:v4.29.0`; Lean 4.29.0 at commit
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
| `python3 scripts/stage1_target.py show THM-M-1302` | 0 | Rank 470, planned, legacy artifacts unaccepted, theorem incomplete |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean version and commit recorded above |
| `cd Formalizations/Lean && lake --version` | 0 | Lake version recorded above |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | Produced the two hashes recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | Produced the pinned mathlib revision recorded above |
| Repository `rg` search for the Chinese title/gloss, `paradifferential`, `pseudodifferential`, and the candidate article title | 0 | Found the underspecified source metadata, this intake dossier, and unrelated legacy discovery text; no source-frozen proposition for this target |
| Pinned-mathlib `rg` search for paradifferential operators, pseudodifferential operators, paraproducts, Littlewood-Paley theory, symbol classes, and Hormander terminology | 1 | No matching source declaration (`rg` exit 1 means no match) |

There is no applicable `lake env lean <target>.lean` validation because an exact target expression
does not exist. Elaborating an invented interface would be false statement evidence rather than
the assigned deliverable.

## Retry condition

An accountable source review must select an immutable primary-source edition and exact theorem or
definition-plus-property page, check surrounding definitions and errata, and freeze every domain,
cutoff, quantization, symbol-class, regularity, space, hypothesis, conclusion, and boundary
convention listed above. It must explain why that proposition is the intended identity of this
catalog record and distinguish it from `THM-M-1301`. A later statement run can then encode the
source-faithful expression, minimize pinned imports, fingerprint its elaboration and environment,
compile any transports, and run all four structural mutation classes.

This artifact records the first failed gate. It does not complete the statement node, accept a
receipt, alter the execution DAG, or claim audit/theorem completion. The assigned phase is not
genuinely self-tested to its completion gate, so no `.stage1-worker-selftest.json` is emitted.
