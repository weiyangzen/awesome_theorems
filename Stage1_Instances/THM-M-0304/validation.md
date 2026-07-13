# Intake validation

Base revision: `d257e1e5e5fa003d6e1f26344c0331bf99374fa9`; base tree:
`fa06b50b528e038d182d5479a18296f63fa5eae5`.

Validation ran on 2026-07-13 (Asia/Shanghai) in the isolated worker clone. It covers target
membership, the planned dossier and open task DAG, repository and same-gloss target provenance,
bibliographic original/correction leads, JSON and scoped invariants, a narrow pinned Lean API probe,
a bounded local formal search, prohibited-construct hygiene, and whitespace. It does not validate
a canonical theorem statement or proof.

The preflight worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts. It was used read-only. No
`lake update`, `lake build`, dependency clone or fetch, network-triggering Lake operation, or other
`.lake` mutation was performed. The owned intake files and root worker packet make the final tree
dirty and nonrelease.

## Source boundary

The catalog record was traced to its uncited introduction commit. Crossref metadata identifies
Morrey's 1940 paper and a 1942 correction whose title expressly refers to the 1940 paper. Project
Euclid blocked both bodies in this worker environment, so no theorem, formula, definitions, proof,
or correction content was inspected. The same catalog gloss is separately retained as
`THM-M-1242`. The intake therefore freezes the ambiguity, correction requirement, and ownership
boundary rather than selecting or borrowing a familiar theorem.

## Environment fingerprint

- Platform: Linux `7.0.0-27-generic`, x86_64, Asia/Shanghai.
- Lean: `4.29.0`, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- Lake: `5.0.0-src+98dc76e`.
- Pinned mathlib: `8a178386ffc0f5fef0b77738bb5449d50efeea95`; tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; package worktree clean.
- `Formalizations/Lean/lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `Formalizations/Lean/lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Commands and results

All repository commands ran from the repository root unless a different `cwd` is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0304` | 0 | rank 1306; planned; no legacy slot; legacy artifacts unaccepted; theorem_complete false |
| initial `git status --short --untracked-files=all` | 0 | only `?? Formalizations/Lean/.lake`; preserved read-only |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree shown above |
| `git blame -L 2181,2186 -- Docs/researches/math_theorems.md` | 0 | all six uncited target lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `git blame -L 9087,9092 -- Docs/researches/math_theorems.md` | 0 | the six same-gloss `THM-M-1242` source lines originate at the same commit |
| Crossref work query for DOI `10.1215/S0012-7094-40-00615-9` | 0 | Morrey, original title, Duke Math. J. 6(1), 1940, DOI and publisher locator confirmed; response SHA-256 `b17843ec...a76a` |
| Crossref work query for DOI `10.1215/S0012-7094-42-00911-6` | 0 | Morrey, explicit correction title, Duke Math. J. 9(1), 1942, DOI and publisher locator confirmed; response SHA-256 `e6c7cb78...68ff` |
| Project Euclid download attempts for both DOIs plus `file` | 0 HTTP transport | each response was a roughly 1 KB Incapsula HTML denial, not a source PDF; no source-content or H0 credit |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | Lean and Lake versions agree with the fingerprint; no update or build was run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned mathlib revision/tree above; package worktree clean |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0304/IntakeProbe.lean)` | 0 | five smooth-function derivative-norm inequalities and two Holder interfaces elaborated; output SHA-256 `328a4d40...b27225`; no target theorem declared |
| bounded exact-topic `rg` over repo-local Lean and pinned mathlib | 0 only for boundary prose and Rademacher comments | no target-specific Morrey-Sobolev declaration; this is intake discovery, not an exhaustive anchor audit |
| `python3 -m json.tool` on all structured owned artifacts and `.stage1-worker-selftest.json` | 0 after finalization | all structured artifacts parse |
| Python `ast.parse` on `Stage1_Instances/THM-M-0304/check_intake.py` | 0 | scoped validator parses without writing bytecode |
| `python3 -B Stage1_Instances/THM-M-0304/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 after finalization | target identity, planned H5/M4/R4 boundary, null formal target, source/neighbor hashes, exact inventory, packet, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-0304/check_intake.py` | 0 after finalization | public replay mode passes without the scheduler-only root packet |
| prohibited Lean proof-escape scan over the owned path | 1 (expected no match) | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration in the API-only probe |
| per-file `git diff --no-index --check /dev/null` for every owned file and worker packet | 0 aggregate | no whitespace diagnostics; each no-index exit 1 is only the expected new-file content difference |
| `git diff --check -- Stage1_Instances/THM-M-0304 .stage1-worker-selftest.json` | 0 | no tracked whitespace diagnostics; untracked-file coverage comes from the preceding per-file checks |

## Known downstream failures

- No approved immutable original or modern source text, exact theorem and definition locators,
  correction-content audit, source-to-node map, proof boundary, or independent H review exists.
- The identity, variant, and proof-ownership relationship with `THM-M-1242` remains open.
- Domain, dimension, differentiability order, exponent and endpoints, Sobolev model, value space,
  representative, Holder exponent and scope, quantitative estimate, constants, binders, and boundary
  cases remain open.
- No canonical Lean expression, exact imports, expression/environment fingerprint, checked
  alternate encoding, or required statement mutation is frozen.
- Formal anchor audit, discovery and obligation freezes, typed graphs, proof, composition, trust
  closure, readable reconstruction, hermetic replay, deterministic bundle, independent release
  verification, and master acceptance remain open.

These failures prevent statement, audit-completion, and theorem-completion claims. They do not
invalidate a truthful, self-tested `planned` intake whose purpose is to preserve ambiguity and open
work. Only the integration lane may accept the provisional receipt.
