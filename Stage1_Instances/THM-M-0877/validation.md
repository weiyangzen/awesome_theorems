# Intake validation

Base revision: `748243faadc15828fb087059337fd05b7be9fdeb`; base tree:
`e46d642646f80980838b6f016f5d69b817bd464d`.

This validation covers target membership, the planned dossier and open task DAG, catalog and
neighbor provenance, the inspected primary-source discriminator, structured intake invariants, a
narrow pinned Lean substrate probe, prohibited-construct hygiene, and whitespace. It does not
validate a canonical network-flow statement or proof because no exact proposition is selected.

The initial worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` link to canonical pinned artifacts. It was used read-only. No `lake
update`, `lake build`, dependency clone or fetch, network-triggering Lake operation, or other
`.lake` mutation was performed. The final worker tree is dirty and nonrelease.

## Source boundary

The repository record is only the topic `网络流` and gloss `最大流与最小割理论`. The publisher copy
of Ford and Fulkerson, *Maximal Flow Through a Network*, *Canadian Journal of Mathematics* 8
(1956), 399-404, was inspected at PDF SHA-256
`344c1288f84ccddba6e292751813d613657c69fbe71b9bedb7b19df72a3bdf08` and extracted-text SHA-256
`c70d333cecdfff7c0fdc30a7aae11b32e63bb4e6baab3384c5feab4d6d305ab5`. Definitions on printed
pages 399-400 and Theorem 1 on page 400 identify a precise finite undirected weighted-chain-flow
minimum-cut theorem, but that result directly matches separately owned `THM-M-0814`. It is used
only to expose the duplicate and representation boundary; it supplies no H1/H0 or proof credit to
this broad target.

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

All repository commands ran at the worker root on 2026-07-13 in Asia/Shanghai unless another
`cwd` is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and execution skill presence passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0877` | 0 | rank 1430; planned; no legacy slot; legacy artifacts unaccepted; theorem_complete false |
| initial `git status --short --untracked-files=all` | 0 | only the pre-existing automation-provided `Formalizations/Lean/.lake` link; preserved read-only |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree shown above |
| `git blame -L 6425,6430 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| download the publisher PDF, run `pdftotext -layout`, and inspect printed pages 399-402 | 0 | six-page Ford/Fulkerson primary paper and Theorem 1 inspected; hashes above; neighboring discriminator only |
| `cd Formalizations/Lean && lake env lean --version` and `lake --version` | 0 | Lean and Lake versions agree with the fingerprint; no update or build ran |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned mathlib revision/tree above; package worktree clean |
| bounded exact-topic `rg` over repo-local Lean and pinned mathlib | 1 (expected no match) | no max-flow, min-cut, network-flow, Ford-Fulkerson, or cut-capacity declaration located; not a complete anchor audit |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0877/IntakeProbe.lean` | 0 | six adjacent graph, digraph, finite-sum, and finite-maximum APIs elaborated; complete stdout SHA-256 `e4daeb1cace9ec6c576cbb8e2875df5dcaf956dd8a9f722e9d8a8431967741ff`; no target declared |
| `python3 -m json.tool` on all structured owned artifacts and `.stage1-worker-selftest.json` | 0 | all structured artifacts parsed after finalization |
| Python `ast.parse` on `Stage1_Instances/THM-M-0877/check_intake.py` | 0 | scoped checker parsed without writing bytecode |
| `python3 -B Stage1_Instances/THM-M-0877/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | identity, pinned inputs, null target, planned H5/M4/R4 boundary, exact artifact inventory, receipt, packet, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-0877/check_intake.py` | 0 | public replay mode passes without the scheduler-only worker packet |
| prohibited Lean proof-escape scan over the owned path | 1 (expected no match) | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| per-file `git diff --no-index --check /dev/null` plus scoped `git diff --check` | 0 aggregate | no whitespace diagnostics; no-index exit 1 for each new file was treated only as the expected difference |

## Known downstream failures

- The catalog supplies a theory label, not a stable proposition, and does not select equality,
  attainment, integrality, augmenting paths, an algorithm, or a typed family ledger.
- Network, terminal, capacity, feasible-flow, cut, extrema, ordered binder, boundary, and
  computation choices remain open; the dedicated `THM-M-0814` equality target must be reconciled.
- No canonical Lean expression, exact imports, expression/environment fingerprint, checked
  alternate encoding, statement mutation, or usable exact formal candidate is frozen.
- Discovery and obligation freezes, typed graphs, proof, composition, provenance/trust closure,
  readable reconstruction, hermetic replay, deterministic bundle, independent verification, and
  master acceptance remain open.

These failures prevent statement, audit-completion, and theorem-completion claims. They do not
invalidate a truthful self-tested `planned` intake. Only the integration lane may accept the
provisional worker receipt.
