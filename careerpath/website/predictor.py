from __future__ import annotations

import csv
from dataclasses import dataclass
from django.conf import settings


DATASET_PATH = settings.BASE_DIR / "ml" / "BasicTestQue.csv"
QUESTION_ORDER = [f"q{index}" for index in range(1, 21)]

QUESTION_TEXT = {
    "q1": "I enjoy solving problems using logic or math.",
    "q2": "I find it easy to explain concepts clearly to others.",
    "q3": "I often come up with new ideas for businesses or products.",
    "q4": "I am curious about how the human mind and behavior work.",
    "q5": "I enjoy caring for others and ensuring their well-being.",
    "q6": "I like creating art, designs, or digital media.",
    "q7": "I am interested in how computers, apps, or the internet work.",
    "q8": "I feel confident speaking to groups or leading discussions.",
    "q9": "I am drawn to nature and protecting the environment.",
    "q10": "I enjoy reading, writing, or analyzing literature.",
    "q11": "I like working with data, statistics, or graphs.",
    "q12": "I am passionate about justice and helping people legally.",
    "q13": "I find fulfillment in physical activity or fitness coaching.",
    "q14": "I often think about how to lead or manage people effectively.",
    "q15": "I am comfortable with technical tools and scientific equipment.",
    "q16": "I enjoy helping others deal with emotional or personal issues.",
    "q17": "I like staying up to date with political or legal events.",
    "q18": "I enjoy tracking financial data or creating budgets.",
    "q19": "I prefer hands-on work or being in a natural environment.",
    "q20": "I aspire to build something of my own in the future.",
}

QUESTION_TRAITS = {
    "q1": "Logic and mathematical problem solving",
    "q2": "Explaining ideas clearly",
    "q3": "Business and product ideation",
    "q4": "Psychology and behavior",
    "q5": "Care and wellbeing",
    "q6": "Creative design and media",
    "q7": "Technology curiosity",
    "q8": "Public speaking and leadership",
    "q9": "Environmental interest",
    "q10": "Writing and literature",
    "q11": "Data and analytics",
    "q12": "Law and justice",
    "q13": "Fitness and coaching",
    "q14": "Management thinking",
    "q15": "Scientific and technical tools",
    "q16": "Emotional support and counseling",
    "q17": "Political and legal awareness",
    "q18": "Finance and budgeting",
    "q19": "Hands-on practical work",
    "q20": "Entrepreneurial drive",
}

ROLE_RECOMMENDATIONS = {
    "Business & Management": "Business Operations Manager",
    "Data & Analytics": "Data Scientist",
    "Design & Arts": "UI/UX Designer",
    "Engineering & Technology": "Software Engineer",
    "Entrepreneurship & Innovation": "Startup Founder",
    "Environmental Sciences": "Environmental Scientist",
    "Finance & Banking": "Financial Analyst",
    "Healthcare": "Healthcare Professional",
    "IT & Cybersecurity": "Cybersecurity Analyst",
    "Law & Political Science": "Corporate Lawyer",
    "Media and Communication": "Communication Specialist",
    "Psychology & Social Work": "Counselor",
    "Science & Research": "Research Scientist",
    "Sports & Physical Wellness": "Fitness Coach",
    "Teaching & Education": "Educator",
    "Writing & Literature": "Content Writer",
}


@dataclass
class PredictionResult:
    top_domain: str
    recommended_role: str
    confidence: int
    probabilities: dict[str, int]
    top_traits: list[str]

    def as_session_payload(self) -> dict[str, object]:
        return {
            "top_domain": self.top_domain,
            "recommended_role": self.recommended_role,
            "confidence": self.confidence,
            "probabilities": self.probabilities,
            "top_traits": self.top_traits,
        }


def _load_label_profiles() -> dict[str, list[float]]:
    grouped_rows: dict[str, list[list[int]]] = {}
    with DATASET_PATH.open(newline="", encoding="utf-8-sig") as csv_file:
        for row in csv.DictReader(csv_file):
            label = row["Label"].strip()
            grouped_rows.setdefault(label, []).append(
                [int(row[f"Q{index}"]) for index in range(1, 21)]
            )

    profiles: dict[str, list[float]] = {}
    for label, rows in grouped_rows.items():
        row_count = len(rows) or 1
        profiles[label] = [
            sum(row[column_index] for row in rows) / row_count
            for column_index in range(20)
        ]
    return profiles


LABEL_PROFILES = _load_label_profiles()


def _score_against_profile(answer_map: dict[str, int], profile: list[float]) -> float:
    distance = sum(
        abs(answer_map[question_id] - profile[index])
        for index, question_id in enumerate(QUESTION_ORDER)
    )
    return 1 / (1 + distance)


def _normalize_scores(scores: dict[str, float]) -> dict[str, int]:
    total = sum(scores.values()) or 1
    percentages = {
        label: round((score / total) * 100)
        for label, score in scores.items()
    }

    difference = 100 - sum(percentages.values())
    if difference:
        best_label = max(percentages, key=percentages.get)
        percentages[best_label] += difference

    return dict(sorted(percentages.items(), key=lambda item: item[1], reverse=True))


def predict_basic_assessment(answer_map: dict[str, int]) -> PredictionResult:
    similarity_scores = {
        label: _score_against_profile(answer_map, profile)
        for label, profile in LABEL_PROFILES.items()
    }
    probabilities = _normalize_scores(similarity_scores)
    top_domain = max(similarity_scores, key=similarity_scores.get)

    ranked_traits = sorted(
        QUESTION_ORDER,
        key=lambda question_id: answer_map[question_id],
        reverse=True,
    )
    top_traits = [QUESTION_TRAITS[question_id] for question_id in ranked_traits[:3]]

    return PredictionResult(
        top_domain=top_domain,
        recommended_role=ROLE_RECOMMENDATIONS.get(top_domain, top_domain),
        confidence=probabilities[top_domain],
        probabilities=probabilities,
        top_traits=top_traits,
    )
