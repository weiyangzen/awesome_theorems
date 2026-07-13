# Intake validation

Base revision: `c6fd6dad8fcfe5fd464416cd452f50286b546978` (tree
`5a80b61d8fa09336779f8d1453dcfe4299c9472f`). Validation ran on 2026-07-13 in the
isolated worker clone.

Validation is limited to target-set consistency, planned-dossier structure, source/scope and
non-substitution boundaries, repository and external-source provenance, pinned environment
identity, a narrow candidate and prospective-wrapper Lean check, axiom reports, JSON integrity,
proof-escape hygiene, and whitespace. Because the repository gloss is not a proposition and no
authoritative exact theorem package has been approved, no canonical target, expression hash,
statement mutation, H0 source closure, M0 proof status, or theorem completion is claimed.

The preflight worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts. It was used read-only. No
`lake update`, `lake build`, dependency clone or fetch, or other `.lake` mutation was performed.
This dirty worker run is nonrelease evidence.

## Environment fingerprint

- Platform: Linux 7.0.0-27-generic, x86_64; timezone Asia/Shanghai.
- Lean: `4.29.0`, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- Lake: `5.0.0-src+98dc76e`.
- Pinned mathlib: `8a178386ffc0f5fef0b77738bb5449d50efeea95`; tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; package worktree clean.
- `Formalizations/Lean/lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `Formalizations/Lean/lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Commands and results

| Command (repository root unless noted) | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0226` | 0 | rank 1239; planned; L0/rework_required; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| initial `git status --short --untracked-files=all` | 0 | only the pre-existing automation-provided `Formalizations/Lean/.lake` symlink |
| `git blame -L 1633,1638 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate at commit `bcf3f9fa...b74f` |
| Crossref lookup for DOI `10.1515/crll.1869.70.105` | 0 | title, journal 70 (1869), pages 105-120; payload SHA-256 `b9653e50...5030`; Crossref omitted author |
| Goettingen Digitization Centre IIIF manifest and article scan inspection | 0 | manifest independently names H. A. Schwarz; manifest SHA-256 `01fcec85...c313`; 17-page scan SHA-256 `907da8e8...20f4`; article concerns conformal mapping, but no modern normalized self-map lemma passage was identified |
| MathWorld Schwarz-lemma statement inspection | 0 | retrieved HTML SHA-256 `9200b85b...b8e8`; standard premise, both inequalities, and rotation equality case located; secondary E5 source only |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | Lean and Lake versions match the recorded pins; no update or build ran |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned revision/tree above; package source clean |
| pinned source/history inspection of `Mathlib/Analysis/Complex/Schwarz.lean` | 0 | strong pointwise, derivative, slope, and affine equality candidates located; generalized forms introduced at immutable commit `60148e94...1a86` |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0226/IntakeProbe.lean)` | 0 | six candidate/bridge signatures and prospective two-inequality wrapper elaborated; axiom reports were `[propext, Classical.choice, Quot.sound]`; stdout SHA-256 `860f0019...c955` |
| initial exploratory elaboration of `IntakeProbe.lean` | 1 | superseded: function composition was used for a `MapsTo` proof; replaced with an explicit lambda, after which the final probe passed without placeholders |
| bounded exact-topic `rg` over pinned mathlib and repo-local Lean | 0 | exact Schwarz module and candidates located; no prior THM-M-0226 dossier; intake discovery only |
| `python3 -m json.tool` on `instance.json`, `task-dag.json`, finalized `intake-receipt.json`, and `.stage1-worker-selftest.json` | 0 | all structured artifacts are valid JSON |
| isolated `python3 -m py_compile Stage1_Instances/THM-M-0226/check_intake.py` | 0 | validator compiled with cache redirected outside the owned path |
| `python3 -B Stage1_Instances/THM-M-0226/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | manifest/DAG identity, planned H1/M3/R4 boundary, null target, source/pin hashes, candidate boundary, exact artifact inventory, provisional receipt, worker packet, and six open tasks agree |
| prohibited proof-escape scan over the owned Lean file | 1 | expected no-match exit; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| scoped `git diff --check` plus new-file no-index whitespace checks | 0 | no whitespace diagnostics |

## Known downstream failures

- No accepted immutable authoritative edition supplies the exact fixed-origin premise, open/closed
  disk-map convention, conjunction of conclusions, equality cases, proof mapping, or errata.
- The 1869 article is a credible historical primary lead, not yet a pinpoint source for the modern
  named lemma. The inspected modern statement is secondary and its cited book passage is open.
- No canonical expression/environment fingerprint, checked source transport, alternate-encoding
  certificate, or four-class statement mutation exists.
- The pinned candidates and prospective wrapper are usable M3 evidence only. Exact terminal-body
  provenance, exhaustive trust/axiom audit, wrapper acceptance, and equality specialization remain
  downstream.
- Obligation registry, discovery protocol, typed graphs, composition, readable reconstruction,
  hermetic replay, deterministic evidence bundle, independent verification, and master acceptance
  remain open.

These failures prevent statement, source-fidelity, proof, audit-completion, and theorem-completion
claims. They do not invalidate a truthful self-tested `planned` intake. Only the integration lane
may accept the provisional worker receipt.
