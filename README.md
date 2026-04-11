# Pro Paisa Application

## Objective
The application tries to provide behavorial nudges to aid dialy wagers to handle their income and try to to reach their goal of **financial independence**.
This application helps the daily or the weekly wagers where they are unable to visualize their projected income and match the expenses accordingly.

## A brief history of ProPaisa
How did i get the idea of ProPaisa.
To be enterted
#### Current Version 1.0.0.12

## Key Features

* Expense Category Management
    * Create Expense Category
    * Update Expense Category
    * Delete Expense Category
* Frequency Management
    * Create Frequency
    * Update Frequency
* Expense Management
    * List of active/unsettled expenses
    * List of archived expenses
    * Create New Expense 
    * Update Expense
* Income Management
    * List of incomes captured
    * Create New Income
* Visualization Management
    * Expenses trends for the current month
    * Income and expenses trends
    * Interest trends over the period of capture
* Nudge Viewer
    * Alert to highlight the upcomming expenses that are required within next N (configurable) days
    * Alert to highlight if the daily savings required to settle the expense is more than N (configurable)
    * Alert to higghlight if the projected yearly interest is higher than N (configurable)
    * Positive reinforcement is 80% (configurable) of the amount has been saved or settled
* System Management
    * Import expense csv file
    * Export expense csv file
## Expense Management
In this module, the user can capture the details of their expenses. The key fields that are captured are:
* Brief description of the expenses
* Amount
* Amount already saved
* Amount alreadyy settled
* Category of the expenses
* Due date
* Status (Paid/Unpaid)
Following fields are autocalcuated
* Gap amount
* Projected interest is the required amount is not reached
The data is provided as two separate lists
* Active expenses that have not been paid
* Archived expenses that have been paid and closed
The expenses can be enterted and updated anytime during the period

## Income Management
This module captures the income details of the user. The amount could be daily, weekly, fortnighlty or monthly. The system aggregates on a monthly basis for all intents and purpose.
Key fields captured are
* Amount
* Brief description
* Data of record
The list of the incomes over a period of time can be viewed as list in this module
#### Note : Version 1.0.0.12 does not support updating the income details. Future version will include this feature

## Visualization Module
This module provides three key visual artefacts
* A grouped bar chart of the active expenses, their amount, saved/settleda amount, projected interest. This gives a visual cue to the user to fill the required gap
*  Income-Expenses Trends. This graph shows the accumulated income per month and the expenses projected for the same period. This gives the visual cue to the users to realise where they are mismanaging their available funds
* Interest Trends. This graphs provides the visual representation of the interest paid by them to money lenders have matured. Ideally this should be a reduction graph to highlight that the interest paid is comming down month by month.

## Technical Details
The application has been developed in python using [Beeware](https://tutorial.beeware.org/),which is a framework to develop application for Web, Android and iOS devices. [Toga](https://toga.beeware.org/en/stable/) is used for all controls used in the application.

### How to install 

#### Get the latest version of the application from [ProPaisa]()

#### Execute `briefcase dev`

### To build Android APK package

#### Execute `briefcase build android`

#### Copy the apk file to mobile device usually found at `\android\gradle\app\build\outputs\apk\debug`

## How was the experiment conducted

### Phase 1
I identified 30 willing daily wagers who had android mobile devices to test ProPaisa.
Since the application is not published in Playstore, I build the application and copied the apk file manually to their devices and installed it for them. Since the application doesnt need network connection, it was quite safe for their usage.
I helped them enter the details for the first few days. Given the simple user interface provided, they become conversant very soon.
The experiment started in the Mid of September 2025 and I let them enter data for ~ 3 months and then using the export functionality, got the csv file and copied to my laptop for detailed analysis.

### Phase 1 Fundings

To be enterted

### Phase 2
Following the positive feedback from the users, I identified 45 more people for the experiment (with the help of my existing users, this was relatively easier). I followed the same process and helped the new users for the first few days.
The experiment started in the Mid of Jan 2026 and I let them enter data for ~ 3 months and then using the export functionality, got the csv file and copied to my laptop for detailed analysis.

### Phase 2 Fundings

To be enterted

## Key observations and findings

The people were not short of earnings, but since it was spread across the entire month, they could not visualize the total income and the expenses for each month. Some days, when they had higher cash flow, they ended up spending on fancy expenses instead of saving for more importtant things. It was not that they did not have the control, but mostly because they could not visualize this.
Income-Expense and Expense trends graph helped them visualize this easily.

The nudges provided for each expenses really helped them bring in more discipline which ended in they taking lesser loan from loan-sharks which ultimately meant they spent lesser amount on additional interests.

Interest graph help them visual this easily.

## Conclusion
TBD

## General Warning
### Note: The application does not transmit any data to the cloud or store them in the cloud. All data are captured with the local repository which the users can clear when required. 

