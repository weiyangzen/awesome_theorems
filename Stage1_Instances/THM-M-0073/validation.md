# Intake validation

Base revision: `5fe11f4b5e32a06ffb4432460319fc8ae906fe7b` (tree
`64c5aacf7cf3eb79008f5a1970151e3e53cb9966`). Validation date: 2026-07-13
(Asia/Shanghai).

This validation covers manifest membership, the planned dossier, source-identity and
non-substitution boundaries, the open task DAG, scoped intake invariants, and a narrow pinned Lean
API probe. It does not validate a canonical Goldschmidt proposition or proof because neither is
frozen. The automation-provided canonical `.lake` symlink was pre-existing and used read-only; no
update, build, clone, fetch, or other `.lake` mutation was performed. The dirty worker run is
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

## Commands and results

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; all 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0073` | exit 0; rank 1527, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `git status --short --untracked-files=all` | preflight exit 0; only the automation-provided untracked `Formalizations/Lean/.lake` symlink existed before this intake |
| `git blame -L 540,545 -- Docs/researches/math_theorems.md` | exit 0; all six uncited catalog lines originate in commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| Crossref and official Annals inspection for DOI `10.2307/1971040` | exit 0; David M. Goldschmidt, 1975, pages 475-489 located; Crossref SHA-256 `88977d0e35b45eadf5381e465b64fe47b9a49bb7bcb4aa62b567fa5b5933f1e5`; publisher page SHA-256 `1110278e0e8fc968aa9590e2acadd127f2129ebeed4b21008ee7bd20cb1ff9a1`; no abstract or exact theorem passage available |
| Crossref and official Annals inspection for DOI `10.2307/1971014` | exit 0; David M. Goldschmidt, 1974, pages 70-117 located; Crossref SHA-256 `35fe97f837c982f0ea9e3abbf49fe5fce66b84b79cb6571ac6e50aca5b558e95`; publisher page SHA-256 `b2e4338ebd3015327cf2852cc94d25ecc9f85e7ed9c46a8e9b97086c04a2eea7`; no abstract or exact theorem passage available |
| bounded inspection of arXiv `2011.05011v2` | exit 0; Theorem 5.9 states the modern Alperin-Goldschmidt generation equality; PDF SHA-256 `19a1a29a9c5d8f4352aad511dcf7f8c522493db930091a490d67ce4b30721602`; secondary statement-family witness only |
| `git -C Formalizations/Lean/.lake/packages/mathlib grep -in -E 'Goldschmidt\|fusion.?system\|strongly.?closed' HEAD -- Mathlib` | exit 1 as expected; no exact topic declaration located |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | exit 0; versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | exit 0; pinned revision and tree recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | exit 0; empty output |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0073/IntakeProbe.lean)` | exit 0; ten conjugacy, Sylow, normalizer, transfer, and focal APIs elaborated; two inspected declarations reported only `propext`, `Classical.choice`, and `Quot.sound`; stdout SHA-256 `2bcc942a57a1dfb0d1ad70e90eefe4e55a4b80860c5b06593211d18648952f0b`; no target theorem declared |
| `python3 -m json.tool` on `instance.json`, `task-dag.json`, `intake-receipt.json`, and `.stage1-worker-selftest.json` | exit 0 for each finalized JSON artifact |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0073-pycache python3 -m py_compile Stage1_Instances/THM-M-0073/check_intake.py` | exit 0; scoped validator compiled without generated files in the owned path |
| `python3 -B Stage1_Instances/THM-M-0073/check_intake.py --worker-packet .stage1-worker-selftest.json` | exit 0; target/DAG identity, source and pin hashes, H1/M4/R4 null-target boundary, exact inventory, packet agreement, Lean replay, and six open tasks agree |
| `rg -n --glob '*.lean' '(^|[^A-Za-z])(sorry|admit|sorryAx|axiom|constant|opaque|unsafe)([^A-Za-z]|$)' Stage1_Instances/THM-M-0073` | exit 1 as expected; no prohibited declaration or proof escape matched |
| scoped per-new-file `git diff --no-index --check` loop, followed by `git diff --check -- Stage1_Instances/THM-M-0073 .stage1-worker-selftest.json` | exit 0; every new file passed the explicit whitespace check, with no tracked-diff diagnostics |

## Known open gates

Exact catalog-source identity, one admitted source edition and theorem passage, complete
definition/assumption/errata crosswalk, independent source review, classical-versus-abstract fusion
domain, essential-subgroup definition, generation/factorization encoding, binder order, and boundary
cases remain open. So do canonical target elaboration and mutations, exhaustive
anchor/provenance/trust audits, discovery and obligation freezes, typed graphs, proof and
composition, readable reconstruction, hermetic replay, deterministic bundle, independent
verification, master acceptance, audit completion, and theorem completion. These open gates do not
invalidate a truthful self-tested `planned` intake.

Schema authority remains an integration boundary: the artifacts use the repository's prevalent
`stage1-instance-intake/1.0`, `stage1-open-task-dag/1.0`, and `stage1-node-receipt/1.0` identifiers
and the scoped checker enforces their intake fields, but no repository-wide published strict-schema
validator was found. This worker does not claim that master schema-acceptance gate.
