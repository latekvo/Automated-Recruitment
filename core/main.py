from colorama import Fore, Style
from database import (
    add_application,
    add_personal_data,
    add_recruitment,
    add_submission,
    add_task,
    get_best_applicants,
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

arthur_powell = add_personal_data("Arthur Powell")
application_ap = add_application(recruitment, arthur_powell)
add_submission(application_ap, task_experience)
add_submission(application_ap, task_good)
add_submission(application_ap, task_challenge)
add_submission(application_ap, task_accomplish)

jonathan_max = add_personal_data("Jonathan Max")
application_jm = add_application(recruitment, jonathan_max)
add_submission(application_jm, task_experience)
add_submission(application_jm, task_good)
add_submission(application_jm, task_challenge)
add_submission(application_jm, task_accomplish)


evaluator.evaluate_application(application_ap, recruitment)
evaluator.evaluate_application(application_jm, recruitment)

best_applicants = get_best_applicants(recruitment)

for applicant in best_applicants:
    print(
        f"{Style.BRIGHT}{Fore.CYAN}Score: {round(applicant.score*100, 2)}%{Style.NORMAL}, name: {applicant.full_name}"
    )
