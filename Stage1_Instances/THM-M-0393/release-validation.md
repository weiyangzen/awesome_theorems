# THM-M-0393 Release Decision Handoff

## Exact verdict

`S56-M-0393-RELEASE` is **blocked**. The lifecycle remains `planned`, the root vector remains
`[H3, M4, R3]`, `audit_complete=false`, and `theorem_complete=false`. No receipt is accepted and
no theorem-completion promotion is proposed.

The first failed gate is `S56-10.2-DEPENDENCY-ACCEPTANCE`: the validation prerequisite is only
`[_]` worker evidence. Independently of that workflow failure, `THEOREM-Z` fails because the exact
root has no proof body or composition certificate. The validated lemma proves only that possible
integer scale factors are finite once `g^n | m`; it does not prove that a solution's gcd satisfies
that divisibility. Thus `M0393-N1` itself and all 17 canonical obligations remain open.

## Evidence reconciliation

The partial proof and an independently written same-workspace replay elaborate with only `propext`,
`Classical.choice`, and `Quot.sound` reported. Their local placeholder scans pass. This is narrow
kernel evidence for a strict subclaim, not Thue's theorem and not a closed registry node.

Direct replay of the frozen `Statement.lean` fails because `evalBinary` depends on a noncomputable
instance but is not declared `noncomputable`. Release therefore cannot credit canonical statement
reproduction. The dossier also lacks accepted H0 primary-source review, accepted R0 reconstruction,
root provenance/axiom/TCB closure, an immutable clean snapshot, cold offline reproduction,
SBOM/licenses, independent signed runners, a minimal independent verifier, required CI/mutation
results, and a deterministic evidence bundle. Same-checkout repetition over the shared pinned cache
does not satisfy independent verification.

## Self-test record

Commands run from base revision `15a5351889f1657f452569fe630c9e39edb81877`:

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups; 1546 uniform-L0 targets

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required

python3 scripts/stage1_target.py show THM-M-0393
  exit 0: rank 6; lifecycle planned; theorem_complete=false

python3 Stage1_Instances/THM-M-0393/validate_obligation_tree.py
  exit 0: 17 obligations; root M4/open

python3 Stage1_Instances/THM-M-0393/check_validation.py
  exit 0: independent finite-choice replay; root H3/M4/R3 open

(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0393/Proof.lean)
  exit 0: finite_pow_divisors elaborated; axioms propext, Classical.choice, Quot.sound

(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0393/Validation.lean)
  exit 0: independent_finite_pow_divisors elaborated with the same axiom report

(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0393/Statement.lean)
  exit 1: evalBinary depends on a noncomputable instance

python3 Stage1_Instances/THM-M-0393/check_release.py
  exit 0: blocked decision and fail-closed release cut set agree

python3 -m json.tool Stage1_Instances/THM-M-0393/release-decision.json
  exit 0: valid JSON

rg -n '\b(sorry|admit)\b|^[[:space:]]*(axiom|unsafe)\b' \
  Stage1_Instances/THM-M-0393/{Proof,Validation}.lean
  exit 1 with empty output: pass, no prohibited declaration or placeholder

git diff --check -- Stage1_Instances/THM-M-0393 .stage1-worker-selftest.json
  exit 0 with no output
```

No dependency update, build, clone, fetch, network access, or `.lake` mutation was performed. The
pre-existing untracked canonical `.lake` symlink is nonrelease input and is not a changed path.

## Retry boundary

The owning phases must repair and refreeze the statement and close the exact root proof graph. The
integration lane must accept the full dependency chain. A separately provisioned release lane must
then close all reproducibility, supply-chain, review, independent-verification, and bundle gates.
Only the master may accept the resulting terminal decision.
