# Intake validation

Base revision: `d05520867fab3367a9b61b9544c3e12241204f54` (tree
`fb2cfc62077d5b53e9938632cd6361dd60872067`). Validation date: 2026-07-13
(Asia/Shanghai).

This validation covers manifest membership, the planned dossier, the two-component scope boundary,
repository and bibliographic crosswalk, open downstream DAG, JSON/scoped invariants, and a narrow
pinned Lean API probe. It does not validate a canonical source statement or proof: exact primary
passages and the regular/CFL branch formulas have not been frozen. The automation-provided
canonical `.lake` symlink was pre-existing and used read-only; no dependency update, build, clone,
fetch, or other `.lake` mutation was performed. This dirty worker result is nonrelease evidence.

## Environment

- Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, target
  `x86_64-unknown-linux-gnu`.
- Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; its package worktree was clean.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Commands and results

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0761` | exit 0; rank 1347, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | pre-edit exit 0; only the automation-provided `Formalizations/Lean/.lake` symlink existed; base revision/tree recorded above |
| inspect the target manifest, execution node, repository math record, Stage0 projection, related computer-science records, and pinned mathlib DFA/CFG sources | exit 0; established a collective two-branch catalog claim, kept distinct-target ownership separate, and found one DFA-local proof candidate without transferring statement or proof credit |
| `curl -L --fail --silent --show-error 'https://api.crossref.org/works/10.1524/stuf.1961.14.14.143'` | exit 0; bibliographic metadata found for Bar-Hillel, Perles, and Shamir (1961), but no Crossref page field or theorem locator; response SHA-256 `afcb615b...a850` |
| `curl -L --fail --silent --show-error -o /tmp/bps1961.pdf 'https://www.degruyter.com/document/doi/10.1524/stuf.1961.14.14.143/pdf'` | curl exit 0 but returned a zero-byte body; rejected as primary-source evidence, so no passage, page-level component map, proof boundary, correction, or errata claim was recorded |
| `(cd Formalizations/Lean && lake env lean --version)` | exit 0; pinned Lean version and target recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | exit 0; pinned revision/tree recorded above; empty package status |
| `sha256sum` on pinned `Language.lean`, `DFA.lean`, and `ContextFreeGrammar.lean` | exit 0; respectively `f4c3964...8d2e`, `d311736c...d021`, and `d0e893c7...3f19` |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0761/IntakeProbe.lean)` | exit 0; fourteen adjacent pinned interfaces plus one prospective branch-container shape elaborated; no theorem or proof body declared; stdout SHA-256 `68b93232...8c64` |
| `rg -n -i '\bpumping\b|pump'` on pinned `DFA.lean` and `ContextFreeGrammar.lean` | exit 0; matches only the DFA documentation and declaration; bounded local name search gives no exhaustive absence or anchor-audit claim |
| `python3 -m json.tool` on `instance.json`, `task-dag.json`, `intake-receipt.json`, and the worker packet | exit 0 for each after finalization |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0761-pycache python3 -m py_compile Stage1_Instances/THM-M-0761/check_intake.py` | exit 0; scoped validator compiled without creating an owned generated file |
| `python3 -B Stage1_Instances/THM-M-0761/check_intake.py --worker-packet .stage1-worker-selftest.json` | exit 0 after finalization; target/DAG identity, null collective target, H1/M4/R4 boundary, artifact inventory, input hashes, worker packet, and six open tasks agree |
| `rg -n --glob '*.lean' '\b(sorry\|admit)\b\|\bsorryAx\b\|^[[:space:]]*(axiom\|constant\|opaque\|unsafe)[[:space:]]' Stage1_Instances/THM-M-0761` | exit 1 as expected for no match; no prohibited declaration or proof escape |
| `git diff --check -- Stage1_Instances/THM-M-0761 .stage1-worker-selftest.json` plus per-file `git diff --no-index --check /dev/null <new-file>` | exit 0 for the tracked check; every no-index command found only the expected new-file difference and no whitespace diagnostic |

The first draft of the discovery probe used nonexistent qualified constants `Language.mul` and
`Language.kstar`; Lean exited 1 with two unknown-identifier diagnostics. They were corrected to the
actual pinned declarations `Language.mul_def` and `Language.kstar_def`, and the exact final probe
then exited 0 as recorded above. The failed draft is retained here as validation history, not
hidden or counted as evidence. A later combined final-check command was also first launched from
`Formalizations/Lean`, so its repository-root-relative checker path was not found and Python exited
2. The checker and Lean recipe were immediately rerun separately from their recorded `cwd` values;
both exited 0. The path mistake supplies no evidence and does not change the recorded recipes.

## Known open gates

Immutable primary full text, exact proposition locators for both branches, complete incorporated
definitions, assumptions, conclusions, proof boundaries, corrections, errata, translations, and
independent source review remain open. So do the alphabet and language encodings, pumping-length
dependency order, three- and five-factor clauses, bounds, joint nonemptiness, exponent domain,
collective root representation, checked transports, boundary cases, canonical Lean expression and
environment fingerprints, semantic mutations, discovery protocol, obligation registry, typed
graphs, formal anchor and provenance audit, proof and composition, trust closure, readable
reconstruction, hermetic replay, deterministic evidence bundle, independent verification, master
acceptance, audit completion, and theorem completion. These failures do not invalidate a truthful,
self-tested `planned` intake.
