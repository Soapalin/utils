import wx
import re


class ConversionType:
    DEC = "DEC"
    HEX = "HEX"
    HEX_WORD = "HEX_WORD"
    BIN = "BIN"
    ASCII = "ASCII"



class Style: 
    def __init__(self):
        self.title = wx.Font(20, family = wx.FONTFAMILY_DEFAULT, style = 0, weight = 90,
                    underline = False, faceName ="", encoding = wx.FONTENCODING_DEFAULT)
        self.heading = wx.Font(14, family = wx.FONTFAMILY_DEFAULT, style = 0, weight = 90,
                    underline = False, faceName ="", encoding = wx.FONTENCODING_DEFAULT)
        self.backgroundGrey = "#F1F1F1"

class CalculatorFrame(wx.Frame, ConversionType):
    """
    The view of the application
    """

    def __init__(self, *args, **kw):
        # ensure the parent's __init__ is called
        super(CalculatorFrame, self).__init__(*args, **kw)

        self.style = Style()

        # create a panel in the frame
        self.pnl = wx.Panel(self)
        self.frameSizer = wx.BoxSizer(wx.VERTICAL)
        self.mainSizer = wx.BoxSizer(wx.HORIZONTAL)

        self.notepad_Widget =  wx.TextCtrl(self.pnl,  size=(250, 572), style=wx.TE_MULTILINE|wx.TE_RICH)
        self.notepad_Widget.SetOwnBackgroundColour("#f8f8f8")


        self.calculatorSizer = wx.BoxSizer(wx.VERTICAL)

        resultSizer = wx.BoxSizer(wx.VERTICAL)
        resultText = wx.StaticText(self.pnl, label = "RESULT")
        resultText.SetOwnFont(self.style.title)
        self.result_TextCtrl = wx.TextCtrl(self.pnl, size=(250,75), style=wx.BORDER_NONE|wx.TE_READONLY) # wx.TE_READONLY
        self.result_TextCtrl.SetOwnBackgroundColour(self.style.backgroundGrey)
        self.result_TextCtrl.SetOwnFont(self.style.title)

        resultSizer.Add(resultText, wx.SizerFlags().Border(wx.BOTTOM, 30))
        resultSizer.Add(self.result_TextCtrl)
        self.calculatorSizer.Add(resultSizer, wx.SizerFlags().Border(wx.BOTTOM, 30))




        self.decBuilder()
        self.hexBuilder()
        self.asciiBuilder()
        self.binaryBuilder()
        self.hexWordBuilder()

        self.mainSizer.Add(self.calculatorSizer, wx.SizerFlags().Border(wx.LEFT, 20))
        self.mainSizer.Add(self.notepad_Widget, wx.SizerFlags().Border(wx.LEFT, 20))

        self.evalBuilder()




        self.frameSizer.Add(self.mainSizer, wx.SizerFlags().Border(wx.BOTTOM, 20))
        self.frameSizer.Add(self.evalSizer, wx.SizerFlags().Border(wx.LEFT, 20))

        self.pnl.SetSizer(self.frameSizer)

        # create a menu bar
        self.makeMenuBar()

        # and a status bar
        self.CreateStatusBar()
        self.SetStatusText("Welcome.")



    def decBuilder(self):
        decSizer = wx.BoxSizer(wx.VERTICAL)
        decText = wx.StaticText(self.pnl, label = "DEC: ")
        decText.SetOwnFont(self.style.heading)
        self.dec_TextCtrl = wx.TextCtrl(self.pnl, size=(250,50))
        self.dec_TextCtrl.SetOwnFont(self.style.heading)

        decSizer.Add(decText)
        decSizer.Add(self.dec_TextCtrl)
        self.Bind(wx.EVT_TEXT, lambda event: self.UpdateResult(event, ConversionType.DEC), self.dec_TextCtrl)
        self.calculatorSizer.Add(decSizer, wx.SizerFlags().Border(wx.TOP|wx.LEFT, 0))


    def asciiBuilder(self):
        asciiSizer = wx.BoxSizer(wx.VERTICAL)
        asciiText = wx.StaticText(self.pnl, label = "ASCII:")
        asciiText.SetOwnFont(self.style.heading)
        self.ascii_TextCtrl = wx.TextCtrl(self.pnl, size=(250,50))
        self.ascii_TextCtrl.SetOwnFont(self.style.heading)

        asciiSizer.Add(asciiText)
        asciiSizer.Add(self.ascii_TextCtrl)
        self.Bind(wx.EVT_TEXT, lambda event: self.UpdateResult(event, ConversionType.ASCII), self.ascii_TextCtrl)
        self.calculatorSizer.Add(asciiSizer, wx.SizerFlags().Border(wx.TOP, 10))

    def hexBuilder(self):
        hexSizer = wx.BoxSizer(wx.VERTICAL)
        hexText = wx.StaticText(self.pnl, label = "HEX:")
        hexText.SetOwnFont(self.style.heading)
        self.hex_TextCtrl = wx.TextCtrl(self.pnl, size=(250,50))
        self.hex_TextCtrl.SetOwnFont(self.style.heading)

        hexSizer.Add(hexText)
        hexSizer.Add(self.hex_TextCtrl)
        self.Bind(wx.EVT_TEXT, lambda event: self.UpdateResult(event, ConversionType.HEX), self.hex_TextCtrl)
        self.calculatorSizer.Add(hexSizer, wx.SizerFlags().Border(wx.TOP, 10))


    def binaryBuilder(self):
        binarySizer = wx.BoxSizer(wx.VERTICAL)
        binaryText = wx.StaticText(self.pnl, label = "BIN:")
        binaryText.SetOwnFont(self.style.heading)
        self.binary_TextCtrl = wx.TextCtrl(self.pnl, size=(250,50))
        self.binary_TextCtrl.SetOwnFont(self.style.heading)

        binarySizer.Add(binaryText)
        binarySizer.Add(self.binary_TextCtrl)
        self.Bind(wx.EVT_TEXT, lambda event: self.UpdateResult(event, ConversionType.BIN), self.binary_TextCtrl)
        self.calculatorSizer.Add(binarySizer, wx.SizerFlags().Border(wx.TOP, 10))


    def hexWordBuilder(self):
        hexWordSizer = wx.BoxSizer(wx.VERTICAL)
        hexWordText = wx.StaticText(self.pnl, label = "HEX WORD:")
        hexWordText.SetOwnFont(self.style.heading)
        self.hexWord_TextCtrl = wx.TextCtrl(self.pnl, size=(250,50))
        self.hexWord_TextCtrl.SetOwnFont(self.style.heading)

        hexWordSizer.Add(hexWordText)
        hexWordSizer.Add(self.hexWord_TextCtrl)
        self.Bind(wx.EVT_TEXT, lambda event: self.UpdateResult(event, ConversionType.HEX_WORD), self.hexWord_TextCtrl)
        self.calculatorSizer.Add(hexWordSizer, wx.SizerFlags().Border(wx.TOP, 10))

    def evalBuilder(self):
        self.evalSizer = wx.BoxSizer(wx.VERTICAL)
        evalText = wx.StaticText(self.pnl, label="eval{\}")
        self.eval_TextCtrl = wx.TextCtrl(self.pnl, size=(450,30), style=wx.TE_PROCESS_ENTER)
        evalResText = wx.StaticText(self.pnl, label= "Result")
        self.evalRes_TextCtrl = wx.TextCtrl(self.pnl, size=(450, 80))

        self.evalSizer.Add(evalText)
        self.evalSizer.Add(self.eval_TextCtrl)
        self.evalSizer.Add(evalResText,wx.SizerFlags().Border(wx.TOP, 10))
        self.Bind(wx.EVT_TEXT, lambda event: self.evaluateExpression(event), self.eval_TextCtrl)
        self.Bind(wx.EVT_TEXT_ENTER, lambda event: self.evaluateFinalise(event), self.eval_TextCtrl)
        self.evalSizer.Add(self.evalRes_TextCtrl)
    
    def changeAllTextCtrlValue(self, value):
        self.hex_TextCtrl.ChangeValue(value)
        self.dec_TextCtrl.ChangeValue(value)
        self.result_TextCtrl.ChangeValue(value)
        self.binary_TextCtrl.ChangeValue(value)
        self.ascii_TextCtrl.ChangeValue(value)
        self.hexWord_TextCtrl.ChangeValue(value)
    
    def hexTohexWord(self, hexa):
        if len(hexa)%2 == 0:
            hexWord = "0x" + " 0x".join(character for character in re.findall('..?',hexa))
        else: 
            first_digit = hexa[0]
            characters = re.findall('..',hexa[1:])
            print(f"DEBUG: characters: {characters}")
            characters.insert(0, first_digit)
            hexWord =  "0x" + " 0x".join(character for character in characters)
             
        return hexWord

    def UpdateResult(self, event, id):
        print(id)
        print(event.GetString())
        number = event.GetString()
        if number == "":
            # if no value, clear all fields 
            self.changeAllTextCtrlValue(value="")
            return
        if id == ConversionType.BIN:
            original = number 
            number = re.sub(r"[^0-1\s]", "", number)
            if original.replace(" ", "") != number:
                self.SetStatusText(f"{id}: Illegal Character Removed.")
            binary = int(number.replace(" ", ""),2)
            hexa = hex(binary).replace("0x", "")
            hexWord = self.hexTohexWord(hexa=str(hexa))
            self.binary_TextCtrl.ChangeValue(number)
            self.binary_TextCtrl.SetInsertionPoint(-1)
            self.result_TextCtrl.ChangeValue(str(binary))
            self.dec_TextCtrl.ChangeValue(str(binary))
            self.hex_TextCtrl.ChangeValue(str(hexa))
            self.hexWord_TextCtrl.ChangeValue(hexWord)
        elif id == ConversionType.DEC:
            original = number
            number = re.sub(r"[^0-9\s]", "", number)
            if original.replace(" ", "") != number:
                self.SetStatusText(F"{id}: Illegal Character Removed.")
                self.dec_TextCtrl.ChangeValue(number)
                self.dec_TextCtrl.SetInsertionPoint(-1)
            number = number.replace(" ", "")
            binary = str(bin(int(number))).replace("0b", "")
            hexa = str(hex(int(number))).replace("0x", "")
            try:
                ascii_value = chr(int(number))
            except:
                ascii_value = "INVALID"
            hexWord = self.hexTohexWord(hexa=str(hexa))
            self.result_TextCtrl.ChangeValue(number)
            self.binary_TextCtrl.ChangeValue(binary)
            self.hex_TextCtrl.ChangeValue(hexa)
            self.hexWord_TextCtrl.ChangeValue(hexWord)
            self.ascii_TextCtrl.ChangeValue(ascii_value)
        elif id == ConversionType.HEX:
            original = number 
            number = re.sub(r"[^0-9a-fA-F\s]", "", number)
            if original.replace(" ", "") != number:
                self.SetStatusText(F"{id}: Illegal Character Removed.")
                self.hex_TextCtrl.ChangeValue(number)
                self.hex_TextCtrl.SetInsertionPoint(-1)
            number = number.replace(" ", "")
            print(f"DEBUG: {number}")
            decimal = int(number,16)
            print(f"DEBUG: dec: {decimal}")
            ascii_value = "".join(chr(int(character, 16)) for character in re.findall('..?',number) )
            self.ascii_TextCtrl.ChangeValue(ascii_value)
            print(f"DEBUG: ascii_value: {ascii_value}")
            self.dec_TextCtrl.ChangeValue(str(decimal))
            self.result_TextCtrl.ChangeValue(str(decimal))
            self.binary_TextCtrl.ChangeValue(str(bin(decimal)).replace("0b",""))
            hexWord = self.hexTohexWord(hexa=number)
            self.hexWord_TextCtrl.ChangeValue(hexWord)
        elif id == ConversionType.HEX_WORD:
            original = number 
            word = number.replace("0x", "")
            print(f"DEBUG: word: {word}")
            hexa = word.replace(" ", "")
            self.hex_TextCtrl.ChangeValue(hexa)
            self.binary_TextCtrl.ChangeValue("")
            self.dec_TextCtrl.ChangeValue("")
            result = ""
            for character in word.split(" "):
                try:
                    result += chr(int(character,16))
                    print(f"DEBUG: result: {result}")
                except:
                    self.ascii_TextCtrl.ChangeValue("INVALID")
                    return
            self.ascii_TextCtrl.ChangeValue(result)
        elif id ==ConversionType.ASCII:
            original = number 
            hexWord = " ".join(hex(ord(num)) for num in number)
            print(f"DEBUG: hexWord: {hexWord}")
            self.hexWord_TextCtrl.ChangeValue(hexWord)
            hexa = hexWord.replace("0x", "").replace(" ", "")
            self.hex_TextCtrl.ChangeValue(hexa)
            self.binary_TextCtrl.ChangeValue("")
            self.dec_TextCtrl.ChangeValue("")



    def evaluateExpression(self, event):
        print(event.GetString())
        if event.GetString() == "":
            self.evalRes_TextCtrl.ChangeValue("")
            return
        try:
            result = ""
            print(f"{'result = ' + event.GetString()}")
            setResult = eval(event.GetString())
            print(result)
            self.evalRes_TextCtrl.ChangeValue(str(setResult))
            return str(setResult)
        except: 
            self.evalRes_TextCtrl.ChangeValue("INVALID OPERATION")
        


    def evaluateFinalise(self,event):
        print("FINALISE")
        result = self.evaluateExpression(event)
        if result is not None:
            self.sendToNote(event.GetString(), result)

    def sendToNote(self, operation, result):
        if type(result) is not str:
            result = str(result)
        self.notepad_Widget.SetInsertionPoint(-1)
        self.notepad_Widget.AppendText(operation + "\n")
        self.notepad_Widget.AppendText("    = " + result + "\n\n")
        


    def makeMenuBar(self):
        """
        A menu bar is composed of menus, which are composed of menu items.
        This method builds a set of menus and binds handlers to be called
        when the menu item is selected.
        """

        # Make a file menu with Hello and Exit items
        fileMenu = wx.Menu()
        # The "\t..." syntax defines an accelerator key that also triggers
        # the same event
        helloItem = fileMenu.Append(-1, "&Hello...\tCtrl-H",
                "Help string shown in status bar for this menu item")
        self.clearConsoleItem = fileMenu.Append(-1, "&Clear Console...\tCtrl-Q", "Clear Console Output")
        fileMenu.AppendSeparator()
        # When using a stock ID we don't need to specify the menu item's
        # label
        exitItem = fileMenu.Append(wx.ID_EXIT)

        # Now a help menu for the about item
        helpMenu = wx.Menu()
        aboutItem = helpMenu.Append(wx.ID_ABOUT)

        # Make the menu bar and add the two menus to it. The '&' defines
        # that the next letter is the "mnemonic" for the menu item. On the
        # platforms that support it those letters are underlined and can be
        # triggered from the keyboard.
        menuBar = wx.MenuBar()
        menuBar.Append(fileMenu, "&File")
        menuBar.Append(helpMenu, "&Help")

        # Give the menu bar to the frame
        self.SetMenuBar(menuBar)

        # Finally, associate a handler function with the EVT_MENU event for
        # each of the menu items. That means that when that menu item is
        # activated then the associated handler function will be called.
        self.Bind(wx.EVT_MENU, self.OnHello, helloItem)
        self.Bind(wx.EVT_MENU, self.OnExit,  exitItem)
        self.Bind(wx.EVT_MENU, self.OnAbout, aboutItem)


    def OnExit(self, event):
        """Close the frame, terminating the application."""
        self.Close(True)


    def OnHello(self, event):
        """Say hello to the user."""
        wx.MessageBox("Hello again from wxPython")


    def OnAbout(self, event):
        """Display an About Dialog"""
        wx.MessageBox("This is a wxPython Hello World sample",
                      "About Hello World 2",
                      wx.OK|wx.ICON_INFORMATION)





if __name__ == '__main__':
    # When this module is run (not imported) then create the app, the
    # frame, show it, and start the event loop.
    app = wx.App()
    # app = wx.App(redirect=True,filename="LogAnalyserGUI.txt")
    frm = CalculatorFrame(None, title='Calculator', size=(500,850))
    frm.Show()
    app.MainLoop()
