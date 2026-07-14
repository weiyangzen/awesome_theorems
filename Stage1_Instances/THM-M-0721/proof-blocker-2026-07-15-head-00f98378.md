# THM-M-0721 proof attempt: blocked

Item: `S56-M-0721-PROOF`

Attempt: 2026-07-15 (Asia/Shanghai)

Base revision: `00f98378e8c1c63097871ae62aeed895d83b0cb4`

Base tree: `4f2396db6d6d1c2b9948f401079f136dd0ed8f16`

## Verdict

The assigned proof phase is **blocked**. No proof body was added, no frozen obligation was closed,
and the root remains `[H1, M3, R4]`. Because the phase is not genuinely self-tested as complete,
`.stage1-worker-selftest.json` is deliberately absent and the item remains `[ ]`.

The exact target is `Stage1Instances.THM_M_0721.ExistsNPCompleteLanguage`: over binary words, some
language belongs to the frozen verifier-based `InNP`, and every such NP language has a polynomial-
time TM2 many-one reduction to it. The checked `root_of_candidate_packages` composition consumes
the exact two necessary packages, but both remain uninhabited:

- `M0721-T-SAT-IN-NP`: a faithful encoded SAT language, verifier, correctness theorem, certificate
  bound, and `TM2ComputableInPolyTime` runtime witness;
- `M0721-T-UNIVERSAL-HARDNESS`: arbitrary-verifier normalization, Cook-Levin tableau construction,
  both correctness directions, and a `TM2ComputableInPolyTime` reduction witness.

Pinned mathlib at `8a178386ffc0f5fef0b77738bb5449d50efeea95` supplies the TM2 polynomial-
time structure and an identity machine, but no NP, SAT-language, or Cook-Levin theorem. Its only
TM2 polynomial-time composition endpoint is explicitly `proof_wanted`. Mathlib's computable
`ManyOneReducible` is not the frozen polynomial-time relation. The immutable audit likewise records
no eligible external root: one candidate has no NP endpoint, while two headline endpoints have
root-relevant gaps or invalid contracts and no checked transport to this binary-word TM2 target.

Assuming either terminal package, invoking the `proof_wanted` endpoint, or substituting computable
reducibility, a fixed source, a finite instance, or the conditional composition would violate the
exact theorem gate. A truthful implementation therefore requires the full missing SAT and
Cook-Levin development or an immutable compatible proof dependency.

## Validation

All commands ran in this worker clone and reused the automation-provided canonical `.lake` symlink
read-only. No dependency update, build, clone, fetch, or mutation was performed.

| Command | Exit | Exact result |
| --- | ---: | --- |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Passed 15 assurance groups and all 1546 uniform-L0 Lean 4 targets. |
| `python3 scripts/stage1_target.py check` | 0 | Passed 1546 unique targets at ranks 1 through 1546. |
| `python3 scripts/stage1_target.py show THM-M-0721` | 0 | Rank 578; `planned`; L0/rework-required; theorem incomplete. |
| `timeout 360s python3 Stage1_Instances/THM-M-0721/check_statement.py` | 0 | Expression hash `758b1033...204`; all four mutations were distinguished; pinned environment matched. |
| `python3 Stage1_Instances/THM-M-0721/check_obligation_tree.py` | 0 | Passed 18 obligations and 45 typed edges; root open `M3`; both terminal packages `M4`. |
| From `Formalizations/Lean`, concatenate `Statement.lean` and `ObligationTree.lean` to `lake env lean --trust=0 --stdin` | 0 | Exact statement and conditional body elaborated; axioms were only `propext` and `Quot.sound`; no terminal package was produced. |
| Scoped declaration search for NP-completeness, SAT-language, and Cook-Levin endpoints | 1 | Expected no-match exit: no matching local or pinned-mathlib definition/theorem was found. |
| Prohibited-device scan over the two owned Lean files and pinned `Computable.lean` | 0 | Sole hit: mathlib's `proof_wanted TM2ComputableInPolyTime.comp`; the owned files had no prohibited token. |
| `python3 Stage1_Instances/THM-M-0721/check_anchor_audit.py` | 1 | Local pins/hashes passed, then remote immutable-candidate replay failed with `Network is unreachable`; no fresh external evidence is claimed. |
| Run `git diff --no-index --check /dev/null` on each fresh blocker artifact and assert both expected new-file exits equal 1 | 0 | Neither diff emitted a whitespace diagnostic; the final assertion passed. |

Full hashes, command results, and the structured boundary are in
`proof-blocker-2026-07-15-head-00f98378.json`. The pre-existing untracked `.lake` symlink makes this
nonrelease evidence.

## Reopen Condition

Resume after placeholder-free bodies exist for the eleven frozen SAT and Cook-Levin packages, or
after an immutable compatible Lean 4 proof can be pinned, exact-type checked, transported to the
frozen encodings, and provenance-audited. Until then the minimal open root cut remains
`M0721-T-SAT-IN-NP` plus `M0721-T-UNIVERSAL-HARDNESS`, and `S56-M-0721-PROOF` cannot truthfully
receive `[_]` credit.
