# Exact-statement gate: blocked

Item: `S56-M-1323-STATEMENT`  
Theorem: `THM-M-1323`  
Base revision: `1cad5fb04b4f845438a8105579b15a830b03b7e7`

## Decision

No exact Lean 4 target can be truthfully elaborated from the authoritative repository record. The
record supplies only the title "eigenvalue comparison theorem" and the gloss "comparison of
eigenvalues of different domains." It supplies no primary source, operator, boundary condition,
domain class, eigenvalue construction, indexing convention, or inequality. The `已验证` label is
explicitly untrusted under rev-5.6.

The intake dossier provisionally interprets the phrase as domain monotonicity for variational
Dirichlet-Laplacian eigenvalues on nested bounded open Euclidean domains. It also explicitly marks
that interpretation as pending primary-source and statement review. The repository evidence does
not select it over materially different possibilities, including:

- Dirichlet, Neumann, Robin, mixed-boundary, or another operator spectrum;
- ordinary set inclusion, an embedding, a geometric deformation, or unrelated domains;
- Euclidean domains or domains in a Riemannian manifold;
- individual eigenvalues, the first eigenvalue, spectral gaps, or counting functions;
- variational eigenvalues under compact-resolvent assumptions or another spectral convention;
- weak or strict comparison, its direction, multiplicity policy, and zero- or one-based indexing.

Each choice changes the proposition's domains, binders, hypotheses, or conclusion. In particular,
elaborating the intake's plausible Dirichlet candidate would convert a provisional interpretation
into an invented canonical root. An abstract predicate that assumes an eigenvalue function and the
desired comparison would merely restate the result and would not elaborate the source theorem.

Consequently the gate fails before minimal imports, an exact declaration, an elaborated-expression
hash, checked alternate transports, or meaningful removed-hypothesis, changed-domain,
binder-scope, and boundary mutations can be established. No Lean declaration, `sorry`, axiom,
placeholder, special case, broadened target, or substituted theorem was introduced. Machine state
remains `M4`; statement acceptance and theorem completion are false.

## Pinned environment and validation

- Validation date: 2026-07-12 (Asia/Shanghai).
- Lean toolchain: `leanprover/lean4:v4.29.0`; Lean 4.29.0, commit
  `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- Lake: `5.0.0-src+98dc76e`.
- Pinned mathlib revision: `8a178386ffc0f5fef0b77738bb5449d50efeea95`.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

Commands ran inside this worker clone. The canonical pinned `.lake` artifacts were read only; no
update, build, clone, or fetch command was used.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1323` | 0 | Rank 485, planned, legacy artifacts unaccepted, theorem incomplete |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0 at the commit recorded above |
| `cd Formalizations/Lean && lake --version` | 0 | Lake version recorded above |
| `cd Formalizations/Lean && sha256sum lean-toolchain lake-manifest.json` | 0 | Produced the two hashes recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | Produced the pinned mathlib revision recorded above |
| repository `rg` search for the Chinese title/gloss and the provisional Dirichlet interpretation | 0 | Found only the underspecified metadata, target-list projections, and this dossier; no source-frozen proposition or legacy formal target |
| pinned-mathlib `rg` search for domain monotonicity, Dirichlet eigenvalues, eigenvalue comparison, and Laplacian eigenvalues | 1 | No matching theorem-specific API (`rg` exit 1 means no match) |
| `git diff --check -- Stage1_Instances/THM-M-1323` | 0 | No whitespace errors |

There is no applicable `lake env lean <target>.lean` check because no exact target exists.
Compiling the provisional interpretation would be false statement-gate evidence rather than the
assigned deliverable.

## Retry condition

An accountable review must select an immutable primary-source edition and exact theorem/page,
resolve errata, and freeze the operator, boundary condition, ambient space, domain assumptions,
comparison relation, eigenvalue construction, multiplicity/index convention, inequality, and all
degenerate cases. It must either accept the intake's provisional Dirichlet domain-monotonicity
reading or correct it without crossing into the separately scheduled Cheng comparison target
`THM-M-1324`. A later statement run can then elaborate the exact expression with minimal pinned
imports, fingerprint it, add checked transports, and run the required structural mutations.

The assigned phase is not genuinely self-tested to its completion gate, so no
`.stage1-worker-selftest.json` is emitted.
