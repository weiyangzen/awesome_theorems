# Intake validation

Base revision: `46a0f2a3ea74765a0467c489264b838ffbb70675`; base tree:
`7b1b5269d7da840fd086da731d6f92903c209c35`. Validation date: 2026-07-13
(`Asia/Shanghai`). No release-grade timing evidence is claimed.

This validation covers target membership, the planned dossier and open task DAG, literal repository
provenance, source-identity discrimination, structured scope invariants, a narrow pinned Lean
substrate probe, bounded repository/mathlib discovery, prohibited-construct hygiene, and
whitespace. It does not validate a canonical Andrews identity or proof because the catalog title,
source result, and binder-complete proposition remain unresolved.

The preflight worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts. It was used read-only. No
`lake update`, `lake build`, dependency clone or fetch, or other `.lake` mutation was performed.
The owned intake files and root worker packet make the final tree dirty and nonrelease.

## Environment

- Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, target
  `x86_64-unknown-linux-gnu`.
- Lake `5.0.0-src+98dc76e`.
- Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; package source status was clean before and after the
  probe.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Source discovery boundary

The six-field catalog record contains no bibliography, and all fields originate in repository
commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The title says "splitting" while the gloss says
"integer partition," and it supplies no formula or proposition.

The PubMed Central page images for George E. Andrews' 1974 PNAS paper were inspected transiently.
Theorem 1 on page 4082 is a multiple-series/product identity for odd moduli; pages 4083-4084 prove
it. This is the strongest source lead but not an admitted root. Crossref separately identifies the
1974 AMS Memoir *On the general Rogers-Ramanujan theorem*, so the author/year/topic tuple is not
unique. Exact source selection, full premise/formula/correction mapping, and independent review are
open. No external source file was added to the repository and no H0 credit is claimed.

## Commands and results

All repository commands ran from the repository root unless a different `cwd` is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0920` | 0 | rank 1462; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all` (preflight) | 0 | only `?? Formalizations/Lean/.lake`; preserved read-only |
| `git rev-parse HEAD HEAD^{tree}` | 0 | base revision and tree shown above |
| `git blame -L 6728,6733 -- Docs/researches/math_theorems.md` | 0 | all uncited catalog fields originate at the source-record commit |
| bounded Crossref, PubMed Central, and repository source-identity inspection | 0 | PNAS Theorem 1 recorded as a strong unadmitted lead; AMS Memoir recorded as a competing lead; no canonical result selected |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0 and pinned commit/target above |
| `(cd Formalizations/Lean && lake --version)` | 0 | Lake `5.0.0-src+98dc76e`; no update or build run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` | 0 | pinned revision and tree recorded above; package status clean |
| `sha256sum` on authoritative inputs, source records, toolchain, lockfile, and probed mathlib modules | 0 | hashes recorded in `instance.json` and the provisional receipt |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0920/IntakeProbe.lean)` | 0 | seven adjacent partition, generating-function, and congruence API checks elaborated; stdout SHA-256 `a9759475...ff55`; stderr empty |
| bounded exact-topic `rg` search in repo-local Lean and pinned mathlib | 1, expected no-match | no Andrews-Gordon, general Rogers-Ramanujan, odd-modulus, or Eulerian-series target; intake discovery only |
| `python3 -m json.tool` on `instance.json`, `task-dag.json`, `intake-receipt.json`, and `.stage1-worker-selftest.json` | 0 | every structured artifact is valid JSON after finalization |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0920-pycache python3 -m py_compile Stage1_Instances/THM-M-0920/check_intake.py` | 0 | scoped validator compiled without generated files under the owned path |
| `python3 -B Stage1_Instances/THM-M-0920/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | target and authoritative-DAG identity, input hashes, H5/M4/R4 null-target boundary, inventory, packet agreement, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-0920/check_intake.py` | 0 | public replay mode passed without the scheduler-only worker packet |
| prohibited Lean construct scan over the owned path | 1, expected no-match | no proof escape, bodyless declaration, or unsafe declaration in the API-only probe |
| per-file `git diff --no-index --check /dev/null` for every owned file and worker packet | 0 aggregate | no whitespace diagnostics; each no-index exit 1 was only the expected new-file difference |
| `git diff --check -- Stage1_Instances/THM-M-0920 .stage1-worker-selftest.json` | 0 | no tracked whitespace diagnostics; no-index checks cover every untracked artifact |

## Known open gates

Catalog title correction, an immutable authoritative source, exact work and theorem selection,
complete parameter/sum/product/restriction/convergence/conclusion mapping, analytic versus
combinatorial transport, corrections and errata, neighbor reconciliation, and independent source
approval remain open. So do the canonical Lean target and minimal imports, expression/environment
fingerprints, checked transports, four statement mutation classes, exhaustive anchor audit,
discovery protocol, obligation registry, typed graphs, proof and composition, readable
reconstruction, source/provenance/trust closure, hermetic replay, deterministic bundle, independent
verification, master acceptance, audit completion, and theorem completion.

These failures block ordinary statement and theorem execution but do not invalidate a truthful
self-tested planned intake. The `H5` classification applies only to the unstable received catalog
record, not to any source-complete Andrews theorem.

## Status boundary

This is provisional worker self-test evidence for `S56-M-0920-INTAKE` only. It supports a planned
dossier and concrete source-selection blocker, not an accepted node receipt. No canonical
statement, H0 source closure, proof, audit completion, theorem completion, or master acceptance is
claimed.
