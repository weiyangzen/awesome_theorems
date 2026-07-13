# THM-M-1479 intake validation

Base revision: `fc0de001c634823043636f9380a991c027e42533` (tree
`b2e4d058036a1e9ec56bfc6aa5de3b015efe6330`). Validation date: 2026-07-13
(Asia/Shanghai).

Validation covers target-set consistency, the fail-closed planned dossier, source-statement and
non-substitution boundaries, the six-node open task DAG, structured intake invariants, and a narrow
pinned Lean API probe. It does not validate a canonical Monte Carlo proposition or proof: the
catalog provides a method-family gloss rather than a source-selected truth-valued statement. The
automation-provided canonical `.lake` symlink was pre-existing and used read-only. No dependency
update, build, clone, fetch, or other `.lake` mutation was performed. This dirty worker run is
nonrelease evidence.

## Environment

- Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, target
  `x86_64-unknown-linux-gnu`.
- Lake `5.0.0-src+98dc76e`.
- Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; package source status was clean.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Commands and exact results

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-1479` | 0 | rank 1156; planned; `L0/rework_required`; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all` before edits | 0 | only the pre-existing automation-provided `Formalizations/Lean/.lake` symlink was untracked |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree match this record |
| `git blame -L 10791,10796 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `curl -LsS --fail 'https://api.crossref.org/works/10.1080/01621459.1949.10483310' \| jq -c '{DOI:.message.DOI,title:.message.title,author:[.message.author[]\|{given,family}],published:.message.published,volume:.message.volume,issue:.message.issue,page:.message.page,container:.message["container-title"],type:.message.type}' \| sha256sum` | 0 | deterministic projection SHA-256 `d4061580fd50532e28d984325f3ca201629efe280e4653969e6d2e43e26d7dbf`; bibliographic discovery only |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | versions recorded above; no update or build was run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | pinned revision and tree recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | 0 | empty output |
| `rg -n -i 'THM-M-1479\|Monte.?Carlo\|random sampling\|随机采样' Formalizations/Lean/AwesomeTheorems Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'` | 0 | one unrelated mathlib bibliography mention; output SHA-256 `51897e9eb7ac1f2631f633f9a821a9d7b1b3b04691a1c4048038a7bc8bc04565`; no source-selected estimator or terminal theorem |
| `(cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-1479/IntakeProbe.lean)` | 0 | eight adjacent probability APIs elaborated; stdout/stderr SHA-256 `804eac01ac63d5f11fb964e6a055933afbdc0770de775ec89f7f177fde6df665`; three representative axiom reports contained only `propext`, `Classical.choice`, and `Quot.sound`; no target theorem |
| `for f in Stage1_Instances/THM-M-1479/*.json .stage1-worker-selftest.json; do python3 -m json.tool "$f" >/dev/null \|\| exit; done` | 0 after finalization | all JSON objects parsed |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-1479-pycache-final python3 -m py_compile Stage1_Instances/THM-M-1479/check_intake.py` | 0 | scoped validator compiled without adding generated files to the owned path |
| `python3 -B Stage1_Instances/THM-M-1479/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 after finalization | manifest/DAG identity, null target, H5/M4/R4 boundary, pins, artifact hashes, provisional receipt/packet, and six open tasks agree |
| `if rg -n --glob '*.lean' '\b(sorry\|admit\|sorryAx\|axiom\|constant\|opaque\|unsafe)\b' Stage1_Instances/THM-M-1479; then exit 1; fi` | 0 | expected no-match branch; no prohibited declaration |
| `git diff --check -- Stage1_Instances/THM-M-1479 .stage1-worker-selftest.json` | 0 | no diagnostics; the scoped intake checker separately performs final-newline, LF, NUL, trailing-whitespace, and per-file `git diff --no-index --check` checks |

## Known open gates

An accountable correction must select and independently review one immutable exact proposition.
The target quantity, domains and measures, sampling law, estimator or algorithm, sample indexing,
measurability/integrability/moment assumptions, convergence or error notion, conclusion, constants,
rates, quantifier order, computation/randomness boundary, corrections, and degenerate cases remain
open. So do the canonical Lean expression and environment fingerprint, checked transports,
statement mutations, exhaustive formal anchor audit, discovery protocol, obligation registry,
typed graphs, proof and composition, trust and provenance closure, readable reconstruction,
hermetic replay, deterministic bundle, independent verification, master acceptance, audit
completion, and theorem completion.

These open gates block ordinary theorem-proof execution but do not invalidate a truthful,
self-tested `planned` intake whose purpose is to freeze the ambiguity and dependent work. Only the
integration lane can accept the provisional node receipt.
