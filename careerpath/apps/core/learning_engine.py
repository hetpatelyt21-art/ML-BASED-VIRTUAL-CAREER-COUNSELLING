TRUSTED_PROVIDERS = {
    "Coursera",
    "edX",
    "MIT OCW",
    "Stanford Online",
    "Harvard CS50",
    "Kaggle",
    "Google Certificates",
    "IBM SkillsBuild",
    "Microsoft Learn",
    "freeCodeCamp",
    "Khan Academy",
}


def resource(title, provider, url, level, targets):
    return {
        "title": title,
        "provider": provider,
        "url": url,
        "level": level,
        "targets": targets,
    }


CAREER_RESOURCE_ENGINE = {
    "Software Engineer": [
        resource("CS50x Introduction to Computer Science", "Harvard CS50", "https://cs50.harvard.edu/x/", "beginner", ["logic", "programming", "computer science"]),
        resource("Responsive Web Design", "freeCodeCamp", "https://www.freecodecamp.org/learn/2022/responsive-web-design/", "beginner", ["html", "css", "frontend"]),
        resource("Microsoft Learn: GitHub Foundations", "Microsoft Learn", "https://learn.microsoft.com/en-us/training/github/", "beginner", ["git", "portfolio"]),
        resource("MIT 6.0001 Python", "MIT OCW", "https://ocw.mit.edu/courses/6-0001-introduction-to-computer-science-and-programming-in-python-fall-2016/", "intermediate", ["python", "problem solving"]),
    ],
    "Data Scientist": [
        resource("Kaggle Python", "Kaggle", "https://www.kaggle.com/learn/python", "beginner", ["python"]),
        resource("Kaggle Intro to Machine Learning", "Kaggle", "https://www.kaggle.com/learn/intro-to-machine-learning", "intermediate", ["machine learning"]),
        resource("Khan Academy Statistics", "Khan Academy", "https://www.khanacademy.org/math/statistics-probability", "beginner", ["statistics"]),
        resource("IBM Data Science Professional Certificate", "Coursera", "https://www.coursera.org/professional-certificates/ibm-data-science", "intermediate", ["python", "sql", "data analysis"]),
    ],
    "UI/UX Designer": [
        resource("Google UX Design Certificate", "Google Certificates", "https://www.coursera.org/professional-certificates/google-ux-design", "beginner", ["ux", "research", "prototyping"]),
        resource("Stanford d.school Resources", "Stanford Online", "https://dschool.stanford.edu/resources", "intermediate", ["design thinking"]),
        resource("edX Design Thinking", "edX", "https://www.edx.org/learn/design-thinking", "beginner", ["design thinking"]),
    ],
    "Business Analyst": [
        resource("Google Data Analytics Certificate", "Google Certificates", "https://www.coursera.org/professional-certificates/google-data-analytics", "beginner", ["analytics", "sql"]),
        resource("Microsoft Learn Power BI", "Microsoft Learn", "https://learn.microsoft.com/en-us/training/powerplatform/power-bi", "intermediate", ["dashboards", "reporting"]),
        resource("Business Foundations", "Coursera", "https://www.coursera.org/specializations/wharton-business-foundations", "beginner", ["business"]),
    ],
}


def recommend_resources(target_role, weak_skills=None, level="beginner", limit=6):
    weak_terms = {skill.lower() for skill in (weak_skills or [])}
    candidates = CAREER_RESOURCE_ENGINE.get(target_role) or CAREER_RESOURCE_ENGINE["Software Engineer"]

    def score(item):
        target_hits = len(weak_terms.intersection({target.lower() for target in item["targets"]}))
        level_bonus = 2 if item["level"] == level else 0
        return target_hits * 3 + level_bonus

    ranked = sorted(candidates, key=score, reverse=True)
    return ranked[:limit]

