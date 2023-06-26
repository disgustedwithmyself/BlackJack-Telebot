if (Message.Command == "!blackJack_начать"):
        Session = BlackJack(Bot, Message.ChatID, Message.MessageID, True)
        PleerList[Message.ChatID] = Session
        Session.startGame()


if (Message.Command == "!blackJack_взять"):
    PleerList[int(Message.Arg)].take()


if (Message.Command == "!blackJack_пропустить"):
    PleerList[int(Message.Arg)].miss()
