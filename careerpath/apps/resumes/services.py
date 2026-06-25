import re
from io import BytesIO

from website.career_resources import get_career_resource

from .models import ResumeAnalysis


ACTION_VERBS = {"built", "created", "led", "improved", "designed", "analyzed", "deployed", "optimized", "automated", "launched"}


def extract_text(uploaded_file):
    extension = uploaded_file.name.rsplit(".", 1)[-1].lower()
    content = uploaded_file.read()
    uploaded_file.seek(0)
    if extension == "pdf":
        return _extract_pdf_text(content)
    if extension == "docx":
        return _extract_docx_text(content)
    return ""


def _extract_pdf_text(content):
    try:
        from PyPDF2 import PdfReader
    except ImportError:
        return ""
    reader = PdfReader(BytesIO(content))
    return "\n".join(page.extract_text() or "" for page in reader.pages)


def _extract_docx_text(content):
    try:
        from docx import Document
    except ImportError:
        return ""
    document = Document(BytesIO(content))
    return "\n".join(paragraph.text for paragraph in document.paragraphs)


def analyze_resume(user, uploaded_file, target_role):
    target_role = target_role or _latest_target_role(user)
    extracted_text = extract_text(uploaded_file)
    report = score_resume_text(extracted_text, target_role)
    return ResumeAnalysis.objects.create(
        user=user,
        target_role=target_role,
        resume_file=uploaded_file,
        original_filename=uploaded_file.name,
        extracted_text=extracted_text[:20000],
        **report,
    )


def score_resume_text(text, target_role):
    normalized = text.lower()
    resource_pack = get_career_resource(target_role)
    required_skills = resource_pack.get("required_skills", [])
    keyword_matches = [skill for skill in required_skills if skill.lower() in normalized]
    missing_keywords = [skill for skill in required_skills if skill not in keyword_matches]
    weak_bullets = _find_weak_bullets(text)
    formatting_issues = _formatting_issues(text)

    keyword_score = round((len(keyword_matches) / max(len(required_skills), 1)) * 45)
    bullet_score = 30 if not weak_bullets else max(10, 30 - len(weak_bullets) * 5)
    formatting_score = 25 if not formatting_issues else max(8, 25 - len(formatting_issues) * 5)
    ats_score = min(100, keyword_score + bullet_score + formatting_score)

    suggestions = [
        f"Add role-specific keywords: {', '.join(missing_keywords[:5])}." if missing_keywords else "Keep the current role-specific keyword coverage.",
        "Rewrite weak bullets with action verb + metric + outcome.",
        "Mirror the target role title in your summary and top project bullets.",
    ]
    return {
        "ats_score": ats_score,
        "keyword_matches": keyword_matches,
        "missing_keywords": missing_keywords,
        "weak_bullets": weak_bullets[:8],
        "formatting_issues": formatting_issues,
        "improvement_suggestions": suggestions,
    }


def _find_weak_bullets(text):
    candidates = [line.strip(" -•\t") for line in text.splitlines() if len(line.strip()) > 20]
    weak = []
    for line in candidates:
        first_word = re.split(r"\W+", line.lower())[0]
        has_metric = bool(re.search(r"\d+|%|\busers\b|\brevenue\b|\btime\b", line.lower()))
        if first_word not in ACTION_VERBS or not has_metric:
            weak.append(line)
    return weak


def _formatting_issues(text):
    issues = []
    if len(text.strip()) < 500:
        issues.append("Resume text is very short or could not be extracted cleanly.")
    if "@" not in text:
        issues.append("Email address was not detected.")
    if not re.search(r"github|linkedin|portfolio", text, flags=re.I):
        issues.append("Portfolio, GitHub, or LinkedIn link was not detected.")
    return issues


def _latest_target_role(user):
    latest = user.assessment_results.first()
    return latest.career_name if latest else "Software Engineer"

