# THM-M-0045 anchor-audit validation

Item: `S56-M-0045-ANCHOR_AUDIT`  
Base revision: `c76fe0f1a7514b41f191d16840eff25e64ee9d17` (tree
`388bc991837bae9741d7e7cb88b43c216eab966a`)  
Validation date: 2026-07-13 (`Asia/Shanghai`)

## Result

Pinned mathlib at `8a178386ffc0f5fef0b77738bb5449d50efeea95` has the eigenvalue,
generalized-eigenspace, Gram-Schmidt triangularity, orthonormal-basis, unitary, and matrix APIs
needed for a future proof, but no declaration closing the exact Schur target. The retained
interfaces re-elaborate and report only `propext`, `Classical.choice`, and `Quot.sound`. The
Hermitian spectral theorem is also retained but classified `M5` for the unrestricted root because
its Hermitian hypothesis is a strict scope mismatch. The checked
adapter in `AnchorAudit.lean` proves that a unitary factorization
`A = U * T * star U` with upper-triangular `T` implies the target's exact
`BlockTriangular (star U * A * U) id` conclusion. It does not produce those witnesses.

The audit found an unusually strong external source candidate in the canonical mathlib Git object
store: remote-tracking ref `origin/kuotsanhsu.schur_triangulation`, immutable revision
`0a539f0ce764fd16726509b62ed7b870461070eb`, tree
`5da322f204f788b5eb2649c51fbfd54ffadb7265`. Its 300-line Apache-2.0 module defines unitary and
upper-triangular witnesses and proves `Matrix.schur_triangulation`. Specializing to `Complex` and
`Fin n`, then applying the checked adapter, has the exact mathematical scope of the frozen target.

This source anchor is not machine completion evidence. It uses Lean `v4.17.0-rc1`, diverges from
the current pin by 12,251 pinned-only and two candidate-only commits after their merge base, is absent from the lake-manifest closure, and
fails to elaborate against current mathlib because several APIs were removed or renamed. No
own-pin kernel/CI receipt, machine axiom report, parser-aware transitive placeholder/unsafe audit,
or terminal dependency closure was available. Its textual prohibited-token scan is only defensive.
It is therefore `M5`, not `M1`; the strongest evidence is `E3`. The exact root remains `M3` and
`[H1, M3, R4]`.

## Commands and exact outcomes

The automation-provided `.lake` symlink and already materialized Git objects were used read-only.
No Lake update/build, clone, fetch, checkout, package edit, or other dependency mutation occurred.

| Command | Exit | Outcome |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0045` | 0 | rank 1085, planned, L0/rework-required, theorem incomplete |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and status | 0 | immutable revision/tree `8a178386...` / `bdc39a31...`; worktree clean |
| repo-local and all-package `rg` alias queries | 0 | no exact declaration; one neighboring QR prose match only; result-list hashes recorded in the ledger |
| four Sourcegraph query families | 0 | exact aliases and API-shape queries completed with zero matches; substrate query completed with nine interface uses in three repositories; response hashes recorded |
| two GitHub repository queries | 0 | both complete with `total_count=0`; response SHA-256 `08c082fd...2600b2` |
| GitHub code-search query | 0 | HTTP 403 rate-limit denial; captured response SHA-256 `1db366a2...5e386e`; no negative claim |
| local `git log`, `show`, `rev-parse`, `merge-base`, and `rev-list` on candidate `0a539f0c...` | 0 | commit/tree/parent, exact module/declaration, pins, eight dependency revisions, source/blob/license hashes, and `2/12251` divergence recorded |
| candidate source prohibited-token scan | 0 | no textual `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe`; not credited as a transitive trust audit |
| `cd Formalizations/Lean && lake env lean /tmp/m0045-audit/SchurTriangulation.lean` | 1 | expected current-pin incompatibility: removed/renamed APIs and declaration collisions prevent the historical source from elaborating; no external kernel credit |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0045/Statement.lean` | 0 | exact frozen statement re-elaborated; expected `#check_failure` diagnostics and explicit target print only |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0045/AnchorAudit.lean` | 0 | seven retained interfaces and exact equation adapter kernel-checked; all six axiom reports exclude `sorryAx` |
| `python3 -B Stage1_Instances/THM-M-0045/check_anchor_audit.py --worker-packet .stage1-worker-selftest.json` | 0 | structured identities, hashes, pins, candidate classifications, receipt, and packet agree |
| `python3 -m json.tool` on four new structured artifacts and root packet | 0 | all JSON parsed |
| prohibited-token scan over `AnchorAudit.lean` | 1 | expected no-match exit |
| `git diff --check -- Stage1_Instances/THM-M-0045 .stage1-worker-selftest.json` | 0 | no whitespace errors |

## Open integration gate

Reopen the external candidate only after reproducing commit `0a539f0c` at its exact Lean and
manifest pins in an isolated permitted environment, obtaining kernel and transitive trust evidence,
then porting or pinning it and checking a wrapper to the exact target at this repository's pin. This
node finishes only the bounded formal-anchor inventory and classification pending master acceptance;
it supplies no proof, full-audit, or theorem-completion credit.
