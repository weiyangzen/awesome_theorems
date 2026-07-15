# THM-M-0721 proof recheck at `16621ebb` (slot71)

Item: `S56-M-0721-PROOF`

Intent: `prove`

Recheck date: `2026-07-15T09:04:05+08:00`

Base revision: `16621ebbf3c00d82e7efdbdffd1265f97c435ef9`

Base tree: `4dedd863ce86580567542085e46598c963df88b7`

## Verdict

`blocked`. No eligible proof body was implemented or found for the exact root
`Stage1Instances.THM_M_0721.ExistsNPCompleteLanguage`. The root remains
`[H1, M3, R4]`, and this proof item remains `[ ]`.

The conditional declaration `root_of_candidate_packages` consumes, but does not construct, the two
immediate root packages:

- `M0721-T-SAT-IN-NP`, requiring an encoded SAT language, a correct bundled polynomial-time TM2
  verifier, and a certificate bound;
- `M0721-T-UNIVERSAL-HARDNESS`, requiring arbitrary-verifier normalization, Cook-Levin tableaux,
  both correctness directions, and a bundled polynomial-time TM2 reduction.

Eleven frozen SAT/Cook-Levin obligations remain open. Pinned mathlib supplies only the TM2
substrate and identity machine. Its relevant composition item is source-level `proof_wanted`, and
Lean confirms that no checked constant was created. The pinned source has no NP-completeness,
SAT-language, or Cook-Levin endpoint. The three immutable external candidates still fail eligibility:
one is supporting-only and two depend on placeholders or incompatible contracts, with no checked
transport to the frozen Bool-word TM2 target.

The first failed gate is `M0721-N-SAT-ENCODING`. The remaining immediate root cut is
`M0721-T-SAT-IN-NP` plus `M0721-T-UNIVERSAL-HARDNESS`. Assuming either package, invoking the
`proof_wanted` item, using merely computable reducibility, or proving a conditional/fixed-source
substitute would violate the exact-target gate. Because the assigned proof phase is incomplete, no
proof receipt or `.stage1-worker-selftest.json` is emitted.

## Validation

The automation-provided untracked `Formalizations/Lean/.lake` symlink to canonical pinned artifacts
was reused read-only. No dependency update, build, clone, fetch, or `.lake` mutation was performed.

| Command | Exit | Exact result |
|---|---:|---|
| `git rev-parse HEAD HEAD^{tree}; git status --short --untracked-files=all; readlink Formalizations/Lean/.lake` | 0 | Base `16621ebb...35ef9`, tree `4dedd863...df88b7`; only the automation-provided `.lake` symlink was initially untracked. |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Passed 15 assurance groups and all 1546 uniform-L0 Lean 4 targets. |
| `python3 scripts/stage1_target.py check` | 0 | Passed 1546 unique targets at ranks 1 through 1546. |
| `python3 scripts/stage1_target.py show THM-M-0721` | 0 | Rank 578; `planned`; L0/rework-required; theorem incomplete. |
| `LEAN_NUM_THREADS=1 timeout 600s python3 Stage1_Instances/THM-M-0721/check_statement.py` | 0 | Expression hash `758b1033...b204`; four weakened mutations were distinguished; pinned Lean and mathlib matched. |
| `python3 Stage1_Instances/THM-M-0721/check_obligation_tree.py` | 0 | Passed 18 obligations and 45 typed edges; denominator `375921a1...b92a`; root remained M3 with both terminal packages M4. |
| From `Formalizations/Lean`, stream the statement declarations and obligation composition to `LEAN_NUM_THREADS=1 timeout 300s lake env lean --trust=0 -t0 --stdin` | 0 | Exact statement and conditional composition elaborated; `root_of_candidate_packages` reported `[propext, Quot.sound]` and produced neither terminal package. |
| Scan owned Lean files for `sorry`, `admit`, `axiom`, `unsafe`, `proof_wanted`, or `sorryAx` | 1 expected | No prohibited token occurs in the owned Lean files. |
| Scan pinned mathlib Lean source for `IsNPComplete`, `NPcomplete`, `NPComplete`, `CookLevin`, `cook_levin`, or `SATLang` | 1 expected | No eligible endpoint exists. |
| Ask Lean to `#print axioms Turing.TM2ComputableInPolyTime.comp` under the pinned import and trust-zero environment | 1 expected | Lean reported `Unknown constant`, confirming that source-level `proof_wanted` added no checked declaration. |
| `python3 Stage1_Instances/THM-M-0721/check_anchor_audit.py` | 0 | Local pins/hashes and all three immutable external candidates matched; root classification remained M2. |

## Reopen Condition

Resume after placeholder-free bodies exist for the eleven frozen SAT and Cook-Levin packages, or
after an immutable compatible Lean 4 proof already in the pinned closure can be exact-type checked,
transported to the frozen TM2 encodings, and provenance-audited without changing the dependency lock.

This is current-base nonrelease blocker evidence only. It does not satisfy
`S56-M-0721-PROOF`, change scheduler state, close either terminal package or the root, or claim
audit completion, theorem completion, validation, release, receipt acceptance, or master acceptance.
