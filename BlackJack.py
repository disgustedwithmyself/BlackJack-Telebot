import random, telebot


# СПИСОК СЕССИЙ
PleerList = dict()


class BlackJack():
    def __init__(self, Bot: telebot.TeleBot, ChatID, MessageID, Repeat = False):
        self.TeleBot       = Bot
        self.ChatID        = ChatID
        self.MessageID     = MessageID
        self.Repeat        = Repeat

        self.Cards = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11] * 4
        random.shuffle(self.Cards)

        self.Player = 0
        self.Bot    = 0


    def getPlayerCards(self):
        Result = f"\nВыпала карта - {str(self.Cards[-1])}"
        self.Player += self.Cards.pop()

        return Result


    def getBotCards(self):
        if self.Bot < 21 and self.Bot < 20 and self.Bot < 19 and self.Bot < 18 and self.Bot < 17:
            self.Bot += self.Cards.pop()


    def sendMessage(self, Player):
        if Player == "Player":
            Result = "ПОБЕДА"

        elif Player == "Bot":
            Result = "ПОРАЖЕНИЕ"

        else:
            Result = "НИЧЬЯ"

        return f"Ваш баланс: {self.Player}\nБаланс соперника: {self.Bot}\n\nРезультат: {Result}"


    def getWinner(self):
        if self.Player <= 21 and self.Bot > 21:
            return BlackJack.sendMessage(self, "Player")

        elif self.Player <= 21 and self.Bot < 21 and self.Player > self.Bot:
            return BlackJack.sendMessage(self, "Player")

        elif self.Player > 21 and self.Bot <= 21:
            return BlackJack.sendMessage(self, "Bot")

        elif self.Player < 21 and self.Bot <= 21 and self.Player < self.Bot:
            return BlackJack.sendMessage(self, "Bot")

        elif self.Player > 21 and self.Bot > 21:
            return BlackJack.sendMessage(self, "Bot")

        elif self.Player == self.Bot:
            return BlackJack.sendMessage(self, "Draw")


    def take(self):
        if self.Player < 21:
            BlackJack.getBotCards(self)
            Var = BlackJack.getPlayerCards(self)

            self.TeleBot.edit_message_text(chat_id = self.ChatID, message_id = self.MessageID, text = f"Баланс: {self.Player}\n\n{Var}", reply_markup = BlackJack.getGameButtons(self))

        if self.Player >= 21:
            self.TeleBot.edit_message_text(chat_id = self.ChatID, message_id = self.MessageID, text = BlackJack.getWinner(self), reply_markup = BlackJack.getRepeatButton(self))
            BlackJack.endGame(self)


    def miss(self):
        if self.Player < 21 :
            BlackJack.getBotCards(self)
            self.TeleBot.edit_message_text(chat_id = self.ChatID, message_id = self.MessageID, text = BlackJack.getWinner(self), reply_markup = BlackJack.getRepeatButton(self))


        else:
            self.TeleBot.edit_message_text(chat_id = self.ChatID, message_id = self.MessageID, text = BlackJack.getWinner(self), reply_markup = BlackJack.getRepeatButton(self))

        BlackJack.endGame(self)


    def getGameButtons(self):
        Markup = telebot.types.InlineKeyboardMarkup(row_width = 1)

        Button_1 = telebot.types.InlineKeyboardButton("Взять", callback_data = f"!blackJack_взять {self.ChatID}")
        Button_2 = telebot.types.InlineKeyboardButton("Пропустить", callback_data = f"!blackJack_пропустить {self.ChatID}")

        Markup.add(Button_1, Button_2)
        return Markup


    def getRepeatButton(self):
        Markup = telebot.types.InlineKeyboardMarkup(row_width = 1)
        Markup.add(telebot.types.InlineKeyboardButton("Повторить", callback_data = f"!blackJack_начать {self.ChatID}"))

        return Markup


    def startGame(self):
            if (self.Repeat):
                self.TeleBot.edit_message_text(chat_id = self.ChatID, message_id = self.MessageID, text = f"Баланс: {self.Player}", reply_markup = BlackJack.getGameButtons(self))
        
            else:
                self.TeleBot.send_message(chat_id = self.ChatID, text = f"Баланс: {self.Player}", reply_markup = BlackJack.getGameButtons(self))
                self.MessageID += 1
                self.Repeat    = True


    def endGame(self):
        PleerList.pop(self.ChatID)
