import tkinter as tk
from tkinter import ttk
import winsound

# TODO: Correct timer to tick of system clock instead of system count
# TODO: Block non-number input
# TODO: Save timers instead of hard code with pickling or json
# TODO: Different end timer sounds

class WorkTimer():
    """ A visual task timer that can add and delete tasks

    A visual timer with default timers and tasks.
    Additional timers/tasks can be added from the toolbar at the top.
    Timers that reach zero will "ding" and count past zero, highlighted in red.
    You can count down from a specific time or count up from zero.
    Timers can be run simulatneously or individually.
    Minutes are adjusted in singles. Seconds are adjusted in tens.
    
    Parameters
    ----------
    name (str): The name of the new timer
    mins (int): The number of minutes for the timer
    secs (int): The number of seconds for the timer

    Notes
    -----
    Flags are used to allow stopping and restarting counts.
    If you want a non-stop timer, you can remove the counting flags.
    """

    def __init__(self, name, mins, secs) -> None:
        # Object parameters
        self.name = name
        self.mins = mins
        self.secs = secs

        # Format for display of timers
        self.time_format = f"{self.mins:02d}:{self.secs:02d}" 
        self.label = tk.Label(text="00:00")
        self.button = tk.Button(text="Start/Stop")
        self.button_row = 1

        # Setting all counting flags to False
        self.counting = False
        self.counting_up = False
        self.counting_down = False
        self.negative_count = False
        

    ### Methods to add and subtract minuntes/seconds
    def add_mins():
        """ Add minutes to new timer """
        global temp_mins
        temp_mins +=1
        minute_amount_entry.delete(0, last=30)
        minute_amount_entry.insert(0, f"{temp_mins}")

    def sub_mins():
        """" Subtract seconds from new timer """
        global temp_mins
        temp_mins -= 1
        minute_amount_entry.delete(0, last=30)
        minute_amount_entry.insert(0, f"{temp_mins}")

    def add_secs():
        """ Add 10 seconds to new timer """
        global temp_secs
        temp_secs += 10
        second_amount_entry.delete(0, last=30)
        second_amount_entry.insert(0, f"{temp_secs}")
    
    def sub_secs():
        """ Subtract 10 seconds from new timer """
        global temp_secs
        temp_secs -= 10
        second_amount_entry.delete(0, last=30)
        second_amount_entry.insert(0, f"{temp_secs}")


    ### Methods to control counting up/down or back up after zero on countdown
    def countdown(self, mins, secs):
        """ Controls counting and ticks of any running timer
        
        This method controls the basic formatting and second ticks of running timers.
        If a timer reaches zero or starts at zero, the negative_countup() method is invoked.
        Flags are used to track the positive or negative state of the timer object.

        Parameters
        ----------
        mins: int
            The number of minutes in the current timer
        secs: int
            The number of seconds in the current timer

        
        """
        # variables and flags
        self.counting_down = True
        self.mins = mins
        self.secs = secs
        
        # Continue counting past zero if timer has reached zero
        if self.negative_count == True:
            self.negative_countup()
            return

        # Count from zero if timer started at zero minutes and seconds 
        if self.mins <= 0 and self.secs <= 0:
            self.negative_countup()
            return

        # Formating and single second ticks of running clocks
        if self.counting == True:
            if self.secs < 0:
                self.secs = 59
                self.mins -= 1
            self.new_timer_label["text"] = f"{self.mins:02d}:{self.secs:02d}"
            self.secs -= 1
            root.after(1000, self.countdown, self.mins, self.secs)

    def negative_countup(self):
        """ Counts past zero with red background once timer reaches zero """
        # Beeps when timer reaches zero
        if self.negative_count == False:
            winsound.Beep(1000, 1000)

        # Sets negative count flag to True
        self.negative_count = True

        # Timer counts up from zero and background turns red after timer ends
        if self.counting == True:
            if self.secs >= 60:
                self.secs = 0
                self.mins += 1
            self.new_timer_label["text"] = f"- {self.mins:02d}:{self.secs:02d}"
            self.new_timer_label["bg"] = "red"
            self.secs += 1
            root.after(1000, self.negative_countup)

    def countup(self):
        """ Used to count up from zero 
        
        Notes
        -----
        Different from the negative_count() method because it doesn't affect timer background color

        """
        self.counting_up = True
        if self.counting == True:
            if self.secs >= 60:
                self.secs = 0
                self.mins += 1
            self.new_timer_label["text"] = f"{self.mins:02d}:{self.secs:02d}"
            self.secs += 1
            root.after(1000, self.countup)


    # To control start/stop button 
    def btn_click(self):
        """ Checks which flags are True or False to control timer behavior"""
        # Default to pause a ticking timer
        if self.counting == True:
            self.counting = False
        
        # Flag to ensure a count up timer still counts up after pause
        elif self.counting_up == True:
            self.counting = True
            self.countup()
        
        # Flag for a indicatie a timer that counts down
        elif self.counting_down == True:
            self.counting = True
            self.countdown(self.mins, self.secs)
        
        # Flag to indicate a timer counting past zero
        elif self.negative_count == True:
            self.negative_count = False
       
       # Flag a countdown in cases where timer isn't at zero (a count-up timer)
        else:
            if self.mins == 0 and self.secs == 0:
                self.counting = True
                self.countup()
            else:
                self.counting = True
                self.countdown(self.mins, self.secs)

