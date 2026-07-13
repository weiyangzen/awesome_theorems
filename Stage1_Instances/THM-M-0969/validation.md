# Intake validation

Base revision: `fcabbf1e0ad9507eebe91663bccabfa87d22813e` (tree
`873e589c594454b7f263c7ed2342089a4d15e842`). Validation date: 2026-07-13
(Asia/Shanghai).

This validation covers the planned dossier, scope and source-statement boundary, open task DAG,
JSON and scoped invariants, and a narrow pinned Lean API probe. It does not validate a canonical
Lovasz-local-lemma statement or proof because neither has been frozen. The automation-provided
canonical `.lake` symlink was pre-existing and used read-only; no dependency update, build, clone,
fetch, or other `.lake` mutation was performed. The dirty worker evidence is nonrelease evidence.

## Environment

- Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, target
  `x86_64-unknown-linux-gnu`.
- Lake `5.0.0-src+98dc76e`.
- Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; package source status was clean.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Commands and results

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; all 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0969` | exit 0; rank 1503, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `git status --short --untracked-files=all` | preflight exit 0; only the automation-provided untracked `Formalizations/Lean/.lake` symlink existed before this intake |
| `git rev-parse HEAD 'HEAD^{tree}'` | exit 0; base revision and tree recorded above |
| `git blame -L 7078,7083 -- Docs/researches/math_theorems.md` | exit 0; all six uncited catalog lines originate at repository commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `stat -c '%s' /tmp/erdos-lovasz-1975.pdf && sha256sum /tmp/erdos-lovasz-1975.pdf && pdfinfo /tmp/erdos-lovasz-1975.pdf` | exit 0; complete 1,880,140-byte, 19-page PDF with SHA-256 `fc99b53c12d75066934e2f4e35c7189b35276f0a006af075010e01cffd74e2e0` |
| `pdftotext -layout /tmp/erdos-lovasz-1975.pdf /tmp/erdos-lovasz-1975-check.txt` plus page-image inspection of PDF page 8 | exit 0; Section 2, printed pp. 616-617 contains the finite `1/(4d)` candidate statement and its complement bars; source-family discovery only, no canonical selection or H0 acceptance |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | exit 0; versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | exit 0; pinned revision and tree recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | exit 0; empty output |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | exit 0; hashes recorded above |
| `rg -n -i --glob '*.lean' 'lov[aá]sz.?local\|lovász.?local\|lovasz.?local' Formalizations/Lean/.lake/packages/mathlib/Mathlib` | exit 1; expected no-match, with no exact local-lemma declaration found; bounded intake discovery, not an exhaustive anchor audit |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0969/IntakeProbe.lean)` | exit 0; thirteen adjacent pinned measurable-event, measure, intersection, independence, and finite-graph APIs elaborated; no target theorem declared |
| `python3 -m json.tool` on `instance.json`, `task-dag.json`, `intake-receipt.json`, and the root worker packet | exit 0 for each after finalization |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0969-pycache python3 -m py_compile Stage1_Instances/THM-M-0969/check_intake.py` | exit 0; scoped validator compiled without adding generated files to the owned path |
| `python3 -B Stage1_Instances/THM-M-0969/check_intake.py --worker-packet .stage1-worker-selftest.json` | exit 0; manifest and authoritative-DAG identity, null target, H1/M4/R4 boundary, source and environment pins, exact artifact inventory and hashes, receipt/worker packet, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-0969/check_intake.py` | exit 0; public replay mode passed without requiring the scheduler-only root packet |
| prohibited Lean construct scan over the owned path | exit 1; expected no match for `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` |
| scoped per-new-file whitespace checks plus `git diff --check` | exit 0; no whitespace errors |

## Known open gates

Canonical variant selection, admission of the inspected primary scan and exact proposition,
complete definition/premise/conclusion/proof-boundary/errata crosswalk, and independent source
review remain open. So do the canonical Lean expression and environment fingerprints,
checked transports, statement mutations, exhaustive formal anchor audit, discovery protocol,
obligation registry, typed graphs, proof and composition, trust and provenance closure, readable
reconstruction, hermetic replay, deterministic bundle, independent verification, master acceptance,
audit completion, and theorem completion. These failures do not invalidate a truthful self-tested
`planned` intake.
