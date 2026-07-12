# Intake validation

Base revision: `d502dd6f3d278ca9cb0ead8cbdc5f16c0e1fd8c9` (tree
`829a47c47ae831cada4f8acc6c2c00ba5883215e`). Validation ran on 2026-07-13 in
the isolated worker clone.

Validation is limited to target-set consistency, dossier structure and scope invariants, source
provenance and discrimination, pinned environment identity, a narrow Lean API probe, bounded local
searches, proof-escape hygiene, and whitespace. The source wording is not a proposition, so
elaborating a purported canonical Lean target would invent missing mathematics. `IntakeProbe.lean`
therefore checks only possible substrate; it introduces no theorem and supplies no statement or
proof credit.

The preflight worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts. It was used read-only. No
`lake update`, `lake build`, dependency clone or fetch, or other `.lake` mutation was performed.
This is nonrelease worker evidence.

## Environment fingerprint

- Platform: Linux 7.0.0-27-generic, x86_64; worker timezone `Asia/Shanghai`.
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
| `python3 scripts/stage1_target.py show THM-M-1391` | 0 | rank 1001, planned, L0/rework_required, no legacy slot, legacy artifacts unaccepted, theorem_complete false |
| `git status --short --untracked-files=all` (preflight) | 0 | only pre-existing automation symlink `Formalizations/Lean/.lake`; preserved read-only |
| `git blame -L 10132,10137 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog fields originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `sed -n '10132,10137p' Docs/researches/math_theorems.md \| sha256sum` | 0 | exact catalog block SHA-256 `779ee22f53ab010e61ea8181ec3ffdce38f3f185ae3bd0d87555b44f78f90af3` |
| Crossref query for DOI `10.1007/BF01206624` and Springer article metadata inspection | 0 | Heinz Pruefer, exact title, *Mathematische Annalen* 95(1), pp. 499-518, December 1926; bibliographic identity only |
| GDZ article-range manifest and PDF inspection for volume `PPN235181684_0095`, range `LOG_0033` | 0 | 21-page article PDF SHA-256 `d452d9b2eb170c0505030457dbdec688bf2c739262ec2747bb4af6eb821b2f67`; printed pp. 499 and 502-505 inspected; no source admitted or H0 credited |
| Teschl *Ordinary Differential Equations and Dynamical Systems* and errata inspection | 0 | modern regular formulation and variants compared; PDF SHA-256 `362433156525216abf596c17ce843204510e96d57afa4284a37c7aa5a9ffc36e`, errata SHA-256 `3eacbac5b8fc762c5d3f21183cba3ae638b9ac5fbe703cc52cf2857b9605996e`; no canonical-root selection or source credit |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | Lean and Lake versions agree with the fingerprint; no update or build was run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned revision and tree above; package worktree clean |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1391/IntakeProbe.lean)` | 0 | eighteen generic ODE, derivative, polar-coordinate, argument-continuity, and quotient-angle APIs elaborated; complete output SHA-256 `68584c0aad837fd65c6e07d09dc40e19102ea81d1e39e312be21f90fa6a62117`; no target declaration |
| bounded Pruefer/Sturm-Liouville name search over repo-local and pinned-mathlib `*.lean` | 0 | only an unrelated Pruefer subgroup, Pruefer-domain TODO, its import, and one repo planning string; no transform declaration; intake discovery only |
| bounded derivative-of-argument and continuous angle/path lift searches in pinned mathlib | 1/0 | no argument derivative; broad lift search found only unrelated lift APIs and quotient definitions, no solution-curve real phase lift; intake discovery only |
| `python3 -m json.tool` on the three owned JSON files and `.stage1-worker-selftest.json` | 0 | instance, open task DAG, provisional receipt, and worker handoff are valid JSON |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-1391-pycache python3 -m py_compile Stage1_Instances/THM-M-1391/check_intake.py` | 0 | scoped validator compiles without adding generated files to the owned path |
| `python3 -B Stage1_Instances/THM-M-1391/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | manifest/item identity, pinned inputs, planned H5/M4/R4 boundary, null target, artifact hashes, handoff, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-1391/check_intake.py` | 0 | public replay mode passes without the scheduler-only worker packet |
| prohibited Lean proof-escape scan over `Stage1_Instances/THM-M-1391` | 1 | expected no-match result; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| scoped `git diff --check` plus no-index checks for every untracked changed file | 0 | no whitespace diagnostics |

## Known downstream failures

- The catalog wording is not a stable proposition. No approved correction selects the exact
  construction, equations, equivalence direction, zero or phase result, oscillation theorem, or
  spectral/expansion consequence.
- The historical scan and modern formulation have not received a complete transcription,
  translation, definition/assumption/conclusion/proof-node/errata mapping or independent review.
- No canonical Lean expression, expression/environment hash, exact statement imports, checked
  alternate encoding, or statement mutation test exists.
- Discovery protocol, exhaustive anchor audit, obligation registry and typed graphs, proof,
  composition and trust checks, readable reconstruction, hermetic replay, deterministic evidence
  bundle, and independent release verification are open.

These failures prevent statement, audit, and theorem-completion claims. They do not invalidate a
truthful, self-tested `planned` intake whose purpose is to freeze the honest ambiguity boundary and
open DAG. Only the integration lane may accept the provisional worker receipt.
