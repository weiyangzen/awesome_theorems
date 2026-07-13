# Intake validation

Base revision: `fb0baac89ea0633612be3b47448464b4b8e4bef7` (tree
`018557070da18ea1733a82de81a238750c59aa84`). Validation date: 2026-07-13
(Asia/Shanghai).

This validation covers target membership, a fail-closed planned dossier and open task DAG, literal
catalog provenance, primary and secondary source-family discrimination, JSON and scoped invariants,
a narrow pinned Lean substrate probe, bounded formal discovery, prohibited-construct hygiene, and
whitespace. It does not validate an exact Vosper statement or proof because the primary article,
addendum, exact source root, and encoding decisions remain open.

The preflight worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts. It was used read-only. No
`lake update`, `lake build`, dependency clone or fetch, or other `.lake` mutation was performed.
The owned intake files and root worker packet make the final snapshot dirty and nonrelease.

## Source and environment inspection

- Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, target
  `x86_64-unknown-linux-gnu`; Lake `5.0.0-src+98dc76e`.
- Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; package source status was clean.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

Crossref metadata confirmed the original article DOI, April 1956 date, and pages 200-205, and the
addendum DOI, July 1956 date, and pages 280-282. The publisher route returned an access challenge;
the primary texts were not inspected. Boothby, DeVos, and Montejano's arXiv:1301.0095v2 was
retrieved to temporary storage only. Its 197,059-byte PDF has SHA-256
`641f3122cdce22d2358ed8f079c9e1d909f92d2ab53e62c64971f256663f38e8`; Theorem 1.3 and its
definitions were inspected as a secondary source. No external bytes were added to the repository
or accepted as H0.

## Commands and results

All repository commands ran from the repository root unless a different `cwd` is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0937` | 0 | rank 1476; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all` (preflight) | 0 | only `?? Formalizations/Lean/.lake`; preserved read-only |
| `git rev-parse HEAD HEAD^{tree}` | 0 | base revision and tree shown above |
| `git blame -L 6847,6852 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog fields originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| Stage0 history inspection at `c61be3c80710c07c5f7626e3404e51f40ecb39a6` | 0 | Vosper moved from pre-dedup `THM-M-0964` to current `THM-M-0937`; the old bare ID named Caucal, so provenance is bound to ID plus title and gloss |
| Crossref exact DOI queries for the original article and addendum | 0 | author, titles, journal, volume, issues, 1956 dates, pages, and DOIs confirmed; mutable discovery metadata only |
| publisher and Semantic Scholar access checks | mixed | publisher text-mining endpoint returned HTTP 400 empty body, DOI route returned HTTP 403 challenge, and Semantic Scholar reported closed access with no open PDF; primary text not inspected |
| `curl -L --fail --silent --show-error https://arxiv.org/pdf/1301.0095v2 -o /tmp/1301.0095v2.pdf` | 0 | secondary PDF retrieved outside the repository; 197059 bytes and SHA-256 `641f3122...8e8` |
| `pdftotext -layout /tmp/1301.0095v2.pdf /tmp/1301.txt` and scoped inspection | 0 | definitions and Theorem 1.3 on printed pages 1-3 inspected; four classification branches and references to both primary papers recorded |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean version, commit, and target recorded above |
| `(cd Formalizations/Lean && lake --version)` | 0 | Lake version above; no update or build run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` | 0 | pinned revision and tree recorded above; package status clean |
| bounded `rg` for Vosper, critical pairs, Cauchy-Davenport, sumsets, and arbitrary-length arithmetic progressions in repo-local Lean and pinned mathlib | 0 | exact forward Cauchy-Davenport theorem and adjacent APIs found; no named Vosper/inverse-classification target; intake discovery only |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0937/IntakeProbe.lean)` | 0 | eight adjacent finite-set, sumset, and Cauchy-Davenport API signatures elaborated; complete stdout SHA-256 `b604d21b...c421`; no target statement or proof body |
| `python3 -m json.tool` on all structured owned files and `.stage1-worker-selftest.json` | 0 each | valid JSON after finalization |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0937-pycache python3 -m py_compile Stage1_Instances/THM-M-0937/check_intake.py` | 0 | scoped validator compiled without generated files in the owned path |
| `python3 -B Stage1_Instances/THM-M-0937/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | target/DAG identity, source and dependency hashes, H1/M4/R4 null-target boundary, exact inventory, provisional receipt, packet, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-0937/check_intake.py` | 0 | public replay mode passed without the scheduler-only root packet |
| scoped Lean scan for `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declarations | 1 (expected no match) | no prohibited declaration in the discovery-only probe |
| per-new-file `git diff --no-index --check /dev/null FILE` and scoped `git diff --check` | 0 aggregate | no whitespace diagnostics; no-index exit 1 was accepted only as the expected new-file difference |

## Known open gates

Primary article and addendum access, lawful immutable preservation, exact root selection, full
critical-pair versus equality-case organization, finite-set carrier, exceptional branches,
progression and common-difference conventions, premise/proof-node mapping, corrections and errata,
neighbor ownership, and independent source approval remain open. So do canonical Lean elaboration,
minimal imports, expression/environment fingerprints, checked transports, all four mutation
classes, exhaustive anchor audit, discovery and obligation freezes, typed graphs, proof and
composition, trust closure, readable reconstruction, hermetic replay, deterministic bundle,
independent verification, and release.

These gates block the statement and theorem, but do not invalidate a truthful self-tested planned
intake. `H1` records a published complete proof family and an inspected exact secondary statement;
it does not grant H0.

## Status boundary

This is provisional worker self-test evidence for `S56-M-0937-INTAKE` only. It supports a planned
dossier and concrete statement blocker, not an accepted node receipt. No canonical statement,
H0 source closure, proof, audit completion, theorem completion, or master acceptance is claimed.
