# Intake validation

Base revision: `c6fd6dad8fcfe5fd464416cd452f50286b546978` (tree
`5a80b61d8fa09336779f8d1453dcfe4299c9472f`). Validation ran on 2026-07-13 in
the isolated worker clone.

Validation is limited to target-set consistency, dossier structure and scope invariants,
repository-source provenance, pinned environment identity, direct candidate API elaboration and
representative axiom reports, proof-escape hygiene, JSON integrity, and whitespace. It does not
freeze or prove a canonical theorem. The catalog omits the source definition of domain,
nonemptiness/openness/connectedness, the meaning of nonconstant on that domain, and relative versus
total openness. `IntakeProbe.lean` therefore authenticates candidate interfaces only.

The preflight worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts. It was used read-only. No
`lake update`, `lake build`, dependency clone or fetch, or other `.lake` mutation was performed.
This is nonrelease worker evidence.

## Environment

- Lean `4.29.0`, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, target
  `x86_64-unknown-linux-gnu`; Lake `5.0.0-src+98dc76e`.
- Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; package status was clean after the probe.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.
- `Mathlib.Analysis.Complex.OpenMapping` source SHA-256:
  `352dd28e4e85d7c15c69ad792b6db68d2bab2e18c652b461823002a0cba755e6`.

## Commands and results

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0235` | exit 0; rank 1247, planned, L0/rework_required, no legacy slot, legacy artifacts unaccepted, theorem_complete false |
| `git status --short --untracked-files=all` before edits | exit 0; only the pre-existing automation-provided `Formalizations/Lean/.lake` symlink was untracked and it was preserved read-only |
| `git rev-parse HEAD 'HEAD^{tree}'`; `git blame -L 1696,1701 -- Docs/researches/math_theorems.md` | exit 0; base revision/tree recorded above; all six uncited source-record lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `git ls-remote --tags https://github.com/jirilebl/ca.git refs/tags/v1.9` | exit 0 during source discovery; tag `v1.9` resolved to commit `a4d25d9ba37a486a5a020219eb8bd4e6602fd14c` |
| `curl -L --fail --silent --show-error --max-time 30 -o /tmp/ca-v1.9.tar.gz https://codeload.github.com/jirilebl/ca/tar.gz/refs/tags/v1.9` | exit 0; immutable release archive retrieved |
| `sha256sum /tmp/ca-v1.9.tar.gz` | exit 0; `1d50a21c5e07e3b6d77b13b01974480ad9d3d29281513cd1e09fe9e2789b4c33` |
| `tar -xOf /tmp/ca-v1.9.tar.gz ca-1.9/ca.tex \| sha256sum` | exit 0; `ca.tex` SHA-256 `a99ed1bfceca960f98abd08e7d3c4f20d907b2fa392c211b522c06283ac61935` |
| `tar -xOf /tmp/ca-v1.9.tar.gz ca-1.9/ca.tex \| sed -n '970,988p' \| sha256sum` and the same pipeline without `sha256sum` | exit 0; domain-definition excerpt SHA-256 `5fa687a04daa72bb304d4eef9fae306cfef49f62b78b18c3c542311a15a08861`; Definition 1.1 and its nonemptiness footnote inspected |
| `tar -xOf /tmp/ca-v1.9.tar.gz ca-1.9/ca.tex \| sed -n '11712,11760p' \| sha256sum` and the same pipeline without `sha256sum` | exit 0; theorem/proof excerpt SHA-256 `0b6124d1b3474e43289d1ccb6eb2dafe2c73a7a20f8b4103e476355f62ad9cf8`; Theorem 5.5.1 and its Rouché proof inspected; named H1 source lead only |
| `rg -n -C 5 'THM-M-0235\|THM-M-0276\|非常值全纯函数是开映射\|满射有界线性算子是开映射' Docs` | exit 0; catalog and Stage0 omission boundary plus distinct Banach target `THM-M-0276` confirmed |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | exit 0; versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'`; package `status --short` | exit 0; pinned revision/tree recorded above; empty status output |
| `rg -n 'AnalyticAt.eventually_constant_or_nhds_le_map_nhds\|AnalyticOnNhd.is_constant_or_isOpen\|AnalyticOnNhd.is_constant_or_isOpenMap\|analyticOnNhd_iff_differentiableOn' Formalizations/Lean/.lake/packages/mathlib/Mathlib/Analysis/Complex Formalizations/Lean/AwesomeTheorems --glob '*.lean'` | exit 0; direct global, whole-domain, local, and terminology-bridge interfaces located; no source identity or proof credit inferred |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0235/IntakeProbe.lean)` | exit 0; six direct candidate/bridge APIs elaborated; three representative candidates report `[propext, Classical.choice, Quot.sound]`; stdout SHA-256 `50d100d55ec43fbcff16f201176c08f27c4a5eaefd3e9a0748e293335fd26596` |
| `python3 -m json.tool Stage1_Instances/THM-M-0235/instance.json`; same command for `task-dag.json`, `intake-receipt.json`, and `.stage1-worker-selftest.json` | exit 0 for each after finalization |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0235-pycache python3 -m py_compile Stage1_Instances/THM-M-0235/check_intake.py` | exit 0; scoped validator compiled without generated files in the owned path |
| `python3 -B Stage1_Instances/THM-M-0235/check_intake.py --worker-packet .stage1-worker-selftest.json` | exit 0 after finalization; target/DAG identity, source and dependency hashes, H1/M3/R4 boundary, null target, exact inventory, receipt/packet agreement, probe, and six open tasks agree |
| `rg -n --glob '*.lean' '\b(sorry\|admit\|sorryAx\|axiom\|constant\|opaque\|unsafe)\b' Stage1_Instances/THM-M-0235` | exit 1 as expected; no prohibited declaration token; `#print axioms` is an allowed diagnostic |
| `git diff --check -- Stage1_Instances/THM-M-0235 .stage1-worker-selftest.json` and `for f in .stage1-worker-selftest.json Stage1_Instances/THM-M-0235/*; do git diff --no-index --check -- /dev/null "$f"; done` with expected new-file difference status | exit 0/no diagnostics after treating no-index exit 1 as the expected added-file difference |

## Known open gates

Catalog-to-source identity, the source's optional nonemptiness convention, complete premise and
conclusion mapping, historical attribution, corrections or errata disposition, and independent
source review remain open. So do canonical Lean expression and environment
fingerprints, minimal imports, checked transports, statement mutations, exhaustive anchor and
terminal-body provenance audit, discovery and obligation freezes, typed graphs, proof and
composition, accepted trust closure, readable reconstruction, hermetic replay, deterministic
bundle, independent verification, master acceptance, audit completion, and theorem completion.
These open gates do not invalidate a truthful, self-tested `planned` intake.
