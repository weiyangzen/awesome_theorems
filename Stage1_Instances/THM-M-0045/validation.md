# Intake validation

Base revision: `4ecdda4863162748b3ee70bc4ec842789418145d` (tree
`aace54662cd5e9ca38472011f41afdbffdedfa04`). Validation date: 2026-07-13
(Asia/Shanghai).

This validation covers the planned dossier, repository and source provenance, scope and
non-substitution boundaries, six-node open task DAG, exact owned-artifact inventory, structured
intake invariants, and a narrow pinned Lean API/axiom probe. It does not validate a canonical Schur
proposition or root proof because neither has been frozen. The automation-provided canonical
`.lake` symlink was pre-existing and used read-only; no dependency update, build, clone, fetch, or
other `.lake` mutation was performed. This dirty worker run is nonrelease evidence.

## Environment

- Linux 7.0.0-27-generic, x86_64.
- Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- Lake `5.0.0-src+98dc76e`.
- Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; package source status was clean.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Commands and results

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; all 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0045` | exit 0; rank 1085, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| initial `git status --short --untracked-files=all` | exit 0; only the automation-provided untracked `Formalizations/Lean/.lake` symlink existed before intake |
| `git blame -L 342,347 -- Docs/researches/math_theorems.md` | exit 0; all six uncited catalog lines originate in commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `curl -L --fail --silent --show-error 'https://gdz.sub.uni-goettingen.de/download/pdf/PPN235181684_0066/LOG_0049.pdf' -o /tmp/gdz-schur1909.pdf` followed by `sha256sum`, `pdfinfo`, and read-only scan/fulltext inspection | exit 0; 24-page scan SHA-256 `a32565f7...a488`; printed pages 489-492 define unitary and contain Satz I plus its induction proof; source lead only, no H0 |
| `curl -L --fail --silent --show-error 'https://linear.axler.net/LADR4e.pdf' -o /tmp/LADR4e.pdf` followed by `sha256sum`, `pdftotext -layout`, and bounded theorem-text inspection | exit 0; SHA-256 `45f821b6...d03`; Theorems 6.37-6.38 on printed pages 203-204 located; source lead only, no H0 |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | exit 0; versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and status | exit 0; pinned revision/tree above; package worktree clean |
| bounded exact-topic `rg` in repo-local Lean and pinned mathlib | exit 0; relevant substrate and explicit triangularizable-endomorphism TODO found, but no exact Schur triangularization declaration; intake discovery only |
| first `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0045/IntakeProbe.lean)` | exit 1; the Gram-Schmidt declaration needed its `InnerProductSpace` namespace; no proof or dependency change was made |
| corrected `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0045/IntakeProbe.lean)` | exit 0; eight pinned interfaces elaborated; both substantive candidate lemmas report `[propext, Classical.choice, Quot.sound]`; no root theorem declared |
| `python3 -m json.tool` on structured artifacts and root packet | exit 0 for each after finalization |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0045-pycache python3 -m py_compile Stage1_Instances/THM-M-0045/check_intake.py` | exit 0; scoped validator compiled without generated files in the owned path |
| `python3 -B Stage1_Instances/THM-M-0045/check_intake.py --worker-packet .stage1-worker-selftest.json` | exit 0; target/DAG identity, H1/M3/R4 null-target boundary, source/pin/artifact hashes, provisional receipt/packet, and six open tasks agree |
| prohibited Lean construct scan over `IntakeProbe.lean` | exit 1 as expected; no match for `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` |
| scoped new-file whitespace checks plus `git diff --check` | exit 0; no whitespace diagnostics |

## Known open gates

The exact source-to-catalog specialization and lower/upper-triangular transport, accepted source
definitions and translation, correction audit, lawful archive/recovery policy, independent source
review, exact dimension/index/order/unitary/conjugation/boundary conventions, and operator/basis to
matrix/unitary transport remain open. So do the canonical Lean expression and environment
fingerprint, checked alternate transports, statement mutations, exhaustive anchor/provenance
audit, discovery protocol, obligation registry, typed graphs, proof and composition, source and
trust closure, readable reconstruction, hermetic replay, deterministic bundle, independent
verification, master acceptance, audit completion, and theorem completion.

The first failed downstream gate is `S56-M-0045-STATEMENT`; these failures do not invalidate a
truthful self-tested `planned` intake. Only the integration lane may accept its provisional receipt.
