# Statement gate blocker

Item: `S56-M-1293-STATEMENT`  
Theorem: `THM-M-1293`  
Verdict: blocked; no exact canonical Lean target is claimed.

## First failed gate

The repository catalog identifies only "Lions concentration-compactness principle" and describes
critical-growth compactness. That names a family of results, not one proposition. The intake
deliberately leaves the exact source identity open: it does not pin a theorem or lemma number, exact
text, hypotheses, normalization, or errata from Lions' 1984 papers. It also does not select among
the original measure lemma, the locally compact and limit cases, a Sobolev specialization, or an
application-specific compactness consequence. These alternatives have materially different
domains, quantifiers, normalizations, symmetry groups, and conclusions. Selecting one in this phase
would invent missing mathematics or substitute a narrower theorem.

The legacy declaration
`AwesomeTheorems.Stage1.S1_M_173.StatementShape` cannot repair that ambiguity. It quantifies over a
user-supplied `ConcentrationCompactnessProblem` whose `tightUpToSymmetry` and
`compactnessConclusion` are arbitrary predicates. Its dichotomy witness also represents geometric
separation by an arbitrary proposition accompanied by a proof. Consequently the legacy shape can
be instantiated degenerately and is not established as an encoding of any pinpointed Lions
theorem. Its successful elaboration below is discovery evidence only, not exact-statement credit.

Rev-5.6 sections 0.1 and 5 therefore require a hard stop. Without a selected immutable source
statement, this worker cannot truthfully freeze the ordered binders and hypotheses, normalized
expression fingerprint, credited transports, or the required mutations of hypothesis, domain,
binder scope, and boundary cases. No canonical Lean file or broadened proxy was introduced. The
intake machine grade remains `M3`; statement acceptance and theorem completion remain false.

## Environment fingerprint

- Repository base revision: `66ea3415424fb2dd9f2dc93a957a93df337749e6`.
- Validation date: 2026-07-12 (Asia/Shanghai).
- Lean toolchain: `leanprover/lean4:v4.29.0`; Lean `4.29.0`, commit
  `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- Checked mathlib revision: `8a178386ffc0f5fef0b77738bb5449d50efeea95`.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- Lake manifest SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.
- Legacy discovery module SHA-256:
  `d1f6c049e2b618a75db95c70835bded28017c1631389cd6ec96a79a7bc5e6f35`.

## Validation evidence

Commands ran in this worker clone. Lean used the existing canonical pinned `.lake` link; no Lake
update, build, dependency clone/fetch, or `.lake` mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1293` | 0 | rank 173, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |
| `cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_173.lean` | 0 | legacy generic boundary elaborated; this does not establish source identity or exactness |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | checked revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_173.lean` | 0 | hashes match the environment fingerprint above |

## Retry condition

Provide an immutable primary-source edition and a pinpointed theorem or lemma, including its exact
statement, all referenced definitions, assumptions, normalization, and any corrections. The next
statement run can then select the intended Lions variant; encode its measure space, mass sequence,
concentration function, translation or symmetry action, three alternatives, and boundary cases;
use the smallest pinned imports; serialize the elaborated expression; check every credited
transport; and run the required statement mutations.

Until that source identity is fixed, the assigned phase cannot be genuinely self-tested to its
completion gate. Consequently no `.stage1-worker-selftest.json` is emitted.
