"""
Visualization Script — GBV LLM Red-Teaming Research
========================================================
Generates publication-ready charts from your three result files:
1. GBV_LLM_Responses_JUDGED.json     (stance classification)
2. GBV_LLM_Responses_LANGID.json     (language identity analysis)
3. GBV_LLM_Responses_Groq_CLEAN.json (raw data, for religion control check)

Requires: pip install matplotlib --break-system-packages (if not installed)

Saves all charts as PNG files
"""

import json
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("Agg")  # no GUI needed, just save files
from collections import Counter

# ============================================================
# CONFIG — update paths if needed
# ============================================================
inpput = 
OUTPUT_DIR = 

import os
os.makedirs(OUTPUT_DIR, exist_ok=True)

MODEL_SHORT_NAMES = {
    "llama-3.3-70b-versatile": "Llama-3.3-70B",
    "openai/gpt-oss-120b": "GPT-OSS-120B",
    "openai/gpt-oss-20b": "GPT-OSS-20B",
    "qwen/qwen3.6-27b": "Qwen3.6-27B",
}

COLORS = {
    "explicit_condemnation": "#2E7D32",
    "bare_refusal": "#F9A825",
    "soft_deflection": "#EF6C00",
    "validation_justification": "#C62828",
}

# ============================================================
# CHART 1: Language Identity Failure Rate by Model
# ============================================================
def chart_language_failure_by_model():
    with open(LANGID_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    ur_records = [r for r in data if r.get("language") == "Roman Urdu"
                  and r.get("detected_response_language") != "technical_error"]

    models = list(MODEL_SHORT_NAMES.keys())
    failure_rates = []
    for model in models:
        subset = [r for r in ur_records if r["model_requested"] == model]
        fail = sum(1 for r in subset if r["language_identity_failure"])
        rate = 100 * fail / len(subset) if subset else 0
        failure_rates.append(rate)

    labels = [MODEL_SHORT_NAMES[m] for m in models]

    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.bar(labels, failure_rates, color=["#2E7D32", "#C62828", "#C62828", "#F9A825"])
    ax.set_ylabel("Language Identity Failure Rate (%)", fontsize=11)
    ax.set_title("Roman Urdu Language Identity Failure Rate by Model", fontsize=13, fontweight="bold")
    ax.set_ylim(0, 105)
    ax.axhline(0, color="black", linewidth=0.8)

    for bar, rate in zip(bars, failure_rates):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1.5,
                f"{rate:.1f}%", ha="center", fontsize=10, fontweight="bold")

    plt.tight_layout()
    out_path = os.path.join(OUTPUT_DIR, "1_language_failure_by_model.png")
    plt.savefig(out_path, dpi=150)
    plt.close()
    print(f"Saved: {out_path}")


# ============================================================
# CHART 2: English vs Roman Urdu — grouped bar comparison
# ============================================================
def chart_english_vs_urdu_failure():
    with open(LANGID_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    models = list(MODEL_SHORT_NAMES.keys())
    en_rates, ur_rates = [], []

    for model in models:
        en_subset = [r for r in data if r["model_requested"] == model and r["language"] == "English"
                     and r.get("detected_response_language") != "technical_error"]
        ur_subset = [r for r in data if r["model_requested"] == model and r["language"] == "Roman Urdu"
                     and r.get("detected_response_language") != "technical_error"]

        en_fail = sum(1 for r in en_subset if r["language_identity_failure"])
        ur_fail = sum(1 for r in ur_subset if r["language_identity_failure"])

        en_rates.append(100 * en_fail / len(en_subset) if en_subset else 0)
        ur_rates.append(100 * ur_fail / len(ur_subset) if ur_subset else 0)

    labels = [MODEL_SHORT_NAMES[m] for m in models]
    x = range(len(labels))
    width = 0.35

    fig, ax = plt.subplots(figsize=(9, 5.5))
    bars1 = ax.bar([i - width/2 for i in x], en_rates, width, label="English", color="#1565C0")
    bars2 = ax.bar([i + width/2 for i in x], ur_rates, width, label="Roman Urdu", color="#C62828")

    ax.set_ylabel("Failure Rate (%)", fontsize=11)
    ax.set_title("Language Identity Failure: English vs Roman Urdu", fontsize=13, fontweight="bold")
    ax.set_xticks(list(x))
    ax.set_xticklabels(labels)
    ax.legend()
    ax.set_ylim(0, 105)

    for bars in [bars1, bars2]:
        for bar in bars:
            h = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2, h + 1.5, f"{h:.1f}%",
                    ha="center", fontsize=9)

    plt.tight_layout()
    out_path = os.path.join(OUTPUT_DIR, "2_english_vs_urdu_failure.png")
    plt.savefig(out_path, dpi=150)
    plt.close()
    print(f"Saved: {out_path}")


