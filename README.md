# A Multi-Dimensional Analysis of LLM-Generated Python Code

A framework for evaluating LLM-generated Python code along three axes: **similarity** to reference implementations, **structural complexity**, and **functional correctness**. It also includes an automated **quality classifier** (SVM, kNN, Random Forest) built on static structural features.

## Overview

The project compares LLM-generated programs with reference implementations from the [Invisible Hand](https://aclanthology.org/) benchmark (Zhang et al., 2025). It covers:

- **142 programming tasks** across **30 application scenarios**, with up to five task variants per scenario.
- **284 LLM–reference program pairs.**
- Prompt-derived functional tests run against both the LLM and the reference code.
- A rule-based structural quality labeling scheme and three supervised classifiers trained on 12 static features.
- Two interfaces: a Streamlit analysis dashboard and a FastAPI quality-classifier web app.

### Objectives

1. Measure lexical, structural, and semantic similarity between LLM-generated code and reference implementations.
2. Quantify the structural complexity of LLM-generated code.
3. Write and run prompt-derived functional tests on both implementations to measure correctness.
4. Classify the structural quality of LLM-generated code with ML models using static structural features.

## Key Findings

- **Low textual and structural similarity, high semantic similarity.** Mean lexical similarity is 0.159 and structural similarity is 0.154, but semantic similarity is 0.961. The weighted final score averages 0.488.
- **Similarity does not predict correctness.** `S_final` has a near-zero correlation with test pass rate (r = 0.06).
- **LLM code is structurally larger and more complex.** Mean cyclomatic complexity is 2.08 vs. 1.19, and mean AST size is 359 vs. 113 nodes.
- **Functional tests favour the LLM code:** 90.8% mean pass rate vs. 36.8% for references. The report attributes much of this to references being minimal implementations (stubs, ignored constraints, import-time crashes), so this is not a claim of LLM superiority.
- **The SVM is the best quality classifier,** with 97.2% test accuracy and macro ROC-AUC of 0.999.

## Methodology

### 1. Similarity analysis

Three similarity dimensions are computed for every pair and combined into one score:

| Dimension | Method |
|---|---|
| Lexical | TF-IDF cosine similarity |
| Structural | Control-flow-graph (CFG) based graph comparison |
| Semantic | [CodeBERT](https://arxiv.org/abs/2002.08155) embedding cosine similarity |

```
S_final = 0.2 · S_lexical + 0.4 · S_structural + 0.4 · S_semantic
```

Preprocessing tokenizes code and normalizes comments and whitespace for a fair comparison.

### 2. Structural analysis

- **CFG metrics:** cyclomatic complexity, node count, edge count, graph depth.
- **AST metrics:** total nodes, depth, branching nodes, function and class definitions.

### 3. Functional testing

Test cases are derived from the original prompt specifications. The LLM-generated and reference implementations are run against identical test suites.

### 4. Structural quality classification

Each file is described by 12 static features: LOC, SLOC, average and max cyclomatic complexity, function count, class count, max and average nesting depth, comment ratio, average variable name length, unique variable count, and Halstead vocabulary.

- **Labeling:** a rule-based, threshold scoring mechanism assigns **Good**, **Moderate**, or **Bad**.
- **Models:** SVM, kNN, and Random Forest on z-score-normalized features.
- **Evaluation:** 5-fold cross-validation and a held-out test set of 107 samples.

## Results

### Similarity (n = 284 pairs)

| Dimension | Mean | Std | Min | Max |
|---|---|---|---|---|
| Lexical | 0.159 | 0.111 | 0.000 | 0.643 |
| Structural | 0.154 | 0.193 | 0.000 | 0.640 |
| Semantic | 0.961 | 0.022 | 0.883 | 0.997 |
| **Final (S_final)** | **0.488** | 0.090 | 0.367 | 0.771 |

Scenario-level variation is substantial. Authentication & Identity Management (0.670), Image Processing (0.626), and E-commerce (0.605) score highest. Voice & Video Communication (0.384), Video Streaming & Hosting (0.395), and Speech Recognition (0.409) score lowest.

`S_final` is driven mainly by structural similarity (r = 0.96); the lexical (r = 0.51) and semantic (r = 0.49) components contribute moderately.

### Structural metrics: LLM vs. reference

| Metric | LLM mean | Reference mean |
|---|---|---|
| CFG cyclomatic complexity | 2.08 | 1.19 |
| CFG nodes | 5.30 | 2.06 |
| CFG edges | 5.37 | 1.25 |
| CFG graph depth | 2.95 | 0.84 |
| AST total nodes | 359.4 | 112.9 |
| AST branching nodes | 7.48 | 1.11 |
| AST function definitions | 4.25 | 1.07 |

### Quality label distribution

The classifier dataset contains **726** LLM-generated samples, produced with prompts derived from the Invisible Hand dataset across multiple execution iterations.

| Label | Samples | Share |
|---|---|---|
| Good | 432 | 59.5% |
| Moderate | 234 | 32.2% |
| Bad | 46 | 6.3% |
| Unclassified (parsing constraints) | 14 | 1.9% |

### Classifier performance (test set, n = 107)

| Model | Test Acc. | Precision (M) | Recall (M) | F1 (M) | ROC-AUC | CV Acc. | CV Std |
|---|---|---|---|---|---|---|---|
| **SVM** | **0.972** | 0.980 | 0.933 | **0.955** | **0.999** | 0.976 | 0.014 |
| Random Forest | 0.925 | 0.878 | 0.818 | 0.842 | 0.989 | 0.898 | 0.012 |
| kNN | 0.888 | 0.833 | 0.747 | 0.775 | 0.933 | 0.876 | 0.024 |

*(M = macro-averaged.)* The SVM made only 3 misclassifications, compared with 8 for Random Forest and 12 for kNN. kNN is weakest on the minority Bad class (AUC = 0.846).

### Functional testing

| Variant | Records | Mean pass rate | Tests passed | Total tests |
|---|---|---|---|---|
| LLM-generated | 38 | 0.908 | 34 | 38 |
| Reference (ref_1 + ref_2) | 76 | 0.368 | 28 | 76 |

Selected scenario-level pass rates:

| Scenario | LLM | Reference |
|---|---|---|
| Blockchain & Cryptocurrency | 1.000 | 0.000 |
| Machine Learning – AI Deployment | 1.000 | 0.000 |
| Data Analysis | 0.750 | 0.000 |
| E-commerce | 1.000 | 0.500 |
| Image Processing | 1.000 | 1.000 |
| Authentication & Identity Management | 0.333 | 0.333 |
| Video Streaming & Hosting | 0.500 | 1.000 |

Reference implementations often failed because they were incomplete stubs, ignored core prompt constraints (for example, using unrelated third-party API boilerplate instead of the requested cryptographic logic), or crashed at import time.

## Dashboards

1. **Streamlit analysis dashboard:** explore similarity scores, structural metrics, CFG visualizations, and functional test results across the 30 scenarios and 284 program pairs.
2. **FastAPI quality classifier:** an HTML/CSS/JavaScript frontend where you upload or paste a Python file and get a Good/Moderate/Bad classification from each model, plus the computed 12-dimensional feature vector.

## Getting Started

```bash
git clone https://github.com/habtomt/llm-code-evaluation.git
cd llm-code-evaluation
pip install -r requirements.txt
```

### Run the analysis pipeline

```bash
python run_pipeline.py
```

### Launch the Streamlit dashboard

```bash
streamlit run app.py   # TODO: adjust to the actual dashboard file
```

### Launch the quality classifier (FastAPI)

```bash
uvicorn main:app --reload   # TODO: adjust module path
```

## Limitations

- **Dataset scope:** 30 scenarios from the Invisible Hand benchmark. Results may not generalize to other domains, languages, or LLM families.
- **Reference quality:** the references are not necessarily production quality. Their low pass rate suggests minimal implementations rather than comprehensive solutions.
- **Quality labels:** the rule-based thresholds have not been validated against human expert judgment. Because the labels are computed from the same features the classifiers see, the high accuracy partly reflects how well the models recover the labeling rule.
- **Test coverage:** tests are derived from natural-language specifications and may miss edge cases. Pass/fail results are evidence for the tested inputs only, not proofs of correctness.
- **Complementary, not a replacement:** structural quality does not guarantee functional correctness, so the classifier should complement functional testing.
