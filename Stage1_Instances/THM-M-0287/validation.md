# THM-M-0287 intake validation

Base revision: `2eea98305d46266f078a50cf0e85853bf6a5e702` (tree
`02279a8caa5f31ed8e37e35c8584a336eed9b974`). Validation date: 2026-07-13
(Asia/Shanghai).

Validation covers target-set consistency, the fail-closed planned dossier, repository and
primary-source discrimination, the six-node open task DAG, structured intake invariants, and a
narrow pinned Lean API probe. It does not validate a canonical Lusin proposition or proof because
the catalog does not choose among materially different historical and modern variants.

The initial worktree contained only the automation-provided untracked `Formalizations/Lean/.lake`
symlink to canonical pinned artifacts. It was used read-only. No `lake update`, `lake build`,
dependency clone or fetch, network-triggering Lake operation, or other `.lake` mutation was
performed. The owned intake files and root worker packet make the final tree dirty and nonrelease.

## Source boundary

The uncited catalog record was traced to its introduction commit. A public-domain Gallica scan of
Lusin's 1912 note was located through the BnF OAI, pagination, table-of-contents, content-search,
and IIIF services. Printed pages 1688-1690 were inspected; page 1689 contains the large perfect-set
relative-continuity theorem described in the crosswalk. Each inspected 1600-by-2165 page image was
hashed. This is a strong source lead only: catalog-to-source identity, exact translation and
definition chain, corrections or errata, proof boundary, and independent review remain open.

## Environment

- Platform: Linux `7.0.0-27-generic`, x86_64, Asia/Shanghai.
- Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, target
  `x86_64-unknown-linux-gnu`.
- Lake `5.0.0-src+98dc76e`.
- Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; package source status was clean before and after
  the probe.
- `Formalizations/Lean/lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `Formalizations/Lean/lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Commands and exact results

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0287` | 0 | rank 1293; planned; `L0/rework_required`; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all` before edits | 0 | only the pre-existing automation-provided `Formalizations/Lean/.lake` symlink was untracked |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree match this record |
| `git blame -L 2062,2067 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog fields originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| bounded BnF Gallica OAI/pagination/TOC/content-search/IIIF inspection | 0 | volume 154, 17 June 1912, pages 1688-1690 identified and inspected; page 1689 states the interval large-perfect-set continuity theorem; three page-image digests are in `instance.json`; source lead only |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | versions recorded above; no update or build was run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | pinned revision and tree recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` before and after probe | 0 | empty output |
| bounded exact-topic `rg` over repo-local Lean and pinned mathlib | 0 only for a distinct name match | found the unrelated Lusin separation comment; no usual large-measure continuous-restriction declaration; intake discovery only |
| `(cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0287/IntakeProbe.lean)` | 0 | six adjacent pinned APIs elaborated; complete output SHA-256 `c3532189de5c770680d83f72305b0d8bece4f3297925bcb84436fbed0d0d4aaf`; no target theorem |
| `python3 -m json.tool` on all structured intake artifacts and the worker packet | 0 after finalization | valid JSON objects |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0287-pycache python3 -m py_compile Stage1_Instances/THM-M-0287/check_intake.py` | 0 | scoped validator compiled without adding generated files to the owned path |
| `python3 -B Stage1_Instances/THM-M-0287/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 after finalization | authorities, target/DAG identity, null target, H1/M4/R4 boundary, pins, source and artifact hashes, receipt/packet, and six open tasks agree |
| prohibited-declaration scan of `IntakeProbe.lean` | 1 (expected no match) | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| per-file whitespace checks plus `git diff --check -- Stage1_Instances/THM-M-0287 .stage1-worker-selftest.json` | 0 | no LF, CR, NUL, trailing-space, or tracked-diff whitespace diagnostics in the complete inventory |

## Known open gates

An accountable source review must select one immutable exact proposition and approve catalog
identity, source edition and passage, definitions, translation, assumptions, proof and corrections.
Historical versus modern form; domain and topology; measure and regularity; codomain and
measurability; perfect/closed/compact large set; relative continuity versus global representative;
epsilon, binders, and boundary cases remain open. So do the canonical Lean expression and
environment fingerprint, checked transports, statement mutations, exhaustive anchor/provenance
audit, discovery protocol, obligation registry, typed graphs, proof and composition, trust closure,
readable reconstruction, hermetic replay, deterministic bundle, independent verification, master
acceptance, audit completion, and theorem completion.

These open gates block statement and proof execution but do not invalidate a truthful,
self-tested `planned` intake whose purpose is to freeze the source and scope boundary. Only the
integration lane can accept the provisional node receipt.
