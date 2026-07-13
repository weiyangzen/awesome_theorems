# Intake validation

Base revision: `0e5ae82e6d507ee607c3f011900571ffd8096800`; base tree:
`400e6edf1f69b971b60a367e3ea29be359b07907`.

This validation covers target membership, the planned dossier and open task DAG, repository and
source-family crosswalks, exact owned-file invariants, and a narrow pinned Lean substrate and
prospective-representation probe. Because the primary proof statements and c.e.-set-to-oracle
encoding are not frozen, no canonical target, expression hash, source acceptance, transport, or
proof is claimed. The automation-provided canonical `.lake` symlink was pre-existing and used
read-only; no dependency update, build, clone, fetch, or `.lake` mutation was performed. This is
nonrelease worker evidence.

## Environment

- Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, target
  `x86_64-unknown-linux-gnu`.
- Lake `5.0.0-src+98dc76e`.
- Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; its package worktree was clean.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Commands and results

All commands ran from the worker clone root on 2026-07-13 (Asia/Shanghai), except where a `cwd` is
shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and execution skill presence passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0749` | 0 | rank 1335; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all` (preflight) | 0 | only the automation-provided `Formalizations/Lean/.lake` symlink was untracked; preserved read-only |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree recorded above |
| repository record, Stage0 projection, duplicate CS record, neighboring-target, and Git-provenance inspection | 0 | identified the named theorem family, precise incomparable-c.e.-degree corroboration, separate `THM-C-0016` ownership, and all open exact-statement fields; no status transferred |
| fetch archived Stanford Encyclopedia Summer 2026 `Recursive Functions` entry, then scoped inspection and `sha256sum` | 0 | Section 3.2, Theorem 3.8 states the two incomparable c.e. witnesses and identifies Friedberg/Muchnik sources; secondary page SHA-256 `7b22369f...e6e83e`; no H0 credit |
| Crossref query for DOI `10.1073/pnas.43.2.236`, then scoped `jq`, `wc`, and `sha256sum` | 0 | confirmed Friedberg, exact title, PNAS 43(2), 1957, pages 236-238; 2201-byte metadata response SHA-256 `4b2fd407...b76726`; no primary-text claim |
| PNAS/PMC/Europe PMC primary full-text fetch attempts | nonzero or rejected response | publisher returned HTTP 403; PMC returned browser challenges or empty responses; no file was accepted as a primary proof source |
| Crossref query for DOI `10.3233/COM-150042`, then scoped `jq`, `wc`, and `sha256sum` | 0 | reprint metadata bibliography identifies Muchnik, Doklady 108(2), 1956, pages 194-197; 4810-byte response SHA-256 `e6c2989b...e16cf`; original and reviewed translation remain open |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | pinned Lean and Lake versions recorded above; no update or build was run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned revision/tree recorded above; empty package status |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0749/IntakeProbe.lean)` | 0 | `REPred`, `RecursiveIn`, Turing reducibility/equivalence/degree APIs and a prospective predicate-to-partial-function encoding elaborated; no theorem or proof body added |
| bounded exact-topic `rg` over pinned mathlib and repo-local Lean | 1 (expected no match) | no Friedberg, Muchnik, Post-problem, or c.e.-degree incomparability declaration found; not a global absence claim or downstream anchor audit |
| `python3 -m json.tool` on all structured artifacts and the worker packet | 0 each | all JSON is valid |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0749-pycache python3 -m py_compile Stage1_Instances/THM-M-0749/check_intake.py` | 0 | scoped validator compiled without creating an owned generated file |
| `python3 -B Stage1_Instances/THM-M-0749/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | target/DAG identity, H1/M4/R4 planned boundary, null canonical target, source hashes, exact inventory, packet agreement, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-0749/check_intake.py` | 0 | public replay mode passes without requiring the scheduler-only root packet |
| prohibited-construct `rg` over owned Lean files | 1 (expected no match) | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| per-new-file `git diff --no-index --check` loop, plus `git diff --check -- Stage1_Instances/THM-M-0749 .stage1-worker-selftest.json` | 0 | no whitespace diagnostics; no-index exit 1 for a new file was treated as a difference, not an error |

## Known open gates

Primary proof-text acquisition, exact definition/result locators, premise, construction,
conclusion, translation and errata crosswalks, and independent source review remain open. So do the
canonical Lean target and environment fingerprint, checked set/predicate/oracle/degree and
intermediate-degree transports, semantic mutations, discovery protocol, obligation registry,
typed graphs, formal anchor and provenance audit, priority proof and composition, trust closure,
readable reconstruction, hermetic replay, deterministic evidence bundle, independent verification,
master acceptance, audit completion, and theorem completion. These failures do not invalidate a
truthful self-tested `planned` intake.
