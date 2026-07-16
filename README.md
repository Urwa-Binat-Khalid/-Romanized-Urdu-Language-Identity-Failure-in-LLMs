# -Romanized-Urdu-Language-Identity-Failure-in-LLMs

Red-teaming study evaluating 4 LLMs on a self-constructed 1,503-case Pakistani gender-based-violence (GBV) dataset, testing bilingual (English / Romanized Urdu) prompting to measure linguistic consistency and safety-engagement quality in a widely-used but unstandardized, unbenchmarked written register.

## Key Findings

**1. Language Identity Failure**
- English prompts: **0.0% failure rate** (perfect consistency)
- Roman Urdu prompts: **55.7% failure rate** — models frequently defaulted to English, Hindi (Devanagari), or Urdu script instead of maintaining Roman Urdu
- Failure rate is highly model-dependent, ranging from **2.2%** (Llama-3.3-70B) to **96.6%** (GPT-OSS-120B) — a 44x gap indicating the issue stems from training-data composition, not model scale

| Model | Roman Urdu Failure Rate |
|---|---|
| Llama-3.3-70B | 2.2% |
| Qwen3.6-27B | 27.7% |
| GPT-OSS-20B | 96.5% |
| GPT-OSS-120B | 96.6% |

**2. Safety Engagement Degrades Alongside Language Failure**
Models with the worst language-identity failure also showed a near-doubling of bare-refusal rate in Roman Urdu vs. English:

| Model | Bare Refusal (English) | Bare Refusal (Roman Urdu) |
|---|---|---|
| Llama-3.3-70B | 0.0% | 0.0% |
| Qwen3.6-27B | 0.9% | 2.5% |
| GPT-OSS-120B | 24.8% | 48.8% |
| GPT-OSS-20B | 35.3% | 53.4% |

**3. Actionable-Resource Gap**
Models providing safety advice mentioned concrete resources (police, helplines, hospitals) **3–4x less often** in Roman Urdu than in English for identical cases (e.g., GPT-OSS-120B: 3.10 mentions in English vs. 0.70 in Roman Urdu).

**4. Minimal Religion-Based Bias (Control Check)**
Explicit condemnation and refusal rates were nearly identical across victim religious identity (Islam/Hindu/Christian, ~77–78% condemnation across all three), ruling out religion as a confounding factor.

**5. Overall Safety Result**
Across 4,512 stance-taking responses, only **1 (0.02%)** validated a victim-blaming or perpetrator-justification premise — models overwhelmingly reject harmful framings, though bare refusal (20.7% overall) represents a missed opportunity for substantive ethical engagement.

## Repository Structure
