# THM-M-0263 intake validation

Base revision: `c6fd6dad8fcfe5fd464416cd452f50286b546978` (tree
`5a80b61d8fa09336779f8d1453dcfe4299c9472f`). Validation date: 2026-07-13
(Asia/Shanghai).

Validation covers target-set consistency, the fail-closed planned dossier, the cut/order versus
metric source-statement boundary, six-node open task DAG, scoped intake invariants, and a narrow
pinned Lean API probe. It does not validate a canonical real-completeness proposition or proof:
the catalog does not select one exact formulation. The automation-provided canonical `.lake`
symlink was pre-existing and used read-only. No dependency update, build, clone, fetch, or other
`.lake` mutation was performed. This dirty worker run is nonrelease evidence.

## Environment

- Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, target
  `x86_64-unknown-linux-gnu`.
- Lake `5.0.0-src+98dc76e`.
- Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; package source status was clean before and after
  the probe.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Commands and exact results

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0263` | 0 | rank 1271; planned; `L0/rework_required`; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all` before edits | 0 | only the pre-existing automation-provided `Formalizations/Lean/.lake` symlink was untracked |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree match this record |
| `git blame -L 1894,1899 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog fields originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| download Project Gutenberg ebook 21016 TeX and inspect *Continuity and Irrational Numbers*, Section V theorem IV | 0 | artifact SHA-256 `f837b8376cbbfca11690cea3bc0fac14fffecb88ae669e4f15158f096c915f44`; lines 934-1002 excerpt SHA-256 `5ec3165fe512eeeeb524902c4cdde4c3182efd87020425cf2ce3b42c0a591c55`; source discovery only |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | versions recorded above; no update or build was run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | pinned revision and tree recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` before and after probe | 0 | empty output |
| bounded exact-topic name/documentation search over repo-local Lean and pinned mathlib | 1, expected | no exact phrase/name match; declaration candidates were found through source/API inspection; intake discovery only, not an exhaustive absence claim |
| `(cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0263/IntakeProbe.lean)` | 0 | six distinct completeness APIs and both relevant instances elaborated; stdout plus stderr SHA-256 `eebd83c158257addb356e904d089b3bb9b23089416849fef9663a01700f67386`; representative axiom reports contain only `propext`, `Classical.choice`, and `Quot.sound`; no target theorem |
| `python3 -m json.tool` on all JSON artifacts and the worker packet | 0 after finalization | valid JSON objects |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0263-pycache python3 -m py_compile Stage1_Instances/THM-M-0263/check_intake.py` | 0 | scoped validator compiled without adding generated files to the owned path |
| `python3 -B Stage1_Instances/THM-M-0263/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 after finalization | authorities, target/DAG identity, null target, H1/M3/R4 boundary, pins, artifact hashes, receipt/packet, and six open tasks agree |
| prohibited-declaration scan of `IntakeProbe.lean` | 1 | expected no-match; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| `git diff --check`, plus `git diff --no-index --check /dev/null <file>` for every new file | 0 aggregate | no whitespace diagnostics; no-index status 1 was accepted only as the expected content difference |

## Known open gates

An accountable source decision must select and independently review one immutable exact
completeness proposition. The relationship among Dedekind cut continuity, the nonempty bounded-set
least-upper-bound property, conditional-complete-order instances, Cauchy sequence/filter
convergence, and other equivalent principles remains open, as do the Weierstrass attribution,
original-edition and correction audit, domain, ordered binders, hypotheses, conclusion, uniqueness,
and degenerate cases. So do the canonical Lean expression and environment fingerprint, checked
transports, statement mutations, exhaustive formal anchor audit, discovery protocol, obligation
registry, typed graphs, proof and composition, trust and provenance closure, readable
reconstruction, hermetic replay, deterministic bundle, independent verification, master
acceptance, audit completion, and theorem completion.

These gates block ordinary theorem-proof execution but do not invalidate a truthful, self-tested
`planned` intake whose purpose is to freeze the ambiguity and dependent work. Only the integration
lane can accept the provisional node receipt.
