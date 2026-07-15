# THM-M-0721 proof recheck at `9bce865a` (slot59)

Item: `S56-M-0721-PROOF`

Intent: `prove`

Recheck date: `2026-07-15T13:51:09+08:00`

Base revision: `9bce865a14bcc270344ea909d6936c6ea22aa1c2`

Base tree: `523a9471aac257c4cf54acceee07172fab22f5b4`

## Verdict

`blocked`. No eligible proof body was implemented or found for the exact root
`Stage1Instances.THM_M_0721.ExistsNPCompleteLanguage`. The root remains
`[H1, M3, R4]`, and this proof item remains `[ ]`.

The checked declaration `root_of_candidate_packages` is only conditional composition. It consumes
but does not construct the immediate root packages:

- `M0721-T-SAT-IN-NP`, requiring faithful binary SAT encoding, a correct bundled polynomial-time
  TM2 verifier, and a polynomial certificate bound;
- `M0721-T-UNIVERSAL-HARDNESS`, requiring arbitrary-verifier normalization, Cook-Levin tableaux,
  both correctness directions, and a bundled polynomial-time TM2 reduction.

Eleven frozen SAT and Cook-Levin obligations remain open. Pinned mathlib supplies the TM2 substrate
and identity machine, but no NP-completeness endpoint. Its composition declaration is source-level
`proof_wanted`; trust-zero Lean reports that no checked constant exists. Empty, universal,
identity, and classical-choice constructions do not provide the required universal polynomial-time
verifier and reduction witnesses.

An immutable external-candidate replay initially passed at this base and reconfirmed one
supporting-only candidate plus two headline endpoints whose root paths contain proof gaps or
incompatible complexity contracts. A final rerun failed after the network became unreachable, so
the network-backed result is not reproducible in the final worker state and no new external credit
is claimed. None of the frozen candidates can be imported or transported to the target. The first failed gate is
`M0721-N-SAT-ENCODING`; the immediate root cut is `M0721-T-SAT-IN-NP` plus
`M0721-T-UNIVERSAL-HARDNESS`. Because the positive proof phase is incomplete, no proof receipt or
`.stage1-worker-selftest.json` is emitted.

## Validation

The automation-provided untracked `Formalizations/Lean/.lake` symlink to canonical artifacts was
reused read-only. No dependency update, build, clone, fetch, checkout, or `.lake` mutation was
performed. The canonical `flt-regular` package has an invalid `HEAD`; normal `lake env lean` fails
before target elaboration. The exact target and conditional composition were therefore additionally
elaborated with immutable Lean 4.29.0 and existing precompiled pinned artifacts. This fallback is
nonrelease evidence only.

| Command | Exit | Exact result |
|---|---:|---|
| `git rev-parse HEAD HEAD^{tree}; git status --short --untracked-files=all; readlink Formalizations/Lean/.lake` | 0 | Base `9bce865a...a1c2`, tree `523a9471...f5b4`; only the automation-provided `.lake` symlink was initially untracked. |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Passed 15 assurance groups and all 1546 uniform-L0 Lean 4 targets. |
| `python3 scripts/stage1_target.py check; python3 scripts/stage1_target.py show THM-M-0721` | 0 | Passed 1546 targets; rank 578 is `planned`, L0/rework-required, and theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0721/check_obligation_tree.py` | 0 | Passed 18 obligations and 45 typed edges; denominator `375921a1...b92a`; root remained M3 with both terminal packages M4. |
| `LEAN_NUM_THREADS=1 timeout 360s python3 Stage1_Instances/THM-M-0721/check_statement.py` | 1 | Lake exited through external Git code 128 because pinned `flt-regular` could not resolve `HEAD`; no dependency repair was attempted. |
| Derive `LEAN_PATH` only from existing pinned build outputs, then run immutable Lean 4.29.0 with `--trust=0 -t0` on `Statement.lean` | 0 | The exact target elaborated and printed `ExistsNPCompleteLanguage` as an existential language satisfying `NPComplete`. |
| Concatenate the declaration-bearing statement and import-adjusted obligation tree in a temporary file, then run the same immutable trust-zero Lean | 0 | The conditional composition elaborated; `root_of_candidate_packages` reported exactly `[propext, Quot.sound]` and supplied no terminal-package inhabitant. |
| Scan owned Lean files for `sorry`, `admit`, `axiom`, `unsafe`, `proof_wanted`, or `sorryAx` | 0 | The underlying searches returned expected no-match exits; no prohibited token occurs in owned Lean files. |
| Scan pinned mathlib and other repo-local Lean sources for NP-completeness, SAT-language, Cook-Levin, or target-package endpoints | 0 | The underlying searches returned expected no-match exits; no eligible endpoint or implementation exists outside this dossier. |
| Ask immutable trust-zero Lean to print axioms for `Turing.TM2ComputableInPolyTime.comp` | 1 expected | Lean reported `Unknown constant`, confirming that source-level `proof_wanted` created no checked declaration. |
| `python3 Stage1_Instances/THM-M-0721/check_anchor_audit.py` | 0, then 1 | The first invocation matched local pins/hashes and all three immutable candidates with root M2; the final rerun failed when the network became unreachable, so only the frozen classifications are retained. |
| Hash frozen inputs and inspect immutable toolchain/mathlib identities | 0 | All hashes match; Lean is 4.29.0 at `98dc76e...740`; mathlib is `8a178386...ea95`, tree `bdc39a31...c2b`, and clean. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion self-test deliberately absent because the proof phase is blocked. |

## Reopen Condition

Resume after placeholder-free bodies exist for the eleven frozen SAT and Cook-Levin packages, or
after an immutable compatible Lean 4 proof already in the pinned closure can be exact-type checked,
transported to the frozen TM2 encodings, and provenance-audited without changing the dependency
lock. The canonical `flt-regular` checkout must also be repaired outside this worker before the
normal `lake env lean` recipe can replay.

This is current-base nonrelease blocker evidence only. It does not satisfy
`S56-M-0721-PROOF`, change scheduler state, close either terminal package or the root, or claim
audit completion, theorem completion, validation, release, receipt acceptance, or master acceptance.
