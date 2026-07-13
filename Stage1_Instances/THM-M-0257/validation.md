# THM-M-0257 intake validation

Base revision: `c6fd6dad8fcfe5fd464416cd452f50286b546978` (tree
`5a80b61d8fa09336779f8d1453dcfe4299c9472f`). Validation date: 2026-07-13
(Asia/Shanghai).

Validation covers target-set consistency, the fail-closed planned dossier, the source-statement and
neighbor boundaries, the six-node open task DAG, structured intake invariants, and a narrow pinned
Lean API probe. It does not validate a canonical Ahlfors-Bers proposition or proof because the
catalog does not choose among materially different source and theorem variants. The pre-existing
automation-provided `.lake` symlink was used read-only. No dependency update, build, clone, fetch,
or other `.lake` mutation was performed. This dirty worker run is nonrelease evidence.

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
| `python3 scripts/stage1_target.py show THM-M-0257` | 0 | rank 1265; planned; `L0/rework_required`; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all` before edits | 0 | only the pre-existing automation-provided `Formalizations/Lean/.lake` symlink was untracked |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree match this record |
| `git blame -L 1850,1855 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog fields originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| bounded Crossref work lookups for the four recorded 1960/1961 DOIs | 0 | joint Ahlfors-Bers paper, Ahlfors complex-structure chapter, Bers bounded-domain article, and Bers correction metadata confirmed; discovery only |
| bounded extracted-summary inspection for the Bers article and correction | 0 | exposed finite-type/marking assumptions and a correction to an invalid lemma in the proof sketch; summaries are not admitted primary texts or H0 evidence |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | versions recorded above; no update or build was run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | pinned revision and tree recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` before and after probe | 0 | empty output |
| `rg -n -i --glob '*.lean' 'Ahlfors.?Bers\|Teichm[uü]ller[ _-]+space\|TeichmullerSpace\|quasiconformal\|Beltrami[ _-]+coefficient\|measurable[ _-]+Riemann[ _-]+mapping' Formalizations/Lean/AwesomeTheorems Formalizations/Lean/.lake/packages/mathlib/Mathlib` | 1 | expected no match for the bounded exact-topic terms; intake discovery only, not an exhaustive anchor audit |
| `(cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0257/IntakeProbe.lean)` | 0 | twelve adjacent pinned APIs elaborated; stdout plus stderr SHA-256 `bc9f031ddd49b19ffb8a1f58e1732f9a6875829918759bfc9db5db8f91bef0a6`; no target theorem |
| `python3 -m json.tool` on all JSON artifacts and the worker packet | 0 after finalization | valid JSON objects |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0257-pycache python3 -m py_compile Stage1_Instances/THM-M-0257/check_intake.py` | 0 | scoped validator compiled without adding generated files to the owned path |
| `python3 -B Stage1_Instances/THM-M-0257/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 after finalization | authorities, target/DAG identity, null target, H1/M4/R4 boundary, pins, artifact hashes, receipt/packet, and six open tasks agree |
| prohibited-declaration scan of `IntakeProbe.lean` | 1 | expected no match; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| `git diff --check`, plus final-LF/CR/NUL/trailing-whitespace checks in `check_intake.py` | 0 | no whitespace diagnostics in the complete owned inventory |

## Known open gates

An accountable source correction must select and independently review one immutable exact
proposition. Catalog identity; primary theorem, proof and correction mapping; surface class;
marking and equivalence; Teichmuller model; Beltrami coefficient and equality conventions; norm
bound; normalization; solution regularity; quotient and chart construction; analytic conclusion;
ordered binders; and boundary cases remain open. So do the canonical Lean expression and
environment fingerprint, checked transports, statement mutations, exhaustive anchor audit,
discovery protocol, obligation registry, typed graphs, proof and composition, trust and provenance
closure, readable reconstruction, hermetic replay, deterministic bundle, independent verification,
master acceptance, audit completion, and theorem completion.

These open gates block ordinary theorem-proof execution but do not invalidate a truthful,
self-tested `planned` intake whose purpose is to freeze ambiguity and dependent work. Only the
integration lane can accept the provisional node receipt.
