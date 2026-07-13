# THM-M-1485 source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:10854-10859` records:

- title: `反向传播算法`;
- attribution: David Rumelhart, Geoffrey Hinton, and Ronald Williams;
- date: 1986;
- gloss: `神经网络的训练算法`;
- importance: high; and
- formalization status: `已验证`.

All six uncited lines originate at repository commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. `Docs/Stage0_Blueprint.md:40378-40403`
repeats the label and gloss while explicitly leaving the formal system, exact definitions and
premises, proof route, dependencies, equivalent forms, axiom policy, machine status, and artifact
link open. The rev-5.6 manifest preserves `已验证` only as `source_status_untrusted` and resets the
target to `L0 / rework_required`.

This record identifies an algorithm family, not a truth-valued proposition. It provides no ordered
binders, assumptions, conclusion, edition, theorem identifier, page, proof boundary, correction
record, Lean declaration, or proof body.

## Inspected primary-source lead

David E. Rumelhart, Geoffrey E. Hinton, and Ronald J. Williams, *Learning representations by
back-propagating errors*, Nature 323(6088), 533-536 (9 October 1986), DOI
`10.1038/323533a0`, matches the catalog authors and year. Crossref confirms the bibliographic
identity. An author-hosted four-page facsimile was inspected at
`https://www.cs.toronto.edu/~hinton/absps/naturebp.pdf`; its observed SHA-256 was
`d26997baf588222109d32545604a2a2ed400dc769a21fd49a5acdc4a955396ae`.

The article is a high-quality target-disambiguation lead, but it is not cited by the repository.
The remote facsimile was not vendored or admitted into an immutable source bundle, translation and
correction status were not audited, and no independent reviewer approved the mapping. The locator
therefore remains discovery evidence and cannot satisfy `H0`.

## Clause crosswalk

| Source locus | Human mathematical component | Prospective Lean component | Intake result |
|---|---|---|---|
| p. 533, prose and eqs. (1)-(2) | finite layered feed-forward connections, weighted input `x_j = sum_i y_i w_ji`, sigmoid output, biases via a fixed input | finite graph/layers, weights, `Finset.sum` or matrices, `Real.sigmoid` | inspected source candidate; representation and scope not selected |
| p. 534, eq. (3) | total half squared error over finite input-output cases and output units | finite sums and squared norm/coordinate loss | inspected candidate; loss carrier and normalization not frozen |
| p. 534, eqs. (4)-(5) | output error derivative and sigmoid chain rule | `Real.hasDerivAt_sigmoid`, chain-rule composition | inspected candidate; derivative convention and target open |
| p. 534, eq. (6) | derivative with respect to an edge weight equals local error derivative times the source activation | coordinate or continuous-linear-map parameter derivative | inspected candidate; no parameter encoding selected |
| p. 535, eq. (7) | derivative at a hidden unit is the sum over all outgoing connections | reverse recurrence over a finite acyclic graph | strongest correctness-root candidate, but not selected by catalog |
| p. 535, eq. (8) | plain gradient change `Delta w = -epsilon partial E / partial w` | one exact-real parameter update | training candidate only; learning-rate contract open |
| p. 535, eq. (9) | momentum update using the previous weight change | stateful update recurrence | distinct algorithm variant, not an equivalent restatement |
| p. 535, final discussion | gradient descent is not guaranteed to find a global minimum | explicit exclusion from an inferred convergence theorem | prevents a title-derived global-convergence claim |
| catalog `已验证` | untrusted inventory status | no expression or proof | explicitly rejected as evidence |

The article also references a longer 1986 chapter, *Learning Internal Representations by Error
Propagation*, pages 318-362 of *Parallel Distributed Processing*, volume 1. This is a further
source-audit lead, not an admitted premise or proof boundary for the root.

## Candidate-meaning boundary

At least these mutually nonidentical roots remain compatible with the catalog:

1. the displayed recursive formulas compute the derivatives of the displayed sigmoid-network
   squared error;
2. a generalized reverse-mode algorithm computes gradients for finite acyclic differentiable
   computation graphs;
3. an executable program implements one such recurrence correctly and terminates;
4. equations (8) or (9) update parameters exactly as specified; or
5. a training method has a convergence, minimization, complexity, or performance guarantee.

The source supports investigation of the first and fourth readings but does not let intake infer the
fifth. Choosing any reading without accountable source selection would substitute a theorem.

## Pinned Lean crosswalk

At mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`:

| Module/declaration | Available role | Boundary |
|---|---|---|
| `Mathlib.Analysis.Calculus.FDeriv.Comp`, `HasFDerivAt.comp`, `fderiv_comp` | generic Frechet chain rule | no network graph, reverse sweep, or source identity |
| `Mathlib.Analysis.Calculus.FDeriv.Add`, `HasFDerivAt.fun_sum`, `fderiv_sum` | derivative of a finite sum | no cases, loss, or parameter-gradient encoding selected |
| `Mathlib.Analysis.SpecialFunctions.Sigmoid`, `Real.hasDerivAt_sigmoid` | derivative of the source's displayed sigmoid | one local activation lemma, not backpropagation correctness |
| `Mathlib.Analysis.InnerProductSpace.Calculus`, `HasFDerivAt.norm_sq` | squared-norm derivative | generic loss ingredient only |
| `Mathlib.LinearAlgebra.Matrix.ToLin`, `Matrix.mulVecLin`, `Matrix.mulVecLin_mul` | matrix-vector and composition encoding | no layerwise semantics or reverse recurrence |

`IntakeProbe.lean` checks these pinned interfaces and selected axiom closures. A bounded
case-insensitive search over repo-local Lean and pinned mathlib found no exact backpropagation,
back-propagation, or reverse-mode declaration. This is intake discovery only, not an exhaustive
negative anchor audit and not proof that no formalization exists.

## Required source gate

Before statement elaboration, accountable source and scope reviewers must admit an immutable source
edition, select one exact result and every incorporated definition, map all premises, transitions,
and conclusions, audit corrections and historical variants, resolve the choices in `scope-map.md`,
and approve exclusions. Only then can an exact Lean target, expression/environment fingerprints,
checked transports, and statement mutations be created.
