# THM-M-0831 intake validation

Base revision: `be8701e88e791545c16a262edd1909486d5cef4b` (tree
`78b0a751473bf6d71f453a6aad18b130268a3428`). Validation date: 2026-07-13
(Asia/Shanghai).

This validation covers target membership, the planned dossier, source-statement and
non-substitution boundaries, the six-node open task DAG, structured intake invariants, and a narrow
pinned Lean API probe. It does not validate a canonical Karger proposition or proof because the
catalog provides a method gloss and the inspected source contains several distinct claims. The
automation-provided canonical `.lake` symlink was pre-existing and used read-only; no dependency
update, build, clone, fetch, or other `.lake` mutation was performed. This dirty worker run is
nonrelease evidence.

## Source evidence

The author-hosted copy of David R. Karger, *Global Min-cuts in RNC, and Other Ramifications of a
Simple Min-Cut Algorithm*, SODA 1993, pages 21-30, was downloaded to temporary storage and
inspected. The 10-page, 224338-byte PDF has SHA-256
`f090415d0aeeeaa7c907f76bb78fc2ce9293fd45c6bbca19276a5a5eb0c354cd`; extracted text has SHA-256
`78976ca293150e16fa33322eb1279b78882a55f7dea0b84a0ecce2cee98f9890`. Section 2 defines
multigraph contraction, Theorem 2.1 gives the fixed-minimum-cut `Omega(n^-2)` result with explicit
`1 / binom(n, 2)` proof bound, and Corollary 2.1 gives amplification. This supports the scope map,
but target selection, full definition/premise mapping, correction status, independent review, and
H0 remain open.

## Environment

- Platform: Linux `7.0.0-27-generic`, x86_64.
- Lean: `4.29.0`, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- Lake: `5.0.0-src+98dc76e`.
- Pinned mathlib: `8a178386ffc0f5fef0b77738bb5449d50efeea95`; tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; package source status clean.
- `Formalizations/Lean/lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `Formalizations/Lean/lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Commands and results

All repository commands ran at the repository root unless a different `cwd` is shown.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0831` | exit 0; rank 1389, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| initial `git status --short --untracked-files=all` | exit 0; only the automation-provided untracked `Formalizations/Lean/.lake` symlink existed before intake |
| `git rev-parse HEAD 'HEAD^{tree}'` | exit 0; base revision and tree recorded above |
| `git blame -L 6103,6108 -- Docs/researches/math_theorems.md` | exit 0; all six uncited catalog lines originate in commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `curl -L --fail --max-time 60 -sS https://people.csail.mit.edu/karger/Papers/mincut.pdf -o /tmp/thm-m-0831-karger-mincut.pdf` | exit 0; observed PDF byte count and SHA-256 recorded above |
| `pdfinfo` and `pdftotext -layout` on the temporary PDF, followed by Section 1-2 inspection | exit 0; 10 pages; graph/cut model, contraction algorithm, Theorem 2.1 proof, and Corollary 2.1 crosswalked |
| `curl -L --fail --max-time 60 -sS https://dblp.org/rec/conf/soda/Karger93.bib -o /tmp/thm-m-0831-karger.bib` | exit 0; DBLP confirmed author, title, SODA 1993, pages 21-30; BibTeX SHA-256 `b05e844f0af9317c7ad4416b3a155f8060374e63b09be04e9b13a66586941aff` |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | exit 0; versions recorded above; no update or build run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | exit 0; pinned revision/tree above; package worktree clean |
| `rg -n -i 'Karger\|min.?cut\|minimum cut\|edge contraction\|contract.*vertex\|vertex.*contract' Formalizations/Lean/AwesomeTheorems Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'` | expected no-match exit 1; no candidate declaration found; search-output SHA-256 was the empty-file hash `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0831/IntakeProbe.lean)` | exit 0; ten multigraph and finite-sampling APIs elaborated; stdout SHA-256 `91f3035c7ca8b77949624c692bc49f833a487aa5cf8f0c02ae157515d86b7a1d` |
| `python3 -m json.tool` on `instance.json`, `task-dag.json`, `intake-receipt.json`, and `.stage1-worker-selftest.json` | exit 0 for each after finalization |
| Python `ast.parse` on `Stage1_Instances/THM-M-0831/check_intake.py` | exit 0; scoped validator parses without writing bytecode |
| `python3 -B Stage1_Instances/THM-M-0831/check_intake.py --worker-packet .stage1-worker-selftest.json` | exit 0 after finalization; manifest/DAG identity, null target, H5/M4/R4 boundary, source/pins/hashes, receipt/packet, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-0831/check_intake.py` | exit 0; public replay mode passes without the scheduler-only packet |
| `rg -n -e '\bsorry\b' -e '\badmit\b' -e '\bsorryAx\b' -e '^[[:space:]]*axiom\b' -e '^[[:space:]]*constant\b' -e '^[[:space:]]*opaque\b' -e '^[[:space:]]*unsafe\b' Stage1_Instances/THM-M-0831 --glob '*.lean'` | expected no-match exit 1; no prohibited declaration in the API-only probe |
| `for f in .stage1-worker-selftest.json Stage1_Instances/THM-M-0831/*; do git diff --no-index --check /dev/null "$f"; done` with expected new-file exit 1 handled per file | all files produced no whitespace diagnostics |
| `git diff --check -- Stage1_Instances/THM-M-0831 .stage1-worker-selftest.json` | exit 0; tracked-diff command emitted no diagnostics; untracked-file coverage comes from the preceding no-index checks |

## Known open gates

- Master acceptance of this intake is pending.
- A reviewer must select the single-trial fixed-cut theorem, amplification, weighted result,
  algorithm correctness, runtime, RNC result, or another exact source claim, then map all
  definitions, assumptions, conclusions, corrections, probability conventions, and boundary cases.
- Canonical Lean target, minimal imports, expression and environment fingerprints, checked
  transports, and all four required statement mutations remain open.
- Exhaustive formal anchor and proof-body provenance audit, discovery protocol, obligation registry,
  typed graphs, proof, composition, trust closure, readable reconstruction, hermetic replay,
  deterministic bundle, independent verification, audit completion, and theorem completion remain
  open.

These failures block statement and theorem execution but do not invalidate a truthful, self-tested
`planned` intake. Only the integration lane may accept the provisional worker receipt.
