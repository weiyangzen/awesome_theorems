# THM-M-1244 Proof-Phase Validation

Item: `S56-M-1244-PROOF`. Base revision:
`8f22279fd1216cdfb5676c758e6bdb08e0ba3e01`.

## Implemented Proof

The complete 24-module import closure of
`GaussianLSI.gaussian_logSobolev_W12_pi` is vendored from
`YuanheZ/lean-stat-learning-theory` at immutable commit
`7b82b1323c80f0c21ca449fd12e1c24315ae9782`. Sixteen sources are unchanged;
eight receive only recorded Lean 4.29/mathlib API compatibility edits. Exact upstream and port
hashes, invertible diffs, closure facts, authorship, and the upstream license omission are recorded
in `PORT_PROVENANCE.md`; the standard Apache 2.0 text is supplied in `LICENSE`.

`Proof.lean` proves checked measure and entropy identities, derives the upstream Sobolev membership
and regularity hypotheses from the frozen assumptions, and applies the vendored terminal theorem.
Its existing sign-vector proof bounds the sum of coordinate derivative squares by the squared
operator norm. The pre-frozen package composer then constructs the unchanged exact
`GaussianLogSobolevTarget`, including dimension zero and the zero-safe entropy convention.

## Commands And Results

Validation uses only the existing pinned Lake environment. No `lake update`, `lake build`, clone,
fetch, network access, or `.lake` mutation is used.

```text
python3 Stage1_Instances/THM-M-1244/check_proof.py
  exit 0
  Reconstructed all 24 immutable upstream sources; checked the exact import
  closure, receipts, pins, and prohibited tokens; compiled Statement,
  ObligationTree, every vendored module, and Proof in a fresh temporary
  directory with --trust=0; verified four sorry-free reports and the exact
  root's [propext, Classical.choice, Quot.sound] axiom profile.

python3 Stage1_Instances/THM-M-1244/check_obligation_tree.py
  exit 0
  Frozen 18-obligation denominator and 36 typed edges remain valid.

python3 Docs/tools/check_stage1_standard.py
python3 scripts/stage1_target.py check
python3 scripts/stage1_target.py show THM-M-1244
  exit 0 for all three preflight commands.

git diff --check -- Stage1_Instances/THM-M-1244 \
  .stage1-worker-selftest.json
  exit 0; no whitespace errors.
```

This is a provisional proof-phase `M0-P` proposal pending master acceptance, not an authoritative
state transition. The frozen definition, domain, boundary, and foundation machine obligations
remain open for downstream validation. Human-source and readable acceptance, full transitive trust,
hermetic empty-cache replay, independent verification, validation, and release remain open. Neither
audit completion nor theorem completion is claimed.
