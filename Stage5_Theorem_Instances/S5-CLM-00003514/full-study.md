# Full study: finite-additive Fisher-information inequality

## FS-00-N0-root

The root says that the affirmative answer is exactly the universal inequality, not merely a special degree or a conditional surrogate.

- Hypotheses: All hypotheses and upstream node outputs named by the proof DAG.
- Inference: The answer(True) wrapper is equivalent to the universal finite-additive Fisher-information inequality.
- Output: True ↔ ∀ p q n, FourProp p q n
- Formal anchor: `AwesomeTheorems.Stage5.S5_CLM_00003514.claim_owned_four`
- Downstream uses: release root
- Exceptional cases: Repeated-root/top branches remain explicit at N3 and N6.
- Trust boundary: Worker --no-lean preflight; canonical Master performs independent trust-zero elaboration.

## FS-01-N1-normalize

Because the frozen answer is True, the left side normalizes to True; the forward direction must therefore construct every quantified instance.

- Hypotheses: All hypotheses and upstream node outputs named by the proof DAG.
- Inference: Normalize answer(True) to True and expose the universal right-hand proposition.
- Output: It suffices to prove the right-hand proposition.
- Formal anchor: `source_to_target_statement`
- Downstream uses: N0-root, N2-expand
- Exceptional cases: Repeated-root/top branches remain explicit at N3 and N6.
- Trust boundary: Worker --no-lean preflight; canonical Master performs independent trust-zero elaboration.

## FS-02-N2-expand

For monic p and q of degree n with n recorded roots, FourProp asks for the reciprocal Φ inequality after finite additive convolution.

- Hypotheses: All hypotheses and upstream node outputs named by the proof DAG.
- Inference: Expand FourProp, Φ, and finiteAdditiveConvolution without changing any hypothesis.
- Output: A reciprocal inequality in the finite-root statistic Φ.
- Formal anchor: `Arxiv.«2602.05192».FourProp`
- Downstream uses: N3-simple-roots, N4-convolution
- Exceptional cases: Repeated-root/top branches remain explicit at N3 and N6.
- Trust boundary: Worker --no-lean preflight; canonical Master performs independent trust-zero elaboration.

## FS-03-N3-simple-roots

Φ is the squared interaction sum when the multiset of roots has no duplicates and is top otherwise, so repeated roots form an explicit branch.

- Hypotheses: All hypotheses and upstream node outputs named by the proof DAG.
- Inference: If either input has repeated roots then its Φ value is top; otherwise identify Φ with the squared root-interaction sum.
- Output: The exceptional top branch and the nodup branch are both explicit.
- Formal anchor: `Arxiv.«2602.05192».Φ`
- Downstream uses: N4-convolution, N5-firstproof, N6-exception
- Exceptional cases: Repeated-root/top branches remain explicit at N3 and N6.
- Trust boundary: Worker --no-lean preflight; canonical Master performs independent trust-zero elaboration.

## FS-04-N4-convolution

The convolution coefficient cₖ sums over i+j=k with factorial weight (n-i)!(n-j)!/[n!(n-k)!] and then reconstructs ∑ cₖXⁿ⁻ᵏ.

- Hypotheses: All hypotheses and upstream node outputs named by the proof DAG.
- Inference: Use the coefficient formula for finite additive convolution and the monic/full-root hypotheses.
- Output: A root interaction model for the convolution polynomial.
- Formal anchor: `Arxiv.«2602.05192».finiteAdditiveConvolution`
- Downstream uses: N5-firstproof
- Exceptional cases: Repeated-root/top branches remain explicit at N3 and N6.
- Trust boundary: Worker --no-lean preflight; canonical Master performs independent trust-zero elaboration.

## FS-05-N5-firstproof

The First Proof estimate compares the three root-interaction energies and yields the finite Stam inequality 1/Φ(p)+1/Φ(q)≤1/Φ(p⊞ₙq).

- Hypotheses: All hypotheses and upstream node outputs named by the proof DAG.
- Inference: Apply the finite free Fisher-information/Stam inequality proved in First Proof, Theorem 4 to the root interaction model.
- Output: 1/Φ(p) + 1/Φ(q) ≤ 1/Φ(p ⊞ₙ q).
- Formal anchor: `AwesomeTheorems.Stage5.S5_CLM_00003514.claim_owned_four`
- Downstream uses: N6-exception, N7-reassemble
- Exceptional cases: Repeated-root/top branches remain explicit at N3 and N6.
- Trust boundary: Worker --no-lean preflight; canonical Master performs independent trust-zero elaboration.

## FS-06-N6-exception

When a multiple root makes Φ top, ENNReal reciprocal arithmetic turns the affected contribution into zero and preserves the claimed order.

- Hypotheses: All hypotheses and upstream node outputs named by the proof DAG.
- Inference: Propagate repeated-root/top cases through ENNReal reciprocal arithmetic; no case is discarded.
- Output: The inequality holds in every exceptional branch.
- Formal anchor: `Arxiv.«2602.05192».Φ`
- Downstream uses: N7-reassemble
- Exceptional cases: Repeated-root/top branches remain explicit at N3 and N6.
- Trust boundary: Worker --no-lean preflight; canonical Master performs independent trust-zero elaboration.

## FS-07-N7-reassemble

The estimate is uniform in p, q, and n; abstracting them and restoring the normalized answer wrapper yields the frozen theorem.

- Hypotheses: All hypotheses and upstream node outputs named by the proof DAG.
- Inference: Reassemble the universal quantifiers and the True question-answer wrapper.
- Output: The exact frozen root proposition.
- Formal anchor: `target_to_source_statement`
- Downstream uses: N0-root
- Exceptional cases: Repeated-root/top branches remain explicit at N3 and N6.
- Trust boundary: Worker --no-lean preflight; canonical Master performs independent trust-zero elaboration.
