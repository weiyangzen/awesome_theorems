# THM-M-0391 Release Decision Handoff

## Exact verdict

`S56-M-0391-RELEASE` is **blocked**. The lifecycle remains `planned`, the root vector remains
`[H1, M4, R4]`, `audit_complete=false`, and `theorem_complete=false`. There are no accepted receipt
IDs and no theorem-completion promotion.

The first failed gate is `S56-10.2-DEPENDENCY-ACCEPTANCE`: the validation prerequisite is `[_]`
worker evidence with `support_state=provisional_worker_selftest`, not a master-accepted dependency.
Even after dependency acceptance, `THEOREM-Z` would immediately fail root kernel closure: the
validation receipt records `root_closed=false` and closes only `M0391-B-EE`.

## Reconciliation

The statement elaborates exactly, and two different same-workspace Lean implementations validate
the elementary fact that two nontrivial squares cannot differ by one. This is provisional local
kernel evidence for one branch. It is not a proof of Mihailescu's theorem. Fourteen of the fifteen
frozen root-relevant obligations remain open, including exponent normalization, power lifting, the
EO/OE/OO branches, lift-back, and exact root composition. Therefore the root remains `M4`, not
`M0-*` or `M2`.

The human-source packet is still `H1`: it lacks an independently reviewed exact primary-source
theorem/page, assumptions, errata, and node crosswalk. The readable surface remains `R4`: the open
architecture is not an independently accepted complete reconstruction. Hence `AUDIT-Z` also does
not pass.

Release evidence is absent for complete root provenance/axiom/TCB closure, an immutable clean
snapshot, empty-cache network-denied cold build, offline archive restoration, SBOM/licenses,
protected CI and mutation gates, two separately provisioned signed attestations, an independently
implemented minimal release verifier, and a deterministic content-addressed bundle. The existing
independent branch probe ran in this same checkout with the shared read-only dependency cache and
does not satisfy section 10.7.

## Self-test

Commands were run from base revision `62c2c0315a74e39528d22069068ffe85fea50afd` on 2026-07-12:

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups; 1546 uniform-L0 targets; execution skill present

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required

python3 scripts/stage1_target.py show THM-M-0391
  exit 0: rank 5; lifecycle planned; theorem_complete=false

python3 Stage1_Instances/THM-M-0391/check_validation.py
  exit 0: exact partial proof re-elaborated; independent M0391-B-EE probe passed;
  root remains open

cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0391/Statement.lean
  exit 0 with no output: exact statement and checked transports elaborated

cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0391/Proof.lean
  exit 0: M0391-B-EE proof elaborated; axioms propext and Quot.sound

cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0391/Validation.lean
  exit 0: independently reconstructed M0391-B-EE proof elaborated; axioms propext,
  Classical.choice, and Quot.sound

python3 Stage1_Instances/THM-M-0391/check_release.py
  exit 0: blocked decision, unaccepted dependency, one closed branch, fourteen open
  obligations, false terminal booleans, and release cut set agree

python3 -m json.tool Stage1_Instances/THM-M-0391/release-decision.json
  exit 0: valid JSON

rg -n '\b(sorry|admit)\b|^[[:space:]]*(axiom|unsafe)\b' \
  Stage1_Instances/THM-M-0391/{Statement,Proof,Validation}.lean
  exit 1 with empty output: pass, no prohibited local declaration or placeholder

git diff --check -- Stage1_Instances/THM-M-0391
  exit 0: no whitespace errors
```

No `lake update`, `lake build`, dependency fetch, clone, or `.lake` mutation was performed. The
pre-existing untracked `.lake` symlink is excluded from changed paths and is not release evidence.

## Retry boundary

The proof lane must close the remaining root obligations and exact composition. The integration
lane must then master-accept the dependency chain. A separately provisioned release lane must close
H0/R0 reviews, root trust and provenance, hermetic and independent reproduction, supply-chain and
CI gates, and deterministic bundle verification. Only the master may accept the terminal decision.
