# Intake validation

Base revision: `bd81d4853a030765585ef6fed4310484ceb1e458` (tree
`fb92fc7476bff9a2ce8c20f1d7be34c6655ca6b4`). Validation ran on 2026-07-13 in the isolated
worker clone, timezone `Asia/Shanghai`.

Validation is limited to target-set consistency, dossier structure and scope invariants, repository
source provenance, historical-source discovery, pinned environment identity, a narrow Lean
candidate probe, bounded local discovery, JSON integrity, proof-escape hygiene, and whitespace. The
catalog gloss does not determine one exact Fubini formulation, so no canonical Lean target was
invented. The candidate probe supplies statement/interface feasibility evidence only.

The preflight worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts. It was used read-only. No
`lake update`, `lake build`, dependency clone or fetch, or other `.lake` mutation was performed.
This is nonrelease worker evidence.

## Environment fingerprint

- Platform: Linux `7.0.0-27-generic` x86_64.
- Lean: `4.29.0`, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- Lake: `5.0.0-src+98dc76e`.
- Pinned mathlib: revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; package worktree clean.
- `Formalizations/Lean/lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `Formalizations/Lean/lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.
- Pinned `Mathlib/MeasureTheory/Integral/Prod.lean` SHA-256:
  `3f695c14e45e3e97e28df9e90bd6db4d0283ced3db5572c67ca67f4297f0e1f9`.

## Commands and results

| Command (repository root unless noted) | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok`; 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0271` | 0 | rank 1278, planned, L0/rework_required, no legacy slot, legacy artifacts unaccepted, theorem_complete false |
| `git status --short --untracked-files=all` before edits | 0 | only the pre-existing automation-provided `Formalizations/Lean/.lake` symlink; preserved read-only |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree above |
| `git blame -L 1950,1955 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `sed -n '1950,1955p' Docs/researches/math_theorems.md \| sha256sum` | 0 | exact catalog excerpt SHA-256 `f239e4051b0aa5458e4b7d28fa46091cbc3cce1918f6d4f56a9f15c8a8734e20` |
| `curl -L --fail --max-time 30 -sS 'https://api.zbmath.org/v1/document/2643959' -o /tmp/thm-m-0271-zbmath.json` plus `wc`, `sha256sum`, and `jq` inspection | 0 | 2,132-byte response, SHA-256 `ef765b200e1067b5818c1a0ca8e6d5c2bf51e051df511ac3ab9fa4595fc2186c`; Fubini 1907 paper identity and contemporary German statement review inspected; secondary source lead only |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | Lean and Lake versions above; no update or build was run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}' 'HEAD:Mathlib/MeasureTheory/Integral/Prod.lean'` and package status | 0 | pinned revision/tree above; source blob `184104dac5a7787740bde1cd69a420699274b81a`; package worktree clean |
| `rg -n -i --glob '*.lean' 'theorem integral_prod\|integral_integral_swap\|Fubini.s theorem\|fubini theorem' Formalizations/Lean/AwesomeTheorems Formalizations/Lean/.lake/packages/mathlib/Mathlib/MeasureTheory/Integral/Prod.lean` | 0 | bounded search located the pinned candidate family and no repo-local target-owned Fubini declaration; intake discovery only |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0271/IntakeProbe.lean)` | 0 | ten representative candidate signatures elaborated; three axiom reports each list `propext`, `Classical.choice`, `Quot.sound`; complete output SHA-256 `f11c2335158b8a4a5dba42d5601e820a1914f182432a420148704d7e7d31ef83`; no target declaration |
| `python3 -m json.tool` separately on `instance.json`, `task-dag.json`, finalized `intake-receipt.json`, and `.stage1-worker-selftest.json` | 0 | all structured artifacts are valid JSON |
| path-free Python `compile(...)` syntax check on `Stage1_Instances/THM-M-0271/check_intake.py` | 0 | scoped validator syntax is valid without adding generated files to the owned path |
| `python3 -B Stage1_Instances/THM-M-0271/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | manifest/DAG identity, source and dependency hashes, planned H1/M3/R4 boundary, null target, exact artifact inventory, packet, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-0271/check_intake.py` | 0 | public replay mode passes without requiring the scheduler-only worker packet |
| prohibited Lean proof-escape scan over `Stage1_Instances/THM-M-0271` | 1 | expected no-match result; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration in the API-only probe |
| scoped `git diff --check` plus no-index checks for every untracked changed file | 0 | no whitespace diagnostics |

## Known downstream failures

- No immutable primary copy of Fubini's 1907 paper, exact Italian theorem and incorporated
  definitions, complete proof boundary, corrections or errata audit, or independent source review
  is accepted. The inspected zbMATH/JFM record is a strong secondary historical lead only.
- The catalog does not select integral model, region or product measure, scalar or Banach codomain,
  completeness, measure finiteness, measurability/integrability package, exceptional sections,
  product-to-iterated or order-swap conclusion, binders, hypotheses, or boundary cases.
- No canonical Lean expression, exact minimal import claim, expression/environment fingerprint,
  checked alternate encoding, or required statement mutation exists. Strong pinned candidates and
  axiom reports support `M3` feasibility only; exact target match and proof credit are not claimed.
- Formal anchor and terminal-body audit, discovery protocol, obligation registry and typed graphs,
  proof, composition, full provenance and trust closure, source-faithful readable reconstruction,
  hermetic replay, deterministic evidence bundle, and independent release verification remain open.
- Master acceptance remains pending.

These failures prevent statement, audit, and theorem-completion claims. They do not invalidate a
truthful, self-tested `planned` intake whose purpose is to freeze the theorem-family boundary,
candidate crosswalk, and open task DAG. Only the integration lane may accept the provisional worker
receipt.
