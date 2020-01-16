import requests
from telebot import TeleBot


bot = TeleBot("692339912:AAHPGScMMq1LCYaMatbvCwsGrdJIIoWemXg")


def beautify_output(obj: dict):
    return '\n'.join(f'{key}: {obj[key]}' for key in obj)


@bot.message_handler(commands=["start", "help"])
def intro(message):
    bot.reply_to(message, 'This bot is created to assist in Task management.\n'
                          'Available commands: \n'
                          'for Users:'
                          '/users - gives a list of user names \n'
                          '/users id - gives individual user info by id \n'
                          '/add_user John Doe - adds user to Users list \n'
                          '/del_user id - deletes user with specific id'
                          '\n'
                          'for Dashboards:'
                          '/dashboards - gives a list of dashboards created \n'
                          '/dashboards id - gives specific dash info by id \n'
                          '/dashboard_tasks id - gives a list of tasks on '
                          'a certain dash by its id \n'
                          '\n'
                          'for Tasks:'
                          '/tasks id - gives task info by its id \n'
                          '/task_comments id - gives comments on a task with '
                          'given id')


@bot.message_handler(commands=["users"])
def get_users(message):
    try:
        id = message.text.split(' ')[1]
        user = requests.get(f"http://localhost:5000/users/{id}").json()
        bot.send_message(message.chat.id, beautify_output(user))
        return
    except IndexError:
        pass
    users = requests.get("http://localhost:5000/users").json()
    bot.send_message(message.chat.id, "\n".join(user["name"] for user in users))
    bot.send_message(message.chat.id, "Individual user info is available at:"
                                      " /users id")


@bot.message_handler(commands=["dashboards"])
def get_dashes(message):
    try:
        id = message.text.split(' ')[1]
        user = requests.get(f"http://localhost:5000/dashboards/{id}").json()
        bot.send_message(message.chat.id, beautify_output(user))
        bot.send_message(message.chat.id, "Certain dash's tasks are available "
                                          "at: /dashboard_tasks id")
        return
    except IndexError:
        pass
    users = requests.get("http://localhost:5000/dashboards").json()
    bot.send_message(message.chat.id, "\n".join(user["name"] for user in users))
    bot.send_message(message.chat.id, "Individual dash info is available at "
                                      "/dashboards id")


@bot.message_handler(commands=["dashboard_tasks"])
def get_tasks(message):
    id = message.text.split(' ')[1]
    tasks = requests.get(f"http://localhost:5000/dashboards/{id}/tasks").json()
    bot.send_message(message.chat.id,
                     "\n".join(f'{task["id"]}. {task["name"]}' for task in tasks)
                     )
    bot.send_message(message.chat.id, "Individual task info is available at"
                                      "/tasks id")


@bot.message_handler(commands=["tasks"])
def get_task(message):
    id = message.text.split(' ')[1]
    task = requests.get(f'http://localhost:5000/tasks/{id}').json()
    bot.send_message(message.chat.id, beautify_output(task))
    bot.send_message(message.chat.id, "Type /task_comments id for comments on"
                                      "specific task.")


@bot.message_handler(commands=["task_comments"])
def get_comments(message):
    id = message.text.split(' ')[1]
    comms = requests.get(f'http://localhost:5000/tasks/{id}/comments').json()
    bot.send_message(message.chat.id, "\n".join(
        f'user {com["user id"]}: {com["body"]}' for com in comms)
    )


@bot.message_handler(commands=["add_user"])
def add_user(message):
    name = " ".join(message.text.split(' ')[1:])
    requests.post("http://localhost:5000/users", json={'name': name})
    bot.send_message(message.chat.id, f"{name} was added to the names list.")


@bot.message_handler(commands=["del_user"])
def delete_user(message):
    id = message.text.split(' ')[1]
    requests.delete(f"http://localhost:5000/users/{id}")
    bot.send_message(message.chat.id, f"{id} user was deleted.")


if __name__ == "__main__":
    bot.polling()