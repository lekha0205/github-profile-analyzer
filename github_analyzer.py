import requests


def get_github_data(username):
    headers = {
        "Accept": "application/vnd.github+json"
    }

    profile_url = f"https://api.github.com/users/{username}"

    profile_response = requests.get(
        profile_url,
        headers=headers,
        timeout=10
    )

    if profile_response.status_code != 200:
        return None, None

    profile = profile_response.json()

    repos_url = f"https://api.github.com/users/{username}/repos"

    response = requests.get(
        repos_url,
        headers=headers,
        params={"per_page": 100, "sort": "updated"},
        timeout=10
    )

    if response.status_code != 200:
        return profile, None

    return profile, response.json()


def analyze_repositories(repositories):
    total_stars = 0
    total_forks = 0
    languages = {}

    for repo in repositories:
        total_stars += repo.get("stargazers_count", 0)
        total_forks += repo.get("forks_count", 0)

        language = repo.get("language")

        if language:
            languages[language] = languages.get(language, 0) + 1

    if languages:
        top_language = max(languages, key=languages.get)
    else:
        top_language = "None"

    return total_stars, total_forks, languages, top_language


def calculate_score(profile, repositories, stars, forks):
    follower_score = min(profile.get("followers", 0), 25)
    repository_score = min(len(repositories) * 2, 25)
    star_score = min(stars, 30)
    fork_score = min(forks * 2, 20)

    return (
        follower_score
        + repository_score
        + star_score
        + fork_score
    )


def get_rating(score):
    if score >= 80:
        return "Excellent"
    elif score >= 60:
        return "Good"
    elif score >= 40:
        return "Average"
    else:
        return "Needs Improvement"


def generate_suggestions(
    profile,
    repositories,
    stars,
    forks,
    languages
):
    suggestions = []

    if profile.get("followers", 0) < 10:
        suggestions.append(
            "Increase followers by contributing to open-source projects."
        )

    if len(repositories) < 5:
        suggestions.append(
            "Create more quality projects to showcase your skills."
        )

    if stars < 10:
        suggestions.append(
            "Build useful projects and share them with the developer community."
        )

    if forks < 5:
        suggestions.append(
            "Create reusable projects that other developers can contribute to."
        )

    if len(languages) <= 1:
        suggestions.append(
            "Try learning and using another programming language."
        )

    if profile.get("following", 0) == 0:
        suggestions.append(
            "Follow developers and interesting open-source projects."
        )

    if not suggestions:
        suggestions.append(
            "Excellent profile! Keep contributing and maintaining your projects."
        )

    return suggestions


def analyze_profile(profile, repositories):
    stars, forks, languages, top_language = (
        analyze_repositories(repositories)
    )

    score = calculate_score(
        profile,
        repositories,
        stars,
        forks
    )

    rating = get_rating(score)

    suggestions = generate_suggestions(
        profile,
        repositories,
        stars,
        forks,
        languages
    )

    top_repositories = sorted(
        repositories,
        key=lambda repo: repo.get("stargazers_count", 0),
        reverse=True
    )[:5]

    return {
        "total_repositories": len(repositories),
        "total_stars": stars,
        "total_forks": forks,
        "languages": languages,
        "top_language": top_language,
        "score": score,
        "rating": rating,
        "suggestions": suggestions,
        "top_repositories": top_repositories
    }
