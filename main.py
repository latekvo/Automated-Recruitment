from colorama import Fore, Style
from database import (
    add_application,
    add_personal_data,
    add_recruitment,
    add_submission,
    add_task,
    init_db,
)
import evaluator

init_db()

recruitment = add_recruitment("Medium software engineer", "Acme")

task_experience = add_task(
    recruitment,
    "Tell me about your experience with working with clients, what's the most important thing in that field?",
)
task_good = add_task(
    recruitment, "What makes you a good candidate for software engineer position?"
)
task_challenge = add_task(
    recruitment,
    "Tell me about a challenging situation at work or your project, and how you dealt with it.",
)
task_accomplish = add_task(
    recruitment, "Are there any acomplishments you'd like to tell us about?"
)

application_ap = add_application(recruitment)
add_personal_data(application_ap, "Arthur Powell")
add_submission(application_ap, task_experience)
add_submission(application_ap, task_good)
add_submission(application_ap, task_challenge)
add_submission(application_ap, task_accomplish)

summary, score = evaluator.evaluate_application(application_ap)

# normal to see negatives if the AI thinks the interview is abhorrent
print(
    f"{Fore.CYAN}{Style.BRIGHT}normalized score: ",
    score * 100,
    f"%{Style.RESET_ALL}",
    sep=None,
)
print(f"{Fore.CYAN}summary:", summary)
