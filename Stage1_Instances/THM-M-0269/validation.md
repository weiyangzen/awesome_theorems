# Intake validation

Base revision: `c2e294becadae6ce784f27ee69f2e8dbf57e0b30`; base tree:
`3f567e7f76b189432b73444354070c0ff75925b9`.

Validation ran on 2026-07-13 (Asia/Shanghai) in the isolated worker clone. It covers target
membership, the planned dossier and open task DAG, repository-source provenance, modern and
historical source discovery, JSON and scoped invariants, a narrow pinned Lean interface/axiom
probe, bounded formal search, prohibited-construct hygiene, and whitespace. It does not validate a
canonical theorem statement or proof.

The preflight worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts. It was used read-only. No
`lake update`, `lake build`, dependency clone or fetch, network-triggering Lake operation, or other
`.lake` mutation was performed. The owned intake files and root worker packet make the final tree
dirty and nonrelease.

## Source boundary

The uncited catalog record was traced to its introduction commit. Axler's open-access current
author PDF was inspected at Theorem 3.11 and its complete proof on printed page 78; the author
page and current errata were also inspected. The source is a close modern match, but it is not
admitted as H0 because the repository did not cite it, no independent reviewer accepted the map,
and historical source identity remains unresolved.

Crossref and Zenodo metadata plus the CC0 scan identify Lebesgue's 1902 *Integrale, Longueur,
Aire*. A bounded OCR and page inspection did not pinpoint the modern monotone convergence theorem.
Pinned mathlib calls the result the Beppo Levi lemma. The historical work therefore remains a
bibliographic lead and attribution blocker rather than a source-statement proof crosswalk.

## Environment fingerprint

- Platform: Linux `7.0.0-27-generic`, x86_64, Asia/Shanghai.
- Lean: `4.29.0`, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- Lake: `5.0.0-src+98dc76e`.
- Pinned mathlib: `8a178386ffc0f5fef0b77738bb5449d50efeea95`; tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`.
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
| `python3 scripts/stage1_target.py show THM-M-0269` | 0 | rank 1276; planned; no legacy slot; legacy artifacts unaccepted; theorem_complete false |
| initial `git status --short --untracked-files=all` | 0 | only `?? Formalizations/Lean/.lake`; preserved read-only |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree shown above |
| `git blame -L 1936,1941 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `curl -L --fail --silent --show-error https://measure.axler.net/ -o /tmp/thm-m-0269-axler-final.html`, the analogous `MIRA.pdf` and `errata1e.html` commands, then `sha256sum` | 0 | fresh downloads reproduce SHA-256 `f0a9ae06...55d36`, `7a7ab07f...fb4e`, and `20d3f842...9fb8`; network discovery only, not a hermetic receipt |
| author page/PDF/errata inspection for Axler, *Measure, Integration & Real Analysis* | 0 | open-access current PDF SHA-256 `7a7ab07f...fb4e`; Theorem 3.11 and complete proof inspected on printed page 78; no theorem-changing erratum located; not independently reviewed H0 evidence |
| `curl -L --fail --silent --show-error https://api.crossref.org/works/10.1007/BF02420592 -o /tmp/thm-m-0269-crossref-final.json`, analogous Zenodo metadata/PDF commands, then `sha256sum` | 0 | fresh downloads reproduce metadata hashes `14ecc707...00ac`, `4f830924...37f3`, and scan hash `046ba2cc...0893`; network discovery only |
| Crossref DOI `10.1007/BF02420592`, Zenodo record 2313710, and bounded scan inspection | 0 | Lebesgue 1902 metadata and CC0 scan SHA-256 `046ba2cc...0893` authenticated; exact modern MCT passage not located, so only a historical lead |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | Lean and Lake versions agree with the fingerprint; no update or build was run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned mathlib revision/tree above; package worktree clean |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0269/IntakeProbe.lean)` | 0 | seven direct/related monotone-convergence interfaces elaborated; four candidate axiom reports are `propext`, `Classical.choice`, and `Quot.sound`; output SHA-256 `089904c4...fb9a` |
| bounded exact-topic `rg` over repo-local Lean and pinned mathlib | 0 | located the explicit monotone-convergence module, ENNReal/AE/limit/directed variants, a real-valued corollary, and docs indices; no source-identical root transport credited |
| `python3 -m json.tool` on all structured owned artifacts and `.stage1-worker-selftest.json` | 0 | all structured artifacts parse after finalization |
| Python `ast.parse` on `Stage1_Instances/THM-M-0269/check_intake.py` | 0 | scoped validator parses without writing bytecode |
| `python3 -B Stage1_Instances/THM-M-0269/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | target identity, source/dependency hashes, planned H1/M3/R4 boundary, null target, exact inventory, receipt/packet, Lean output, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-0269/check_intake.py` | 0 | pre-integration worker replay mode passes without the scheduler-only root packet; integration must review the explicit `ALLOW_INTEGRATED_HEAD` boundary before post-merge replay |
| prohibited Lean proof-escape scan over the owned path | 1 (expected no match) | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration in the API-only probe; diagnostic `#print axioms` is permitted |
| per-file `git diff --no-index --check /dev/null` for every owned file and the worker packet | 0 aggregate | no whitespace diagnostics; no-index exit 1 for each new file is only the expected new-file difference |
| `git diff --check -- Stage1_Instances/THM-M-0269 .stage1-worker-selftest.json` | 0 | tracked-diff command emitted no diagnostics; untracked-file coverage comes from the preceding no-index checks |

## Known downstream failures

- An independently approved exact source identity, historical attribution, formulation, definition
  chain, proof boundary, source-to-node map, and H0 review remain open.
- The root does not yet freeze the measure space, value type, positivity, measurability, pointwise
  versus AE monotonicity, supremum versus explicit limit, integral codomain, binders, or boundary
  cases.
- No canonical Lean expression, exact minimal imports, expression/environment fingerprint,
  checked alternate encoding, or required statement mutation is frozen.
- Formal anchor/provenance audit, discovery and obligation freezes, typed graphs, proof,
  composition, trust closure, readable reconstruction, hermetic replay, deterministic bundle,
  independent release verification, and master acceptance remain open.

These failures prevent statement, audit-completion, and theorem-completion claims. They do not
invalidate a truthful, self-tested `planned` intake whose purpose is to preserve the source scope
and open work. Only the integration lane may accept the provisional receipt.
