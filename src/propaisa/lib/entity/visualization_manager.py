#https://www.geeksforgeeks.org/data-science/data-visualization-different-charts-python/
#multiple bar chart: https://www.geeksforgeeks.org/matplotlib-bar-chart-in-python/
from datetime import datetime
import traceback
from unicodedata import name
import pandas as pd
import matplotlib.pyplot as plt
from lib.entity.expense_manager import Expense, ExpenseManager
class VisualizationManager:
    def __init__(self, db_file):
        self.db_file = db_file
    def on_close(event):
        print('Figure closed. Performing cleanup or next steps...')
    def plot_income_expense_trends(self):
        try:
            list_income_trends=[]
            income_trends=ExpenseManager(self.db_file).get_income_trends()
            for trend in income_trends:
                list_income_trends.append([trend.period, trend.total_income])
            list_expense_trends=[]
            expense_trends=ExpenseManager(self.db_file).get_expense_trends()
            for trend in expense_trends:
                list_expense_trends.append([trend.period, trend.total_expense])
            print(f"Plotting income and expense trends for {len(income_trends)} income records and {len(expense_trends)} expense records.")

            # Convert to DataFrames and specify column names
            df1 = pd.DataFrame(list_income_trends, columns=['period', 'total_income'])
            df2 = pd.DataFrame(list_expense_trends, columns=['period', 'total_expense'])

            # Merge on the common column 'period'
            # Use how='inner', 'left', 'right', or 'outer'
            print(f"Income Trends DataFrame:\n{df1}")
            print(f"Expense Trends DataFrame:\n{df2}")
            merged_df = pd.merge(df1, df2, on='period', how='inner')
            print(f"Master DataFrame:\n{merged_df}")
            merged_list = merged_df.values.tolist()
            data=[]
            period=[]
            total_income=[]
            total_expense=[]
            for row in merged_list:
                data.append([row[0], row[1], row[2]])
                period.append(row[0])
                total_income.append(row[1])
                total_expense.append(row[2])
            print(f"Data for plotting:\n{data}")
            print(f"Period: {period}")
            print(f"Total Income: {total_income}")
            print(f"Total Expense: {total_expense}")

            df_expense_bar = pd.DataFrame({'Period': period , 'Total Income': total_income, 'Total Expense': total_expense})
            bar_colors = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple', 'tab:brown', 'tab:pink']
            ax=df_expense_bar.plot(x="Period"
                                , y=["Total Expense", "Total Income"]
                                    , kind="bar"
                                    , color=bar_colors
                                    , width=0.8
                                    , figsize=(12, 6)
                                    , linewidth=.1)
            plt.ylabel("Interest Amount");        
            ax.tick_params(axis='x', labelrotation=18,labelsize=8)
            for i, p in enumerate(ax.patches):
                height = p.get_height()
                #print(f"height: {height} Index : {i} ")
                ax.text((p.get_x() + p.get_width() / 2)
                        , height/2
                        , f'{height}'
                        , ha='center', va='center', rotation='vertical', color="white", size=6, fontweight='bold')    
            plt.show()
            plt.close()

        except Exception as e:
            print("--- Full Traceback ---")
            traceback.print_exc()
            print("----------------------")
            self.app.main_window.error_dialog("Error", f"An error occurred while importing expenses: {e}")
    def plot_interest_trends(self):
        try:
            list_interest=ExpenseManager(self.db_file).get_interest_trends()
            print(f"Plotting interest trends for {len(list_interest)} interest records.")
            data=[]
            period=[]
            amount=[]
            for interest in list_interest:
                data.append([interest.period, interest.rate])
                period.append(interest.period)
                amount.append(interest.rate)
            df_expense_bar = pd.DataFrame({'Period': period , 'Amount': amount})
            bar_colors = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple', 'tab:brown', 'tab:pink']
            ax=df_expense_bar.plot(x="Period"
                                , y=["Amount"]
                                    , kind="bar"
                                    , color=bar_colors
                                    , width=0.8
                                    , figsize=(12, 6)
                                    , linewidth=.1)
            plt.ylabel("Interest Amount  Paid");        
            ax.tick_params(axis='x', labelrotation=18,labelsize=8)
            for i, p in enumerate(ax.patches):
                height = p.get_height()
                #print(f"height: {height} Index : {i} ")
                ax.text((p.get_x() + p.get_width() / 2)
                        , height/2
                        , f'{height}'
                        , ha='center', va='center', rotation='vertical', color="white", size=6, fontweight='bold')    
            plt.show()
            plt.close()

        except Exception as e:
            print("--- Full Traceback ---")
            traceback.print_exc()
            print("----------------------")
            self.app.main_window.error_dialog("Error", f"An error occurred while importing expenses: {e}")
    def plot_expense_trends(self):
        all_expenses = ExpenseManager(self.db_file).get_expenses()
        print(f"Plotting expense trends for {len(all_expenses)} expenses.")
        data=[]
        name=[]
        amount=[]   
        savedamount=[] 
        settledamount=[]  
        gapamount=[]
        daily_saving_amount=[]
        projected_yearly_interest=[]    
        # Assuming a list of 'User' objects with a 'role' attribute
        active_expenses = [obj for obj in all_expenses if obj.status == 0]  # Assuming 0 means active

        for obj in active_expenses:
            data.append([obj.name, obj.amount, obj.savedamount, obj.settledamount, obj.duedate, obj.userid, obj.categoryid, obj.frequencyid, obj.status])
            name.append(obj.name)
            amount.append(obj.amount)
            savedamount.append(obj.savedamount)
            settledamount.append(obj.settledamount)
            gapamount.append(obj.gapamount)
            daily_saving_amount.append(obj.daily_saving_amount)
            projected_yearly_interest.append(obj.projected_yearly_interest)

        df_master = pd.DataFrame(data, columns=['name', 'amount', 'savedamount', 'settledamount', 'duedate', 'userid', 'categoryid', 'frequencyid', 'status'])
        #print(df_master)
        df_expense_bar = pd.DataFrame({'name': name
                                       , 'amount': amount
                                       , 'savedamount': savedamount
                                       , 'settledamount': settledamount
                                       , 'gapamount': gapamount
                                       , 'daily_saving_amount': daily_saving_amount
                                       , 'projected_yearly_interest': projected_yearly_interest})
        df = df_master.set_index('name')

        # 2. Plot the bar chart
        bar_colors = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple', 'tab:brown', 'tab:pink']
        ax=df_expense_bar.plot(x="name"
                               , y=[
                                   "amount"
                                   , "savedamount"
                                   , "settledamount"
                                   , "gapamount"
                                   , "daily_saving_amount"
                                   , "projected_yearly_interest"]
                                   , kind="bar"
                                   , color=bar_colors
                                   , width=0.8
                                   , figsize=(12, 6)
                                   , linewidth=.1)
        plt.ylabel("Values");        
        ax.tick_params(axis='x', labelrotation=18,labelsize=8)
        for i, p in enumerate(ax.patches):
            height = p.get_height()
            #print(f"height: {height} Index : {i} ")
            ax.text((p.get_x() + p.get_width() / 2)
                    , height/2
                    , f'{height}'
                    , ha='center', va='center', rotation='vertical', color="white", size=6, fontweight='bold')    
        plt.show()
        plt.close()

