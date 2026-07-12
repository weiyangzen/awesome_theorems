# Anchor audit

Item: `S56-M-0559-ANCHOR_AUDIT`

Audit snapshot: repository base `9898022a0eed3cf9fb3c55a6affb6176224f33cf`; Lean
`v4.29.0`; mathlib `8a178386ffc0f5fef0b77738bb5449d50efeea95`. The mathlib revision is the
immutable revision already present in the canonical `lake-manifest.json`; this audit did not update
or fetch a dependency.

## Search protocol

The audit searched, in order:

1. the target dossier and repository Lean files;
2. every Lean source under the already pinned `.lake/packages` tree, using case-insensitive terms
   `whitehead`, `weak homotopy equivalence`, `WeakHomotopy`, and `IsWeak.*Homotopy`;
3. GitHub repository discovery for Lean projects using `Whitehead theorem`, `homotopy group`, and
   `CW complex`, followed by immutable-source inspection of the directly relevant repository.

The complete pinned mathlib source search found only the candidates below. Substrate-name hits in
`Topology/CWComplex/Classical/Basic.lean` and `Topology/Homotopy/LocallyContractible.lean` are
documentation references, not theorem declarations.

The exact source-discovery commands were:

```bash
rg -n -i "whitehead|weak homotopy equival|WeakHomotopy|IsWeak.*Homotopy" \
  Formalizations/Lean/.lake/packages -g '*.lean'
curl -L --fail --silent --show-error \
  https://codeload.github.com/jzxia/WhiteheadTheorem/tar.gz/ee1d4a5c332e6b95853bfa0719efd9f435317307 \
  -o "$tmp/a.tgz"
tar -xzf "$tmp/a.tgz" -C "$tmp"
sha256sum "$tmp/a.tgz"
rg -n -i "theorem.*whitehead|whitehead|weak.*equiv|homotopyEquiv|HomotopyEquiv" \
  "$tmp/WhiteheadTheorem-ee1d4a5c332e6b95853bfa0719efd9f435317307" -g '*.lean'
rg -n '^[[:space:]]*(axiom|unsafe|sorry|admit)\\b|:=\\s*(sorry|by\\s+admit)\\b|\\b(sorryAx)\\b' \
  "$tmp/WhiteheadTheorem-ee1d4a5c332e6b95853bfa0719efd9f435317307" -g '*.lean'
```

The first command exited zero with the inventory described below. Download, extraction, checksum,
and declaration search exited zero. The final scan exited zero because it found one occurrence of
`sorry` inside a commented-out declaration; manual context inspection confirmed it was inactive.

## Candidate inventory

| Candidate | Immutable identity | Exact declaration/type result | Provenance and feasibility | Verdict |
|---|---|---|---|---|
| mathlib model-category Whitehead theorem | mathlib `8a178386ffc0f5fef0b77738bb5449d50efeea95`, `Mathlib/AlgebraicTopology/ModelCategory/Homotopy.lean:216` | `RightHomotopyClass.whitehead`: a weak equivalence between bifibrant objects has a two-sided right-homotopy inverse; left version at line 231 | Local proof body in pinned mathlib. `AnchorAudit.lean` elaborates its full interface. It uses abstract `ModelCategory`, `WeakEquivalence`, cofibrancy/fibrancy, and categorical homotopy relations. No checked bridge from topological CW complexes or the target's homotopy-group predicate is present. | useful architecture anchor; not an exact target and no M0 credit |
| pinned topology/CW substrate | same mathlib revision; `Mathlib/Topology/CWComplex/Classical/Basic`, `Topology/Homotopy/HomotopyGroup`, `Topology/Homotopy/Equiv` | supplies `Topology.CWComplex`, `HomotopyGroup.Pi`, and `ContinuousMap.HomotopyEquiv`; no topology-level Whitehead declaration found | Already integrated and elaborated. It supports the canonical statement but provides no terminal proof body. | substrate only |
| `jzxia/WhiteheadTheorem` | commit `ee1d4a5c332e6b95853bfa0719efd9f435317307`; source archive SHA-256 `4faf267fd0ce760ca4db88240fec8782278d9fa2e28977b2c70fd54c9a291023` | `WhiteheadTheorem/Basic.lean:36`, `WhiteheadTheorem (X Y : CWComplex) (f : X ⟶ Y) : IsWeakHomotopyEquiv f.hom → IsHomotopyEquiv f.hom` | Lean `v4.21.0-rc3`, mathlib `2239a8d321747551f090ee416301afcf1b434321`, Apache-2.0. The inspected archive has a local proof body and no active `sorry`, `admit`, `axiom`, `sorryAx`, or `unsafe` declaration (one `sorry` occurs only in commented code). It defines its own sequential-colimit `CWComplex`, restricts both spaces to one universe, assumes `Nonempty X`, and defines weak equivalence as bijectivity of its induced map for every natural dimension. It is not a dependency of this repository, and its old mathlib API is not checked against the pinned current environment. | credible external proof anchor, but anchor-only and statement/integration bridges remain open |

The external theorem is the closest candidate, but it cannot be reported as the canonical theorem:
its CW-complex representation and induced homotopy map are project-local, its universe and empty-space
scope differ, and there is no checked equivalence between its weak-equivalence predicate and
`Stage1Instances.THM_M_0559.IsWeakHomotopyEquivalence`. Importing it would also require a deliberate,
pinned dependency integration and compatibility port, which this worker phase may not manufacture by
fetching into `.lake`.

## Classification and next cut

The audit is complete for this phase but does not close the theorem audit or proof. Human debt stays
`H3`: primary theorem/page/assumption/errata verification is outside this anchor phase. Machine debt
stays `M4`: the canonical proposition elaborates, but no exact repo-integrated proof body exists.
Readability debt stays `R4`. The next phase must model at least these bridge obligations: reconcile
the two CW representations, reconcile weak-equivalence definitions including components/dimension
zero, transport the given forward map and homotopies, handle universe and empty-space scope, or build
a direct proof using the pinned topology API.

Status boundary: this is a worker-self-tested immutable candidate audit only. It grants neither
external proof credit nor `AUDIT-Z`, `M0`, or theorem completion.
