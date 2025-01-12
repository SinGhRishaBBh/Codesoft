import tkinter as tk
from tkinter import scrolledtext
import re

def get_response(user_input):
  """
  Converts input to lowercase for easier matching and returns a response based on defined rules.
  """
  user_input = user_input.lower()

  rules = {
      r'hello|hi|hey': 'Hello! How can I help you today?',
      r'how are you': "I'm doing well, thank you for asking!",
      r'what is your name': "My name is ChatBot. It's nice to meet you!",
      r'bye|goodbye': 'Goodbye! Have a great day!',
      r'thank you|thanks': "You're welcome!",
      r'weather': "I'm sorry, I don't have access to real-time weather information.",
      r'help': "I can answer simple questions. Try asking about my name or how I'm doing!",
  }

  for pattern, response in rules.items():
    if re.search(pattern, user_input):
      return response

  return "I'm not sure how to respond to that. Can you try rephrasing or asking something else?"

class ChatbotGUI:
  """
  Class to handle the graphical user interface for the chatbot.
  """
  def __init__(self, master):
    self.master = master
    master.title("Rule-Based Chatbot")
    master.geometry("400x500")
    master.resizable(False, False)

    # Chat display
    self.chat_display = scrolledtext.ScrolledText(master, wrap=tk.WORD, width=45, height=25)
    self.chat_display.grid(row=0, column=0, columnspan=2, padx=10, pady=10)
    self.chat_display.config(state=tk.DISABLED)

    # Input field
    self.input_field = tk.Entry(master, width=30)
    self.input_field.grid(row=1, column=0, padx=10, pady=10)
    self.input_field.bind("<Return>", self.send_message)

    # Send button
    self.send_button = tk.Button(master, text="Send", command=self.send_message)
    self.send_button.grid(row=1, column=1, padx=10, pady=10)

    self.display_message("ChatBot: Hello! I'm a simple rule-based chatbot. How can I help you?")

  def send_message(self, event=None):
    user_input = self.input_field.get()
    self.input_field.delete(0, tk.END)

    if user_input:
      self.display_message(f"You: {user_input}")
      response = get_response(user_input)
      self.display_message(f"ChatBot: {response}")

  def display_message(self, message):
    self.chat_display.config(state=tk.NORMAL)
    self.chat_display.insert(tk.END, message + "\n\n")
    self.chat_display.see(tk.END)
    self.chat_display.config(state=tk.DISABLED)

root = tk.Tk()
chatbot_gui = ChatbotGUI(root)
root.mainloop()  # This line is corrected, removing the extra closing parenthesis