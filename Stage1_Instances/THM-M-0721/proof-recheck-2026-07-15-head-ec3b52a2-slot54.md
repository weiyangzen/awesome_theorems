# THM-M-0721 proof recheck at `ec3b52a2` (slot54)

Item: `S56-M-0721-PROOF`

Intent: `prove`

Recheck date: `2026-07-15T14:52:00+08:00`

Base revision: `ec3b52a20f5e28de012c23dce1af403343b9a1cb`

Base tree: `b08b83715d8f74868d1f31bbe82a7951b26edad1`

## Verdict

`blocked`. No eligible proof body was implemented or found for the exact root
`Stage1Instances.THM_M_0721.ExistsNPCompleteLanguage`. The root remains
`[H1, M3, R4]`, and this proof item remains `[ ]`.

The checked `root_of_candidate_packages` declaration is conditional composition only. It consumes
but does not construct the two immediate root packages:

- `M0721-T-SAT-IN-NP`: faithful binary SAT encoding, a correct bundled polynomial-time TM2
  verifier, and a polynomial certificate bound;
- `M0721-T-UNIVERSAL-HARDNESS`: arbitrary-verifier normalization, Cook-Levin tableaux, both
  correctness directions, and a bundled polynomial-time TM2 reduction.

Eleven frozen SAT and Cook-Levin obligations remain open. Pinned mathlib supplies the
`TM2ComputableInPolyTime` substrate and identity machine but no NP-completeness endpoint. Its
composition declaration is source-level `proof_wanted`; trust-zero Lean confirms there is no
checked constant. Empty, universal, identity, singleton, certificate-smuggling, and classical-choice
shortcuts cannot provide the required universal reductions. A universal encoded-verifier language
would still require the absent machine serialization and polynomial-time universal simulator.

The registry gives the eleven open entries planned prose targets rather than exact Lean declaration
types. Its only exact open proof interface is `CandidateMembership candidate` plus
`CandidateHardness candidate`; concrete leaf signatures require append-only registry refinement
before proof credit. The first failed gate is `M0721-N-SAT-ENCODING`; the immediate root cut is
`M0721-T-SAT-IN-NP` plus `M0721-T-UNIVERSAL-HARDNESS`.

The frozen external audit retains one supporting-only candidate and two headline endpoints that
are placeholder-dependent or contract-incompatible. Fresh remote replay was attempted but outbound
networking was unavailable, so no fresh external result or proof credit is claimed. Because the
positive proof phase is incomplete, no proof receipt or `.stage1-worker-selftest.json` is emitted.

## Validation

The automation-provided untracked `Formalizations/Lean/.lake` symlink was reused read-only. No
dependency update, build, clone, fetch, checkout, or `.lake` mutation was performed.

| Command | Exit | Exact result |
|---|---:|---|
| `git rev-parse HEAD HEAD^{tree}; git status --short --untracked-files=all; readlink Formalizations/Lean/.lake` | 0 | Base `ec3b52a2...a1cb`, tree `b08b8371...dad1`; only the automation-provided `.lake` symlink was initially untracked. |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Passed 15 assurance groups and all 1546 uniform-L0 Lean 4 targets. |
| `python3 scripts/stage1_target.py check; python3 scripts/stage1_target.py show THM-M-0721` | 0 | Passed 1546 targets; rank 578 is `planned`, L0/rework-required, and theorem incomplete. |
| `LEAN_NUM_THREADS=1 timeout 600s python3 Stage1_Instances/THM-M-0721/check_statement.py` | 0 | Exact target elaborated; expression hash `758b1033...b204` matched and all four mutations were distinguished. |
| `python3 Stage1_Instances/THM-M-0721/check_obligation_tree.py` | 0 | Passed 18 obligations and 45 typed edges; denominator `375921a1...b92a`; root remained M3 with both terminal packages M4. |
| Stream declaration-bearing statement and obligation-tree portions to `LEAN_NUM_THREADS=1 timeout 180 lake env lean --trust=0 -t0 --stdin` | 0 | Conditional composition elaborated; `root_of_candidate_packages` reported exactly `[propext, Quot.sound]` and supplied no terminal-package inhabitant. |
| Scan owned Lean files for `sorry`, `admit`, `axiom`, `unsafe`, `proof_wanted`, or `sorryAx` | 1 expected | No prohibited proof device occurs in owned Lean files. |
| Search pinned mathlib and other repo-local Lean sources for the exact root, terminal packages, NP-completeness, SAT-language, or Cook-Levin endpoints | 1 expected | No eligible endpoint or implementation was found outside this dossier. |
| Ask trust-zero Lean to print axioms for `Turing.TM2ComputableInPolyTime.comp` | 1 expected | Lean reported `Unknown constant`, confirming source-level `proof_wanted` created no checked declaration. |
| `timeout 180s python3 Stage1_Instances/THM-M-0721/check_anchor_audit.py` | 1 | Local pin/hash checks ran; the first remote request failed with `network unreachable`. No network result is credited. |
| Inspect Lean/Lake/mathlib/flt-regular revisions, trees, and worktrees | 0 | Lean 4.29.0; Lake 5.0.0; mathlib `8a178386...ea95`, tree `bdc39a31...c2b`, clean; flt-regular `56161b6e...1a27`, tree `32c9eace...c893`, clean. |
| Hash frozen target and environment inputs | 0 | All current hashes matched the frozen records. |
| `git diff --check; test ! -e .stage1-worker-selftest.json` | 0 | Tracked diff hygiene passed and the completion self-test was deliberately absent before handoff creation. |

## Reopen Condition

Resume after placeholder-free bodies exist for the eleven frozen SAT and Cook-Levin packages, or
after an immutable compatible Lean 4 proof already in the pinned closure can be exact-type checked,
transported to the frozen TM2 encodings, and provenance-audited without changing the dependency
lock.

This is current-base nonrelease blocker evidence only. It does not satisfy
`S56-M-0721-PROOF`, change scheduler state, close either terminal package or the root, or claim
audit completion, theorem completion, validation, release, receipt acceptance, or master acceptance.
