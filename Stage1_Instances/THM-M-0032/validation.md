# THM-M-0032 intake validation

Base revision: `837792d9180ab731db89c16a5cc22128a9599bc8`; base tree:
`5c5bd784032e9859e4c88b48a886d50194be1732`. Validation ran on 2026-07-13
(Asia/Shanghai) in the isolated worker clone.

This validation covers target membership, the planned dossier and six-node open task DAG,
repository and primary-source provenance, source/statement boundaries, pinned environment identity,
a narrow Lean API probe, scoped structural invariants, proof-escape hygiene, and whitespace. It
does not elaborate or prove a canonical regular-local-ring-to-UFD proposition.

The preflight worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts. It was used read-only. No
`lake update`, `lake build`, dependency clone or fetch, network-triggering Lake operation, or other
`.lake` mutation was performed. The owned artifacts make this dirty, nonrelease worker evidence.

## Source boundary

The NCBI page scans of the two-page Auslander-Buchsbaum paper were inspected. Theorem 5 on page
734 exactly states that every regular local ring is a unique factorization domain. Its 1959
publication conflicts with the catalog's unexplained 1958 date. The paper imports definitions and
notation from prior work and uses Nagata's reduction beyond dimension three. Those dependencies,
definitions, corrections, and independent review remain open, so no H0 is claimed. Stacks Project
tag `0AG0` was inspected only as a modern exact-statement and proof-route cross-check.

## Environment

- Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, target
  `x86_64-unknown-linux-gnu`.
- Lake `5.0.0-src+98dc76e`; no update or build was run.
- Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; package source status was clean.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Commands and results

All commands ran at the repository root unless another working directory is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | all 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0032` | 0 | rank 1076; planned; no legacy slot; legacy artifacts unaccepted; theorem_complete false |
| `git status --short --untracked-files=all` (preflight) | 0 | only the pre-existing automation `Formalizations/Lean/.lake` symlink; preserved read-only |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree shown above |
| `git blame -L 249,254 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| Crossref DOI query for `10.1073/pnas.45.5.733` | 0 | title, authors, May 1959, PNAS 45(5), pages 733-734 confirmed; response SHA-256 `bf2d19da0d8f2d731a1121552956dd648ae7636b475cb68759154d24a3d69bcc` |
| NCBI page-scan downloads for pages 733 and 734 | 0 | exact paper and Theorem 5 inspected; image hashes recorded in `instance.json`; discovery and source-map evidence, not H0 acceptance |
| `curl -L --fail --silent --show-error --max-time 30 https://stacks.math.columbia.edu/tag/0AG0 -o /tmp/stacks_0AG0.html` | 0 | exact modern statement and proof route inspected; HTML SHA-256 `785af7cb4e040abda98bcbe4414785a4c2367059925a01b6d5524c44455008b7` |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | pinned Lean and Lake versions shown above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | pinned revision and tree shown above; package status clean |
| bounded exact-topic search for `Auslander`, `Buchsbaum`, and regular-local-to-UFD declarations in pinned mathlib and repo-local Lean | 1 (expected no match) | no terminal target declaration located; intake discovery only, not an exhaustive anchor audit |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0032/IntakeProbe.lean)` | 0 | seven local, Noetherian, regular-local, and UFD interface checks elaborated; stdout SHA-256 `40e530fe1f6e1e7f857f15edd9643187f9123d836637b8d36c4e0441c7963e62`; no target declared |
| `python3 -m json.tool` on the three structured owned files and root worker packet | 0 | valid JSON after finalization |
| `python3 -c` with `ast.parse` on `check_intake.py` | 0 | scoped checker parsed without bytecode output |
| `python3 -B Stage1_Instances/THM-M-0032/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | identity, null planned target, H1/M4/R4 boundary, source pins, exact artifact inventory, worker packet, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-0032/check_intake.py` | 0 | public replay mode passed without the scheduler-only worker packet |
| prohibited Lean construct scan over the owned path | 1 (expected no match) | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| per-new-file `git diff --no-index --check /dev/null` checks | 0 aggregate | no whitespace diagnostics; exit 1 from each comparison was only the expected new-file difference |
| `git diff --check -- Stage1_Instances/THM-M-0032 .stage1-worker-selftest.json` | 0 | no tracked whitespace diagnostics; per-file checks cover untracked files |

## Known open gates

Immutable repository admission of the primary pages and all incorporated earlier definitions,
assumption/proof/dependency/errata mapping, explanation of the 1958 date, and independent source
review remain open. So do the exact Lean target, minimal imports, expression/environment
fingerprints, checked transports, four statement mutation classes, exhaustive anchor/proof-body
audit, discovery protocol, obligation registry, typed graphs, proof and composition, trust and
provenance closure, readable reconstruction, hermetic replay, deterministic bundle, independent
verification, master acceptance, audit completion, and theorem completion.

## Status boundary

This is provisional worker self-test evidence for `S56-M-0032-INTAKE` only. It supports a truthful
planned dossier and open DAG, not an accepted node receipt or an exact statement/proof claim. No
H0, M0, R0, audit completion, theorem completion, or master acceptance is claimed.
