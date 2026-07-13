# Intake validation record

## Boundary

This record validates only the `planned` intake artifacts for `S56-M-1586-INTAKE`: target
membership and identity, dossier structure, frozen ambiguity, source and neighbor boundaries, the
open downstream task projection, and a pinned Lean API probe. It does not validate an exact Hamming
bound statement, a source-faithful proof, an exhaustive anchor audit, or any theorem proof.

The worker reused the automation-provided `Formalizations/Lean/.lake` symlink and canonical pinned
artifacts read-only. It ran no `lake update`, `lake build`, dependency clone/fetch, or other `.lake`
mutation. Initial worktree status contained only that pre-existing untracked symlink.

## Immutable inputs

| Input | Value |
|---|---|
| repository base | `62fad55ced807fdc06921c45d6fcd1f9ad86a1c2` |
| repository base tree | `9d7c8fe49a4c859d90f3069dc47973ffc5ced768` |
| catalog-origin commit | `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| Lean | `4.29.0`, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| Lake | `5.0.0-src+98dc76e` |
| mathlib revision | `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| mathlib tree | `bdc39a3123201dae413a9d9be56ec242c19e5c2b` |
| mathlib Hamming source SHA-256 | `2552acbec60f1a370482bbdadee849049aa2c7c32452cbcf84d1dbca39e8ccf8` |
| platform | Linux `x86_64`, kernel `7.0.0-27-generic` |
| validation date | 2026-07-13 Asia/Shanghai |

## Source inspection

Crossref's DOI endpoint confirmed Hamming's 1950 article title, author, journal, volume, issue, and
pages. The exact JSON response had SHA-256
`55bb5c6edb8dffc69fa290c9c357b7c61fe5bf9bcfb592701ff673af13941473` and 1595 bytes; the
Unixref response had SHA-256
`1717b02a5c67d27f09b804e4c77ffa7f080fa66b8e482f3c8f8b798ba9de3a69` and 1931 bytes.
Semantic Scholar independently returned the same DOI/title/author/year and a scan candidate; its
response had SHA-256 `19d5209ecac3fab086b084133a163afc1d15ef9c890d1ffd10c8086d9c9ce69e`
and 542 bytes.

The DOI destination returned an automated-access challenge. Connections to the scan host timed out
before the paper was retrieved. Those access failures are recorded rather than repaired with a
moving or unofficial substitute. No primary theorem text or proof was inspected, and no H0 claim is
made.

## Commands and results

All repository commands ran from the repository root unless another `cwd` is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-1586` | 0 | rank 1208; planned; no legacy slot; legacy artifacts unaccepted; theorem_complete false |
| initial `git status --short --untracked-files=all` | 0 | only `?? Formalizations/Lean/.lake`; preserved read-only |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree shown above |
| `git blame -L 11686,11691 -- Docs/researches/math_theorems.md` | 0 | all six uncited mathematical catalog lines originate at the catalog-origin commit above |
| Crossref DOI JSON and Unixref metadata requests | 0 | article-level bibliographic metadata captured in temporary storage with the response sizes and hashes above; no source-text credit |
| Semantic Scholar DOI metadata request | 0 | matching bibliographic identity and inaccessible scan candidate captured in temporary storage; no source-text credit |
| DOI landing and scan-candidate retrieval attempts | non-success | DOI endpoint challenged automated access; scan host connections timed out; no paper bytes admitted |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | Lean and Lake versions agree with the fingerprint; no update or build was run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned mathlib revision/tree above; package worktree clean |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1586/IntakeProbe.lean)` | 0 | nine Hamming and finite-cardinality API checks elaborated; complete stdout SHA-256 `f3773fe62e0132df4d9a9da795af55486f19f7a12cb886908e86e1699e6197f4`, 1249 bytes |
| bounded exact-topic search over pinned mathlib and repo-local Lean | 1 (expected no match) | no Hamming-bound, sphere-packing-code, code-minimum-distance, or code-size target occurrence; empty-output SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`; discovery only |
| `python3 -m json.tool` on every structured owned artifact and `.stage1-worker-selftest.json` | 0 | all structured artifacts valid JSON after finalization |
| Python `ast.parse` on `Stage1_Instances/THM-M-1586/check_intake.py` | 0 | scoped validator parses without writing bytecode |
| `python3 -B Stage1_Instances/THM-M-1586/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | identity, planned H1/M4/R4 boundary, null target, source and neighbor boundaries, inventory, packet, hashes, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-1586/check_intake.py` | 0 | public replay mode passes without the scheduler-only packet |
| prohibited-construct scan over owned Lean | 1 (expected no match) | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration in the API-only probe |
| per-file `git diff --no-index --check /dev/null` for every owned file and worker packet | 0 aggregate | no whitespace diagnostics; no-index exit 1 for each new file was only the expected new-file difference |
| `git diff --check -- Stage1_Instances/THM-M-1586 .stage1-worker-selftest.json` | 0 | no tracked whitespace diagnostics; preceding per-file checks cover untracked artifacts |

## Known downstream failures

- No complete primary or authoritative theorem text, exact result locator, definition/assumption
  mapping, correction/errata disposition, or independent source review is admitted.
- The catalog does not select binary versus q-ary, arbitrary versus linear, finite versus
  asymptotic, distance versus radius, ball-volume encoding, exact inequality, or boundary cases.
- No canonical Lean expression, minimal import set, expression/environment fingerprint, checked
  alternate encoding, or statement mutation exists.
- Pinned mathlib supplies Hamming-space and finite-counting substrate, not an exact Hamming-bound
  declaration or proof body.
- Formal anchor audit, obligation and discovery freezes, typed graphs, proof, composition, trust
  closure, readable reconstruction, hermetic replay, deterministic bundle, independent release
  verification, and master acceptance remain open.

These failures prevent any statement, proof, audit-completion, or theorem-completion claim. They do
not prevent a truthful, self-tested `planned` intake whose purpose is to freeze the ambiguity and
open the downstream DAG. Only the integration lane may accept its provisional receipt.
