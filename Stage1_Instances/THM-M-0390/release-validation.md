# THM-M-0390 Release Decision Handoff

## Exact verdict

`S56-M-0390-RELEASE` is **blocked**. The lifecycle remains `planned`, the accepted root vector
remains `[H2, M4, R4]`, `audit_complete=false`, and `theorem_complete=false`. There are no accepted
receipt IDs and no theorem-completion promotion.

The first failed gate is `S56-10.2-DEPENDENCY-ACCEPTANCE`: the validation prerequisite is `[_]`
worker evidence with `support_state=provisional_worker_selftest`, not a master-accepted dependency.
Even after dependency acceptance, `THEOREM-Z` would immediately fail root kernel closure. The
validation receipt covers only coprimality step `NP.4`, not a complete canonical obligation.

## Reconciliation

The exact statement elaborates, and two same-workspace Lean implementations validate the genuine
lemma that the bases in a solution are coprime. This is provisional kernel evidence for one step
inside `THM-M-0390-N-PRIMITIVE`. It does not close that normalization obligation, any of the three
exponent branches, the deep Cassels/Wieferich/cyclotomic packages, or the exact Catalan root. All
fourteen frozen root-relevant obligations therefore remain open at canonical-obligation granularity.

The source state remains `H2`: the primary publication is identified, but the exact theorem/page,
assumptions, errata, node crosswalk, and independent H0 review are absent. Readability remains `R4`:
the architecture is not an independently accepted complete reconstruction. Thus `AUDIT-Z` also
does not pass.

Release evidence is absent for complete root provenance/axiom/TCB closure, an immutable clean
snapshot, empty-cache network-denied cold build, offline archive restoration, SBOM/licenses,
protected CI and mutation gates, two separately provisioned signed attestations, an independently
implemented minimal release verifier, and a deterministic content-addressed bundle. The existing
independent lemma probe ran in this checkout with the shared pinned dependency cache and does not
satisfy section 10.7.

## Self-test

Commands were run from base revision `8532255651da718bca9900badd6c74ba110cc9ab` on 2026-07-12:

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups; 1546 uniform-L0 targets; execution skill present

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required

python3 scripts/stage1_target.py show THM-M-0390
  exit 0: rank 4; lifecycle planned; theorem_complete=false

python3 Stage1_Instances/THM-M-0390/check_validation.py
  exit 0: fourteen-node identity, open root, partial proof identity, independent probe,
  and placeholder policy verified

cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0390/Proof.lean
  exit 0: NP.4 proof and wrapper elaborated; axioms propext and Quot.sound

cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0390/Validation.lean
  exit 0: independently reconstructed NP.4 proof elaborated; axioms propext and Quot.sound

python3 Stage1_Instances/THM-M-0390/check_release.py
  exit 0: blocked decision, unaccepted dependency, open exact root, false terminal
  booleans, and release cut set agree

python3 -m json.tool Stage1_Instances/THM-M-0390/release-decision.json
  exit 0: valid JSON

rg -n '\b(sorry|admit)\b|^[[:space:]]*(axiom|unsafe)\b' \
  Stage1_Instances/THM-M-0390/{Proof,Validation}.lean
  exit 1 with empty output: pass, no prohibited local declaration or placeholder

git diff --check -- Stage1_Instances/THM-M-0390
  exit 0: no whitespace errors
```

No `lake update`, `lake build`, dependency fetch, clone, or `.lake` mutation was performed. The
pre-existing untracked `.lake` symlink is excluded from changed paths and is not release evidence.

## Retry boundary

The proof lane must close every root-critical obligation and exact composition. The integration
lane must then master-accept the dependency chain. A separately provisioned release lane must close
H0/R0 reviews, root trust and provenance, hermetic and independent reproduction, supply-chain and
CI gates, and deterministic bundle verification. Only the master may accept the terminal decision.
