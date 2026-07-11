# Statement-phase blocker

Item: `S56-M-0129-STATEMENT`  
Base revision: `00e1e30ff33e4399bb3fdf46894103a5f67be8ab`

## Verdict

The exact-statement gate is blocked. No canonical Lean declaration has been added, and this phase
must not be self-tested or presented for acceptance.

The accepted intake identifies the classical coefficient-defined Shimura lift only as a theorem
family. It expressly leaves the primary-source variant, level and character conventions, parity
conditions, admissibility of the squarefree parameter, target level, coefficient normalization,
and Hecke range open. Those choices change the mathematical proposition. The repository contains
no immutable copy or transcription of Shimura's 1973 paper from which the exact ordered premises
and formula can be checked. The DOI landing page is protected by an anti-automation response, while
Crossref supplies bibliographic metadata but not the theorem text. Selecting conventions from
memory or from the legacy `StatementShape` would therefore invent or substitute missing
mathematics, contrary to the rev-5.6 hard-stop rule.

The historical declaration
`AwesomeTheorems.Stage1.S1_M_047.StatementShape` is not an exact fallback. Its source object stores
the transformation law, cusp condition, and Hecke condition as unconstrained `Prop` fields; its
target stores the coefficient formula and Hecke compatibility as unconstrained `Prop` fields; and
it omits the squarefree parameter and the actual divisor-sum equality. Elaborating a new wrapper
around that declaration would only validate the coarse interface already rejected at intake.

## Failed gate and retry condition

First failed gate: rev-5.6 section 5 exact canonical mathematical claim, before Lean elaboration.

Retry after an immutable primary-source artifact (or an independently accepted exact
transcription) is available and reviewed with all of the following frozen:

- theorem/formula/page pinpoints and errata status;
- ordered binders for `k`, level, character, source form, and squarefree parameter;
- parity, conductor, source-space, and admissibility hypotheses;
- target subgroup, level, weight, and character;
- exact divisor-sum coefficient formula, including character and normalization conventions;
- the precise cuspidality and Hecke-compatibility conclusions and their prime restrictions.

Only then can a minimal-import Lean target, expression hash, checked transports, and the four
required mutation classes truthfully be produced. The pinned environment does have a working Lean
executable and ordinary modular-form imports, so tool availability is not this gate's blocker.

## Commands and results

All repository commands ran from the worker-clone root unless the command itself names another
working directory. No dependency fetch, update, clone, or build was run.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0129` | 0 | rank 47, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `git -C Formalizations/Lean/.lake/packages/flt-regular rev-parse HEAD` | 0 | pinned external revision `56161b6eb5281fbfe9c38f2bcec0f429ebc11a27` |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | hashes `651c8acc...b1d2` and `321626c8...d81` |
| `rg -n -i 'On modular forms of half integral weight|Shimura lift|Shimura lifting|A_t\\(|A_t|divisor.sum formula' . --glob '!Formalizations/Lean/.lake/**' --glob '!Stage1_Instances/THM-M-0129/**'` | 0 | found only legacy/coarse Shimura boundaries; no exact primary-source transcription |
| `curl -L --max-time 15 -sS -o /tmp/shimura-probe -w '%{http_code} %{content_type} %{size_download}\\n' https://projecteuclid.org/journals/annals-of-mathematics/volume-97/issue-3/On-modular-forms-of-half-integral-weight/10.2307/1970831.full` | 0 | HTTP 200 returned a 1162-byte Incapsula anti-automation HTML document, not the paper |
| `curl -L -sS https://api.crossref.org/works/10.2307/1970831` | 0 | confirmed author, title, journal, volume 97, issue 3, May 1973, and first page 440; no theorem text or formula |
| `rg -n '(^|[[:space:]])(sorry|admit)([[:space:]]|$)\|^[[:space:]]*axiom[[:space:]]' Stage1_Instances/THM-M-0129` | 1 | no Lean proof escape or axiom declaration found (`rg` returns 1 for no matches) |
| `git diff --check -- Stage1_Instances/THM-M-0129 .stage1-worker-selftest.json` | 0 | no whitespace errors in the owned artifact |
| `test ! -e .stage1-worker-selftest.json` | 0 | self-test receipt correctly absent for this blocked phase |

No `lake env lean <target>` command is recorded because creating an allegedly exact target without
the frozen source convention would be the prohibited broadened/substituted theorem. No
`.stage1-worker-selftest.json` is emitted because the assigned statement phase is not genuinely
self-tested.
