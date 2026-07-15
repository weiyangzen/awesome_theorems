# THM-M-0721 proof recheck at `db0c2980` (slot59)

Item: `S56-M-0721-PROOF`

Intent: `prove`

Recheck date: `2026-07-15T14:15:00+08:00`

Base revision: `db0c298049d1dde29478ee95e1fe6f30c6fbf803`

Base tree: `2a16d30ab1d6b3870e8eccdbb207a5cde55b2426`

## Verdict

`blocked`. No eligible proof body was implemented or found for the exact root
`Stage1Instances.THM_M_0721.ExistsNPCompleteLanguage`. The root remains
`[H1, M3, R4]`, and this proof item remains `[ ]`.

The checked declaration `root_of_candidate_packages` is conditional composition only. It consumes
but does not construct the two immediate root packages:

- `M0721-T-SAT-IN-NP`, requiring faithful binary SAT encoding, a correct bundled polynomial-time
  TM2 verifier, and a polynomial certificate bound;
- `M0721-T-UNIVERSAL-HARDNESS`, requiring arbitrary-verifier normalization, Cook-Levin tableaux,
  both correctness directions, and a bundled polynomial-time TM2 reduction.

Eleven frozen SAT and Cook-Levin obligations remain open. Pinned mathlib supplies the TM2 substrate
and identity machine, but no NP-completeness endpoint. Its composition declaration is source-level
`proof_wanted`; trust-zero Lean reports that no checked constant exists. Empty, universal,
identity, and classical-choice constructions do not provide the required universal polynomial-time
verifier and reduction witnesses.

The registry currently gives those eleven entries planned prose targets rather than exact Lean
declaration types. Its only exact open proof interface is the pair `CandidateMembership candidate`
and `CandidateHardness candidate`; concrete leaf signatures require append-only registry refinement
before they can receive proof credit.

Fresh immutable external-candidate replay reconfirmed one supporting-only candidate plus two
headline endpoints whose root paths contain proof gaps or incompatible complexity contracts. None
can be imported or transported to the frozen target. The first failed gate is
`M0721-N-SAT-ENCODING`; the immediate root cut is `M0721-T-SAT-IN-NP` plus
`M0721-T-UNIVERSAL-HARDNESS`. Because the positive proof phase is incomplete, no proof receipt or
`.stage1-worker-selftest.json` is emitted.

## Validation

The automation-provided untracked `Formalizations/Lean/.lake` symlink to canonical artifacts was
reused read-only. No dependency update, build, clone, fetch, checkout, or `.lake` mutation was
performed.

| Command | Exit | Exact result |
|---|---:|---|
| `git rev-parse HEAD HEAD^{tree}; git status --short --untracked-files=all; readlink Formalizations/Lean/.lake` | 0 | Base `db0c2980...f803`, tree `2a16d30a...2426`; only the automation-provided `.lake` symlink was initially untracked. |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Passed 15 assurance groups and all 1546 uniform-L0 Lean 4 targets. |
| `python3 scripts/stage1_target.py check; python3 scripts/stage1_target.py show THM-M-0721` | 0 | Passed 1546 targets; rank 578 is `planned`, L0/rework-required, and theorem incomplete. |
| `LEAN_NUM_THREADS=1 timeout 600s python3 Stage1_Instances/THM-M-0721/check_statement.py` | 0 | Exact target elaborated; expression hash `758b1033...b204` matched and all four mutations were distinguished. |
| `python3 Stage1_Instances/THM-M-0721/check_obligation_tree.py` | 0 | Passed 18 obligations and 45 typed edges; denominator `375921a1...b92a`; root remained M3 with both terminal packages M4. |
| Stream declaration-bearing statement and obligation-tree portions to `LEAN_NUM_THREADS=1 timeout 180 lake env lean --trust=0 -t0 --stdin` | 0 | Conditional composition elaborated; `root_of_candidate_packages` reported exactly `[propext, Quot.sound]` and supplied no terminal-package inhabitant. |
| Scan owned Lean files for `sorry`, `admit`, `axiom`, `unsafe`, `proof_wanted`, or `sorryAx` | 1 expected | No prohibited proof device occurs in owned Lean files. |
| Search pinned mathlib and other repo-local Lean sources for the exact root, terminal packages, NP-completeness, SAT-language, or Cook-Levin endpoints | 1 expected | No eligible endpoint or implementation exists outside this dossier. |
| Ask trust-zero Lean to print axioms for `Turing.TM2ComputableInPolyTime.comp` | 1 expected | Lean reported `Unknown constant`, confirming that source-level `proof_wanted` created no checked declaration. |
| `timeout 180s python3 Stage1_Instances/THM-M-0721/check_anchor_audit.py` | 0 | Local pins/hashes and all three immutable candidates matched; the audit retained root M2 and supplied no exact proof body. |
| Inspect Lean/Lake/mathlib/flt-regular revisions, trees, and worktrees | 0 | Lean 4.29.0; Lake 5.0.0; mathlib `8a178386...ea95`, tree `bdc39a31...c2b`, clean; flt-regular `56161b6e...1a27`, tree `32c9eace...c893`, clean. |
| Hash frozen target and environment inputs | 0 | All current hashes matched the frozen records. |
| Compare `validation-specs.json` recipe keys with blueprint section 10.5 | 0 | Legacy shell-string recipes lack the normative structured `cwd`, `argv`, environment, timeout, expected-output, obligation, and declaration fields. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion self-test deliberately absent because the proof phase is blocked. |

## Reopen Condition

Resume after placeholder-free bodies exist for the eleven frozen SAT and Cook-Levin packages, or
after an immutable compatible Lean 4 proof already in the pinned closure can be exact-type checked,
transported to the frozen TM2 encodings, and provenance-audited without changing the dependency
lock.

This is current-base nonrelease blocker evidence only. It does not satisfy
`S56-M-0721-PROOF`, change scheduler state, close either terminal package or the root, or claim
audit completion, theorem completion, validation, release, receipt acceptance, or master acceptance.
