#-----------------------------------------------------
# Creates GUI for SmartIT automation
#
# by Sean Conrad and Joe Rediger
#-----------------------------------------------------

from Tkinter import *
import threading
import Queue
import CreatingAndClosingTicket
import time
import CrossChargeAutomation
import collections
import ttk


# Creates a GUI class. Found that this was easier than making it a function
class GUI:
    def __init__(self, master):

        # Opens the 'CCitems' file to read what's in it.
        # All the cross charge items are in there and send the one of the drop down menus
        self.ccItems = open('CCitems.txt', 'r')

        # Creates the master window
        self.master = master
        # Set window size and location on the screen where it opens
        master.geometry("800x450+1900+500")
        # Title of window
        master.wm_title("Smart IT Automation")

        #username and password labels and textboxes
        self.entrytext1 = StringVar()
        self.entrytext2 = StringVar()

        Label(Label(text="Username: ").grid(row=0, sticky=E, padx=5, pady=1))
        Label(text="Password: ").grid(row=1, sticky=E, padx=5, pady=1)
        self.entry1 = Entry(textvariable=self.entrytext1)
        self.entry2 = Entry(textvariable=self.entrytext2, show="*")

        self.entry1.grid(row=0, column=1, sticky=NW)
        self.entry2.grid(row=1, column=1, sticky=NW)

        # Big Log Box-----------------
        self.text1 = Text(master, bd=3, font="Arial, 14", bg='grey', height=6, width=45, relief=RIDGE, padx=10, pady=5)
        self.text1.grid(row=1, rowspan=20, column=2, sticky=NW)
        self.text1.insert(INSERT, "SmartIT Automation")


        # Big CC Log box--------------
        self.ccLogBox = Text(master, bd=3, font="Arial, 14", bg='grey', height=6, width=45, relief=RIDGE, padx=10, pady=5)
        self.ccLogBox.grid(row=17, rowspan=20, column=2, sticky=NW)
        self.ccLogBox.insert(INSERT, "CrossCharge Automation")
        self.ccLogBox.config(state=DISABLED)

        # Scrollbars------------------


        # Labels-------------------------------------

        Label(text="-----------------------------").grid(row=17, column=1, sticky=W)
        Label(text="CrossCharge Item").grid(row=18, column=1, sticky=W)


        Label(text="Employee username: ").grid(row=6, sticky=E, padx=5, pady=1)
        Label(text="Ticket Description: ").grid(row=14, sticky=E, padx=5, pady=1)
        Label(text="Ticket Resolution: ").grid(row=15, sticky=E, padx=5, pady=1)
        Label(text="Select your site: ").grid(row=4, column=0, sticky=E, padx=5, pady=5)
        Label(text="-----------------------------").grid(row=2, column=1, sticky=W)
        Label(text='Create and Close ticket').grid(row=3, column=1, sticky=W)

        Label(text="Item to CC: ").grid(column=0, row=19, sticky=E, padx=5, pady=1)
        Label(text="User to CC to: ").grid(column=0, row=20, sticky=E, padx=5, pady=1)
        Label(text="Ticket #:").grid(row=21, column=0, sticky=E)
        Label(text="Quantity:").grid(row=22, column=1, sticky=E)



        # Dropdown Menus-----------------------------
        self.var2 = StringVar()
        self.option = OptionMenu(master, self.var2, 'Austin', 'Boston', 'Chandler', 'Guatemala',
                                 'Hunt Valley', 'Mexico', 'New York', 'Newton',
                                 'Omaha', 'Scottsdale', 'San Jose', 'San Francisco',
                                 'Timonium', 'Toronto', 'Washington')

        self.option.grid(row=4, column=1, sticky=EW)

        # This opens, 'CCitems' file,
        # enumerates through it, and for each line, it appends it to list, 'a',

        self.a = []
        with open('CCitems.txt') as input_file:
            for i, line in enumerate(input_file):
                self.a.append(line[:-2])


        # This creates a variable for the drop down menu and whatever is selected,
        # That string becomes the assigned to the 'var3' variable
        self.var3 = StringVar()

        # This adds everything in list 'a', to the drop down menu
        self.ccItemOptions = OptionMenu(master, self.var3, *self.a)
        self.ccItemOptions.grid(row=19, column=1, sticky=EW)

        # CC Quantity dropdown------------------------

        self.var4 = StringVar()
        self.quantityDropDown = OptionMenu(master, self.var4, '1', '2', '3', '4')
        self.quantityDropDown.grid(row=22, column=2, sticky=W)


        # Text Boxes----------------------------------

        # Each text box entry will be stored as a variable

        self.entrytext3 = StringVar()
        self.entrytext4 = StringVar()
        self.entrytext5 = StringVar()
        self.ccUser = StringVar()
        self.ticketNumber = StringVar()

        # Entry boxes are created and variables are assigned to whatever is in the text boxes

        self.entry3 = Entry(textvariable=self.entrytext3)
        self.entry4 = Entry(textvariable=self.entrytext4, width=69)
        self.entry5 = Entry(textvariable=self.entrytext5, width=69)
        self.ccUser = Entry(textvariable=self.ccUser)
        self.ticketNumber = Entry(textvariable=self.ticketNumber)

        self.entry3.grid(row=6, column=1, sticky=NW)
        self.entry4.grid(row=14, columnspan=3, column=1, sticky=SE)
        self.entry5.grid(row=15, columnspan=3, column=1, sticky=SE)
        self.ccUser.grid(row=20, column=1, sticky=W)
        self.ticketNumber.grid(row=21, column=1, sticky=W)

        # Buttons------------------------------------
        self.buttontext = StringVar()
        self.buttontext.set("Submit Ticket")
        # Buttons are created and have functions tied to them
        self.button1 = Button(master, textvariable=self.buttontext, command=self.tb_click)
        self.btnCloseApp = Button(text='Close App', command=self.closeWindow)
        self.btnClearEntryboxes = Button(text="Clear fields", command=self.clearFields)
        self.btnClearLogs = Button(text = "Clear logs", command=self.clearLogs)
        #self.btnSubmitCC = Button(text='Submit CC')
        #self.btnClearCCfields = Button(text="Clear fields", command=self.clearCCFields)

        # Buttons placed and positioned
        self.button1.grid(row=16, column=0, sticky=E)
        self.btnCloseApp.grid(row=23, column=2, sticky=E)
        self.btnClearEntryboxes.grid(row=16, column=1, sticky=W)
        self.btnClearLogs.grid(row=0, column=2, sticky=E)
        #self.btnSubmitCC.grid(row=21, column = 0, sticky=E)
        #self.btnClearCCfields.grid(row=21, column=1, sticky=W)

        #CC Buttons-------
        self.dict = {}
        self.addToCartBtn = Button(text='Add to Cart', command=lambda: self.container(self.dict))
        self.addToCartBtn.grid(row=22, column=0, sticky=E)

        self.clearCartBtn = Button(text='Clear cart', command=lambda: self.clearCart(self.dict))
        self.clearCartBtn.grid(row=22, column=1, sticky=W)

        self.submitBtn = Button(text='Submit', command=lambda: self.ccItem(self.dict))
        self.submitBtn.grid(row=23, column=0, sticky=E)


    def clearFields(self):

        self.entry3.delete(0, END)
        self.entry4.delete(0, END)
        self.entry5.delete(0, END)

    def clearCCFields(self):
        self.ccUser.delete(0, END)

    def clearLogs(self):
        self.text1.config(state=NORMAL)
        self.text1.delete(0.0, END)
        self.ccLogBox.config(state=NORMAL)
        self.ccLogBox.delete(0.0, END)

    def ccItem(self, dict):
        self.ccLogBox.config(state=NORMAL)
        self.ccLogBox.delete(0.0, END)
        self.d = self.dict
        orderedCart = collections.OrderedDict(self.d)  # Creates ordered dict
        self.updateTextBox("Cross charging items to " + self.ccUser.get())
        self.updateTextBox('-------------------------------')
        for k, v in orderedCart.iteritems():
            self.updateTextBox(k + " (" + v + ")")   # Iterates through dict and creates string with format
        self.updateTextBox('-------------------------------')
        self.tb_clickcc()
        #self.clearCart(dict)

    # Function that excepts whatever string as input and updates it to the notification box
    def updateTextBox(self, text):
        self.text1.config(state=NORMAL)
        self.text1.insert(INSERT, "\n" + text)
        self.text1.see(END)

    def updateCCLogBox(self, text):
        self.ccLogBox.config(state=NORMAL)
        self.ccLogBox.insert(INSERT, text + "\n")
        self.ccLogBox.see(END)


    # Creates a queue and whenever it is ran, the queue is filled.
    # Threaded Task then starts up a new thread with the 'doStuff' function.
    def tb_click(self):
        self.queue = Queue.Queue()
        ThreadedTask(self.queue).start()
        self.master.after(100, self.process_queue)

    def tb_clickcc(self):
        self.queue = Queue.Queue()
        ThreadedTaskcc(self.queue).start()
        self.master.after(100, self.process_queue)

    # This reads whatever is in the text boxes, dropdowns, check boxes
    # Assigns them to variables and sends them to the CreatingAndClosingTicket.create_and_close_ticket function
    # Also does some checking to make sure the fields are filled out.
    def doStuff(self):
        self.usrname = self.entrytext1.get()
        self.pwd = self.entrytext2.get()
        self.employeeName = self.entrytext3.get()
        self.ticketInfo = self.entrytext4.get()
        self.resolutioNotes = self.entrytext5.get()
        self.site = self.var2.get()

        # Sees if entry box is empty and if it is, throws notification to the notification text box
        if self.entrytext1.get() == '':
            self.updateTextBox('Please type your username.')
            # self.text.tag_add("here", "2.0", "2.19")
            # self.text.tag_config("here", foreground="red")
        elif self.entrytext2.get() == '':
            self.updateTextBox('Please type your password.')

        elif self.entrytext3.get() == '':
            self.updateTextBox('Please type employee name.')

        elif self.entrytext4.get() == '':
            self.updateTextBox('Please type ticket notes.')

        elif self.entrytext5.get() == '':
            self.updateTextBox('Please type resolution notes.')

        elif self.var2.get() == '':
            self.updateTextBox('Please select a site.')

        # Kicks off process to create a ticket
        else:
            self.updateTextBox(self.entrytext3.get() + " ticket being created...")
            self.updateTextBox(
                self.entrytext3.get() + " ticket closed " + CreatingAndClosingTicket.create_and_close_ticket(
                    self.usrname, self.pwd, self.employeeName,
                    self.ticketInfo, self.resolutioNotes, self.site))

    def update_cc_items_list(self):
        self.usrname = self.entrytext1.get()
        self.pwd = self.entrytext2.get()
        self.employeeName = self.entrytext3.get()
        self.ticketInfo = self.entrytext4.get()
        self.resolutioNotes = self.entrytext5.get()
        self.site = self.var2.get()

        # Sees if entry box is empty and if it is, throws notification to the notification text box
        if self.entrytext1.get() == '':
            self.updateTextBox('Please type your username.')
            # self.text.tag_add("here", "2.0", "2.19")
            # self.text.tag_config("here", foreground="red")
        elif self.entrytext2.get() == '':
            self.updateTextBox('Please type your password.')


    # Closes window
    def closeWindow(self):
        self.master.quit()

    # Queue for threads ?:)?
    def process_queue(self):
        try:
            msg = self.queue.get(0)
            # Show result of the task if needed
            # self.prog_bar.stop()
        except Queue.Empty:
            self.master.after(100, self.process_queue)

