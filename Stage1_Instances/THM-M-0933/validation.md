# THM-M-0933 intake validation

Base revision: `fb0baac89ea0633612be3b47448464b4b8e4bef7` (tree
`018557070da18ea1733a82de81a238750c59aa84`). Validation date: 2026-07-13
(Asia/Shanghai).

This validation covers target membership, the planned dossier, source-statement and
non-substitution boundaries, the six-node open task DAG, structured intake invariants, and a narrow
pinned Lean API probe. It does not validate a canonical Olson proposition or proof because the
catalog gloss does not select one result from the Davenport-constant family. The
automation-provided canonical `.lake` symlink was pre-existing and used read-only; no `lake
update`, `lake build`, dependency clone or fetch, network-triggering Lake action, or other `.lake`
mutation was performed. This dirty worker run is nonrelease evidence.

## Source evidence

Grynkiewicz, arXiv:2208.12895v1, was downloaded to temporary storage and inspected. The 32-page,
380049-byte PDF has SHA-256
`7a6806ca2a5675d75c2e024faf8acc35a029bee6ce4b1889e1d77a3980ea4bb4`; text produced by
`pdftotext -layout` has SHA-256
`08e3da29f114d62ab1ed1789fdc066de20a84ad9e9d00279732df710b13e58ef`.
PDF page 5 defines `D(G)` and `D*(G)`, states Theorem 1.5 for finite abelian p-groups, attributes
it to Olson and van Emde Boas-Kruyswijk, and cites Olson's 1969 paper. Pages 17-18 contain a modern
proof. This is a strong H1 lead, but it does not decide which Olson result the uncited catalog
intends.

Crossref, CORE, and Elsevier metadata for DOI `10.1016/0022-314X(69)90021-3` confirm John E.
Olson, *A Combinatorial Problem on Finite Abelian Groups I*, *Journal of Number Theory* 1(1)
(January 1969), pages 8-10. CORE's abstract says the least sequence length forcing a product-one
subsequence is answered for p-groups. The primary article body was not successfully retrieved, so
its theorem notation, proof, assumptions, correction record, and errata were not inspected. H0 and
catalog-root identity remain open.

Girard (2018, DOI `10.5802/jep.79`) and Wang (2020, DOI `10.3934/math.2020193`) were also
inspected as published secondary cross-checks. Both distinguish Olson Part I's p-group equality
from Part II's rank-two result; Wang labels them Theorems B and A respectively. This confirms the
intake ambiguity rather than resolving it in favor of either root.

## Environment

- Platform: Linux `7.0.0-27-generic`, x86_64.
- Lean: `4.29.0`, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- Lake: `5.0.0-src+98dc76e`.
- Pinned mathlib: `8a178386ffc0f5fef0b77738bb5449d50efeea95`; tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; package worktree clean.
- `Formalizations/Lean/lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `Formalizations/Lean/lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Commands and results

All repository commands ran at the worker root unless a different `cwd` is shown.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0933` | exit 0; rank 1472, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| initial `git status --short --untracked-files=all` | exit 0; only the automation-provided untracked `Formalizations/Lean/.lake` symlink existed before intake |
| `git rev-parse HEAD 'HEAD^{tree}'` | exit 0; base revision and tree recorded above |
| `git blame -L 6819,6824 -- Docs/researches/math_theorems.md` | exit 0; all six uncited catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| download arXiv:2208.12895v1 PDF and API metadata to temporary storage | exit 0; PDF/page/byte and response hashes recorded in `instance.json`; Theorem 1.5 and proof inspected |
| fetch Crossref, CORE, and Elsevier metadata for Olson DOI `10.1016/0022-314X(69)90021-3` | exit 0; author/title, journal, volume/issue, date, pages, PII, and abstract boundary confirmed; response hashes recorded |
| inspect Girard 2018 source and Wang 2020 PDF plus Crossref metadata | exit 0; published sources separately attribute the p-group and rank-two equalities to Olson Parts I and II; hashes recorded in `instance.json` |
| attempts to retrieve the Olson article body from CORE/ScienceDirect publisher surfaces | failed/no usable PDF; recorded as an open source gate rather than fabricating inspection evidence |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | exit 0; versions recorded above; no update or build run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | exit 0; pinned revision/tree above; package worktree clean |
| bounded `rg` search for Olson, Davenport constant, zero-sum-free sequences, and related spellings over repo-local and pinned mathlib Lean | expected no-match for exact topic declarations; adjacent EGZ and general zero-sum text only; this is not a global absence claim |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0933/IntakeProbe.lean)` | exit 0; seven adjacent pinned APIs elaborated; stdout SHA-256 `a82c5636faea3eda9c08ad0f36f5b9d3ee9d7fb4d973ac30569a7f645e9a4ce9` |
| `python3 -m json.tool` on all structured owned artifacts and `.stage1-worker-selftest.json` | exit 0 for each after finalization |
| Python `ast.parse` on `Stage1_Instances/THM-M-0933/check_intake.py` | exit 0; scoped validator parses without writing bytecode |
| `python3 -B Stage1_Instances/THM-M-0933/check_intake.py --worker-packet .stage1-worker-selftest.json` | exit 0 after finalization; identity, planned H1/M4/R4 boundary, null target, sources/pins/hashes, receipt/packet, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-0933/check_intake.py` | exit 0; public replay mode passes without the scheduler-only packet |
| prohibited Lean proof-escape scan over the owned path | expected no-match exit 1; no prohibited proof declaration in the API-only probe |
| per-file `git diff --no-index --check /dev/null` for every owned file and worker packet | no whitespace diagnostics; per-file exit 1 is only the expected new-file difference |
| `git diff --check -- Stage1_Instances/THM-M-0933 .stage1-worker-selftest.json` | exit 0; tracked-diff command emitted no diagnostics; no-index checks cover untracked files |

## Known open gates

- Master acceptance of this intake is pending.
- An independent reviewer must choose the p-group equality, rank-two equality, homocyclic
  rank-two value, direct forcing formulation, or another exact source result.
- The original Olson article proof body, precise definitions/premises, corrections, errata, and
  relationship to the catalog record have not been independently accepted.
- Canonical Lean target, minimal imports, expression and environment fingerprints, checked
  transports, and all four required statement mutation classes remain open.
- Bounded pinned-tree discovery found finite-group, p-group, multiset, and EGZ substrate but no
  exact Olson/Davenport artifact; exhaustive anchor and proof-body provenance audit remains open.
- Obligation registry, typed graphs, proof, composition, trust closure, readable reconstruction,
  hermetic replay, deterministic bundle, independent verification, audit completion, and theorem
  completion remain open.

These failures block statement and theorem execution but do not invalidate a truthful, self-tested
`planned` intake. Only the integration lane may accept the provisional worker receipt.
