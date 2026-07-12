# THM-M-0652 release decision

Item: `S56-M-0652-RELEASE`  
Base revision: `797546bf2bab359f9fc5be515c3d4e8943c9d931`  
Decision time: `2026-07-12T10:26:22+08:00`

## Exact verdict

The release phase is **blocked**. Lifecycle remains `planned`, the accepted root vector remains
`[H2, M3, R3]`, and both `audit_complete` and `theorem_complete` are false. No receipt is accepted.

The first failed gate is `S56-10.2-DEPENDENCY-ACCEPTANCE`: the validation prerequisite is only
`[_]` worker evidence, has `release_grade=false`, and has not been accepted by the master. Even if
that dependency were accepted, theorem release would fail section 6.7 root composition. There is
no unconditional body of `Stage1Instances.THM_M_0652.Statement`; the checked composition theorem
takes completeness, general syntactic interpolation, and soundness as premises.

The minimal mathematical root cut remains `M0652-B-COMPLETENESS`, `M0652-T-SYNTACTIC`, and
`M0652-B-SOUNDNESS`. The local endpoint-vocabulary lemmas and same-workspace reconstructions are
valid provisional partial evidence, not Craig interpolation. Source fidelity remains `H2`, and no
accepted complete readable reconstruction exists beyond `R3`, so `AUDIT-Z` is also blocked.

Release evidence is absent for a clean immutable snapshot, cold empty-cache network-denied build,
offline restoration, complete root provenance/axiom/TCB closure, SBOM/licenses, two independently
provisioned signed runners, an independently implemented verifier, protected CI and mutation
receipts, and a deterministic content-addressed bundle. The shared warm `.lake` cache and a second
proof in the same workspace do not satisfy those gates.

## Self-test

Commands were run from the repository root:

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and 1546 uniform-L0 targets passed

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required

python3 scripts/stage1_target.py show THM-M-0652
  exit 0: rank 298; lifecycle planned; theorem_complete=false

python3 Stage1_Instances/THM-M-0652/check_validation.py
  exit 0: frozen statement and partial bodies re-elaborated; exact root remains M3

python3 Stage1_Instances/THM-M-0652/check_release.py
  exit 0: blocked decision, unaccepted validation dependency, open root cut, and false terminal booleans agree

python3 -m json.tool Stage1_Instances/THM-M-0652/release-decision.json
  exit 0: valid JSON

git diff --check -- Stage1_Instances/THM-M-0652 .stage1-worker-selftest.json
  exit 0: no whitespace errors
```

No `lake update`, `lake build`, dependency clone/fetch, or `.lake` mutation was performed. The
pre-existing untracked `Formalizations/Lean/.lake` symlink is not a changed path or release evidence.

## Retry boundary

The proof lane must close the three root-cut obligations and unconditional root composition. The
integration lane must accept the dependency chain. A separately provisioned release lane must then
close H0/R0 review, root trust and provenance, hermetic supply-chain, independent-verifier, CI, and
deterministic-bundle gates. Only the master may accept the release node.
