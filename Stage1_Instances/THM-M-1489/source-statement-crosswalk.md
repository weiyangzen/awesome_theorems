# THM-M-1489 source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:10882-10887` records only the title `Transformer`, proposer
`Vaswani等`, time `2017`, gloss `注意力机制的神经网络`, importance `高`, and formalization status
`已验证`. All six uncited lines originate at repository commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. That establishes repository provenance, not a
primary mathematical source.

`Docs/Stage0_Blueprint.md:40486-40511` repeats the gloss while explicitly leaving the formal
system, foundation, precise definitions and premises, proof route, dependencies, equivalent forms,
axioms, machine status, and artifact links open. Its generic closure prose receives no rev-5.6
credit. The target manifest preserves `已验证` only as `source_status_untrusted` and resets the
target to `L0 / rework_required`.

The record identifies an architecture family, not a truth-valued proposition. It provides no
ordered binders, hypotheses, conclusion, bibliography, theorem identifier, proof, correction
record, Lean declaration, or proof body.

## Inspected source-family lead

Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N. Gomez, Lukasz
Kaiser, and Illia Polosukhin, *Attention Is All You Need*, Advances in Neural Information
Processing Systems 30 (NIPS 2017), is compatible with the catalog attribution and year. The
official proceedings PDF inspected during intake has 11 pages, 569417 bytes, and observed SHA-256
`d87d482d5ae7960e2e43d7dd6d21377e60e73e8fce1bf2a01aff7aca8a08c537`.

The catalog does not cite this work or choose one claim from it. The inspected PDF was not admitted
to an immutable repository source bundle, edition and correction drift were not audited, and no
independent reviewer approved a source-to-root mapping. The paper is mainly an architecture and
empirical systems report, not a theorem-proof article. It is therefore a strong discovery lead but
not `H0` evidence.

## Clause crosswalk

| Source locus | Possible mathematical component | Prospective Lean component | Intake result |
|---|---|---|---|
| abstract and sections 1-2 | attention-only architecture and empirical quality/parallelism claims | architecture predicate, cost model, or empirical-evidence boundary | lead only; no proposition selected |
| section 3.1 | six-layer encoder and decoder stacks, residual connections, layer normalization, and decoder mask | typed block composition, layer iterator, mask and dependency semantics | definitions and parameters not accepted |
| section 3.2.1, equation (1) | scaled dot-product attention `softmax(QK^T / sqrt(d_k))V` | finite matrices, dot products, exact softmax and dimension hypotheses | strongest evaluation candidate, but not a theorem selected by the catalog |
| section 3.2.2 | projected parallel heads, concatenation, and output projection | finite head family, projection matrices, block concatenation and shape proof | candidate definition only |
| sections 3.3-3.5 | feed-forward layers, embeddings, output softmax, and positional encoding | component functions, parameters, normalization and length domain | candidate model clauses only |
| sections 4-6 | complexity/path-length comparison, training protocol, BLEU and timing results | exact cost theorem or explicitly empirical record | no cost model or experimental proposition selected |
| catalog `已验证` | untrusted inventory status | exact expression, declaration, proof and receipt | no credit |

Official proceedings and evolving arXiv editions report differing empirical values. That observed
edition drift reinforces the need to freeze one immutable edition and proposition; no benchmark
number is transported across editions or credited here.

## Non-equivalent readings

At least these roots remain compatible with the catalog gloss but are not interchangeable:

1. a model definition is well-typed for selected dimensions;
2. the matrix and coordinate forms of scaled dot-product attention agree;
3. exact softmax attention weights are positive and sum to one;
4. the causal mask enforces a selected dependency relation;
5. multi-head attention has an equivariance, expressivity, approximation, or complexity property;
6. training satisfies an optimization or generalization result; or
7. a specific trained model achieved a reported empirical score.

Selecting any of these without accountable source correction would invent a theorem.

## Pinned Lean boundary

At mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, generic real
exponential and square-root functions and finite matrix operations are present. In particular,
`Real.exp`, `Real.exp_pos`, `Real.sqrt`, `Real.sqrt_pos`, `dotProduct`, `Matrix.transpose`,
`Matrix.mul_apply`, `Matrix.mulVec`, `Matrix.mulVecLin`, and `Matrix.mulVecLin_mul` elaborate in
`IntakeProbe.lean`.

A bounded case-insensitive search over repo-local Lean and pinned mathlib found no `softmax`,
self-attention, multi-head-attention, scaled-dot-product-attention, Vaswani, or source-identical
Transformer terminal declaration. Incidental uses of the programming term “monad transformer” and
a holor comment about the neural-network community are unrelated. This is discovery-only evidence,
not an exhaustive external anchor audit or a global absence proof. The checked matrix and scalar
APIs are encoding substrate only and supply no root statement or proof.

## Required source gate

Before statement elaboration, accountable source and domain reviewers must admit an immutable
edition, select one exact truth-valued result and every incorporated definition, map all premises,
transitions, conclusions, experimental boundaries, and corrections, resolve the choices and cases
in `scope-map.md`, and approve why that result is this repository target. A fresh statement worker
must then elaborate exactly that claim with minimal pinned imports and run removed-hypothesis,
changed-domain, binder-scope, and boundary mutations.
