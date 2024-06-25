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
print("submission", submission, end="\n\n")

summary, score = evaluator.evaluate_submission(submission)
print("summary:", summary)

# normal to see negatives if the AI thinks the interview is abhorrent
print("normalized score: ", score * 100, "%", sep=None)
