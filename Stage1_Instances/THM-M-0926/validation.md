# Intake validation

Base revision: `72e9e8092182121a6794921f61fcc9cae22f726d` (tree
`0d6c1fdf06d1573c256af331c6b198e5a787af43`). Validation date: 2026-07-13
(Asia/Shanghai).

Validation covers target membership, the planned dossier and six-task open DAG, catalog/source
provenance, scope and crosswalk invariants, exact owned-file inventory, and a narrow pinned Lean
candidate probe. It does not validate a canonical theorem statement or proof because the received
catalog record supplies no truth-valued formula.

The initial worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts. It was used read only. No
`lake update`, `lake build`, dependency clone or fetch, network-triggering Lake operation, or other
`.lake` mutation was performed. The owned intake files and root worker packet make the final tree
dirty and nonrelease.

## Source discovery boundary

The repository source contains only the identity name, attribution, year, and generic Fibonacci
gloss. MathWorld was inspected as a modern secondary formula lead. Its observed 52,085-byte HTML
response, SHA-256 `cc85db96bde2915bc1bb676527629bcabe97324713cc7458af570a17cdc77fbe`,
states `F_(n-1) * F_(n+1) - F_n^2 = (-1)^n` and supplies later bibliography. OEIS A000045 was also
inspected for the modern Fibonacci convention and Cassini-related leads; its observed 218,934-byte
HTML response has SHA-256 `7fcae408a5f424c6d64188a412b6051e7b8f7383ca7b62d6338ba1de9a2787df`.

Both are mutable secondary resources. Neither preserves or independently reviews Cassini's
asserted 1680 source, exact index domain, complete proof, attribution conflicts, corrections, or
errata. They recognize the formula family but do not repair the catalog into an accepted root or
support H0.

Pinned mathlib contains a precise all-integer theorem explicitly documented as Cassini's identity.
The Lean probe validates its availability and reports axioms `propext`, `Classical.choice`, and
`Quot.sound`, supporting provisional `M3` only. It confers no `M0` credit because no source-approved
catalog root exists to match and the downstream provenance/trust audit has not run.

## Environment fingerprint

- Platform: Linux 7.0.0-27-generic, x86_64.
- Lean: 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- Lake: `5.0.0-src+98dc76e`.
- Pinned mathlib: `8a178386ffc0f5fef0b77738bb5449d50efeea95`; tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; package worktree clean.
- `Formalizations/Lean/lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `Formalizations/Lean/lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.
- Pinned `Mathlib/Data/Int/Fib/Lemmas.lean` SHA-256:
  `5622457f63665e6bcbbef34e67c2a27cd8faf98911678550a6b93ba34d685536`.

## Commands and results

All repository commands ran at the repository root on 2026-07-13 Asia/Shanghai unless a different
`cwd` is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0926` | 0 | rank 1545; planned; no legacy slot; legacy artifacts unaccepted; theorem_complete false |
| initial `git status --short --untracked-files=all` | 0 | only `?? Formalizations/Lean/.lake`; preserved read only |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | produced the base revision and tree above |
| `git blame -L 6770,6775 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| MathWorld and OEIS `curl` requests plus scoped extraction, `wc -c`, and `sha256sum` | 0 | conventional formula, sequence convention, bibliography boundaries, response sizes, and digests recorded; no H0 or target-correction claim |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | Lean and Lake versions agree with the fingerprint; no update or build ran |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned mathlib revision/tree above; package worktree clean |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0926/IntakeProbe.lean)` | 0 | nine public Fibonacci interfaces elaborated; Cassini theorem body and two candidate axiom reports printed; output SHA-256 `f7f0d934748edec5e6a13cf5012caa0387ae63c87de616626dd2c546a2d5b9cc` |
| `python3 -m json.tool` on all structured owned artifacts and `.stage1-worker-selftest.json` | 0 | all structured artifacts valid JSON after finalization |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0926-pycache python3 -m py_compile Stage1_Instances/THM-M-0926/check_intake.py` | 0 | scoped validator compiled without writing into the owned path |
| `python3 -B Stage1_Instances/THM-M-0926/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | target/DAG identity, H5/M3/R4 boundary, null canonical target, hashes, exact inventory, worker packet, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-0926/check_intake.py` | 0 | public replay mode passed without the scheduler-only root packet |
| prohibited Lean proof-escape/declaration scan over `IntakeProbe.lean` | 1 (expected no match) | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, `unsafe`, theorem, lemma, or example declaration |
| `git diff --check -- Stage1_Instances/THM-M-0926 .stage1-worker-selftest.json` plus per-new-file no-index checks | 0 | no whitespace diagnostics |

## Known downstream failures

- The catalog wording is H5 because it does not state one stable proposition. An approved target
  correction/source selection, immutable primary or authoritative source, exact formula and proof,
  attribution and errata audit, and independent review remain open.
- Natural versus positive-natural versus integer indexing, Fibonacci definition, lower bound,
  ordered binders, equation orientation, sign convention, exponent representation, transports, and
  all boundary cases remain statement decisions.
- No canonical Lean expression, minimal-import certificate, expression or environment fingerprint,
  checked alternate encoding, or required statement mutation exists.
- Formal anchor audit, obligation registry, typed graphs, proof integration, composition,
  provenance and trust closure, readable reconstruction, hermetic replay, deterministic bundle,
  independent release verification, and master acceptance remain open.

These failures prevent statement, audit-completion, and theorem-completion claims. They do not
invalidate a truthful, self-tested `planned` intake whose purpose is to freeze the received scope
and correction route. Only the integration lane may accept the provisional worker receipt.
