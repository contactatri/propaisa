from datetime import datetime
import pandas as pd
from typing import Dict, Any, ClassVar
from typing import List, Optional
from lib.entity.sqlitemanager import SQLiteManager 
class Nudge:
    def __init__(self, id, name, nudgedate, message, type, sentiment, status=0):
        self.id = id
        self.name = name
        self.nudgedate = nudgedate
        self.message = message
        self.type = type
        self.sentiment = sentiment
        self.status = status
class Interest:
    def __init__(self, period, rate):
        self.period = period
        self.rate = rate
class Expense:
    def __init__(self, id:int=-1, name="Enter Name", amount=0, savedamount=0, settledamount=0, duedate=pd.Timestamp.now(), userid=1, categoryid=1, frequencyid=1, status=0):
        self.id = id
        self.name = name
        self.amount = amount
        self.savedamount = savedamount
        self.settledamount = settledamount
        self.gapamount = 0
        self.daily_saving_amount = 0
        self.projected_yearly_interest = 0
        self.duedate = duedate
        self.userid = userid
        self.categoryid = categoryid
        self.frequencyid = frequencyid
        self.status = status
        self.due_days = 0
        self.nudges=[]
        self.set_gapamount()
        self.set_due_days()
        self.set_daily_saving_amount()
        self.set_projected_yearly_interest()
        self.set_nudges()

    def set_gapamount(self):
        self.gapamount = self.amount - (self.savedamount + self.settledamount)
    def set_due_days(self):
        self.due_days=0
        #if(datetime.strptime(self.duedate,'%Y-%m-%d %H:%M:%S').date() > pd.Timestamp.now().date()):
        if(self.duedate.date() > pd.Timestamp.now().date()):
            self.due_days=(self.duedate - pd.Timestamp.now()).days
    def set_daily_saving_amount(self):
        self.daily_saving_amount = round(self.gapamount / self.due_days) if self.due_days > 0 else 0
    def set_projected_yearly_interest(self):
        self.projected_yearly_interest = round(self.gapamount * 0.24)
    def set_nudges(self):
        if self.gapamount > 0:
            if self.due_days <=7:
                nudge_message=f"Your expense '{self.name}' is due in {self.due_days} days. Please ensure you have saved enough to cover the amount of {self.gapamount}."
                nudge=Nudge(0, f"Nudge for {self.name}", {pd.Timestamp.now().to_pydatetime()}, nudge_message, "Due Date Nudge",-1, 0)
                self.nudges.append(nudge)
            if self.daily_saving_amount > 100:
                nudge_message=f"Your daily saving amount for expense '{self.name}' is {self.daily_saving_amount:.2f}. Consider adjusting your savings plan."
                nudge=Nudge(0, f"Nudge for {self.name}", pd.Timestamp.now().to_pydatetime(), nudge_message, "High Daily Saving Nudge",0, 0)
                self.nudges.append(nudge)
            if self.projected_yearly_interest > 500:
                nudge_message=f"Your projected yearly interest for expense '{self.name}' is {self.projected_yearly_interest:.2f}. Look for better saving options."
                nudge=Nudge(0, f"Nudge for {self.name}", pd.Timestamp.now().to_pydatetime(), nudge_message, "High Interest Nudge",-1, 0)
                self.nudges.append(nudge)
            if (self.gapamount/self.amount) < 0.2:
                nudge_message=f"Your have amlost reached the goal for '{self.name}' is {self.projected_yearly_interest:.2f}. Great work. You have saved lot on possible interest."
                nudge=Nudge(0, f"Nudge for {self.name}", pd.Timestamp.now().to_pydatetime(), nudge_message, "High Interest Nudge",1, 0)
                self.nudges.append(nudge)
        return 0
    def to_dictionary(self):
        return {
            "id": self.id,
            "name": self.name,
            "amount": self.amount,
            "savedamount": self.savedamount,
            "settledamount": self.settledamount,
            "gapamount": self.gapamount,
            "daily_saving_amount": self.daily_saving_amount,
            "projected_yearly_interest": self.projected_yearly_interest,
            "duedate": self.duedate.strftime('%Y-%m-%d %H:%M:%S'),
            "userid": self.userid,
            "categoryid": self.categoryid,
            "frequencyid": self.frequencyid,
            "status": self.status
        }