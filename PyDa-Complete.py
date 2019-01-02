import wx
import wolframalpha
import wikipedia
import speech_recognition as sr
# I chose not to enable eSpeak

class MyFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None,
                          pos=wx.DefaultPosition, size=wx.Size(450, 100),
                          style=wx.MINIMIZE_BOX | wx.SYSTEM_MENU | wx.CAPTION |
                           wx.CLOSE_BOX | wx.CLIP_CHILDREN,
                          title="Pythonify")
        panel = wx.Panel(self)
        my_sizer = wx.BoxSizer(wx.VERTICAL)
        lbl = wx.StaticText(panel,
        label="Hello I am the Python Digital Assistant. How can I help you?")
        my_sizer.Add(lbl, 0, wx.ALL, 5)
        self.txt = wx.TextCtrl(panel, style=wx.TE_PROCESS_ENTER,size=(400,30))
        self.txt.SetFocus()
        self.txt.Bind(wx.EVT_TEXT_ENTER, self.OnEnter)
        my_sizer.Add(self.txt, 0, wx.ALL, 5)
        panel.SetSizer(my_sizer)
        self.Show()

    def OnEnter(self, event):
        user_input = self.txt.GetValue()
        user_input = user_input.lower()

        # Voice recognition input
        if user_input == '':
            r = sr.Recognizer()
            with sr.Microphone() as source:
                audio = r.listen(source)
            try:
                # Modified so the passed data isn't unicode and the variable stores the value for later
                self.txt.SetValue(str(r.recognize_google(audio)))
                user_input = str(r.recognize_google(audio))
            except sr.UnknownValueError:
                print("Google Speech Recognition could not understand.\nPlease try again.")
            except sr.RequestError as e:
                print("Could not request results from Google Speech Recognition Service; {0}".format(e))
                
        # Try to catch any disambugation and other exceptions
        try:
            # Wolfram
            app_id = "YOUR-WOLFRAM-ID"
            client = wolframalpha.Client(app_id)
            res = client.query(user_input)
            answer = next(res.results).text
            print(answer)
        except:
            # Wikipedia
            """ First, cleanse the string
            of 'who', 'what', 'where'
            queries to obtain info """

            query_options = ["who is", "what is", "where is", "what does", "how does", "who does"]
            split_input = user_input.split(" ")
            # Then it checks if the input string contains any of the query modifiers
            for option in query_options:
                if user_input.__contains__(option):
                    for i in range(2): # Removes the very first thing in the list twice
                        split_input.remove(split_input[0])
            # Rejoin the split input        
            user_input = " ".join(split_input)
            try:
                # Some common language shorthand codes just in case
                # en - English
                # de - German
                # zh - Chinese
                # es - Spanish
                # fr - French
                # ru - Russian
                wikipedia.set_lang("en")
                # I personally like how short yet detailed 3 sentences can be
                result = wikipedia.summary(user_input, sentences=3)
                print("\n" + result + "\n")
            # If the search passed Wolfram yet still finds an issue with disambiguation
            # then it iterates through the items neatly and restarts the search
            except wikipedia.exceptions.DisambiguationError as e:
                print("That didn't work. Try being more specific:\n")
                for item in e.options:
                    print(item)

if __name__ == "__main__":
    app = wx.App(True)
    frame = MyFrame()
    app.MainLoop()
