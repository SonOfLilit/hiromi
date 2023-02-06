# Hiromi - A Django framework for team chat bots

# Contributing

Before making commits, make sure to install `pre-commit` so that `black` auto-formatting will run as a pre-commit hook:

```
poetry run pre-commit install
```

Also, make sure to run tests before every commit:

```
poetry run pytest
```

## Plan

- Slack hello-world (handle command that sends message)
- Discord hello-world
- Commands
- Tasks
- Scheduler
- Tasks with reminders until completed
- Room management API
- Messages with optional buttons
- Permissions
- Full mentorbot sample app
- Teams hello-world
- Handle webhooks
- Send webhooks
