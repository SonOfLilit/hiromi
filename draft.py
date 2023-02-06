"""
- /room command handler
- /schedule command handler
- task - schedule
- weekly task - summary (w/ button handler)
- dashboard
- admin
"""

from django import models

import hiromi.models
from hiromi.commands import command, message, require_staff
from hiromi.rooms import Room, bot_user
from hiromi.tasks import Schedule, Task

# models

# not this, the next one instead
class MentoringRoom(hiromi.models.Room):
    pass


# this


class MentoringRoomParticipant(hiromi.models.RoomParticipant):
    # from super(): room = models.ForeignKey(hiromi.models.Room)
    # from super(): participant = models.ForeignKey(hiromi.models.User)
    BOT = "Bot"
    OBSERVER = "Observer"
    MENTOR = "Mentor"
    MENTEE = "Mentee"
    CHOICES = [BOT, OBSERVER, MENTOR, MENTEE]
    CHOICES = list(zip(CHOICES, CHOICES))
    role = models.CharField(max_length=255, choices=CHOICES)


class MentoringMessage(models.Model):
    room_id = models.ForeignKey(MentoringRoom)
    user_id = models.ForeignKey(hiromi.models.User)
    timestamp = models.DateTime(autoadd=True)
    text = models.TextField()
    other_content = models.JsonField()


# hiromi also gives us Room, Task, Schedule, Message, ... for free

# tasks

# this is empty of content, but it gives us a nice type to filter the admin by
class MentoringSchedule(hiromi.models.Schedule):
    pass


class UsersScheduleWeeklyMeetingTask(hiromi.tasks.RoomTask):
    reminders = Schedule.daily

    def run(self):
        self.room.send(
            "Hi! This is how the mentoring program works: ....\n\nPlease choose a weekly meeting time slot and add it to your calendars. Then tell me about it with the command `/schedule Tuesday 16:15`"
        )

    def remind(self):
        self.room.send(
            "This is a reminder to schedule a weekly meeting and tell me with the command `/schedule Tuesday 16:15`"
        )


class WeeklyMeetingReminderTask(hiromi.tasks.RoomTask):
    def run(self):
        self.room.send(
            "Your meeting starts in 10 min. At the end of the meeting please send (as a normal message) a short summary of non-personal things you covered and click here:",
            buttons=[
                ("We sent a summary", self.handle_sent)
            ],  # TODO: something with private keys to ensure client can't call arbitrary server functions
        )

    def handle_sent(self):
        self.done = True
        self.save()
        self.room.send("Thank you, see you next week!")

    def remind(self):
        self.room.send(
            "This is a reminder to send a short summary of non-personal things you covered and click here:",
            buttons=[
                ("We sent a summary", self.handle_sent)
            ],  # TODO: something with private keys to ensure client can't call arbitrary server functions
        )


# commands


@command("room <user:mentee> <user:mentor> <*user:more_users>")
@require_staff
def create_mentoring_room(command, mentee, mentor, *more_users):
    name = f"{mentee.username}-{mentor.username}"
    mentoring_room = Room.create(name=name, private=True)
    MentoringRoomParticipant.objects.create(
        room=mentoring_room, participant=bot_user, role=MentoringRoomParticipant.BOT
    )
    MentoringRoomParticipant.objects.create(
        room=mentoring_room, participant=mentee, role=MentoringRoomParticipant.MENTEE
    )
    MentoringRoomParticipant.objects.create(
        room=mentoring_room, participant=mentor, role=MentoringRoomParticipant.MENTOR
    )
    for user in more_users:
        MentoringRoomParticipant.objects.create(
            room=mentoring_room,
            participant=user,
            role=MentoringRoomParticipant.OBSERVER,
        )
    mentoring_room.commit()  # blocks until room is created and participants are added
    UsersScheduleWeeklyMeetingTask.objects.create(room=mentoring_room)


@command("schedule <weektime:weektime>")
def schedule(command, weektime):
    task = UsersScheduleWeeklyMeetingTask.objects.get(room=command.room)
    MentoringSchedule.objects.update_or_create(
        room=command.room,
        defaults=dict(
            type=Schedule.WEEKLY,
            weektime=weektime,
            run=schedule_weekly_meeting_reminder,
            params={"room_id": command.room.id},
        ),
    )
    task.done = True
    task.save()
    command.room.send(f"Alright, the meeting is scheduled for each week on {weektime}")


def schedule_weekly_meeting_reminder(room_id):
    WeeklyMeetingReminderTask.objects.create(room=room_id, reminders=Schedule.DAILY)


@message
def log_message(message):
    if isinstance(message.room, MentoringRoom):
        body = message.body
        del body["text"]
        MentoringMessage.objects.create(
            user=message.user, room=message.room, text=message.text, other_content=body
        )


# dashboard and admin are done the usual Django way - as views and django.contrib.admin
# hiromi gives us nice default admin configs for schedules, etc', that we can use or replace
