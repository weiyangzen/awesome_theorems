# THM-M-0236 intake validation

Base revision: `c6fd6dad8fcfe5fd464416cd452f50286b546978` (tree
`5a80b61d8fa09336779f8d1453dcfe4299c9472f`). Validation date: 2026-07-13
(Asia/Shanghai).

This validation covers target membership, the planned dossier, exact catalog boundary, two
source-supported formulation branches, a textbook section locator, the six-node open task DAG,
structured intake invariants, and a narrow pinned Lean candidate probe. It does not validate a
canonical monodromy statement or target proof because the source formulation and analytic bridges
are not frozen. The automation-provided canonical `.lake` link existed before intake and was used
read-only; no dependency update, build, clone, fetch, or other `.lake` mutation was performed.
This dirty worker run is nonrelease evidence.

## Environment

- Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, target
  `x86_64-unknown-linux-gnu`.
- Lake `5.0.0-src+98dc76e` on Linux x86_64.
- Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; package source status was clean before and after
  the probe.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Source discovery boundary

The permanent Encyclopedia of Mathematics revision 36520 was retrieved to `/tmp`, inspected, and
hashed. It supplies exact secondary wording for the homotopy-invariance and simply-connected
branches, not a primary proof or H0 source review. Springer's public front matter for Conway's
*Functions of One Complex Variable I* was likewise retrieved to `/tmp`; its table of contents
locates the relevant Chapter IX sections at pages 213, 217, 227, and 245. The theorem and proof
pages were not available or inspected. No downloaded source was added to the repository.

## Commands and results

All repository commands ran at the repository root unless `cwd` is shown.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0236` | exit 0; rank 1248, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `git status --short --untracked-files=all` (preflight) | exit 0; only the automation-provided untracked `Formalizations/Lean/.lake` link existed before intake |
| `git rev-parse HEAD 'HEAD^{tree}'` | exit 0; base revision and tree match this record |
| `git blame -L 1703,1708 -- Docs/researches/math_theorems.md` | exit 0; all six uncited catalog fields originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| retrieval and inspection of Encyclopedia of Mathematics oldid 36520 | exit 0; 15,989-byte HTML SHA-256 `650a8625f7689c69ba125e06589a232579a528896ea9b36b78b4073a1cd72ed1`; two formulations and bibliography inspected; secondary discovery only |
| retrieval and inspection of Springer front matter for DOI `10.1007/978-1-4612-6313-5` | exit 0; 13-page, 1,116,975-byte PDF SHA-256 `39977896558b0a427fe78ce2fc5a52e0bd72d5bd4f87b17a674d57de1615f332`; exact Chapter IX section/page locators inspected, not theorem or proof text |
| `sha256sum` over authority inputs, catalog/Stage0 excerpts, toolchain/lockfile, pinned homotopy-lifting source, and owned intake inputs | exit 0; exact hashes are recorded in `instance.json` and the provisional receipt |
| `(cd Formalizations/Lean && lake env lean --version)` | exit 0; Lean version and target recorded above |
| `(cd Formalizations/Lean && lake --version)` | exit 0; Lake version recorded above; no update or build was run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | exit 0; pinned revision and tree recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | exit 0 before and after probe; empty output |
| bounded search for monodromy theorem and analytic-continuation-along-path patterns in repo-local Lean and pinned mathlib | exit 0; three exact-topic lines, all the abstract mathlib theorem/docstring; output SHA-256 `69dff3ada8c8fed8b422e3a9ea458ac22f02d4c10aec303f7f49581a011cc966`; intake discovery only, not a global absence or completed anchor audit |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0236/IntakeProbe.lean)` | exit 0; three adjacent pinned declarations elaborated and the abstract candidate reported `[propext, Classical.choice, Quot.sound]`; stdout SHA-256 `0efdb83aabf8679f06ff10f26d3a099a69f3c78382c5756cafe4d13ed9b0efbc`, empty stderr; no target theorem declared |
| `python3 -m json.tool` on `instance.json`, `task-dag.json`, `intake-receipt.json`, and `.stage1-worker-selftest.json` | exit 0 for each after finalization |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0236-pycache python3 -m py_compile Stage1_Instances/THM-M-0236/check_intake.py` | exit 0; scoped validator compiled without adding generated files to the owned path |
| `python3 -B Stage1_Instances/THM-M-0236/check_intake.py --worker-packet .stage1-worker-selftest.json` | exit 0 after finalization; authority/DAG identity and hashes, null target, H1/M4/R4 boundary, exact artifact inventory, receipt/packet, and six open tasks agree |
| `rg -n -e '\bsorry\b' -e '\badmit\b' -e '\bsorryAx\b' -e '^[[:space:]]*(axiom\|constant\|opaque\|unsafe)[[:space:]]' Stage1_Instances/THM-M-0236 --glob '*.lean'` | exit 1 as expected; no prohibited declaration in the discovery-only probe |
| `git diff --check`, plus `git diff --no-index --check /dev/null <file>` for every untracked changed file | exit 0 for whitespace diagnostics; every changed file passed |

The printed candidate axiom report describes a pinned abstract theorem only. It does not select
the foundation profile, prove source identity, instantiate analytic germs, or close the target.

## Known open gates

A lawful immutable theorem-and-proof source, exact formulation and incorporated definitions,
complete assumption/conclusion/proof-boundary/errata crosswalk, independent review, analytic domain
and germ model, continuation and homotopy conventions, and all boundary cases remain open. So do
the canonical Lean target and minimal imports, expression/environment fingerprints, checked
transports and mutations, analytic etale-space and continuation-to-lift bridges, exhaustive formal
candidate audit, obligation registry, typed graphs, proof and composition, source/provenance/trust
closure, readable reconstruction, hermetic replay, deterministic bundle, independent verification,
master acceptance, audit completion, and theorem completion. These gates do not invalidate a
truthful self-tested `planned` intake.
