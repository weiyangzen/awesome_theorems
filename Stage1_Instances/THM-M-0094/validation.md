# Intake validation

Base revision: `d266c6f5ce5732e1fccd687e2f9ce9aa2a0ed1fe` (tree
`e77c8d6d5b41cb13d9d8acab2753ac37c4ebd6b4`). Validation date: 2026-07-13
(Asia/Shanghai).

This validation covers target membership, the planned dossier, source and non-substitution
boundaries, adjacent pinned interfaces, the open task DAG, scoped intake invariants, and a narrow
Lean API probe. It does not validate a canonical Borel-Weil-Bott proposition or proof because
neither is frozen. The automation-provided canonical `.lake` symlink was pre-existing and used
read-only; no dependency update, build, clone, fetch, or other `.lake` mutation was performed. This
dirty worker run is nonrelease evidence.

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
- Global-sections module SHA-256:
  `b88365383a304bd7eb2ae76ad71b0e1c0448ab7b941b0f71d6aa57afc6744dc7`.
- Sheaf-cohomology module SHA-256:
  `8765b1daa9cca22fe316be0619f110f8fff814ae1bb7a70c42f9cfbc4ba8a6f8`.
- Scheme module-sheaf module SHA-256:
  `39ad16dcfaafa9f6d6d8c3546f4fbd59153a1e25255c7ab80c98d4dcb0bcd762`.
- Lie-weight root-system module SHA-256:
  `1912f5af53a4f749aa6715946c7583045495e8ca45a11953c1ced44ea784d5e8`.
- Irreducible-representation module SHA-256:
  `6c94c6476ca26e443d0ec5fe0314deeeb3c01e3beae70247a1d96e3ca0a5c195`.
- Lie-group module SHA-256:
  `2ecc19306d5132c15b9bd988324aa6fc4ce39574648d5b6878bef76a1a8162c0`.

## Commands and results

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, and execution skill presence passed |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0094` | exit 0; rank 1111, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `git status --short --untracked-files=all` | preflight exit 0; only the pre-existing automation-provided `Formalizations/Lean/.lake` symlink existed before intake |
| `git blame -L 691,696 -- Docs/researches/math_theorems.md` | exit 0; all six uncited catalog fields originate in commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| bounded Crossref queries for Bott's *Homogeneous Vector Bundles* and Borel's compact homogeneous-space paper | exit 0; 1957 DOI `10.2307/1969996` and 1953 DOI `10.2307/1969728` authenticated; metadata only and no H0 credit |
| bounded DOI retrieval attempt for Bott's paper | transport reached the publisher, then returned HTTP 403; no article text, exact theorem passage, or correction boundary was inspected |
| `curl -L --fail --max-time 30 https://www.math.ias.edu/~lurie/papers/bwb.pdf` plus `pdftotext` | exit 0; modern proof note Theorem 5 and its conventions inspected; PDF SHA-256 `57d1df87dc0641ec70bc2e353830897dcabd88dd973d82365ee30713f0a1f8f1`; not the original historical source and not admitted as H0 or the canonical root |
| bounded repo-local and pinned-mathlib exact-topic `rg` plus source inspection | exact-topic search returned no match; adjacent sheaf, cohomology, scheme-module, Lie-weight/root, representation, and Lie-group interfaces found, but no Borel-Weil-Bott declaration, flag-variety theorem, or complete bridge |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | exit 0; versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | exit 0; pinned revision and tree recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | exit 0; empty output before and after the probe |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0094/IntakeProbe.lean)` | exit 0; eleven adjacent APIs elaborated; three inspected theorems reported only `propext`, `Classical.choice`, and `Quot.sound`; complete stdout SHA-256 `aef2267700d64ad128c97ae0e86c34d00ae1b4947f5ed82a9de701b52d86f1b5`; no target theorem declared |
| `python3 -m json.tool` on `instance.json`, `task-dag.json`, `intake-receipt.json`, and the root worker packet | exit 0 for each after finalization |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0094-pycache python3 -m py_compile Stage1_Instances/THM-M-0094/check_intake.py` | exit 0; scoped validator compiled without generated files in the owned path |
| `python3 -B Stage1_Instances/THM-M-0094/check_intake.py --worker-packet .stage1-worker-selftest.json` | exit 0; manifest and authoritative-DAG identity, H1/M4/R4 planned boundary, null target, source and pin hashes, exact artifact inventory, provisional receipt/packet, and six open tasks agree |
| prohibited Lean construct scan over `IntakeProbe.lean` | exit 1 as expected; no match for `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` |
| scoped `git diff --no-index --check /dev/null <new-file>` loop, followed by `git diff --check -- Stage1_Instances/THM-M-0094 .stage1-worker-selftest.json` | exit 0; every new owned file and the worker packet passed explicit whitespace validation, with no tracked-diff diagnostics |

## Known open gates

A lawful primary source edition and exact theorem passage/page, complete definition and assumption
crosswalk, Borel/Weil/Bott attribution and 1954/1957 date reconciliation, translation/correction/
errata audit, modern-formulation transport, and independent source review remain open. So do the
full Borel-Weil-Bott formulation and degree-zero special-case relationship, group category, flag
variety, homogeneous line bundle, weight and sign convention, Weyl dot action, regular/singular split, cohomological degree and vanishing,
returned representation and dual convention, binder order, and boundary cases. Exact target
elaboration and mutations, exhaustive anchor and provenance audits, discovery and obligation
freezes, typed graphs, proof and composition, readable reconstruction, hermetic replay,
deterministic evidence bundle, independent verification, master acceptance, audit completion, and
theorem completion also remain open. These open gates do not invalidate a truthful self-tested
`planned` intake.

## Status boundary

This is provisional worker self-test evidence for `S56-M-0094-INTAKE` only. It supports a planned
dossier, not an accepted node receipt. No canonical statement, H0 source closure, formal candidate,
proof, audit completion, theorem completion, or master acceptance is claimed.
