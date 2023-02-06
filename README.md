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
  - have slack_bolt hello world
  - slack_bolt can use "socket mode" to talk to slack, which seems good for us although it's documented as "not for production"
  - in socket mode, slack_bolt just starts some threads and does everything in those threads, so it should be able to live side by side peacefully with Django
  - (in regular mode it's a wsgi app so we can just register it under a subpath, but this requires ngrok for dev and I'd rather develop in socket mode)
  - all that's left to do is implement the machinery for howdy.py in terms of bolt_tutorial.py
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
