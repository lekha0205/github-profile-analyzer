from flask import Flask, render_template, request
import requests

from github_analyzer import (
    get_github_data,
    analyze_profile
)


app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def home():

    profile = None
    analysis = None
    error = None
    username = ""

    if request.method == "POST":

        username = request.form.get(
            "username", ""
        ).strip()

        if not username:
            error = "Please enter a GitHub username."

        else:

            try:
                profile, repositories = get_github_data(
                    username
                )

                if profile is None:

                    error = (
                        "GitHub user not found. "
                        "Please check the username."
                    )

                elif repositories is None:

                    error = (
                        "Unable to fetch repository data."
                    )

                else:

                    analysis = analyze_profile(
                        profile,
                        repositories
                    )

            except requests.exceptions.Timeout:

                error = (
                    "GitHub request timed out. "
                    "Please try again."
                )

            except requests.exceptions.ConnectionError:

                error = (
                    "Unable to connect to GitHub. "
                    "Check your internet connection."
                )

            except requests.exceptions.RequestException:

                error = "GitHub API request failed."

            except Exception as e:

                error = f"Unexpected error: {e}"

    return render_template(
        "index.html",
        profile=profile,
        analysis=analysis,
        error=error,
        username=username
    )


if __name__ == "__main__":

    print("=" * 50)
    print("       GITHUB PROFILE ANALYZER")
    print("=" * 50)
    print("Starting Flask server...")
    print("Open: http://127.0.0.1:5000")
    print("=" * 50)

    app.run(debug=True, use_reloader=False)
