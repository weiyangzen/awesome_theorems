# Intake validation

Base revision: `adc87f8ea24dcc7c5e2668c0a5ede0ca5c5f0f55`; base tree:
`3c83596059f716cde0d50a5f6b390ada6ca7c8e1`.

This validation covers target membership, the planned dossier and open task DAG, catalog and
duplicate provenance, the inspected primary-source theorem, structured intake invariants, a narrow
pinned Lean substrate probe, prohibited-construct hygiene, and whitespace. It does not validate a
canonical max-flow min-cut statement or proof because the exact representation is not frozen.

The initial worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts. It was used read-only. No
`lake update`, `lake build`, dependency clone or fetch, network-triggering Lake operation, or other
`.lake` mutation was performed. The final worker tree is dirty and nonrelease.

## Source boundary

The publisher copy of Ford and Fulkerson, *Maximal Flow Through a Network*, *Canadian Journal of
Mathematics* 8 (1956), 399-404, was inspected at PDF SHA-256
`344c1288f84ccddba6e292751813d613657c69fbe71b9bedb7b19df72a3bdf08`.
Definitions on printed pages 399-400 and Section 1, Theorem 1 on page 400 directly identify the
finite undirected weighted-chain-flow theorem family. Catalog citation identity, modern directed
representation transport, correction and errata status, complete mapping, archival acceptance,
and independent review prevent H0 or statement-freeze credit.

## Environment

- Platform: Linux 7.0.0-27-generic, x86_64.
- Lean: `4.29.0`, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- Lake: `5.0.0-src+98dc76e`.
- Pinned mathlib: `8a178386ffc0f5fef0b77738bb5449d50efeea95`; tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; package worktree clean.
- `Formalizations/Lean/lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `Formalizations/Lean/lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Commands and results

All repository commands ran at the worker root on 2026-07-13 Asia/Shanghai unless another `cwd`
is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and execution skill presence passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0814` | 0 | rank 1373; planned; no legacy slot; legacy artifacts unaccepted; theorem_complete false |
| initial `git status --short --untracked-files=all` | 0 | only `?? Formalizations/Lean/.lake`; preserved read-only |
| `git rev-parse HEAD` and `git rev-parse 'HEAD^{tree}'` | 0 | base revision and tree shown above |
| `git blame -L 5984,5989 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| download publisher PDF and run `pdftotext -layout` | 0 | six-page primary paper; definitions and Theorem 1 on printed pages 399-402 inspected; PDF and text hashes recorded |
| `(cd Formalizations/Lean && lake env lean --version)` and `lake --version` | 0 | Lean and Lake versions agree with the fingerprint; no update or build was run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned mathlib revision/tree above; package worktree clean |
| bounded exact-topic `rg` over repo-local Lean and pinned mathlib | 1 (expected no match) | no max-flow, min-cut, network-flow, Ford-Fulkerson, or cut-capacity declaration located; not a global absence claim |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0814/IntakeProbe.lean)` | 0 | six adjacent graph/incidence/sum/maximum APIs elaborated; complete output SHA-256 `9268c7c2dfc5bc5702f19a7329676c30dc37ad6dca80d9ad622ff2e0edf97d38` |
| `python3 -m json.tool` on all structured owned artifacts and `.stage1-worker-selftest.json` | 0 | all structured artifacts are valid JSON after finalization |
| Python `ast.parse` on `Stage1_Instances/THM-M-0814/check_intake.py` | 0 | scoped validator parses without writing bytecode |
| `python3 -B Stage1_Instances/THM-M-0814/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | identity, hashes, planned H1/M4/R4 boundary, null target, receipt, packet, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-0814/check_intake.py` | 0 | public replay mode passes without the scheduler-only packet |
| prohibited Lean proof-escape scan over the owned path | 1 (expected no match) | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| per-file `git diff --no-index --check /dev/null` plus scoped `git diff --check` | 0 aggregate | no whitespace diagnostics; no-index exit 1 for each new file was treated only as the expected difference |

## Known downstream failures

- The catalog does not define the network, capacity, feasible flow, cut, extrema, binders, or
  boundary cases, and it does not select chain-flow versus directed edge-flow scope.
- The original theorem was inspected and hashed, but exact modern transport, corrections, complete
  source mapping, archival acceptance, and independent review remain open.
- No canonical Lean expression, exact imports, expression/environment fingerprint, checked
  alternate encoding, statement mutation, or usable formal candidate is frozen.
- Discovery and obligation freezes, typed graphs, proof, composition, provenance/trust closure,
  readable reconstruction, hermetic replay, deterministic bundle, independent verification, and
  master acceptance remain open.

These failures prevent statement, audit-completion, and theorem-completion claims. They do not
invalidate a truthful self-tested `planned` intake. Only the integration lane may accept the
provisional worker receipt.
