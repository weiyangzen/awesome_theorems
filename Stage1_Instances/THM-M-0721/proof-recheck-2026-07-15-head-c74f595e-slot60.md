# THM-M-0721 proof recheck at `c74f595e` (slot60)

Item: `S56-M-0721-PROOF`

Intent: `prove`

Recheck date: `2026-07-15T12:10:39+08:00`

Base revision: `c74f595e99fe574f4619307c859ec20986bb2297`

Base tree: `b27451453ff7d1e87d296c6634bd270799c666d9`

## Verdict

`blocked`. No eligible proof body was implemented or found for the exact root
`Stage1Instances.THM_M_0721.ExistsNPCompleteLanguage`. The root remains
`[H1, M3, R4]`, and this proof item remains `[ ]`.

The frozen target is substantively nonvacuous. The checked declaration
`root_of_candidate_packages` only consumes the two immediate root packages; it constructs neither:

- `M0721-T-SAT-IN-NP`, requiring a faithful binary SAT encoding, correct bundled polynomial-time
  TM2 verifier, and polynomial certificate bound;
- `M0721-T-UNIVERSAL-HARDNESS`, requiring arbitrary-verifier normalization, Cook-Levin tableaux,
  both correctness directions, and a bundled polynomial-time TM2 reduction.

Eleven frozen SAT/Cook-Levin obligations remain open. Pinned mathlib supplies the TM2 substrate and
identity machine, but no NP-completeness endpoint. Its relevant composition declaration is
source-level `proof_wanted`; a trust-zero Lean query confirms that no checked constant was created.
Alphabet equivalences only rename symbols, so the identity machine cannot implement the
variable-length `encodePair` to one-bit `encodeBool` verifier or universal reductions. Empty and
universal languages can be shown to belong to the frozen `InNP`, but neither can be hard because the
other is also in `InNP`. Classical-choice reductions do not supply `PolytimeFunction` witnesses.

The immutable audit's three external candidates remain ineligible: one supplies only incomplete
fixed-tableau support, and the two headline endpoints contain root-relevant proof gaps or incompatible
complexity contracts. A fresh discovery-only sweep found no overlooked exact candidate; moving heads
still lack universal placeholder-free hardness and are not in the pinned closure.

The first failed gate is `M0721-N-SAT-ENCODING`. The immediate root cut is
`M0721-T-SAT-IN-NP` plus `M0721-T-UNIVERSAL-HARDNESS`. Because the positive proof phase is
incomplete, no proof receipt or `.stage1-worker-selftest.json` is emitted.

## Validation

The automation-provided untracked `Formalizations/Lean/.lake` symlink to canonical artifacts was
reused read-only. No dependency update, build, clone, fetch, checkout, or `.lake` mutation was
performed. The canonical `flt-regular` package is an empty worktree whose `HEAD` names
`refs/heads/.invalid`; normal `lake env` commands either time out or fail before target elaboration.
This target was therefore additionally elaborated with the immutable Lean 4.29.0 executable and the
existing precompiled pinned package artifacts. That fallback is nonrelease evidence only.

| Command | Exit | Exact result |
|---|---:|---|
| `git rev-parse HEAD HEAD^{tree}; git status --short --untracked-files=all; readlink Formalizations/Lean/.lake` | 0 | Base `c74f595e...b2297`, tree `b2745145...66d9`; only the automation-provided `.lake` symlink was initially untracked. |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Passed 15 assurance groups and all 1546 uniform-L0 Lean 4 targets. |
| `python3 scripts/stage1_target.py check` | 0 | Passed 1546 unique targets at ranks 1 through 1546. |
| `python3 scripts/stage1_target.py show THM-M-0721` | 0 | Rank 578; `planned`; L0/rework-required; theorem incomplete. |
| `LEAN_NUM_THREADS=1 timeout 600s python3 Stage1_Instances/THM-M-0721/check_statement.py` | 1 | After repeated `lake env lean` attempts, Lake exited through external `git` code 128 because the unrelated pinned `flt-regular` checkout has invalid `HEAD`; no dependency repair was attempted. |
| `python3 Stage1_Instances/THM-M-0721/check_obligation_tree.py` | 0 | Passed 18 obligations and 45 typed edges; denominator `375921a1...b92a`; root remained M3 with both terminal packages M4. |
| Copy `Statement.lean` and `ObligationTree.lean` to a temporary directory, add `import Statement`, derive `LEAN_PATH` from existing package build directories, then run immutable Lean 4.29.0 with `--trust=0 -t0` in dependency order | 0 | The exact target and conditional composition elaborated; `root_of_candidate_packages` reported exactly `[propext, Quot.sound]` and produced no terminal-package inhabitant. |
| Scan owned Lean files for `sorry`, `admit`, `axiom`, `unsafe`, `proof_wanted`, or `sorryAx` | 1 expected | No prohibited token occurs in owned Lean files. |
| Scan pinned mathlib Lean source for NP-completeness, SAT-language, or Cook-Levin endpoints | 1 expected | No eligible endpoint exists. |
| Search other repo-local Lean source for the exact target, terminal packages, and NP-completeness/Cook-Levin endpoints | 1 expected | No endpoint or implementation exists outside this target dossier. |
| Ask immutable Lean to `#print axioms Turing.TM2ComputableInPolyTime.comp` under the pinned import and trust-zero environment | 1 expected | Lean reported `Unknown constant`, confirming that source-level `proof_wanted` added no checked declaration. |
| `python3 Stage1_Instances/THM-M-0721/check_anchor_audit.py` | 1 | Fresh immutable-source replay reached its 30-second read timeout on the first GitHub raw request. No fresh network result is credited; the frozen audit and content hashes were not changed. |
| `sha256sum` the statement, composition module, registry, typed graphs, anchor audit, toolchain, manifest, and Lean binary | 0 | All frozen hashes match; Lean is 4.29.0 at `98dc76e...740`, mathlib is `8a178386...ea95`, tree `bdc39a31...c2b`, and its worktree is clean. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion self-test deliberately absent because the assigned proof phase is blocked. |

## Reopen Condition

Resume after placeholder-free bodies exist for the eleven frozen SAT and Cook-Levin packages, or
after an immutable compatible Lean 4 proof already in the pinned closure can be exact-type checked,
transported to the frozen TM2 encodings, and provenance-audited without changing the dependency
lock. The canonical `flt-regular` checkout must also be repaired outside this worker before the
normal `lake env lean` recipe can replay.

This is current-base nonrelease blocker evidence only. It does not satisfy
`S56-M-0721-PROOF`, change scheduler state, close either terminal package or the root, or claim
audit completion, theorem completion, validation, release, receipt acceptance, or master acceptance.
