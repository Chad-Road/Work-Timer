import tkinter as tk
from tkinter import ttk
import winsound

#need to correct timer so no slow clock incorrectness
#need to change time entry to allow manual number entry and block non-numbers

#maybe save timers with pickling or json

class WorkTimer():
    def __init__(self, name, mins, secs) -> None:
        self.label = tk.Label(text="00:00")
        self.button = tk.Button(text="Start/Stop")
        self.button_row = 1
        self.name = name
        self.mins = mins
        self.secs = secs
        self.counting = False
        self.counting_up = False
        self.counting_down = False
        self.negative_count = False
        self.time_format = f"{self.mins:02d}:{self.secs:02d}"

# Methods to add and subtract minuntes/seconds
    def add_mins():
        global temp_mins
        temp_mins +=1
        minute_amount_entry.delete(0, last=30)
        minute_amount_entry.insert(0, f"{temp_mins}")

    def sub_mins():
        global temp_mins
        temp_mins -= 1
        minute_amount_entry.delete(0, last=30)
        minute_amount_entry.insert(0, f"{temp_mins}")

    def add_secs():
        global temp_secs
        temp_secs += 10
        second_amount_entry.delete(0, last=30)
        second_amount_entry.insert(0, f"{temp_secs}")
    
    def sub_secs():
        global temp_secs
        temp_secs -= 10
        second_amount_entry.delete(0, last=30)
        second_amount_entry.insert(0, f"{temp_secs}")

# Methods to control counting up/down or back up after zero on countdown
    def countdown(self, mins, secs):
        self.counting_down = True
        self.mins = mins
        self.secs = secs
        if self.negative_count == True:
            self.negative_countup()
            return
        if self.mins <= 0 and self.secs <= 0:
            self.negative_countup()
            return
        if self.counting == True:
            if self.secs < 0:
                self.secs = 59
                self.mins -= 1
            self.new_timer_label["text"] = f"{self.mins:02d}:{self.secs:02d}"
            self.secs -= 1
            root.after(1000, self.countdown, self.mins, self.secs)

    def negative_countup(self):
        if self.negative_count == False:
            winsound.Beep(1000, 1000)
        self.negative_count = True
        if self.counting == True:
            if self.secs >= 60:
                self.secs = 0
                self.mins += 1
            self.new_timer_label["text"] = f"- {self.mins:02d}:{self.secs:02d}"
            self.new_timer_label["bg"] = "red"
            self.secs += 1
            root.after(1000, self.negative_countup)

    def countup(self):
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
        if self.counting == True:
            self.counting = False
        elif self.counting_up == True:
            self.counting = True
            self.countup()
        elif self.counting_down == True:
            self.counting = True
            self.countdown(self.mins, self.secs)
        elif self.negative_count == True:
            self.negative_count = False
        else:
            if self.mins == 0 and self.secs == 0:
                self.counting = True
                self.countup()
            else:
                self.counting = True
                self.countdown(self.mins, self.secs)

# To help create new objects with dynamic names
    def new_object():
        global timer_number
        global temp_mins
        global temp_secs
        str_name = string_var_name.get()

        timer_name_list = ['one', 'two' , 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten']
        timer_name_list[timer_number] = WorkTimer(str_name, temp_mins, temp_secs)
        timer_name_list[timer_number].create_new_timer_button(str_name)
        timer_number += 1

# To create and initialize new buttons and labels that are created with new_object
    def create_new_timer_button(self, str_name):
        global button_row
        str_name = str_name.upper()

        self.new_button_label_name = tk.Label(root, text=str_name, font='Ariel 12')
        self.start_stop_btn = tk.Button(root, text=u'\u23F5'+ " " + u'\u23F8', command=self.btn_click)
        self.new_timer_label = tk.Label(root, text=f"{self.mins:02d}:{self.secs:02d}", font="Times 16 bold",
        bg="white")
        self.new_button_label_name.grid(row=button_row, column=0, columnspan=4, padx=4, pady=4, sticky='w')
        self.start_stop_btn.grid(row=button_row, column=5, columnspan= 2, padx=4, pady=4)
        self.new_timer_label.grid(row=button_row, column=7, columnspan= 2, padx=4, pady=4)
        button_row += 1

class WorkTask():
    def __init__(self, name, task_num) -> None:
        self.task_num = task_num

    def new_task():
        global task_count
        global task_number
        task_name = task_var_name.get()

        task_name_list = ['one', 'two' , 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten']
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
new_timer_name_label = tk.Label(root, text="Timer/Task Name")
new_timer_button = tk.Button(root, text="Add Timer", command=WorkTimer.new_object)
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


# custom code for remembering countdowns - before saving is implemented
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


# start tkinter loop
root.mainloop()