'''
Unused code for future use
        number_of_rows=len(df_expense_bar)
        num_columns = df_expense_bar.shape[1]
        for i, p in enumerate(ax.patches):
            # Get the height of the bar (the data value)
            height = p.get_height()
            #print(f"height: {height} Index : {i} : numberofrows: {i/number_of_rows}")
            # Get the x position (center it above the bar)
            #x_pos = p.get_x() 
            # Add the text label
            #print(f"Due Date : {df_master.iat[int(i%number_of_rows), 4]} Days remaining: {(datetime.strptime(df_master.iat[int(i%number_of_rows), 4],'%Y-%m-%d %H:%M:%S') - pd.Timestamp.now()).days}")
            
            if(i/number_of_rows>=3):
                #row_index=int(i%number_of_rows)
                #print(f"row_index: {row_index} Amount: {df_expense_bar.iat[row_index, 1]}")
                amount_to_be_saved_per_day = round((df_expense_bar.iat[int(i%number_of_rows), 1] - df_expense_bar.iat[int(i%number_of_rows), 3] - df_expense_bar.iat[int(i%number_of_rows), 2]) / (datetime.strptime(df_master.iat[int(i%number_of_rows), 4],'%Y-%m-%d %H:%M:%S') - pd.Timestamp.now()).days)
                print(f"Amount to be saved per day: {amount_to_be_saved_per_day}")
                if(amount_to_be_saved_per_day>100):
                    ax.text(p.get_x(), df_expense_bar.iat[int(i%number_of_rows), 1], f'{amount_to_be_saved_per_day}', ha='center', va='bottom', color="red", size=8, fontweight='bold')
                else:
                    ax.text(p.get_x(), df_expense_bar.iat[int(i%number_of_rows), 1], f'{amount_to_be_saved_per_day}', ha='center', va='bottom', color="green", size=8, fontweight='bold')

        
        for container in ax.containers:
            #print(container.get_label())
            #print(container.datavalues)
            if(container.get_label() == "gapamount"):
                ax.bar_label(container, labels=df_expense_bar['dayraterequired'], padding=5, color='blue', size=8, fontweight='bold')
        ''' 

    