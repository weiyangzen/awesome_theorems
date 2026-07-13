# THM-M-1487 intake validation

Base revision: `e552e0758e29de307cf357a703e6ecd16e40fb69` (tree
`492b45021fb6ce4973452d8173d32fe2c212a877`). Validation date: 2026-07-13
(Asia/Shanghai).

Validation covers target-set consistency, the fail-closed planned dossier, source-statement and
non-substitution boundaries, the six-node open task DAG, structured intake invariants, and a narrow
pinned Lean API probe. It does not validate a canonical CNN proposition or proof: the catalog
provides a model/application gloss rather than a source-selected truth-valued statement. The
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
| `python3 scripts/stage1_target.py show THM-M-1487` | 0 | rank 1164; planned; `L0/rework_required`; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all` before edits | 0 | only the pre-existing automation-provided `Formalizations/Lean/.lake` symlink was untracked |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree match this record |
| `git blame -L 10868,10873 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog fields originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `curl -L --fail --silent --show-error 'https://api.crossref.org/works/10.1162/neco.1989.1.4.541' \| jq -cS '.message \| {DOI,title,author:[.author[]\|{given,family}],published:.published["date-parts"],container_title:."container-title",volume,issue,page,type,publisher}'` | 0 | deterministic metadata projection confirmed the LeCun et al. 1989 handwritten-ZIP-code article; output SHA-256 `f05eeaec3b93c11cfecc14daf48015ebfa62e0bb589abf1e87becca5a255fa6e` |
| bounded parallel HTTP `Range` retrieval of `http://yann.lecun.com/exdb/publis/pdf/lecun-89e.pdf` in 131,072-byte chunks, ordered concatenation, then `stat -c '%s'`, `sha256sum`, and `pdfinfo` | 0 | the author-hosted scan is 11 pages and 5,661,991 bytes with SHA-256 `378c00b2b3e2f461b79848ef88f671eefdf1dcfde28ad945d15751bccc91fff1`; it presents architecture plus empirical results rather than a selected theorem proof; discovery only |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | versions recorded above; no update or build was run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | pinned revision and tree recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | 0 | empty output |
| `rg -n -i --glob '*.lean' 'convolutional[ _-]?neural\|neural[ _-]?network\|convnet\|backpropagation\|handwritten\|zip code recognition\|LeCun' Formalizations/Lean/.lake/packages/mathlib/Mathlib Formalizations/Lean/AwesomeTheorems` | 0 | one comment says holors are called tensors in the neural-network community; no CNN, ConvNet, backpropagation, handwritten-recognition, or LeCun terminal declaration; intake discovery only |
| `(cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-1487/IntakeProbe.lean)` | 0 | ten adjacent holor, matrix, and sigmoid APIs elaborated; stdout SHA-256 `f13f0069714bc17f2203e7636ec663a2311bb3023a47e37c20978be4216f3a74`; representative axiom reports contain only `propext`, `Classical.choice`, and `Quot.sound`; no target theorem |
| `python3 -m json.tool` on all JSON artifacts and the worker packet | 0 after finalization | valid JSON objects |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-1487-pycache python3 -m py_compile Stage1_Instances/THM-M-1487/check_intake.py` | 0 | scoped validator compiled without adding generated files to the owned path |
| `python3 -B Stage1_Instances/THM-M-1487/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 after finalization | target/DAG identity, null target, H5/M4/R4 boundary, pins, inventory, receipt/packet, and six open tasks agree |
| `rg -n --glob '*.lean' '\b(sorry\|admit)\b\|\bsorryAx\b\|^[[:space:]]*(axiom\|constant\|opaque)\b\|^[[:space:]]*unsafe\b' Stage1_Instances/THM-M-1487` | 1 | expected no-match result; no prohibited declaration |
| scoped final-newline, LF, NUL, trailing-whitespace, no-index diff, and `git diff --check` checks | 0 | no diagnostics |

## Known open gates

An accountable correction must select and independently review one immutable exact proposition.
The architecture, image/task and data models, convolution convention, domains, parameters,
activation and pooling, training or statistical semantics, hypotheses, ordered binders, exact
conclusion, constants, arithmetic and oracle boundaries, source proof rather than empirical
boundary, corrections, and degenerate cases remain open. So do the canonical Lean expression and
environment fingerprint, checked transports, statement mutations, exhaustive formal anchor audit,
discovery protocol, obligation registry, typed graphs, proof and composition, trust and provenance
closure, readable reconstruction, hermetic replay, deterministic bundle, independent verification,
master acceptance, audit completion, and theorem completion.

These open gates block ordinary theorem-proof execution but do not invalidate a truthful,
self-tested `planned` intake whose purpose is to freeze the ambiguity and dependent work. Only the
integration lane can accept the provisional node receipt.
