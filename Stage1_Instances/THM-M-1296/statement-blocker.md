# Exact-statement gate: blocked

Item: `S56-M-1296-STATEMENT`  
Theorem: `THM-M-1296`  
Base revision: `8f4c72eeb09c3eab9ea2ef5a83d0bf48d59fdce6`

## Decision

No exact Lean 4 target can be truthfully elaborated from the authoritative repository record. The
record supplies only the label "profile decomposition", the gloss "decomposition of bounded
sequences", a twentieth-century date, and no author, source, theorem number, page, or exact
statement. The intake accordingly leaves the primary theorem unselected.

Profile decomposition is a family of inequivalent concentration-compactness results. The supplied
words do not determine:

- the ambient dimension, scalar field, function space, regularity, or exponent range;
- whether the space is homogeneous or inhomogeneous and which topology defines boundedness;
- the sequence indexing and exact subsequence/extraction quantifiers;
- the symmetry group, including translations, dilations, time translations, and normalization;
- the profile index set and exact pairwise parameter-orthogonality formula;
- the finite-partial-sum identity and the topology in which profiles are obtained;
- the norm or energy decoupling formula and whether it is an equality, asymptotic identity, or
  inequality;
- the weaker target norm, endpoint policy, and order of limits in remainder smallness;
- the conventions for zero profiles, finite decompositions, representatives, and measurability.

These choices change the domains, binders, hypotheses, and conclusion. Selecting a Sobolev
translation/dilation theorem associated with Solimini or Gerard, a dispersive time-translation
theorem, an abstract Hilbert-space decomposition, or a theorem that assumes the desired profiles
as structure fields would invent or substitute mathematics. The two papers listed in the intake
are explicitly discovery candidates whose exact theorem, page, hypotheses, definitions, and errata
have not been independently inspected. They therefore cannot resolve the identity of the claim.

The canonical human-claim identity gate fails before minimal imports, an elaborated expression
fingerprint, checked transports, or meaningful removed-hypothesis, changed-domain, binder-scope,
and boundary mutations can be established. No Lean declaration, axiom, placeholder, weakened
special case, broadened theorem, or assumed decomposition interface was introduced. Machine state
remains `M4`; statement acceptance, audit completion, and theorem completion are false.

## Pinned environment and search

- Validation date: 2026-07-12 (Asia/Shanghai).
- Lean toolchain: `leanprover/lean4:v4.29.0`; Lean 4.29.0, commit
  `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- Lake: `5.0.0-src+98dc76e`.
- Checked mathlib revision: `8a178386ffc0f5fef0b77738bb5449d50efeea95`.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

Commands ran inside this worker clone. The canonical `.lake` directory was used through the
existing read-only-style symlink; no update, build, clone, fetch, or other dependency mutation was
performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1296` | 0 | Rank 464, planned, legacy artifacts unaccepted, theorem incomplete |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0 at the commit recorded above |
| `cd Formalizations/Lean && lake --version` | 0 | Lake version recorded above |
| `cd Formalizations/Lean && sha256sum lean-toolchain lake-manifest.json` | 0 | Produced the two hashes recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | Produced the pinned mathlib revision recorded above |
| repository `rg` search for profile decomposition, concentration compactness, Solimini, and Gerard | 0 | Found the underspecified source metadata, related but separately owned concentration-compactness/bubble dossiers, and legacy discovery prose; no source-frozen proposition for this target |
| pinned-mathlib `rg` search for profile decomposition, linear profiles, concentration compactness, Solimini, Gerard, defect of compactness, and compact Sobolev results | 1 | No matching profile-decomposition API in pinned mathlib source (`rg` exit 1 means no match) |
| `git diff --check -- Stage1_Instances/THM-M-1296` | 0 | No whitespace errors before this record was added |

There is no applicable `lake env lean <target>.lean` check: an exact target expression does not
exist. Elaborating an arbitrary abstract interface or a selected special case would be false
statement evidence rather than the assigned deliverable.

## Retry condition

An accountable source review must select an immutable primary-source edition and exact
theorem/page, dispose of errata, and freeze every space, exponent, subsequence, symmetry,
orthogonality, decoupling, remainder, limit-order, and boundary convention listed above. It must
also distinguish the claim from the adjacent concentration-compactness and bubble-decomposition
targets. A later statement run can then encode the claim, minimize pinned imports, serialize and
hash its elaborated expression, compile checked transports, and run the required mutations.

The assigned phase is not genuinely self-tested to its completion gate, so no
`.stage1-worker-selftest.json` is emitted.
