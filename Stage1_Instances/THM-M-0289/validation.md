# Intake validation

Base revision: `f294137feee7840fd105a4d3f6073d5cf45508ea`.

This validation covers manifest and authoritative-DAG identity, planned dossier structure, JSON
integrity, repository and duplicate source boundaries, bibliographic discovery, a bounded pinned
mathlib name search, and a narrow Lean API probe. Because neither the repository nor an inspected
source supplies an exact formula, no canonical target, expression hash, mutation result, source
acceptance, or proof is claimed.

The automation-provided canonical `.lake` symlink and pinned artifacts were used read-only. No
dependency update, build, clone, fetch, or `.lake` mutation was performed. The untracked symlink is
a scheduler-provided input outside this target's owned path, so this is nonrelease worker evidence.

## Environment

- Repository base tree: `234b8f273d252c2c42ce6860315ed973049c871a`.
- Lean: 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, target
  `x86_64-unknown-linux-gnu`.
- Mathlib revision: `8a178386ffc0f5fef0b77738bb5449d50efeea95`; tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`.
- `lean-toolchain` SHA-256: `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Commands and results

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; all 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, and execution skill presence passed |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0289` | exit 0; rank 1295, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `git status --short --untracked-files=all` | preflight exit 0; only the automation-provided untracked `Formalizations/Lean/.lake` symlink existed before this intake |
| `git rev-parse HEAD 'HEAD^{tree}'` | exit 0; base revision and tree recorded above |
| `git blame -L 2076,2081 -- Docs/researches/math_theorems.md` | exit 0; all six uncited target lines originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `git blame -L 2675,2680 -- Docs/researches/math_theorems.md` | exit 0; the probable duplicate `THM-M-0368` lines originate at the same commit |
| Crossref request for DOI `10.1007/BF02547518` | exit 0; Hardy/Littlewood, article title, *Acta Mathematica* 54, 1930, pages 81-116, and DOI agreed; response SHA-256 `07fe6dcb...1ff8dc` |
| direct Project Euclid and Springer article-PDF requests | requests returned anti-bot/access HTML instead of a PDF; no source text was inspected or credited |
| `(cd Formalizations/Lean && lake env lean --version)` | exit 0; Lean identity recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | exit 0; pinned revision and tree recorded above; package status was clean |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0289/IntakeProbe.lean)` | exit 0; six adjacent pinned measure, ball, integral, Besicovitch, and Vitali APIs elaborated; stdout SHA-256 `5ca1eab2...01ccd` |
| bounded exact-topic `rg` search in pinned mathlib | exit 1, expected no-match; no Hardy-Littlewood maximal-function definition or weak-type theorem was found |
| corresponding search in repo-local Lean and `THM-M-0368` | exit 0 only for an unrelated Birkhoff maximal-function metadata phrase; no target declaration or proof body was found |
| immutable raw inspection of `fpvandoorn/carleson@fdcce451.../HardyLittlewood.lean` | exit 0; uncentered `maximalFunction` and `hasWeakType_maximalFunction_one` located; source SHA-256 `a6658e...28d22`; uncredited formal lead only |
| GitHub immutable commit, content, license, and Actions API inspection | exit 0; Lean `v4.30.0-rc2`, mathlib `1a4917a...`, Apache-2.0, and successful build/lint run `27613659124` recorded; no local rebuild or M0 claim |
| `python3 -m json.tool` on the three JSON artifacts and root worker packet | exit 0 for each after finalization |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0289-pycache python3 -m py_compile Stage1_Instances/THM-M-0289/check_intake.py` | exit 0; the checker compiled without adding generated files to the owned path |
| `python3 -B Stage1_Instances/THM-M-0289/check_intake.py --worker-packet .stage1-worker-selftest.json` | exit 0; authority identity, null exact target, H1/M4/R4 boundary, source, duplicate, and external-candidate pins, exact artifact inventory and hashes, provisional receipt/packet, and six open tasks agree |
| prohibited Lean construct scan over the owned path | exit 1, expected no match for `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declarations |
| scoped `git diff --check` plus checker newline/whitespace checks | exit 0; no whitespace errors in tracked or untracked owned artifacts |

## Known open gates

An immutable source copy and pinpoint statement/proof inspection, comprehensive errata audit,
proposition-level definition/premise/conclusion/proof crosswalk, `THM-M-0368` duplicate
reconciliation, and independent source review remain open. So do the exact Lean target, minimal
imports, expression and environment fingerprints, checked transports, four statement mutation
classes, exhaustive anchor audit of the external candidate, compatibility/integration, terminal
provenance and trust closure, discovery and obligation freezes, typed graphs, proof and
composition, trust and provenance closure, readable reconstruction, hermetic replay, deterministic
bundle, independent verification, and master acceptance. These failures prevent downstream and
theorem completion but do not invalidate a truthful self-tested `planned` intake.
