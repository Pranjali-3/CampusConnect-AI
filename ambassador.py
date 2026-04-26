import pandas as pd

def get_ambassador_insights(db):
    if not db: return None
    df = pd.DataFrame(db)
    
    # Updated Points Engine: Base GitHub Score + Accumulated Task Points
    # We now use the 'task_points' column which we will update in app.py
    df['points'] = df['score'] + df['task_points'] 
    leaderboard = df.sort_values(by="points", ascending=False)
    
    avg_score = df['score'].mean()
    health = "Strong 💪" if avg_score > 70 else "Growing 🌱" if avg_score > 40 else "Weak ⚠️"
    
    return {
        "leaderboard": leaderboard,
        "avg": avg_score,
        "health": health,
        "needs_help": len(df[df['score'] < 40]),
        "rec": "Host a Hackathon" if avg_score > 60 else "Run a README/Documentation Workshop"
    }