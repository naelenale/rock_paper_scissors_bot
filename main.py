import os
import random

import telebot
from telebot import types
from dotenv import load_dotenv

load_dotenv()


app = telebot.TeleBot(os.environ.get('TG_KEY'))

CHOICES = ['rock', 'paper', 'scissors']
RESULTS = dict()

def rock_scissors_paper(array: list[str]) -> str:
  return random.choice(array)

def init_keyboard() -> types.ReplyKeyboardMarkup:
  keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
  button_1 = types.KeyboardButton('rock')
  button_2 = types.KeyboardButton ('paper')
  button_3 = types.KeyboardButton('scissors')
  back = types.KeyboardButton('/back')
  keyboard.add(button_1, button_2, button_3, back)
  return keyboard

def init_menu() -> types.ReplyKeyboardMarkup:
  menu = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
  play = types.KeyboardButton('/play')
  help = types.KeyboardButton('/help')
  results = types.KeyboardButton('/results')
  menu.add(play, help, results)
  return menu

@app.message_handler(commands=['results'])
def result(message: types.Message) -> None:
  user_result = RESULTS[message.chat.id]
  user_result_str = f"wins: {user_result['wins']} \nlosses: {user_result['losses']}\ndraws: {user_result['draws']}"
  keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
  back = types.KeyboardButton('/back')
  nullify = types.KeyboardButton('/nullify')
  keyboard.add(nullify, back)
  app.send_message(message.chat.id, user_result_str, reply_markup=keyboard)

@app.message_handler(commands=['nullify'])
def nullify_results(message: types.Message) -> None:
    RESULTS[message.chat.id] = {
        'wins': 0,
        'losses': 0,
        'draws': 0,
    }
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    back = types.KeyboardButton('/back')
    keyboard.add(back)
    app.send_message(message.chat.id, 'Your results were reset! Press /back to return.', reply_markup=keyboard)
  
@app.message_handler(commands=['help'])
def help(message: types.Message) -> None:
  keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
  back = types.KeyboardButton('/back')
  keyboard.add(back)
  app.send_message(message.chat.id, "To play the game, choose one of the options: rock, paper, or scissors. The bot will randomly select its move, and the winner is determined by classic rules: rock crushes scissors, scissors cuts paper, and paper covers rock. Click the corresponding button to make your choice.\nPress'/back' to return to the main menu and '/play' to start a new game. Use '/results' to view your wins, losses, and draws. You can reset your results by pressing the '/nullify' button.", reply_markup=keyboard)

@app.message_handler(commands=['play'])
def game_start(message: types.Message) -> None:
  keyboard = init_keyboard()
  app.send_message(message.chat.id, 'Make your move!', reply_markup=keyboard)

@app.message_handler(commands=['start'])
def send_menu(message: types.Message) -> None:
    if message.chat.id not in RESULTS:
        RESULTS[message.chat.id] = {
            'wins': 0,
            'losses': 0,
            'draws': 0,
        }
    menu = init_menu()
    app.send_message(message.chat.id, "Hello there, mighty player! Are you ready to test your skills in rock-paper-scissors? Press /play to start the game and let me have a chance to enjoy victory (or be defeated).", reply_markup=menu)

@app.message_handler(commands=['back'])
def send_menu_back(message: types.Message) -> None:
    menu = init_menu()
    app.send_message(message.chat.id, "Press /play to start.", reply_markup=menu)


@app.message_handler(func=lambda message: message.text.lower() in CHOICES)
def handle_message(message: types.Message) -> None:
  app.reply_to(message, random_answer := rock_scissors_paper(CHOICES))
  if message.text == random_answer:
    app.send_message(message.chat.id, "Draw! Looks like neither of us could cut it this time. Maybe next round we'll decide with a coin toss?")
    RESULTS[message.chat.id]['draws'] += 1
  elif message.text == CHOICES[0]:
    if random_answer == CHOICES[2]:
      app.send_message(message.chat.id, "Congratulations! You've won. Make your next move!")
      RESULTS[message.chat.id]['wins'] += 1
    else:
      app.send_message(message.chat.id, "Unfortunately, you've lost. I'm dissapointed in you. Try again to beat me!")
      RESULTS[message.chat.id]['losses'] += 1
  elif message.text == CHOICES[1]:
    if random_answer == CHOICES[0]:
      app.send_message(message.chat.id, "Congratulations! You've won. Make your next move!")
      RESULTS[message.chat.id]['wins'] += 1
    else:
      app.send_message(message.chat.id, "Unfortunately, you've lost. I'm dissapointed in you. Try again to beat me!")
      RESULTS[message.chat.id]['losses'] += 1
  elif message.text == CHOICES[2]:
    if random_answer == CHOICES[1]:
      app.send_message(message.chat.id, "Congratulations! You've won. Make your next move!")
      RESULTS[message.chat.id]['wins'] += 1
    else:
      app.send_message(message.chat.id, "Unfortunately, you've lost. I'm dissapointed in you. Try again to beat me!")
      RESULTS[message.chat.id]['losses'] += 1



if __name__ == '__main__':
  app.polling(none_stop=True)