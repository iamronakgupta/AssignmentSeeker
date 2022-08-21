import telebot
from telebot import types #add-ons connected
import os
import requests

API_KEY = os.environ['API_KEY']
api=os.environ['api']
bot = telebot.TeleBot(API_KEY)
@bot.message_handler(content_types=["hello"])
def greet(message):
  bot.reply_to(message,"Hey!How its going")

@bot.message_handler(commands=["attendance"])
def attendance(message):
  keyboard = types.ReplyKeyboardMarkup (row_width = 1,       resize_keyboard = True) # Connect the keyboard
  button_phone = types.KeyboardButton (text = "Send phone",request_contact = True) 
  keyboard.add (button_phone) #Add this button
  bot.send_message (message.chat.id, 'Hello Welcome to Attendance Seeker. Please Send your Phone Number so tat we can process info.', reply_markup = keyboard)
  
 
@bot.message_handler (content_types = ['contact']) # Announced a branch in which we prescribe logic in case the user decides to send a phone number :)
def contact (message):
  if message.contact is not None:
    print(message.contact.phone_number[2:11])
    parameters = {"mobile": str(message.contact.phone_number[2:12])}
    jsonDict = get_data(api,parameters)
    keys = jsonDict["data"].keys()
    print(keys)
    output=""
    for key in keys:
      output=output+str(key)+":"+str(jsonDict["data"][key])+"\n"
  
      
    if jsonDict is not None :
      bot.send_message(chat_id=message.chat.id,text=output)
    else:  
      bot.reply_to(message,"Attendance Not shown")

    
def get_data( api,parameters):
        response = requests.get(f"{api}", params=parameters)
        if response is not None:
          print(response.json())
          return response.json();
            
        else:
          print("Not Found")
          return None
bot.polling()