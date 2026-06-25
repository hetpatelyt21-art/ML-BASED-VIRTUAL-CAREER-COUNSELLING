from copy import deepcopy
from urllib.parse import parse_qs, urlparse


def _course(title, url, provider):
    return {"title": title, "url": url, "provider": provider}


def _resource(title, url, resource_type):
    return {"title": title, "url": url, "type": resource_type}


def _video(title, youtube_url):
    return {"title": title, "youtube_url": youtube_url}


CAREER_RESOURCES = {
    "Software Engineer": {
        "roadmap_summary": "Master programming fundamentals, build full-stack projects, practice testing and debugging, then publish polished work on GitHub.",
        "required_skills": ["Python or JavaScript", "Data structures", "Web development", "Git", "Testing"],
        "top_industries": ["Software products", "Fintech", "SaaS", "Cloud platforms"],
        "resources": [
            _resource("MDN Learn Web Development", "https://developer.mozilla.org/en-US/docs/Learn", "Official documentation"),
            _resource("Python Documentation Tutorial", "https://docs.python.org/3/tutorial/", "Official documentation"),
            _resource("freeCodeCamp Developer Certifications", "https://www.freecodecamp.org/learn/", "Practice"),
            _resource("MIT 6.0001", "https://ocw.mit.edu/courses/6-0001-introduction-to-computer-science-and-programming-in-python-fall-2016/", "Open course"),
        ],
        "courses": [
            _course("CS50x Introduction to Computer Science", "https://cs50.harvard.edu/x/", "Harvard CS50"),
            _course("MIT 6.0001 Introduction to CS in Python", "https://ocw.mit.edu/courses/6-0001-introduction-to-computer-science-and-programming-in-python-fall-2016/", "MIT OpenCourseWare"),
            _course("Responsive Web Design", "https://www.freecodecamp.org/learn/2022/responsive-web-design/", "freeCodeCamp"),
        ],
        "videos": [
            _video("Python for Everybody", "https://www.youtube.com/watch?v=8DvywoWv6fI"),
            _video("Git and GitHub for Beginners", "https://www.youtube.com/watch?v=RGOj5yH7evk"),
            _video("Harvard CS50 Full Course", "https://www.youtube.com/watch?v=8mAITcNt710"),
        ],
    },
    "Data Scientist": {
        "roadmap_summary": "Build Python, SQL, statistics, machine learning, visualization, and model evaluation through hands-on datasets.",
        "required_skills": ["Python", "SQL", "Statistics", "Machine learning", "Data visualization"],
        "top_industries": ["AI products", "Healthcare analytics", "Finance", "E-commerce"],
        "resources": [
            _resource("Kaggle Learn", "https://www.kaggle.com/learn", "Practice"),
            _resource("Scikit-learn User Guide", "https://scikit-learn.org/stable/user_guide.html", "Official documentation"),
            _resource("freeCodeCamp Data Analysis with Python", "https://www.freecodecamp.org/learn/data-analysis-with-python/", "Practice"),
            _resource("MIT Statistics Courses", "https://ocw.mit.edu/search/?q=statistics", "Open course"),
        ],
        "courses": [
            _course("IBM Data Science Professional Certificate", "https://www.coursera.org/professional-certificates/ibm-data-science", "Coursera"),
            _course("Machine Learning Specialization", "https://www.coursera.org/specializations/machine-learning-introduction", "Coursera"),
            _course("Data Analysis with Python", "https://www.freecodecamp.org/learn/data-analysis-with-python/", "freeCodeCamp"),
        ],
        "videos": [
            _video("Data Analysis with Python", "https://www.youtube.com/watch?v=r-uOLxNrNk8"),
            _video("SQL Tutorial for Beginners", "https://www.youtube.com/watch?v=HXV3zeQKqGY"),
            _video("Machine Learning for Everybody", "https://www.youtube.com/watch?v=i_LwzRVP7bg"),
        ],
    },
    "UI/UX Designer": {
        "roadmap_summary": "Learn design principles, user research, wireframing, prototyping, usability testing, and portfolio storytelling.",
        "required_skills": ["User research", "Wireframing", "Visual design", "Prototyping", "Usability testing"],
        "top_industries": ["Product design", "SaaS", "E-commerce", "Design agencies"],
        "resources": [
            _resource("Stanford d.school Resources", "https://dschool.stanford.edu/resources", "Design resource"),
            _resource("Google UX Design Certificate", "https://www.coursera.org/professional-certificates/google-ux-design", "Course"),
            _resource("edX Design Thinking", "https://www.edx.org/learn/design-thinking", "Course catalog"),
            _resource("Figma Learn", "https://help.figma.com/hc/en-us/categories/360002042553-Figma-design", "Official documentation"),
        ],
        "courses": [
            _course("Google UX Design Professional Certificate", "https://www.coursera.org/professional-certificates/google-ux-design", "Coursera"),
            _course("Design Thinking", "https://www.edx.org/learn/design-thinking", "edX"),
            _course("Design Thinking Bootleg", "https://dschool.stanford.edu/resources/design-thinking-bootleg", "Stanford"),
        ],
        "videos": [
            _video("UX Design Course for Beginners", "https://www.youtube.com/watch?v=55NvZjUZIO8"),
            _video("Figma UI Design Tutorial", "https://www.youtube.com/watch?v=FTFaQWZBqQ8"),
            _video("Design Thinking Workshop", "https://www.youtube.com/watch?v=_r0VX-aU_T8"),
        ],
    },
    "Cybersecurity Analyst": {
        "roadmap_summary": "Study networking, Linux, security fundamentals, threat detection, incident response, and hands-on labs.",
        "required_skills": ["Networking", "Linux", "Security fundamentals", "Threat analysis", "Incident response"],
        "top_industries": ["Cybersecurity", "Banking", "Cloud infrastructure", "Government"],
        "resources": [
            _resource("Microsoft Learn Security", "https://learn.microsoft.com/en-us/security/", "Official documentation"),
            _resource("MIT Computer Systems Security", "https://ocw.mit.edu/courses/6-858-computer-systems-security-fall-2014/", "Open course"),
            _resource("Google Cybersecurity Certificate", "https://www.coursera.org/professional-certificates/google-cybersecurity", "Course"),
            _resource("edX Cybersecurity", "https://www.edx.org/learn/cybersecurity", "Course catalog"),
        ],
        "courses": [
            _course("Google Cybersecurity Professional Certificate", "https://www.coursera.org/professional-certificates/google-cybersecurity", "Coursera"),
            _course("Computer Systems Security", "https://ocw.mit.edu/courses/6-858-computer-systems-security-fall-2014/", "MIT OpenCourseWare"),
            _course("Microsoft Security Learning Paths", "https://learn.microsoft.com/en-us/training/browse/?products=security", "Microsoft Learn"),
        ],
        "videos": [
            _video("Cybersecurity Full Course", "https://www.youtube.com/watch?v=U_P23SqJaDc"),
            _video("Computer Networking Full Course", "https://www.youtube.com/watch?v=qiQR5rTSshw"),
            _video("Linux for Beginners", "https://www.youtube.com/watch?v=sWbUDq4S6Y8"),
        ],
    },
    "Business Operations Manager": {
        "roadmap_summary": "Build process mapping, project planning, analytics, stakeholder communication, and operations improvement habits.",
        "required_skills": ["Operations strategy", "Project management", "Process improvement", "Excel", "Communication"],
        "top_industries": ["Consulting", "SaaS operations", "Retail", "Manufacturing"],
        "resources": [
            _resource("Coursera Business", "https://www.coursera.org/browse/business", "Course catalog"),
            _resource("edX Business Management", "https://www.edx.org/learn/business-management", "Course catalog"),
            _resource("Microsoft Learn Excel", "https://support.microsoft.com/en-us/excel", "Official documentation"),
        ],
        "courses": [
            _course("Business Foundations", "https://www.coursera.org/specializations/wharton-business-foundations", "Coursera"),
            _course("Project Management", "https://www.coursera.org/professional-certificates/google-project-management", "Google Career Certificates"),
            _course("Supply Chain Fundamentals", "https://www.edx.org/learn/supply-chain-management", "edX"),
        ],
        "videos": [
            _video("Project Management Full Course", "https://www.youtube.com/watch?v=ZKOL-rZ79gs"),
            _video("Excel Tutorial for Beginners", "https://www.youtube.com/watch?v=Vl0H-qTclOg"),
        ],
    },
    "Startup Founder": {
        "roadmap_summary": "Validate a problem, define users, build a lean prototype, test acquisition, and learn startup finance basics.",
        "required_skills": ["Customer discovery", "Product strategy", "Pitching", "Financial modeling", "Experimentation"],
        "top_industries": ["Startups", "Venture studios", "Product innovation", "Digital commerce"],
        "resources": [
            _resource("Stanford eCorner", "https://ecorner.stanford.edu/", "Stanford"),
            _resource("Coursera Entrepreneurship", "https://www.coursera.org/browse/business/entrepreneurship", "Course catalog"),
            _resource("edX Entrepreneurship", "https://www.edx.org/learn/entrepreneurship", "Course catalog"),
        ],
        "courses": [
            _course("Entrepreneurship Specialization", "https://www.coursera.org/specializations/wharton-entrepreneurship", "Coursera"),
            _course("Technology Entrepreneurship", "https://online.stanford.edu/courses/soe-y0001-technology-entrepreneurship", "Stanford Online"),
            _course("Entrepreneurship in Emerging Economies", "https://www.edx.org/learn/entrepreneurship/harvard-university-entrepreneurship-in-emerging-economies", "edX"),
        ],
        "videos": [
            _video("Startup Funding Explained", "https://www.youtube.com/watch?v=677ZtSMr4-4"),
            _video("How to Start a Startup", "https://www.youtube.com/watch?v=CBYhVcO4WgI"),
        ],
    },
    "Environmental Scientist": {
        "roadmap_summary": "Study ecology, climate systems, GIS/data analysis, field methods, reporting, and environmental policy basics.",
        "required_skills": ["Environmental science", "Data analysis", "Field research", "GIS basics", "Scientific writing"],
        "top_industries": ["Sustainability", "Environmental consulting", "Public policy", "Research"],
        "resources": [
            _resource("MIT Environmental Courses", "https://ocw.mit.edu/search/?d=Earth%2C%20Atmospheric%2C%20and%20Planetary%20Sciences", "Open course"),
            _resource("edX Environmental Science", "https://www.edx.org/learn/environmental-science", "Course catalog"),
            _resource("Coursera Environmental Science", "https://www.coursera.org/courses?query=environmental%20science", "Course catalog"),
        ],
        "courses": [
            _course("Climate Change and Health", "https://www.coursera.org/learn/climate-change-health", "Coursera"),
            _course("Environmental Science", "https://www.edx.org/learn/environmental-science", "edX"),
            _course("MIT Climate Science", "https://ocw.mit.edu/search/?q=climate", "MIT OpenCourseWare"),
        ],
        "videos": [
            _video("Climate Science Course", "https://www.youtube.com/watch?v=ifrHogDujXw"),
            _video("GIS Full Course", "https://www.youtube.com/watch?v=19QG6fH87h4"),
        ],
    },
    "Financial Analyst": {
        "roadmap_summary": "Build accounting, Excel, valuation, financial modeling, market analysis, and clear reporting skills.",
        "required_skills": ["Accounting basics", "Excel", "Financial modeling", "Valuation", "Business analysis"],
        "top_industries": ["Banking", "Corporate finance", "Investment research", "Fintech"],
        "resources": [
            _resource("Coursera Finance", "https://www.coursera.org/browse/business/finance", "Course catalog"),
            _resource("edX Finance", "https://www.edx.org/learn/finance", "Course catalog"),
            _resource("Microsoft Excel Help", "https://support.microsoft.com/en-us/excel", "Official documentation"),
        ],
        "courses": [
            _course("Introduction to Corporate Finance", "https://www.coursera.org/learn/wharton-finance", "Coursera"),
            _course("Finance Essentials", "https://www.edx.org/learn/finance", "edX"),
            _course("Excel for Business", "https://www.coursera.org/specializations/excel", "Coursera"),
        ],
        "videos": [
            _video("Financial Modeling Tutorial", "https://www.youtube.com/watch?v=9F99I3jC1b4"),
            _video("Excel for Finance", "https://www.youtube.com/watch?v=OOWAk2aLEfk"),
        ],
    },
    "Healthcare Professional": {
        "roadmap_summary": "Strengthen biology fundamentals, patient communication, health systems knowledge, ethics, and role-specific certifications.",
        "required_skills": ["Biology basics", "Patient communication", "Ethics", "Clinical reasoning", "Documentation"],
        "top_industries": ["Hospitals", "Public health", "Health tech", "Clinical operations"],
        "resources": [
            _resource("Coursera Health", "https://www.coursera.org/browse/health", "Course catalog"),
            _resource("edX Healthcare", "https://www.edx.org/learn/healthcare", "Course catalog"),
            _resource("Harvard Online Health", "https://pll.harvard.edu/subject/health-medicine", "Harvard"),
        ],
        "courses": [
            _course("Anatomy Specialization", "https://www.coursera.org/specializations/anatomy", "Coursera"),
            _course("Introduction to Healthcare", "https://www.edx.org/learn/healthcare", "edX"),
            _course("Public Health Courses", "https://pll.harvard.edu/subject/public-health", "Harvard"),
        ],
        "videos": [
            _video("Anatomy and Physiology", "https://www.youtube.com/watch?v=uBGl2BujkPQ"),
            _video("Public Health Full Course", "https://www.youtube.com/watch?v=ig2cnOLFBR4"),
        ],
    },
    "Corporate Lawyer": {
        "roadmap_summary": "Build legal reasoning, contract basics, research, writing, negotiation, and policy awareness.",
        "required_skills": ["Legal research", "Contract reading", "Writing", "Reasoning", "Negotiation"],
        "top_industries": ["Corporate law", "Compliance", "Policy", "Legal operations"],
        "resources": [
            _resource("Harvard Law Online Courses", "https://pll.harvard.edu/subject/law", "Harvard"),
            _resource("Coursera Law", "https://www.coursera.org/browse/social-sciences/law", "Course catalog"),
            _resource("edX Law", "https://www.edx.org/learn/law", "Course catalog"),
        ],
        "courses": [
            _course("Contract Law", "https://www.edx.org/learn/law/harvard-university-contract-law-from-trust-to-promise-to-contract", "edX"),
            _course("American Contract Law", "https://www.coursera.org/learn/contracts-1", "Coursera"),
            _course("Justice", "https://pll.harvard.edu/course/justice", "Harvard"),
        ],
        "videos": [
            _video("Harvard Justice Lecture", "https://www.youtube.com/watch?v=kBdfcR-8hEY"),
            _video("Contract Law Basics", "https://www.youtube.com/watch?v=7vN_PEmeKb0"),
        ],
    },
    "Communication Specialist": {
        "roadmap_summary": "Practice audience research, writing, presentation, content strategy, analytics, and campaign planning.",
        "required_skills": ["Writing", "Presentation", "Audience research", "Content strategy", "Analytics"],
        "top_industries": ["Marketing", "Public relations", "Media", "Corporate communications"],
        "resources": [
            _resource("Coursera Communication", "https://www.coursera.org/courses?query=communication", "Course catalog"),
            _resource("edX Communication", "https://www.edx.org/learn/communication", "Course catalog"),
            _resource("Google Digital Garage", "https://learndigital.withgoogle.com/digitalgarage", "Google"),
        ],
        "courses": [
            _course("Successful Presentation", "https://www.coursera.org/learn/presentation-skills", "Coursera"),
            _course("Digital Marketing", "https://learndigital.withgoogle.com/digitalgarage/course/digital-marketing", "Google"),
            _course("Marketing Analytics", "https://www.coursera.org/learn/uva-darden-market-analytics", "Coursera"),
        ],
        "videos": [
            _video("Public Speaking Tutorial", "https://www.youtube.com/watch?v=tShavGuo0_E"),
            _video("Digital Marketing Course", "https://www.youtube.com/watch?v=nU-IIXBWlS4"),
        ],
    },
    "Counselor": {
        "roadmap_summary": "Study psychology foundations, active listening, ethics, case documentation, and supervised helping skills.",
        "required_skills": ["Active listening", "Psychology basics", "Ethics", "Empathy", "Case documentation"],
        "top_industries": ["Mental health", "Education", "Community services", "Employee wellbeing"],
        "resources": [
            _resource("Coursera Psychology", "https://www.coursera.org/browse/social-sciences/psychology", "Course catalog"),
            _resource("edX Psychology", "https://www.edx.org/learn/psychology", "Course catalog"),
            _resource("Harvard Psychology Courses", "https://pll.harvard.edu/subject/psychology", "Harvard"),
        ],
        "courses": [
            _course("Introduction to Psychology", "https://www.coursera.org/learn/introduction-psychology", "Coursera"),
            _course("The Science of Well-Being", "https://www.coursera.org/learn/the-science-of-well-being", "Coursera"),
            _course("Psychology Courses", "https://www.edx.org/learn/psychology", "edX"),
        ],
        "videos": [
            _video("Psychology Full Course", "https://www.youtube.com/watch?v=vo4pMVb0R6M"),
            _video("Active Listening Skills", "https://www.youtube.com/watch?v=rzsVh8YwZEQ"),
        ],
    },
    "Research Scientist": {
        "roadmap_summary": "Develop scientific reasoning, literature review, experimental design, data analysis, and publication-quality writing.",
        "required_skills": ["Research methods", "Statistics", "Experimental design", "Scientific writing", "Data analysis"],
        "top_industries": ["R&D", "Biotech", "Academia", "Applied research"],
        "resources": [
            _resource("MIT Research Courses", "https://ocw.mit.edu/search/?q=research", "Open course"),
            _resource("Coursera Research Methods", "https://www.coursera.org/courses?query=research%20methods", "Course catalog"),
            _resource("edX Science", "https://www.edx.org/learn/science", "Course catalog"),
        ],
        "courses": [
            _course("Understanding Research Methods", "https://www.coursera.org/learn/research-methods", "Coursera"),
            _course("Statistics and R", "https://www.edx.org/learn/statistics", "edX"),
            _course("MIT Biology", "https://ocw.mit.edu/search/?d=Biology", "MIT OpenCourseWare"),
        ],
        "videos": [
            _video("Research Methods", "https://www.youtube.com/watch?v=PDjS20kic54"),
            _video("Statistics Full Course", "https://www.youtube.com/watch?v=xxpc-HPKN28"),
        ],
    },
    "Fitness Coach": {
        "roadmap_summary": "Learn anatomy, exercise programming, coaching communication, safety, nutrition basics, and client progress tracking.",
        "required_skills": ["Exercise science", "Anatomy", "Coaching", "Program design", "Safety"],
        "top_industries": ["Fitness centers", "Sports performance", "Wellness", "Rehabilitation support"],
        "resources": [
            _resource("Coursera Fitness", "https://www.coursera.org/courses?query=fitness", "Course catalog"),
            _resource("edX Nutrition and Wellness", "https://www.edx.org/learn/nutrition", "Course catalog"),
            _resource("Harvard Health Courses", "https://pll.harvard.edu/subject/health-medicine", "Harvard"),
        ],
        "courses": [
            _course("Science of Exercise", "https://www.coursera.org/learn/science-exercise", "Coursera"),
            _course("Stanford Introduction to Food and Health", "https://www.coursera.org/learn/food-and-health", "Coursera"),
            _course("Nutrition Courses", "https://www.edx.org/learn/nutrition", "edX"),
        ],
        "videos": [
            _video("Exercise Science", "https://www.youtube.com/watch?v=8COaMKbNrX0"),
            _video("Anatomy and Physiology", "https://www.youtube.com/watch?v=uBGl2BujkPQ"),
        ],
    },
    "Educator": {
        "roadmap_summary": "Practice learning design, explanation, classroom communication, assessment design, and inclusive teaching methods.",
        "required_skills": ["Instructional design", "Communication", "Assessment", "Patience", "Curriculum planning"],
        "top_industries": ["Schools", "Edtech", "Corporate training", "Tutoring"],
        "resources": [
            _resource("Coursera Education", "https://www.coursera.org/browse/education", "Course catalog"),
            _resource("edX Education", "https://www.edx.org/learn/education", "Course catalog"),
            _resource("Harvard Teaching Courses", "https://pll.harvard.edu/subject/education-teaching", "Harvard"),
        ],
        "courses": [
            _course("Foundations of Teaching for Learning", "https://www.coursera.org/specializations/teaching", "Coursera"),
            _course("Leaders of Learning", "https://www.edx.org/learn/education/harvard-university-leaders-of-learning", "edX"),
            _course("Instructional Design", "https://www.coursera.org/specializations/instructional-design", "Coursera"),
        ],
        "videos": [
            _video("Learning How to Learn", "https://www.youtube.com/watch?v=O96fE1E-rf8"),
            _video("Instructional Design Basics", "https://www.youtube.com/watch?v=dW2UJ3H4eHw"),
        ],
    },
    "Content Writer": {
        "roadmap_summary": "Build writing clarity, editing, audience research, SEO basics, content strategy, and a portfolio of published samples.",
        "required_skills": ["Writing", "Editing", "Research", "SEO basics", "Content strategy"],
        "top_industries": ["Content marketing", "Publishing", "SaaS", "Media"],
        "resources": [
            _resource("Coursera Writing", "https://www.coursera.org/courses?query=writing", "Course catalog"),
            _resource("edX Writing", "https://www.edx.org/learn/writing", "Course catalog"),
            _resource("Harvard Writing Courses", "https://pll.harvard.edu/subject/writing", "Harvard"),
        ],
        "courses": [
            _course("Good with Words", "https://www.coursera.org/specializations/good-with-words", "Coursera"),
            _course("Rhetoric: The Art of Persuasive Writing", "https://www.edx.org/learn/rhetoric/harvard-university-rhetoric-the-art-of-persuasive-writing-and-public-speaking", "edX"),
            _course("English for Career Development", "https://www.coursera.org/learn/careerdevelopment", "Coursera"),
        ],
        "videos": [
            _video("Academic Writing", "https://www.youtube.com/watch?v=GgkRoYPLhts"),
            _video("SEO for Beginners", "https://www.youtube.com/watch?v=DvwS7cV9GmQ"),
        ],
    },
}


def youtube_embed_url(url):
    parsed = urlparse(url)
    video_id = ""
    if parsed.netloc.endswith("youtu.be"):
        video_id = parsed.path.lstrip("/")
    elif "youtube.com" in parsed.netloc:
        if parsed.path == "/watch":
            video_id = parse_qs(parsed.query).get("v", [""])[0]
        elif parsed.path.startswith("/embed/"):
            return url

    if not video_id:
        return url
    return f"https://www.youtube.com/embed/{video_id}"


CAREER_ALIASES = {
    "Data Analyst": "Data Scientist",
    "UX Designer": "UI/UX Designer",
}


def get_career_resource(career_name):
    normalized_name = CAREER_ALIASES.get(career_name, career_name)
    resource = deepcopy(CAREER_RESOURCES.get(normalized_name, CAREER_RESOURCES["Software Engineer"]))
    for video in resource["videos"]:
        video["embed_url"] = youtube_embed_url(video["youtube_url"])
    return resource
