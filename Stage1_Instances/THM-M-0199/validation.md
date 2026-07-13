# Intake validation

Base revision: `5fe11f4b5e32a06ffb4432460319fc8ae906fe7b` (tree
`64c5aacf7cf3eb79008f5a1970151e3e53cb9966`). Validation date: 2026-07-13
(Asia/Shanghai).

This validation covers target membership, the planned dossier, the exact catalog wording and
provenance, the source and non-substitution boundary, the open downstream DAG, structured intake
invariants, and a narrow pinned Lean substrate probe. It does not validate a canonical Menelaus
proposition or proof because none has been source-selected. The automation-provided canonical
`.lake` symlink was pre-existing and reused read-only. No dependency update, build, clone, fetch, or
other intentional `.lake` mutation was performed. This dirty worker run is nonrelease evidence.

## Environment

- Platform: Linux `7.0.0-27-generic` x86_64; timezone `Asia/Shanghai`.
- Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, target
  `x86_64-unknown-linux-gnu`.
- Lake `5.0.0-src+98dc76e`.
- Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; package source status was clean.
- `Formalizations/Lean/lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `Formalizations/Lean/lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Commands and results

| Command (repository root unless noted) | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0199` | 0 | rank 1531; planned; L0/rework_required; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all` before edits | 0 | only the pre-existing automation-provided `Formalizations/Lean/.lake` symlink; preserved read-only |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree above |
| `git blame -L 1436,1441 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `sed -n '1436,1441p' Docs/researches/math_theorems.md \| sha256sum` | 0 | exact catalog excerpt SHA-256 `49510ff1eb237d359de74c03be822b340b4e0b7f061ae1f12185b242d9910f5d` |
| `curl -L --fail --max-time 60 -o /tmp/thm-m-0199-mcconnell-1403.0478v1.pdf https://arxiv.org/pdf/1403.0478v1`, then `sha256sum`, `pdfinfo`, and `pdftotext -layout` | 0 | printed pages 1-2 define signed side ratios and state classical Menelaus as collinearity iff product `-1`; PDF SHA-256 `ba8ff135a0bb270547f94e3344b59b35de8c107265638f95537812c0e36a3b77`; retrieved 2026-07-13; server names v1 but PDF metadata/printed date say 2018-10-30, so only hash-bound current content, not original-2014 bytes, is claimed; H1 lead only |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | versions recorded above; no update or build run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | pinned revision and tree recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | 0 | empty output |
| `rg -n -i 'menelaus|menelaos|梅涅劳斯' Formalizations/Lean/AwesomeTheorems --glob '*.lean'`; repeat over `Formalizations/Lean/.lake/packages/mathlib/Mathlib`; then `git -C Formalizations/Lean/.lake/packages/mathlib log --all -SMenelaus --format='%H %cs %s' -- '*.lean'` | 1/1/0 | both source searches returned the expected no-match exit and Git history returned empty output; no repo-local or pinned-mathlib Menelaus declaration identified; neighboring Ceva source was separately found and rejected as a substitute |
| `sha256sum /tmp/MenelausTheorem.lean`, prohibited-construct `rg`, then `(cd Formalizations/Lean && lake env lean /tmp/MenelausProbe.lean)` | 0/1/0 | external `rjwalters/lean-genius@84b23f1...` source SHA-256 `605e0c25...`; 139 source lines; no prohibited construct; unmodified source plus axiom/type prints elaborated under repository pins; `menelaus` reports `propext`, `Classical.choice`, `Quot.sound`; output SHA-256 `48e922a4...`; unpinned, source-unapproved anchor lead only, no M credit |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0199/IntakeProbe.lean)` | 0 | eleven pinned affine-triangle, line-map, line-membership, collinearity, and neighboring Ceva interfaces elaborated; stdout SHA-256 `eae1118a6a36635eb8081636cae497bf279922ef628e34b2ecadfef89fd267a2`; no target theorem declared |
| `python3 -m json.tool` separately on `instance.json`, `task-dag.json`, finalized `intake-receipt.json`, and `.stage1-worker-selftest.json` | 0 | all structured artifacts are valid JSON |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0199-pycache python3 -m py_compile Stage1_Instances/THM-M-0199/check_intake.py` | 0 | scoped validator compiled without generated files in the owned path |
| `python3 -B Stage1_Instances/THM-M-0199/check_intake.py --run-lean --worker-packet .stage1-worker-selftest.json` | 0 | manifest/DAG identity, null target, H1/M4/R4 boundary, hashes, exact artifact inventory, provisional receipt/packet, six open tasks, and an internally rerun byte-for-byte Lean probe agree |
| `python3 -B Stage1_Instances/THM-M-0199/check_intake.py` | 0 | public replay mode passes without requiring the scheduler-only worker packet |
| prohibited Lean construct scan over `IntakeProbe.lean` | 1 | expected no-match result; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| scoped no-index whitespace checks plus `git diff --check` | 0 | no whitespace diagnostics |

## Known open gates

- No independently accepted source selects the exact triangle and side-point correspondence,
  directed-ratio orientation and sign, affine or projective domain, scalar assumptions, direction,
  denominator conditions, infinity convention, binders, or degenerate cases.
- The inspected modern statement is not cited by the catalog, is not a primary historical source,
  is not durably admitted here, and has no accepted definition/assumption/proof/errata crosswalk or
  independent review.
- No canonical Lean expression, minimal-import certificate, expression or environment fingerprint,
  checked alternate encoding, or statement mutation suite exists. The affine APIs and distinct
  Ceva body do not select or prove the root. The external coordinate proof is not a pinned
  repository dependency or source-approved transport and has not passed the later exhaustive
  provenance, trust, license, expression-identity, composition, and acceptance gates.
- Immutable anchor audit, discovery protocol, obligation registry and typed graphs, proof,
  composition, transitive provenance and trust closure, source-faithful reconstruction, hermetic
  replay, deterministic bundle, independent verification, and master acceptance remain open.

These failures block the statement and every completion claim. They do not invalidate a truthful,
self-tested `planned` intake whose purpose is to freeze the received scope and ambiguity boundary.
