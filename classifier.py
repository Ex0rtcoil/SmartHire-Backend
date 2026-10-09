import re

SKILLS = [
    "Python", "Java", "JavaScript", "HTML", "CSS",
    "SQL", "C++", "C#", "Pandas", "Excel",
    "Tableau", "Power BI", "Git", "Flask",
    "React", "Django", "Machine Learning",
    "Communication", "Project Management",
    "Testing", "Selenium", "Linux"
]

ROLE_SKILLS = {
    "Data Analyst": [
        "Python", "SQL", "Pandas", "Excel",
        "Tableau", "Power BI"
    ],
    "Junior Developer": [
        "Python", "Java", "JavaScript", "HTML",
        "CSS", "C++", "C#", "Git", "Flask",
        "React", "Django"
    ],
    "QA Tester": [
        "Testing", "Selenium", "Python", "Java", "Git"
    ],
    "Machine Learning Engineer": [
        "Python", "Pandas", "Machine Learning", "SQL"
    ]
}


def classify_resume(text):
    # Find skills mentioned in the resume.
    found_skills = [
        skill for skill in SKILLS
        if re.search(
            r"(?<!\w)" + re.escape(skill) + r"(?!\w)",
            text,
            re.IGNORECASE
        )
    ]

    # Look for common education terms.
    education_terms = [
        "BS Computer Science",
        "Bachelor of Science in Computer Science",
        "Computer Engineering",
        "Information Technology",
        "Information Systems"
    ]

    education = [
        term for term in education_terms
        if term.lower() in text.lower()
    ]

    # Estimate experience from phrases such as "2 years of experience".
    match = re.search(
        r"(\d+(?:\.\d+)?)\+?\s+years?\s+of\s+experience",
        text,
        re.IGNORECASE
    )
    experience = float(match.group(1)) if match else 0

    # Score each role according to matching skills.
    recommended_roles = []

    for role, required_skills in ROLE_SKILLS.items():
        matched = [
            skill for skill in required_skills
            if skill.lower() in [s.lower() for s in found_skills]
        ]

        missing = [
            skill for skill in required_skills
            if skill.lower() not in [s.lower() for s in found_skills]
        ]

        score = round(100 * len(matched) / len(required_skills))

        recommended_roles.append({
            "title": role,
            "fit_score": score,
            "reasons": (
                ["Matching skills: " + ", ".join(matched)]
                if matched else
                ["No matching listed skills were detected"]
            ),
            "gaps": (
                ["Skills not detected: " + ", ".join(missing)]
                if missing else []
            )
        })

    recommended_roles.sort(
        key=lambda role: role["fit_score"],
        reverse=True
    )

    return {
        "candidate_summary": (
            "Resume analyzed using keyword-based matching. "
            "Results depend on the text extracted from the document."
        ),
        "skills": found_skills,
        "education": education,
        "experience_years": experience,
        "recommended_roles": recommended_roles
    }