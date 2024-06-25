from database import add_application, add_recruitment, add_submission, add_task, init_db
import evaluator

init_db()

recruitment = add_recruitment("Senior software engineer", "Acme")
print("recruitment", recruitment)

task = add_task(recruitment, "Tell me about your experience")
print("task", task)

application = add_application(recruitment)
print("application", application)

submission = add_submission(application, task)
print("submission", submission)


print("details", evaluator.get_submission_details_by_uuid(submission))