# CART CODE -----------------------
    def clearCart(self, dict):
        self.dict = {}
        self.ccLogBox.delete(0.0, END)
        self.updateCCLogBox('Cart emptied, ready to add new items.')

    def container(self, dict):
        self.itemSelection = self.var3.get()
        self.itemQuantity = self.var4.get()
        self.dict[self.itemSelection] = self.itemQuantity
        #Updates to CClog box
        self.updateCCLogBox(self.itemSelection + " (" + self.itemQuantity + ") added to cart")

    def getItemsFromCart(self, dict):
        CrossChargeAutomation.crossCharge(self.entry1.get(), self.entry2.get(), self.ccUser.get(), self.ticketNumber.get(), self.dict)


# Creates the threads ------------
class ThreadedTask(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue

    def run(self):
        main_ui.doStuff()
        time.sleep(5)  # Simulate long running process
        self.queue.put("Task finished")

class ThreadedTaskcc(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue

    def run(self):
        main_ui.getItemsFromCart(dict)
        time.sleep(5)  # Simulate long running process
        self.queue.put("Task finished")


# assigns Tk() class to new object called root
root = Tk()

#REMOVE ME LATER
root.tk.call('after','idle','console','hide')
# Not sure if this is needed. Will delete later
root.title("Test Button")
# More stuff here
main_ui = GUI(root)
# Loop that keeps windows open
root.mainloop()


