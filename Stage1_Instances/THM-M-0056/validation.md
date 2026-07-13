# Intake validation

Validation date: 2026-07-13 (Asia/Shanghai). This is a nonrelease worker check against repository
revision `b56df790fc94c5366cf919a6fe5411d06b427c59` and tree
`18ba629d4c00333f6e17018905f4fbd30558bb4c`. The automation-provided `.lake` symlink was already
untracked and was used read-only. No `lake update`, `lake build`, dependency clone/fetch, or other
`.lake` mutation was run.

## Results

| Command | Exit | Exact result or boundary |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0056` | 0 | rank 1523; planned; `L0/rework_required`; no legacy slot; theorem incomplete |
| `git status --short --untracked-files=all` before editing | 0 | only the pre-existing automation-provided `Formalizations/Lean/.lake` symlink was present; it was preserved |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | revision `b56df790fc94c5366cf919a6fe5411d06b427c59`; tree `18ba629d4c00333f6e17018905f4fbd30558bb4c` |
| `git blame -L 419,424 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog fields originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `curl -L --fail --silent --show-error --max-time 90 https://zenodo.org/record/1526112/files/article.pdf` and `pdftotext -layout` | 0 | 39-page Weyl 1912 public-domain scan; SHA-256 `47a614bca926c86e874335398c589ac4b3fac77452dc2859882f5f6001fda5af`; Section 1 and Satz I inspected as source-family evidence only |
| `curl -L --fail --silent --show-error --max-time 90 https://arxiv.org/pdf/1910.01966v4` and `pdftotext -layout` | 0 | 10-page versioned modern paper; SHA-256 `7ac7b4f9ca55ff5c6a5dd31cd92ec4e12672ea9098497faa6ff5359782cdd66a`; page 1 convention and Corollary 2.5 inspected as an uncredited lead |
| Crossref queries for DOI `10.1007/BF01456804` and `10.1080/03081087.2020.1765957` | 0 | bibliographic fields matched the recorded historical and modern works; metadata is not proof evidence |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, x86_64 Linux |
| `cd Formalizations/Lean && lake --version` | 0 | Lake `5.0.0-src+98dc76e`; no update or build was run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`; tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b` |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --porcelain` | 0 | empty output; pinned mathlib remained clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0056/IntakeProbe.lean` | 0 | nine adjacent pinned declarations elaborated; complete stdout SHA-256 `85d8d4a812b6f3d91ebddb60d20a61c3d59cced0f433e5fa24160f1e3e407a71`; no target or proof body |
| bounded exact-topic Lean search | 0 | only one unrelated eigenvalue-assumption prose match; no Weyl eigenvalue-of-sum or perturbation declaration identified |
| bounded Courant-Fischer/minimax Lean search | 1 | expected no-match; no indexed eigenvalue minimax declaration located in the searched matrix and inner-product-space files |
| prohibited-declaration scan of the owned Lean probe | 1 | expected no-match: no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` token |
| `python3 -m json.tool` on the owned structured files and root worker packet | 0 | valid JSON |
| `python3 -B Stage1_Instances/THM-M-0056/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | target/DAG identity, source and dependency hashes, null target, provisional `H1/M4/R4`, exact inventory, packet agreement, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-0056/check_intake.py` | 0 | public replay mode passes without the scheduler-only packet |
| `git diff --check -- Stage1_Instances/THM-M-0056 .stage1-worker-selftest.json` plus per-file no-index checks | 0 | no whitespace diagnostics; no-index exit 1 represented only each expected new-file diff |

## Boundary

This validates only a `planned` intake dossier, scope map, source-statement crosswalk, adjacent Lean
API probe, and open downstream task DAG. The canonical human and Lean statements remain null because
the catalog does not select a source-identical variant, domain, index scheme, or norm. The first
blocked downstream gate is `S56-M-0056-STATEMENT`. No source is accepted to `H0`; no formal artifact
is accepted to `M0`; no proof reconstruction is accepted to `R0`; and no audit or theorem completion
is claimed.

The receipt timestamps delimit validation of non-receipt inputs. Receipt serialization and later
replay necessarily occur after that cutoff and are not represented as a release-grade signed time
attestation; the packet is explicitly mutable, provisional, and non-content-addressed.
