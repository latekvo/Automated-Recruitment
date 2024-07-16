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

recruitment_batch = add_recruitment("Medium software engineer", "Acme")

task_leadership = add_task(
    recruitment_batch,
    "Can you tell me about a time when you demonstrated leadership skills?",
)
task_deadlines = add_task(
    recruitment_batch, "How do you handle stressful situations and tight deadlines?"
)
task_achievement = add_task(
    recruitment_batch,
    "What do you consider your greatest achievement?",
)
task_coworker = add_task(
    recruitment_batch,
    "Describe a situation where you had to work with a difficult team member.",
)

video_dir = "./static/"

# POOR example
poor_applicant = add_personal_data("Test applicant [POOR]")
poor_application = add_application(recruitment_batch, poor_applicant)
add_submission(poor_application, task_leadership, video_dir + "bad_01_leadership.mp3")
add_submission(poor_application, task_deadlines, video_dir + "bad_02_deadlines.mp3")
add_submission(poor_application, task_achievement, video_dir + "bad_03_achievement.mp3")
add_submission(poor_application, task_coworker, video_dir + "bad_04_coworker.mp3")

# GREAT example
great_applicant = add_personal_data("Test applicant [GREAT]")
great_application = add_application(recruitment_batch, great_applicant)
add_submission(great_application, task_leadership, video_dir + "great_01_leadership.mp3")
add_submission(great_application, task_deadlines, video_dir + "great_02_deadlines.mp3")
add_submission(great_application, task_achievement, video_dir + "great_03_achievement.mp3")
add_submission(great_application, task_coworker, video_dir + "great_04_coworker.mp3")

# MIXED example
mixed_applicant = add_personal_data("Test applicant [MIXED]")
mixed_application = add_application(recruitment_batch, mixed_applicant)
add_submission(mixed_application, task_leadership, video_dir + "great_01_leadership.mp3")
add_submission(mixed_application, task_deadlines, video_dir + "bad_02_deadlines.mp3")
add_submission(mixed_application, task_achievement, video_dir + "great_03_achievement.mp3")
add_submission(mixed_application, task_coworker, video_dir + "bad_04_coworker.mp3")

evaluator.evaluate_application(poor_application, recruitment_batch)
evaluator.evaluate_application(great_application, recruitment_batch)
evaluator.evaluate_application(mixed_application, recruitment_batch)

best_applicants = get_best_applicants(recruitment_batch)

for applicant in best_applicants:
    print(
        f"{Style.BRIGHT}{Fore.CYAN}Score: {round(applicant.score*100, 2)}%{Style.NORMAL}, name: {applicant.full_name}, summary: {applicant.summary}"
    )

