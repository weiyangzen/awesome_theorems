# THM-M-1485 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the repository label
`反向传播算法` (backpropagation algorithm). The catalog supplies only the gloss
`神经网络的训练算法` (a training algorithm for neural networks), attributes it to David
Rumelhart, Geoffrey Hinton, and Ronald Williams in 1986, and labels it `已验证`. An algorithm
name and purpose are not a truth-valued proposition with ordered binders, hypotheses, and a
conclusion. The verified label is untrusted metadata and supplies neither source nor proof credit.

Backpropagation can denote correctness of a reverse chain-rule recurrence, equality of recursively
computed error signals with partial derivatives, a parameter-gradient algorithm, a particular
weight-update rule, or a convergence or complexity claim. These are not interchangeable. The
catalog fixes no network graph, layer and unit index types, activation, loss, data semantics,
parameter representation, bias convention, reverse recurrence, optimizer, learning rate,
arithmetic model, or conclusion. Selecting a familiar finite feed-forward sigmoid-gradient theorem
or a convergence theorem would invent proposition-changing mathematics.

Rumelhart, Hinton, and Williams's 1986 article *Learning representations by back-propagating
errors*, Nature 323(6088), pages 533-536, DOI `10.1038/323533a0`, was inspected as a strong
primary-source lead matching the catalog authors and year. Pages 533-535 give a layered sigmoid
network, squared error, backward derivative recurrence, gradient update, and a momentum variant.
The paper also explicitly says gradient descent is not guaranteed to find a global minimum. The
catalog does not cite the article and does not select among its formulas and algorithm variants;
the facsimile has not been admitted as immutable repository evidence and no correction audit or
independent review exists. It is discovery evidence, not `H0` evidence.

Pinned mathlib supplies generic Frechet chain rules, finite-sum differentiation, real sigmoid
differentiation, squared-norm differentiation, and matrix-vector linear maps. `IntakeProbe.lean`
authenticates those adjacent APIs only. It does not define a neural network, implement a backward
sweep, or state or prove the unidentified root. A bounded exact-topic search found no
backpropagation declaration in pinned mathlib or repo-local Lean; exhaustive discovery remains a
later phase.

The provisional vector is `[H5, M4, R4]`. Here `H5` classifies the received catalog label and gloss
as not yet a stable proposition; it does not say that correctly stated backpropagation results are
false or open. All six downstream phases remain open. No canonical mathematical or Lean statement,
H0, M0, R0, proof body, accepted state, audit completion, theorem completion, accepted receipt, or
master acceptance is claimed.
