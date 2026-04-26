def analyze_profile(data):
    repos = data['repos']
    profile = data['profile']
    
    # Feature 2, 13, 23: Rule-Based AI Engine Logic
    stars = sum(r['stargazers_count'] for r in repos)
    forks = sum(r['forks_count'] for r in repos)
    repo_count = len(repos)
    
    # Feature 3: Intelligent Score Breakdown Categories
    pop_score = min(30, (stars * 5)) # Popularity
    repo_score = min(20, repo_count * 2) # Repository Quality
    has_desc = [r for r in repos if r['description']]
    doc_score = min(15, (len(has_desc) / repo_count * 15) if repo_count > 0 else 0)
    activity_score = 15 # Activity Level
    prof_score = 10 if profile.get('bio') else 5 # Profile Strength
    
    total_score = pop_score + repo_score + doc_score + activity_score + prof_score
    
    # Feature 5 & 8: Top Project and Auto-Fix Suggestions
    top_repo = max(repos, key=lambda x: x['stargazers_count']) if repos else None
    fix_suggestions = []
    if not profile.get('bio'): fix_suggestions.append("Add a professional Bio")
    if len(has_desc) < repo_count: fix_suggestions.append("Missing descriptions in some repos")
    
    # Feature 11: Language Distribution Data
    languages = {}
    for r in repos:
        lang = r.get('language')
        if lang: languages[lang] = languages.get(lang, 0) + 1

    return {
        "score": total_score,
        "ats": total_score * 0.92, # Feature 4: Recruiter-ready ATS score
        "breakdown": {"Popularity": pop_score, "Repos": repo_score, "Documentation": doc_score, "Activity": activity_score, "Profile": prof_score},
        "top_project": top_repo,
        "suggestions": fix_suggestions,
        "languages": languages,
        "benchmark": "🔥 Top-tier" if total_score > 80 else "👍 Good" if total_score > 50 else "⚠ Needs Work"
    }