# Intake validation record

## Scope

This record covers only `S56-M-0249-INTAKE`: target membership, the fail-closed `planned` instance,
the theorem dossier, scope map, source-statement crosswalk, six-task open DAG, and a discovery-only
pinned Lean API probe. It is nonrelease evidence from an isolated dirty worker clone. The
automation-provided untracked `Formalizations/Lean/.lake` symlink was used read-only; no `lake
update`, `lake build`, dependency clone or fetch, or other `.lake` mutation was run.

The exact-statement gate remains blocked because the catalog omits connected complement,
holomorphicity on the interior, and the exact uniform-approximation encoding. Secondary source
leads recover the standard family but do not satisfy the primary-source `H0` contract. That honest
downstream blocker does not prevent a self-tested planned intake. The provisional receipt still
awaits master acceptance.

## Environment

- Repository base: `c6fd6dad8fcfe5fd464416cd452f50286b546978`
- Repository tree: `5a80b61d8fa09336779f8d1453dcfe4299c9472f`
- Lean: `4.29.0`, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`
- Lake: `5.0.0-src+98dc76e`
- Mathlib revision: `8a178386ffc0f5fef0b77738bb5449d50efeea95`
- Mathlib tree: `bdc39a3123201dae413a9d9be56ec242c19e5c2b`
- Platform: Linux x86_64
- Validation date: 2026-07-13, Asia/Shanghai

## Commands and results

All commands ran from the repository root unless another working directory is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0249` | 0 | rank 1259, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `git status --short --untracked-files=all` | 0 | before edits, only the automation-provided `Formalizations/Lean/.lake` symlink was untracked |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree above |
| `git blame -L 1794,1799 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `sed -n '1794,1799p' Docs/researches/math_theorems.md \| sha256sum` | 0 | catalog block SHA-256 `a8d668ef213f9a0973388c042b122b39e7208b47bf86cc1b07380cd98c89b105` |
| inspection of *Encyclopedia of Mathematics*, `Mergelyan theorem`, revision 32115 | 0 | standard statement and 1951/1952 primary bibliography located; secondary lead only |
| inspection of arXiv:1501.00247v1 PDF, page 1, Theorem A | 0 | versioned standard epsilon-form statement located; PDF SHA-256 `19270fa85fa42a7042b41e946ec8171cfc7f4c2a73c5db61550b691298f2bdc1`; H1 lead only |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | Lean and Lake versions agree with the fingerprint above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | pinned mathlib revision and tree above |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | 0 | empty output; pinned package worktree clean |
| bounded exact-topic `rg` over repo-local Lean and pinned mathlib | 1 | expected no match for Mergelyan or the connected-complement complex-polynomial target; intake discovery only |
| bounded adjacent-candidate `rg` in pinned mathlib | 0 | real Weierstrass and complex star-closure results found and classified as non-substitutes |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0249/IntakeProbe.lean)` | 0 | eleven adjacent topology, analytic, polynomial, and continuous-map APIs elaborated; stdout SHA-256 `297e6dd65a55cb54bfc752cb25b0834af367be9130b08f851010b3d5acb3b7e4`; no target theorem declared |
| `python3 -m json.tool` on the three owned JSON files and root worker packet | 0 | all structured artifacts parsed after finalization |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0249-pycache python3 -m py_compile Stage1_Instances/THM-M-0249/check_intake.py` | 0 | scoped validator compiled without generated files in the owned path |
| `python3 -B Stage1_Instances/THM-M-0249/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | target/DAG identity, source and dependency pins, null exact target, H1/M4/R4 boundary, artifact hashes, provisional packet, and six open tasks agree |
| prohibited-construct `rg` over `IntakeProbe.lean` | 1 | expected no match; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| scoped no-index whitespace checks plus `git diff --check` | 0 | no whitespace diagnostics in changed files |

The two acceptance-relevant structured recipes in `intake-receipt.json` use a denied-network
policy. Network observations above are source discovery only and receive no source-acceptance or
machine-proof credit.

## Known open gates

An immutable admitted primary edition, precise theorem and incorporated-definition locators,
translation and errata audit, every omitted hypothesis, exact binder and boundary-case mapping,
and independent source review remain open. So do the canonical Lean expression, minimal imports,
environment and expression fingerprints, checked transports, statement mutations, exhaustive
formal-candidate audit, discovery protocol, obligation registry, typed graphs, proof and
composition, trust and provenance closure, readable reconstruction, hermetic replay,
deterministic evidence bundle, independent verification, master acceptance, audit completion, and
theorem completion. These open gates do not invalidate a truthful self-tested `planned` intake.
