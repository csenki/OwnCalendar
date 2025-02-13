"""
Simple desktop Calendar
"""
import sys
import os
import locale
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.tooltip import ToolTip
import calendar
import datetime




class CalendarApp(ttk.Window):
    def __init__(self):
        super().__init__(themename="morph")
        #super().__init__()
        self.title("Calendar")
        self.geometry("650x200")
        self.language_code="en"
        if (locale.getlocale()[0] == 'hu_HU') or (locale.getlocale()[0] =="Hungarian_Hungary"):
            print(locale.getlocale()[0])
            self.language_code="hu"


        if ( sys.platform.startswith('win')):
            if os.path.isfile("calendar.ico"):
                self.iconbitmap("calendar.ico")
        else:
            if os.path.isfile("calendar.gif"):
                logo = ttk.PhotoImage(file='calendar.gif')
                self.call('wm', 'iconphoto', self._w, logo)

        # Init curent date
        self.current_year = datetime.datetime.now().year
        self.current_month = datetime.datetime.now().month

        # Left arrow button
        self.left_button = ttk.Button(self, text="←", command=self.previous_month)
        self.left_button.place(x=300, y=5)
        ToolTip(self.left_button,"Prvious month")

        # Rigth arrow button
        self.right_button = ttk.Button(self, text="→", command=self.next_month)
        self.right_button.place(x=360, y=5)
        ToolTip(self.right_button,"Next month")


        self.home_button = ttk.Button(self,bootstyle="info", text="H", command=self.goto_home)
        self.home_button.place(x=335, y=5)
        ToolTip(self.home_button,"Go to current month")


        # Calendar text, only read only
        self.calendar_text = ttk.Text(self, height=8, width=25, bg=self.cget("bg"),
                                     fg="black", font=("Courier", 10), wrap="none",
                                     relief="solid", borderwidth=1, highlightthickness=2, highlightbackground="black")

        self.calendar_text2 = ttk.Text(self, height=8, width=25, bg=self.cget("bg"),
                                     fg="black", font=("Courier", 10), wrap="none",
                                     relief="solid", borderwidth=1, highlightthickness=2, highlightbackground="black")

        self.calendar_text0 = ttk.Text(self, height=8, width=25, bg=self.cget("bg"),
                                     fg="black", font=("Courier", 10), wrap="none",
                                     relief="solid", borderwidth=1, highlightthickness=2, highlightbackground="black")

        self.MONTHS_HU = {
            1: "Január",
            2: "Február",
            3: "Március",
            4: "Április",
            5: "Május",
            6: "Június",
            7: "Július",
            8: "Augusztus",
            9: "Szeptember",
            10: "Október",
            11: "November",
            12: "December"
        }
        self.MONTHS_EN = {
        1: "January",
        2: "February",
        3: "March",
        4: "April",
        5: "May",
        6: "June",
        7: "July",
        8: "August",
        9: "September",
        10: "October",
        11: "November",
        12: "December"
        }

        self.calendar_text.place(x=220, y=35)
        self.calendar_text.config(state="disabled")

        self.calendar_text0.place(x=1, y=35)
        self.calendar_text0.config(state="disabled")

        self.calendar_text2.place(x=430, y=35)
        self.calendar_text2.config(state="disabled")


        # Setting up colours
        self.text_tag_add(self.calendar_text)
        self.text_tag_add(self.calendar_text0)
        self.text_tag_add(self.calendar_text2)
        self.update_calendar()

    def text_tag_add(self,wd:ttk.Text):
        """Add stye tags"""
        wd.tag_configure("header", foreground="blue", font=("Courier", 10, "bold"))
        wd.tag_configure("weekend", foreground="red", font=("Courier", 10, "bold"))
        wd.tag_configure("curdate", background="lightgray", foreground="black",font=("Courier", 10, "bold"))
        wd.tag_configure("curdate_weekend",foreground="red", background="lightgray", font=("Courier", 10, "bold"))
        wd.tag_configure("week_number", foreground="green", font=("Courier", 10, "bold"))

    def date_to_tk(self,year,month,wd:ttk.Text):
        """Upload Text with the Calendar datas"""
        wd.config(state="normal")  #Allow write
        wd.delete("1.0", ttk.END)
        cal = calendar.Calendar(firstweekday=0)  # First day is Monday
        month_calendar = cal.monthdays2calendar(year, month)

        # Moth name
        month_name=self.MONTHS_HU[month]

        if self.language_code=="en":
            month_name=self.MONTHS_EN[month]
        month_name =  f"       {year} {month_name} \n"
        wd.insert(ttk.END, month_name, "header")

        # Headers
        weekdays = ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]
        if self.language_code=="hu":
            weekdays = ["Hé", "Ke", "Sze", "Cs", "Pé", "Sz", "Va"]

        wd.insert(ttk.END, "Wk ")  # week number
        for day in weekdays:
            color_tag = "weekend" if day in ["Sz", "Va","Sa","Su"] else "header"
            wd.insert(ttk.END, f"{day} ", color_tag)
        wd.insert(ttk.END, "\n")
        curdate=datetime.date.today()
        # Naptár tartalma
        for week_index, week in enumerate(month_calendar):
            week_number = datetime.date(year, month, max(1, week[0][0])).isocalendar()[1]
            wd.insert(ttk.END, f"{week_number:2} ", "week_number")  # Hét száma

            for day, weekday in week:
                if day == 0:
                    wd.insert(ttk.END, "   ") # Empty page
                else:
                    cur_cal_date=datetime.date(year,month,day)
                    if curdate == cur_cal_date:
                        tag = "curdate_weekend" if weekday in (5, 6) else "curdate"
                    else:
                        tag = "weekend" if weekday in (5, 6) else "normal"
                    wd.insert(ttk.END, f"{day:2} ", tag)


            wd.insert(ttk.END, "\n")

        wd.config(state="disabled")  # Read only mode


    def update_calendar(self):
        """Updates the calendar display for the current month and year."""
        datestring=str(self.current_year)+"-"+str(self.current_month).zfill(2)+"-01"
        mdate=datetime.datetime.strptime(datestring,"%Y-%m-%d")
        prev_dt = mdate - datetime.timedelta(days = 2)
        prev_month = prev_dt.month
        prev_year = prev_dt.year

        next_dt = mdate + datetime.timedelta(days = 33)
        next_month = next_dt.month
        next_year = next_dt.year

        self.date_to_tk(year=prev_year,month=prev_month, wd=self.calendar_text0 )
        self.date_to_tk(year=self.current_year,month=self.current_month , wd=self.calendar_text )
        self.date_to_tk(year=next_year,month=next_month , wd=self.calendar_text2 )

    def previous_month(self):
        """Handles previous month navigation."""
        if self.current_month == 1:
            self.current_month = 12
            self.current_year -= 1
        else:
            self.current_month -= 1
        self.update_calendar()

    def next_month(self):
        """Handles next month navigation."""
        if self.current_month == 12:
            self.current_month = 1
            self.current_year += 1
        else:
            self.current_month += 1
        self.update_calendar()

    def goto_home(self):
        """Goto current month
        """
        self.current_year = datetime.datetime.now().year
        self.current_month = datetime.datetime.now().month
        self.update_calendar()

if __name__ == "__main__":
    app = CalendarApp()
    app.mainloop()
