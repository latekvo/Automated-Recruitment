from colorama import Fore, Style
from core.database import (
    add_application,
    add_personal_data,
    add_recruitment,
    add_submission,
    add_task,
    get_best_applicants,
    init_db,
)
import core.evaluator as evaluator

init_db()

recruitment = add_recruitment("Medium software engineer", "Acme")

task_leadership = add_task(
    recruitment,
    "Can you tell me about a time when you demonstrated leadership skills?",
)
task_deadlines = add_task(
    recruitment, "How do you handle stressful situations and tight deadlines?"
)
task_achievement = add_task(
    recruitment,
    "What do you consider your greatest achievement?",
)
task_coworker = add_task(
    recruitment,
    "Describe a situation where you had to work with a difficult team member.",
)

video_dir = "../static/"

arthur_powell = add_personal_data("Arthur Powell")
application_ap = add_application(recruitment, arthur_powell)
add_submission(application_ap, task_leadership, video_dir + "bad_01_leadership.mp3")
add_submission(application_ap, task_deadlines, video_dir + "bad_02_deadlines.mp3")
add_submission(application_ap, task_achievement, video_dir + "bad_03_achievement.mp3")
add_submission(application_ap, task_coworker, video_dir + "bad_04_coworker.mp3")

jonathan_max = add_personal_data("Jonathan Max")
application_jm = add_application(recruitment, jonathan_max)
add_submission(application_jm, task_leadership, video_dir + "great_01_leadership.mp3")
add_submission(application_jm, task_deadlines, video_dir + "great_02_deadlines.mp3")
add_submission(application_jm, task_achievement, video_dir + "great_03_achievement.mp3")
add_submission(application_jm, task_coworker, video_dir + "great_04_coworker.mp3")


evaluator.evaluate_application(application_ap, recruitment)
evaluator.evaluate_application(application_jm, recruitment)

best_applicants = get_best_applicants(recruitment)

for applicant in best_applicants:
    print(
        f"{Style.BRIGHT}{Fore.CYAN}Score: {round(applicant.score*100, 2)}%{Style.NORMAL}, name: {applicant.full_name}"
    )