# To help create new objects with dynamic names
    def new_timer_obj():
        """ Creates a new timer object when the 'Add Timer' button is pressed"""
        # Setup variables for new timer
        global timer_number
        global temp_mins
        global temp_secs
        str_name = string_var_name.get()

        # New timer given a number to differentiate timer objects
        timer_name_list = list(range(100))
        timer_name_list[timer_number] = WorkTimer(str_name, temp_mins, temp_secs)
        timer_name_list[timer_number].create_new_timer_button(str_name)
        timer_number += 1

# To create and initialize new buttons and labels that are created with new_timer_obj
    def create_new_timer_button(self, str_name):
        """ Functionality and format for new tkinter buttons
        
        Parameters
        ----------
        str_name: str
            The name given to the timer passed from new_timer_obj() from the tkinter get() method
        
        """
        # Global variable to ensure button added to new row
        global button_row

        # Display format for timer and buttons
        self.new_button_label_name = tk.Label(root, text=str_name, font='Ariel 12')
        self.start_stop_btn = tk.Button(root, text=u'\u23F5'+ " " + u'\u23F8', command=self.btn_click)
        self.new_timer_label = tk.Label(root, text=f"{self.mins:02d}:{self.secs:02d}", font="Times 16 bold",
        bg="white")
        self.new_button_label_name.grid(row=button_row, column=0, columnspan=4, padx=4, pady=4, sticky='w')
        self.start_stop_btn.grid(row=button_row, column=5, columnspan= 2, padx=4, pady=4)
        self.new_timer_label.grid(row=button_row, column=7, columnspan= 2, padx=4, pady=4)
        button_row += 1

class WorkTask():
    """ Counter that can add or subtract countable tasks


    """
    def __init__(self, name, task_num) -> None:
        self.task_num = task_num

    def new_task():
        global task_count
        global task_number
        task_name = task_var_name.get()

        task_name_list = list(range(100))
        task_name_list[task_number] = WorkTask(task_name, task_count)
        task_name_list[task_number].create_new_task_button(task_name)
        task_number += 1

    def create_new_task_button(self, task_name):
        global button_row
        task_name = task_name.upper()

        self.new_task_label_name = tk.Label(root, text=task_name, font="Ariel 12")
        self.new_task_sub_button = tk.Button(root, text="-1", command=self.after_sub_task)
        self.new_task_count_label = tk.Label(root, text=f'{self.task_num}', font="Times 16 bold", bg="white")
        self.new_task_add_button = tk.Button(root, text="+1", command=self.after_add_task)
        self.new_task_label_name.grid(row=button_row, column=0, columnspan=4, padx=4, pady=4, sticky='w')
        self.new_task_sub_button.grid(row=button_row, column=5, padx=4, pady=4, sticky='e')
        self.new_task_add_button.grid(row=button_row, column=6, padx=4, pady=4, sticky='w')
        self.new_task_count_label.grid(row=button_row, column=8, padx=4, pady=4)

        button_row += 1

    # Increment/Decrement task count
    def add_task():
        global task_count
        task_count += 1
        task_count_entry.delete(0, last=30)
        task_count_entry.insert(0, f"{task_count}")
    
    def sub_task():
        global task_count
        task_count -= 1
        task_count_entry.delete(0, last=30)
        task_count_entry.insert(0, f"{task_count}")

    def after_add_task(self):
        self.task_num += 1
        self.new_task_count_label["text"] = f'{self.task_num}'

    def after_sub_task(self):
        self.task_num -= 1
        self.new_task_count_label["text"] = f'{self.task_num}'



