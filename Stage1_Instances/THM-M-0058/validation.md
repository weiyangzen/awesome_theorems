# Intake validation

Validation date: 2026-07-13 (Asia/Shanghai). This is a nonrelease worker check against repository
revision `5fe11f4b5e32a06ffb4432460319fc8ae906fe7b` and tree
`64c5aacf7cf3eb79008f5a1970151e3e53cb9966`. The automation-provided `.lake` symlink was already
untracked and points to a writable cache shared by concurrent workers. This worker issued no
`lake update`, `lake build`, dependency clone, or dependency fetch command. During the validation
window, however, that shared cache changed externally: an initially incomplete `flt-regular`
checkout made a replay fail because `HEAD` was unresolved, and the checkout was subsequently
materialized at the manifest pin by an unattributed concurrent process. The successful final probe
was therefore rerun with outbound networking denied and the resolved canonical `.lake` target
mounted read-only; no cache mutation from that replay is claimed.

## Results

| Command | Exit | Exact result or boundary |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0058` | 0 | rank 1525; planned; score 78; `L0/rework_required`; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all` before editing | 0 | only the pre-existing automation-provided `Formalizations/Lean/.lake` symlink was present; it was preserved |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | revision `5fe11f4b5e32a06ffb4432460319fc8ae906fe7b`; tree `64c5aacf7cf3eb79008f5a1970151e3e53cb9966` |
| `git blame -L 433,438 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog fields originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| bounded Crossref, OpenAlex, Semantic Scholar, Internet Archive, Wikipedia/Wikidata, search-engine, publisher, and bibliographic discovery attempts | non-gate discovery | historical title and conventional theorem family were used only as leads; no immutable primary passage, exact theorem/page, proof, correction, errata, or H0 source was admitted; several services timed out, rate-limited, or denied access |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, x86_64 Linux |
| `cd Formalizations/Lean && lake --version` | 0 | Lake `5.0.0-src+98dc76e` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`; tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b` |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --porcelain` | 0 | empty output; the pinned package remained clean |
| first late `lake env lean` replay after artifact finalization | 1 | failed because shared `.lake/packages/flt-regular` could not resolve `HEAD`; this failed attempt is not credited as validation |
| shared-cache incident audit | 0 | `flt-regular` reflog and `FETCH_HEAD` show an external clone/fetch during this worker window; final checkout is clean at manifest pin `56161b6eb5281fbfe9c38f2bcec0f429ebc11a27`; process attribution is unavailable |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0058/IntakeProbe.lean` | 0 | nine adjacent trace and singular-value declarations elaborated; complete stdout SHA-256 `e18b902...fd427`; no canonical target or proof body |
| bounded case-insensitive trace/singular-value/von-Neumann search over pinned mathlib and repo-local Lean | 1 | expected no-match exit; no relevant theorem declaration was identified; this is not an exhaustive external anchor audit |
| `python3 -m json.tool` on owned JSON and `.stage1-worker-selftest.json` | 0 | all structured artifacts are valid JSON |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0058-pycache python3 -m py_compile Stage1_Instances/THM-M-0058/check_intake.py` | 0 | scoped validator compiles without repository cache output |
| `python3 -B Stage1_Instances/THM-M-0058/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | target/DAG identity, source and pin hashes, null target, provisional `H1/M4/R4`, artifact inventory, packet agreement, and six open tasks agree |
| temporarily move `.stage1-worker-selftest.json` aside; `python3 -B Stage1_Instances/THM-M-0058/check_intake.py`; restore the packet byte-for-byte | 0 | public replay mode genuinely passes without the scheduler-only packet |
| prohibited-declaration scan over the owned Lean probe | 1 | expected no-match: no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| `git diff --check -- Stage1_Instances/THM-M-0058 .stage1-worker-selftest.json` plus per-file no-index checks | 0 aggregate | no whitespace errors; no-index exit 1 represented only each expected new-file difference |

## Boundary

This validates only a `planned` intake dossier, scope map, source-statement crosswalk, adjacent Lean
API probe, and open downstream task DAG. The canonical human and Lean statements remain null because
the catalogue does not supply the formula or select its proposition-changing conventions. The first
blocked downstream gate is `S56-M-0058-STATEMENT`. No source is accepted to H0; no formal artifact is
accepted to M0; no reconstruction is accepted to R0; and no audit or theorem completion is claimed.

The receipt timestamps delimit validation of non-receipt inputs. Receipt serialization and later
replay necessarily occur after that cutoff and are not represented as a release-grade signed time
attestation; the packet is explicitly mutable, provisional, and non-content-addressed.

The shared-cache incident prevents any claim that the entire worker session was immutable or
hermetic. It does not supply theorem evidence. The final narrow elaboration remains only a
nonrelease feasibility check over the manifest-pinned dependency state observed after the incident.
