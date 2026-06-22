# Model Card: Financial Inclusion Predictor

## Model Details

- Model family: CatBoost classifier inside a scikit-learn preprocessing pipeline
- Intended task: estimate the likelihood that a FinAccess respondent is financially included
- Target: `financially_included`
- Training data: processed FinAccess 2021 survey data
- Saved artifact: `models/model.pkl`
- Integrity file: `models/model.sha256`
- Provenance file: `models/model_provenance.json`

## Intended Use

The model is intended for academic analysis, exploratory segmentation, and decision-support demonstrations. It may help identify patterns associated with financial inclusion and profiles that merit further investigation.

It is not intended to make automated eligibility, lending, insurance, pricing, or other high-impact decisions about individuals.

## Current Performance Snapshot

The saved evaluation metadata reports:

- Accuracy: 0.926
- ROC-AUC: 0.983
- Recall for financially excluded respondents: 0.975
- Recall for financially included respondents: 0.913

These metrics come from the existing random holdout evaluation stored in `models/model_metrics.json`.

## Important Limitations

- The target is derived from current bank, mobile-money, and insurance usage.
- Closely related access and activity variables remain among the model inputs. Performance may therefore include target-proxy effects and should not be interpreted as proof of future predictive power.
- The current evaluation uses a random respondent-level split. Respondents from the same survey cluster may occur in both training and test data.
- The saved probabilities have not been formally calibrated.
- Performance has not yet been fully evaluated across sex, age, county, income, or other demographic subgroups.
- Feature importance and contribution values describe model behavior, not causal relationships.

## Ethical and Privacy Considerations

- Do not use predictions as the sole basis for decisions affecting a person.
- Confirm that the processed FinAccess data may be redistributed before making the repository or deployment public.
- Avoid displaying respondent-level records in public deployments unless the data owner has approved that use.
- Review subgroup performance and potential disparate impact before operational use.

## Artifact Security

The application verifies `models/model.pkl` against `models/model.sha256` before loading it. This detects accidental corruption and mismatches. It does not make pickle safe when both the model and checksum come from an untrusted source. Only run model artifacts from a trusted repository and reviewed commit.

## Recommended Future Evaluation

- Remove or separately test target-proxy features.
- Use cluster-aware or geographic holdout validation.
- Add probability calibration and Brier score evaluation.
- Report subgroup metrics and confidence intervals.
- Record model-training code, source-data version, and review approval for each release.
