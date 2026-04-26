def get_ai_feedback(score):
    # Feature 6: Simulate hiring decisions
    if score > 75: return "✅ Shortlisted: Exceptional impact and engagement."
    if score > 45: return "⚠️ Maybe: Strong technical skills, needs more documentation."
    return "❌ Rejected: Profile lacks project depth."

def generate_7_day_plan(score):
    # Feature 7: AI-driven improvement roadmap
    if score < 50:
        return ["Day 1-2: Add READMEs to top 3 repos", "Day 3-5: Push 1 new full-stack project", "Day 6-7: Optimize GitHub Bio"]
    return ["Day 1-3: Contribute to 2 Open Source repos", "Day 4-6: Create a personal portfolio site", "Day 7: Get code reviews"]

def generate_readme_template(repo_name, user):
    # Feature 10: AI README Generator
    return f"# {repo_name}\nCreated by @{user}\n\n## Overview\nAuto-analyzed by CampusConnect AI."