if __name__ == "__main__":
    # Set up tkinter environment
    root = tk.Tk()
    root.title("Work Timer")
    root.grid_rowconfigure(2, minsize=20)
    separator = ttk.Separator(root, orient="horizontal")
    separator.grid(row=2, column=0, columnspan=11, sticky='ew')

    # Set up variables
    button_row = 3
    timer_number = 0 
    task_number = 0
    temp_mins = 0
    temp_secs = 0
    task_count = 0
    string_var_name = tk.StringVar()
    task_var_name = tk.StringVar()

    # tkinter Buttons and Labels for timers
    add_min_btn = tk.Button(root, text="+1 Min", command=WorkTimer.add_mins)
    sub_min_btn = tk.Button(root, text="-1 Min", command=WorkTimer.sub_mins)
    add_sec_btn = tk.Button(root, text="+10 Sec", command=WorkTimer.add_secs)
    sub_sec_btn = tk.Button(root, text="-10 Sec", command=WorkTimer.sub_secs)
    minute_amount_label = tk.Label(root, text="Minutes:")
    minute_amount_entry = tk.Entry(root, width=3)
    second_amount_label = tk.Label(root, text="Seconds:")
    second_amount_entry = tk.Entry(root, width=3)
    new_timer_name_label = tk.Label(root, text="Timer Name")
    new_timer_button = tk.Button(root, text="Add Timer", command=WorkTimer.new_timer_obj)
    new_timer_entry_name = tk.Entry(root, textvariable=string_var_name)

    # Align the buttons/labels/entries on grid
    add_min_btn.grid(row=0, column=0, padx=4, pady=4)
    sub_min_btn.grid(row=0, column=1, padx=4, pady=4)
    add_sec_btn.grid(row=0, column=2, padx=4, pady=4)
    sub_sec_btn.grid(row=0, column=3, padx=4, pady=4)
    minute_amount_label.grid(row=0, column=4, padx=4, pady=4)
    minute_amount_entry.grid(row=0, column=5, padx=4, pady=4)
    second_amount_label.grid(row=0, column=6, padx=4, pady=4)
    second_amount_entry.grid(row=0, column=7, padx=4, pady=4)
    new_timer_name_label.grid(row=0, column=8, padx=4, pady=4)
    new_timer_entry_name.grid(row=0, column=9, padx=4, pady=4)
    new_timer_button.grid(row=0, column=10, padx=4, pady=4)

    # Buttons and Labels for tasks
    sub_task_count_button = tk.Button(root, text="-1", command=WorkTask.sub_task)
    add_task_count_button = tk.Button(root, text="+1", command=WorkTask.add_task)
    task_name_label = tk.Label(root, text="Task Name:")
    task_name_entry = tk.Entry(root, textvariable=task_var_name)
    task_count_label = tk.Label(root, text="Task Count:")
    task_count_entry = tk.Entry(root, width=3)
    add_new_task_button = tk.Button(root, text="Add Task", command=WorkTask.new_task)

    # Align task button/labels on grid
    sub_task_count_button.grid(row=1, column=2, padx=4, pady=4, sticky='e')
    add_task_count_button.grid(row=1, column=3, padx=4, pady=4, sticky='w')
    task_count_label.grid(row=1, column=4, padx=4, pady=4)
    task_count_entry.grid(row=1, column=5, padx=4, pady=4)
    task_name_label.grid(row=1, column=8, padx=4, pady=4)
    task_name_entry.grid(row=1, column=9, padx=4, pady=4)
    add_new_task_button.grid(row=1, column=10, padx=4, pady=4, ipadx=3)


    # Custom code for remembering countdowns - before saving is implemented
    str_name = "Coding Practice"
    temp_mins = 10
    temp_secs = 0
    first_timer = WorkTimer(str_name, temp_mins, temp_secs)
    first_timer.create_new_timer_button(str_name)

    str_name = "Coding Project"
    temp_mins = 15
    temp_secs = 0
    second_timer = WorkTimer(str_name, temp_mins, temp_secs)
    second_timer.create_new_timer_button(str_name)

    str_name = "Writing Practice"
    temp_mins = 10
    temp_secs = 0
    third_timer = WorkTimer(str_name, temp_mins, temp_secs)
    third_timer.create_new_timer_button(str_name)

    str_name = "Writing Project"
    temp_mins = 15
    temp_secs = 0
    fourth_timer = WorkTimer(str_name, temp_mins, temp_secs)
    fourth_timer.create_new_timer_button(str_name)

    str_name = "Math"
    temp_mins = 15
    temp_secs = 0
    fourth_timer = WorkTimer(str_name, temp_mins, temp_secs)
    fourth_timer.create_new_timer_button(str_name)

    str_name = "Non-fiction Reading"
    temp_mins = 15
    temp_secs = 0
    fourth_timer = WorkTimer(str_name, temp_mins, temp_secs)
    fourth_timer.create_new_timer_button(str_name)

    str_name = "Social Media/YouTube"
    temp_mins = 30
    temp_secs = 0
    fourth_timer = WorkTimer(str_name, temp_mins, temp_secs)
    fourth_timer.create_new_timer_button(str_name)

    str_name = "Wildcard"
    temp_mins = 60
    temp_secs = 0
    fourth_timer = WorkTimer(str_name, temp_mins, temp_secs)
    fourth_timer.create_new_timer_button(str_name)

    temp_mins = 0
    temp_secs = 0


    # start tkinter loop
    root.mainloop()