# ============================================================
# CHART 3: Overall Stance Classification (Horizontal Bar Chart)
# ============================================================
def chart_stance_distribution():

    with open(JUDGED_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    judged = [r for r in data if r.get("llm_judge_classification") in COLORS]
    counts = Counter(r["llm_judge_classification"] for r in judged)

    labels = [
        "Explicit Condemnation",
        "Bare Refusal",
        "Soft Deflection",
        "Validation/Justification"
    ]

    keys = [
        "explicit_condemnation",
        "bare_refusal",
        "soft_deflection",
        "validation_justification"
    ]

    values = [counts.get(k, 0) for k in keys]
    colors = [COLORS[k] for k in keys]

    total = sum(values)
    percentages = [100 * v / total for v in values]

    fig, ax = plt.subplots(figsize=(9, 5))

    bars = ax.barh(
        labels,
        percentages,
        color=colors,
        edgecolor="black"
    )

    # Add percentage labels
    for bar, pct in zip(bars, percentages):
        ax.text(
            bar.get_width() + 0.5,
            bar.get_y() + bar.get_height() / 2,
            f"{pct:.1f}%",
            va="center",
            fontsize=11,
            fontweight="bold"
        )

    ax.set_xlabel("Percentage of Responses (%)", fontsize=12)
    ax.set_xlim(0, max(percentages) + 10)

    ax.set_title(
        f"Overall Stance Classification (n={total} responses)",
        fontsize=14,
        fontweight="bold"
    )

    ax.grid(axis="x", linestyle="--", alpha=0.4)

    plt.tight_layout()

    out_path = os.path.join(
        OUTPUT_DIR,
        "3_overall_stance_distribution_bar.png"
    )

    plt.savefig(out_path, dpi=300, bbox_inches="tight")
    plt.close()

    print(f"Saved: {out_path}")
    
# ============================================================
# CHART 4: Bare-refusal rate by Language x Model (the key correlation finding)
# ============================================================
def chart_refusal_by_language_model():
    with open(JUDGED_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    judged = [r for r in data if r.get("llm_judge_classification") in COLORS]
    models = list(MODEL_SHORT_NAMES.keys())

    en_refusal, ur_refusal = [], []
    for model in models:
        en_subset = [r for r in judged if r["model_requested"] == model and r["language"] == "English"]
        ur_subset = [r for r in judged if r["model_requested"] == model and r["language"] == "Roman Urdu"]

        en_ref = sum(1 for r in en_subset if r["llm_judge_classification"] == "bare_refusal")
        ur_ref = sum(1 for r in ur_subset if r["llm_judge_classification"] == "bare_refusal")

        en_refusal.append(100 * en_ref / len(en_subset) if en_subset else 0)
        ur_refusal.append(100 * ur_ref / len(ur_subset) if ur_subset else 0)

    labels = [MODEL_SHORT_NAMES[m] for m in models]
    x = range(len(labels))
    width = 0.35

    fig, ax = plt.subplots(figsize=(9, 5.5))
    bars1 = ax.bar([i - width/2 for i in x], en_refusal, width, label="English", color="#1565C0")
    bars2 = ax.bar([i + width/2 for i in x], ur_refusal, width, label="Roman Urdu", color="#F9A825")

    ax.set_ylabel("Bare Refusal Rate (%)", fontsize=11)
    ax.set_title("Bare-Refusal Rate: English vs Roman Urdu\n(Safety-Engagement Degradation)",
                 fontsize=13, fontweight="bold")
    ax.set_xticks(list(x))
    ax.set_xticklabels(labels)
    ax.legend()

    for bars in [bars1, bars2]:
        for bar in bars:
            h = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2, h + 1, f"{h:.1f}%",
                    ha="center", fontsize=9)

    plt.tight_layout()
    out_path = os.path.join(OUTPUT_DIR, "4_refusal_rate_by_language_model.png")
    plt.savefig(out_path, dpi=150)
    plt.close()
    print(f"Saved: {out_path}")


# ============================================================
# CHART 5: Religion control check (shows minimal bias)
# ============================================================
def chart_religion_control():
    with open(JUDGED_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    judged = [r for r in data if r.get("llm_judge_classification") in COLORS]
    religions = ["Islam", "Hindu", "Christian"]

    condemnation_rates = []
    refusal_rates = []
    for rel in religions:
        subset = [r for r in judged if r["religion"] == rel]
        total = len(subset)
        cond = sum(1 for r in subset if r["llm_judge_classification"] == "explicit_condemnation")
        ref = sum(1 for r in subset if r["llm_judge_classification"] == "bare_refusal")
        condemnation_rates.append(100 * cond / total)
        refusal_rates.append(100 * ref / total)

    x = range(len(religions))
    width = 0.35

    fig, ax = plt.subplots(figsize=(7, 5))
    bars1 = ax.bar([i - width/2 for i in x], condemnation_rates, width,
                   label="Explicit Condemnation", color="#2E7D32")
    bars2 = ax.bar([i + width/2 for i in x], refusal_rates, width,
                   label="Bare Refusal", color="#F9A825")

    ax.set_ylabel("Rate (%)", fontsize=11)
    ax.set_title("Response Pattern by Victim Religion\n(Control Check — No Significant Bias Found)",
                 fontsize=13, fontweight="bold")
    ax.set_xticks(list(x))
    ax.set_xticklabels(religions)
    ax.legend()
    ax.set_ylim(0, 100)

    for bars in [bars1, bars2]:
        for bar in bars:
            h = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2, h + 1, f"{h:.1f}%",
                    ha="center", fontsize=9)

    plt.tight_layout()
    out_path = os.path.join(OUTPUT_DIR, "5_religion_control_check.png")
    plt.savefig(out_path, dpi=150)
    plt.close()
    print(f"Saved: {out_path}")


# ============================================================
# CHART 6: Script breakdown (what languages/scripts models drift into)
# ============================================================
def chart_script_breakdown():
    with open(LANGID_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    ur_records = [r for r in data if r.get("language") == "Roman Urdu"
                  and r.get("detected_response_language") != "technical_error"]

    counts = Counter(r["detected_response_language"] for r in ur_records)
    label_map = {
        "roman_urdu": "Roman Urdu\n(Correct)",
        "english": "English\n(Drift)",
        "mixed_script": "Mixed\nScript",
        "urdu_arabic_script": "Urdu\nScript",
        "hindi_devanagari": "Hindi\n(Devanagari)",
        "unclear": "Unclear",
    }
    order = ["roman_urdu", "mixed_script", "english", "urdu_arabic_script", "hindi_devanagari", "unclear"]
    labels = [label_map[k] for k in order if k in counts]
    values = [counts[k] for k in order if k in counts]
    colors_list = ["#2E7D32", "#EF6C00", "#1565C0", "#8E24AA", "#C62828", "#757575"]

    fig, ax = plt.subplots(figsize=(9, 5.5))
    bars = ax.bar(labels, values, color=colors_list[:len(labels)])
    ax.set_ylabel("Number of Responses", fontsize=11)
    ax.set_title(f"What Script/Language Did Roman Urdu Prompts Actually Get?\n(n={len(ur_records)})",
                 fontsize=13, fontweight="bold")

    for bar, v in zip(bars, values):
        pct = 100 * v / len(ur_records)
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 15,
                f"{v}\n({pct:.1f}%)", ha="center", fontsize=9)

    plt.tight_layout()
    out_path = os.path.join(OUTPUT_DIR, "6_script_breakdown.png")
    plt.savefig(out_path, dpi=150)
    plt.close()
    print(f"Saved: {out_path}")


# ============================================================
# RUN ALL
# ============================================================
if __name__ == "__main__":
    print("Generating charts...\n")
    chart_language_failure_by_model()
    chart_english_vs_urdu_failure()
    chart_stance_distribution()
    chart_refusal_by_language_model()
    chart_religion_control()
    chart_script_breakdown()
    print(f"\nAll charts saved to: {OUTPUT_DIR}")
