# Intake validation

Base revision: `d502dd6f3d278ca9cb0ead8cbdc5f16c0e1fd8c9` (tree
`829a47c47ae831cada4f8acc6c2c00ba5883215e`). Validation date: 2026-07-13
(Asia/Shanghai).

This validation covers target membership, the planned dossier, simple-set/simplicial-set scope
boundary, source-statement crosswalk, open task DAG, JSON and scoped invariants, and a narrow pinned
Lean API/prospective-shape probe. It does not validate a canonical source statement or proof because
the primary definition and existence passage have not been inspected and frozen. The
automation-provided canonical `.lake` symlink was pre-existing and used read-only; no dependency
update, build, clone, fetch, or other `.lake` mutation was performed. This dirty worker evidence is
nonrelease evidence.

## Environment

- Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, target
  `x86_64-unknown-linux-gnu`.
- Lake `5.0.0-src+98dc76e`.
- Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; its package worktree was clean.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Commands and results

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0747` | exit 0; rank 1030, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | pre-edit exit 0; only the automation-provided `Formalizations/Lean/.lake` symlink existed; base revision/tree recorded above |
| repository record, Stage0 projection, and neighboring recursion-theory source inspection | exit 0; identified computability-theoretic simple-set existence and excluded the topological simplicial-set reading and weaker noncomputable-c.e.-set gloss |
| `curl -L --fail --max-time 30 -A 'Mozilla/5.0' -sS 'https://api.crossref.org/works/10.1090/S0002-9904-1944-08111-1' -o /tmp/thm-m-0747-crossref.json` then scoped `jq` and `sha256sum` | exit 0; confirmed Post, title, *Bulletin AMS* 50(5), 1944, pages 284-316, DOI and official version-of-record link; response SHA-256 `efa22b14...bd48d0` |
| `curl -L --fail --max-time 60 -A 'Mozilla/5.0' -sS 'https://www.ams.org/bull/1944-50-05/S0002-9904-1944-08111-1/S0002-9904-1944-08111-1.pdf' -o /tmp/thm-m-0747-post-ams2.pdf` | curl exit 22 after HTTP 429; no file accepted and no primary-page claim made |
| `curl -L --fail --max-time 60 -sS 'https://projecteuclid.org/download/pdf_1/euclid.bams/1183505800' -o /tmp/thm-m-0747-euclid-direct.pdf` then `file`, `wc -c`, and `sha256sum` | curl exit 0, but response was a 1053-byte HTML access challenge rather than a PDF; rejected as source evidence |
| `curl -L --fail --max-time 60 -sS 'https://plato.stanford.edu/entries/recursive-functions/' -o /tmp/thm-m-0747-sep.html` then scoped `rg` and `sha256sum` | exit 0; secondary account states the standard c.e./infinite-immune-complement definition and attributes existence to Post (1944); page SHA-256 `5fa44199...a6d7`; no H0 credit |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | exit 0; pinned Lean and Lake versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | exit 0; pinned revision/tree recorded above; empty package status |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0747/IntakeProbe.lean)` | exit 0; eight adjacent pinned APIs and the prospective intersection-form proposition elaborated; no theorem declaration or proof body added |
| `rg -n --glob '*.lean' '^[[:space:]]*(def\|abbrev\|structure\|class\|theorem\|lemma)[[:space:]].*(simple[ _-]*set\|simpleSet\|immune[ _-]*set\|immuneSet)\|^[[:space:]]*(def\|abbrev\|structure\|class\|theorem\|lemma)[[:space:]]*(simple[ _-]*set\|simpleSet\|immune[ _-]*set\|immuneSet)'` over pinned mathlib and repo-local Lean | exit 1 as expected for no match; no named target definition/declaration found; bounded intake discovery, not exhaustive anchor audit |
| `python3 -m json.tool` on `instance.json`, `task-dag.json`, `intake-receipt.json`, and the worker packet | exit 0 for each after finalization |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0747-pycache python3 -m py_compile Stage1_Instances/THM-M-0747/check_intake.py` | exit 0; scoped validator compiled without creating an owned generated file |
| `python3 -B Stage1_Instances/THM-M-0747/check_intake.py --worker-packet .stage1-worker-selftest.json` | exit 0 after finalization; target/DAG identity, null canonical target, H1/M4/R4 boundary, exact artifact inventory, input hashes, worker packet, and six open tasks agree |
| `rg -n --glob '*.lean' '\b(sorry\|admit)\b\|\bsorryAx\b\|^[[:space:]]*(axiom\|constant\|opaque\|unsafe)[[:space:]]' Stage1_Instances/THM-M-0747` | exit 1 as expected for no match; no prohibited declaration or proof escape |
| `git diff --check -- Stage1_Instances/THM-M-0747 .stage1-worker-selftest.json` plus per-file `git diff --no-index --check /dev/null <new-file>` | exit 0 for the tracked check; every no-index exit was the expected new-file difference with no diagnostic; no whitespace error |

## Known open gates

Primary full-text acquisition, exact definition and existence-result locator, complete premise,
conclusion, proof-boundary and errata crosswalk, and independent source review remain open. So do
the exact canonical Lean target and environment fingerprints, checked predicate/set and
immune/intersection transports, semantic mutations, discovery protocol, obligation registry,
typed graphs, formal anchor and provenance audit, proof and composition, trust closure, readable
reconstruction, hermetic replay, deterministic evidence bundle, independent verification, master
acceptance, audit completion, and theorem completion. These failures do not invalidate a truthful
self-tested `planned` intake.
