# Intake validation

Base revision: `fcabbf1e0ad9507eebe91663bccabfa87d22813e` (tree
`873e589c594454b7f263c7ed2342089a4d15e842`). Validation date: 2026-07-13
(Asia/Shanghai).

This validation covers target membership, the fail-closed planned dossier and open task DAG,
catalog-to-primary-source discrimination, structured intake invariants, and a narrow pinned Lean
probability API probe. It does not validate a canonical Moser-Tardos proposition or proof because
the exact source package and stochastic algorithm semantics are not frozen.

The preflight worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts. It was used read-only. No
`lake update`, `lake build`, dependency clone or fetch, or other `.lake` mutation was performed.
The owned intake files and root worker packet make the final snapshot dirty and nonrelease.

## Environment

- Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, target
  `x86_64-unknown-linux-gnu`; Lake `5.0.0-src+98dc76e`.
- Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; package source status was clean.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.
- Platform: Linux `7.0.0-27-generic`, `x86_64`.

## Commands and exact results

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0970` | 0 | rank 1504; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all` | 0 | preflight output was only `?? Formalizations/Lean/.lake`; preserved read-only |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree shown above |
| `git blame -L 7085,7090 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog fields originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| archived primary-source retrieval and `pdfinfo`/`pdftotext` inspection | 0 | arXiv `0903.0544v3` Algorithm 1.1 and Theorem 1.2 on printed page 3, proof in Sections 2-3, and source boundaries were inspected; PDF SHA-256 `394a21143451acad99ae93e934dc12a5d7df4da68659b8060786fdd8a9665a0c`; H1 only |
| bounded arXiv revision and Crossref relation inspection | 0 | Theorem 1.2 formula/conclusions were unchanged through v3; no correction relation or erratum was identified, but the negative search is nonexhaustive |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | versions recorded above; no update or build ran |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | pinned revision and tree recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short --untracked-files=all` | 0 | empty output |
| bounded exact-topic `rg` over pinned mathlib and repo-local Lean | 1 (expected no match) | no Moser-Tardos, algorithmic local-lemma, witness-tree, or bad-event resampling declaration found; scoped discovery only |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0970/IntakeProbe.lean)` | 0 | nine adjacent probability interfaces and three axiom diagnostics elaborated; output was 2154 bytes with SHA-256 `06c4d8ba4c5725ea6fbbcc62f7be8fcea3a1e96898204050cd466618e5713471`; no target theorem declared |
| `python3 -m json.tool` on all structured owned files and `.stage1-worker-selftest.json` | 0 each | valid JSON after finalization |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0970-pycache python3 -m py_compile Stage1_Instances/THM-M-0970/check_intake.py` | 0 | scoped checker compiled without generated files in the owned path |
| `python3 -B Stage1_Instances/THM-M-0970/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | target/DAG identity, source and dependency hashes, null target, H1/M4/R4 boundary, exact artifact inventory, provisional receipt/packet, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-0970/check_intake.py` | 0 | public replay mode passed without the scheduler-only root packet |
| token-anchored prohibited Lean declaration scan over the owned path | 1 (expected no match) | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration token; diagnostic `#print axioms` is intentionally permitted |
| `git diff --check` plus per-new-file `git diff --no-index --check /dev/null FILE` | 0 aggregate | no whitespace diagnostics; each no-index exit 1 was only the expected new-file difference |

## Known open gates

Repository adoption of an immutable source root, journal/archive reconciliation, exhaustive
correction and errata review, complete variable/event/support/dependency/algorithm/expectation and
proof-node mapping, and independent source review remain open. So do canonical Lean elaboration,
minimal imports, expression and environment fingerprints, checked transports, all four mutation
classes, exhaustive anchor and terminal-body provenance audit, discovery protocol, obligation
registry, typed graphs, proof and composition, trust closure, readable reconstruction, hermetic
replay, deterministic bundle, independent verification, and release.

These gates block the statement and theorem, but do not invalidate a truthful self-tested `planned`
intake. The receipt is provisional and unsigned; only the integration lane may accept it.

## Status boundary

This is worker self-test evidence for `S56-M-0970-INTAKE` only. It supports a planned dossier and
concrete statement blocker, not an accepted node. No canonical statement, H0 source closure, M0
proof credit, audit completion, theorem completion, or master acceptance is claimed.
