# Intake validation

Base revision: `a8aba97a7ef2ff387e7814fe517e1b35524a04dc` (tree
`495e962862c2e7bc7c33c880c06fe39b2cb75db6`). Validation ran on 2026-07-13 in
the isolated worker clone.

Validation is limited to target-set consistency, dossier structure and scope invariants, source
provenance, bibliographic metadata discovery, pinned environment identity, a narrow Lean API probe,
a bounded local name search, proof-escape hygiene, JSON integrity, and whitespace. The source
wording is not a proposition, so elaborating a purported canonical target would invent missing
mathematics. `IntakeProbe.lean` therefore checks only generic substrate and supplies no statement
or proof credit.

The preflight worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts. It was used read-only. No
`lake update`, `lake build`, dependency clone or fetch, or other `.lake` mutation was performed.
This is nonrelease worker evidence.

## Environment fingerprint

- Platform: Linux x86_64; worker timezone `Asia/Shanghai`.
- Lean: `4.29.0`, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- Lake: `5.0.0-src+98dc76e`.
- Pinned mathlib: revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; package worktree clean.
- `Formalizations/Lean/lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `Formalizations/Lean/lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Commands and results

| Command (repository root unless noted) | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok`; 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0256` | 0 | rank 942, planned, L0/rework_required, no legacy slot, legacy artifacts unaccepted, theorem_complete false |
| `git status --short --untracked-files=all` (preflight) | 0 | only pre-existing automation symlink `Formalizations/Lean/.lake`; preserved read-only |
| `git blame -L 1843,1848 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `sed -n '1843,1848p' Docs/researches/math_theorems.md \| sha256sum` | 0 | exact catalog block SHA-256 `9a4df3af762ddb0ac5e0b89340e286bf0248d6b16a12b0245a6172f00faa5e07` |
| Crossref query and EMS publisher-page metadata inspection for DOI `10.4171/160-1/11` | 0 | secondary commentary identity and original 1940 work citation located; no primary theorem or H credit accepted |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | Lean and Lake versions agree with the fingerprint; no update or build was run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned revision and tree above; package worktree clean |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0256/IntakeProbe.lean)` | 0 | six generic pinned complex-manifold, group-action, orbit-relation, and quotient API checks elaborated; no target declaration |
| `rg -n -i --glob '*.lean' 'Teichm[uü]ller[ _-]+space\|TeichmullerSpace\|Riemann[ _-]+surface.{0,40}moduli\|moduli.{0,40}Riemann[ _-]+surface\|extremal.{0,20}quasiconformal\|quadratic[ _-]+differential.{0,40}Teichm' Formalizations/Lean/AwesomeTheorems Formalizations/Lean/.lake/packages/mathlib/Mathlib` | 1 | expected no-match result after excluding unrelated Teichmuller-Tukey and ring-theory namesakes; intake discovery only, not a complete anchor audit |
| `python3 -m json.tool` separately on `instance.json`, `task-dag.json`, `intake-receipt.json`, and `.stage1-worker-selftest.json` | 0 | instance, open task DAG, provisional receipt, and worker handoff are valid JSON |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0256-pycache python3 -m py_compile Stage1_Instances/THM-M-0256/check_intake.py` | 0 | scoped intake validator compiles without adding generated files to the owned path |
| `python3 Stage1_Instances/THM-M-0256/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | manifest/item identity, pinned inputs, planned H5/M4/R4 boundary, null target, artifact hashes, handoff, and six open downstream tasks agree |
| `rg -n --glob '*.lean' '\b(sorry\|admit)\b\|\bsorryAx\b\|^[[:space:]]*(axiom\|constant\|opaque)[[:space:]]\|^[[:space:]]*unsafe\b' Stage1_Instances/THM-M-0256` | 1 | expected no-match result; no proof escape declaration in the API-only probe |
| scoped `git diff --check` plus no-index checks for every untracked changed file | 0 | no whitespace diagnostics |

## Known downstream failures

- The catalog wording is not a stable proposition. No approved correction selects the surface
  category, marking, equivalence, quotient/moduli semantics, hypotheses, conclusion, or boundary
  cases.
- No independently reviewed immutable primary theorem, complete definition/assumption/proof/errata
  crosswalk, catalog-identity and date reconciliation, or theorem locator is accepted. The
  secondary commentary is discovery evidence only.
- No canonical Lean expression, expression/environment hash, exact imports, checked alternate
  encoding, or statement mutation test exists.
- Discovery protocol, anchor audit, obligation registry and typed graphs, proof, composition and
  trust checks, readable reconstruction, hermetic replay, deterministic evidence bundle, and
  independent release verification are open.

These failures prevent statement, audit, and theorem-completion claims. They do not invalidate a
truthful, self-tested `planned` intake whose purpose is to freeze the ambiguity boundary and open
DAG. Only the integration lane may accept the provisional worker receipt.
