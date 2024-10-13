from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.spinner import Spinner

from kivy.uix.textinput import TextInput
from kivy.uix.dropdown import DropDown
from datetime import datetime, timedelta
import json
import os
from kivy.properties import DictProperty
from matplotlib import pyplot as plt
from kivy.properties import ObjectProperty
import calendar
from kivy.uix.gridlayout import GridLayout


shared_themes = DictProperty({
    'light': {
        'bg_color': [0.2, 0.1, 0.4, 1],
        'text_color': [1, 1, 1, 1],
        'btn_bg_color': [0.1, 0.6, 0.9, 1],
        'input_bg_color': [0.3, 0.2, 0.5, 1],
        'border_color': [0.5, 0.3, 0.8, 1]
    },
    'dark': {
        'bg_color': [0.05, 0.02, 0.1, 1],
        'text_color': [0.9, 0.9, 0.9, 1],
        'btn_bg_color': [0.15, 0.45, 0.75, 1],
        'input_bg_color': [0.2, 0.1, 0.3, 1],
        'border_color': [0.4, 0.3, 0.6, 1]
    }
})

class CustomDatePicker(Popup):
    callback = ObjectProperty(None)  # Function to call with selected date

    def __init__(self, callback, **kwargs):
        super(CustomDatePicker, self).__init__(**kwargs)
        self.callback = callback
        self.title = "Select Date"
        self.size_hint = (0.9, 0.9)

        self.selected_date = None

        self.current_date = datetime.now()

        self.layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        # Header with month and year navigation
        header = BoxLayout(size_hint_y=None, height=40, spacing=10)

        self.prev_month_btn = Button(text="<", size_hint_x=None, width=40)
        self.prev_month_btn.bind(on_press=self.show_prev_month)
        header.add_widget(self.prev_month_btn)

        self.month_year_label = Label(text=self.current_date.strftime("%B %Y"), font_size=18)
        header.add_widget(self.month_year_label)

        self.next_month_btn = Button(text=">", size_hint_x=None, width=40)
        self.next_month_btn.bind(on_press=self.show_next_month)
        header.add_widget(self.next_month_btn)

        self.layout.add_widget(header)

        # Weekday labels
        weekdays = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
        weekday_layout = GridLayout(cols=7, size_hint_y=None, height=30)

        for day in weekdays:
            lbl = Label(text=day, font_size=14)
            weekday_layout.add_widget(lbl)

        self.layout.add_widget(weekday_layout)

        # Dates grid
        self.dates_grid = GridLayout(cols=7,height=200, spacing=5, size_hint_y=4)
        self.dates_grid.bind(minimum_height=self.dates_grid.setter('height'))
       
        self.layout.add_widget(self.dates_grid)

        self.update_calendar()

        # Cancel and Confirm buttons
        footer = BoxLayout(size_hint_y=None, height=40, spacing=10)

        cancel_btn = Button(text="Cancel")
        cancel_btn.bind(on_press=self.dismiss)
        footer.add_widget(cancel_btn)

        confirm_btn = Button(text="Confirm")
        confirm_btn.bind(on_press=self.confirm_selection)
        footer.add_widget(confirm_btn)

        self.layout.add_widget(footer)

        self.content = self.layout

    def select_day(self, instance):
        

        day = int(instance.text)
        self.selected_date = self.current_date.replace(day=day)
        # Highlight the selected day (optional)
        print(self.selected_date)

    def update_calendar(self):
        self.dates_grid.clear_widgets()

        year = self.current_date.year
        month = self.current_date.month

        # Get first weekday and number of days in month
        first_weekday, num_days = calendar.monthrange(year, month)

        # Adjust first_weekday to start from Sunday (0)
        first_weekday = (first_weekday + 1) % 7

        # Add blank labels for days before the first day
        for _ in range(first_weekday):
            self.dates_grid.add_widget(Label(text=''))

        # Add buttons for each day
        for day in range(1, num_days + 1):
            btn = Button(text=str(day))
            self.dates_grid.add_widget(btn)
            btn.bind(on_press=self.select_day)
         
            
            
              
       

        # Fill the remaining cells of the grid with empty labels
        total_cells = first_weekday + num_days
        remaining = (7 - total_cells % 7) % 7
        for _ in range(remaining):
            self.dates_grid.add_widget(Label(text=''))

        # Update the month-year label
        self.month_year_label.text = self.current_date.strftime("%B %Y")

    def show_prev_month(self, instance):
        first_day_current_month = self.current_date.replace(day=1)
        prev_month_last_day = first_day_current_month - timedelta(days=1)
        self.current_date = prev_month_last_day.replace(day=1)
        self.update_calendar()

    def show_next_month(self, instance):
        days_in_current_month = calendar.monthrange(self.current_date.year, self.current_date.month)[1]
        first_day_next_month = self.current_date + timedelta(days=days_in_current_month)
        self.current_date = first_day_next_month.replace(day=1)
        self.update_calendar()

   

    def confirm_selection(self, instance):
        #instance= self.current_date
        
        if self.selected_date:

            selected_date_str = self.selected_date.strftime('%Y-%m-%d')
            print(selected_date_str)    
            if self.callback:
                self.callback(selected_date_str)
            self.dismiss()
        else:
            # No date selected, show a message or ignore
            popup = Popup(
                title="No Date Selected",
                content=Label(text="Please select a date before confirming."),
                size_hint=(None, None),
                size=(300, 200)
            )
            popup.open()
            
 
        # You can implement visual feedback here if desired
# Custom DropDown Class
class CustomDropDown(DropDown):
    def __init__(self, **kwargs):
        super(CustomDropDown, self).__init__(**kwargs)
        self.theme = None  # To hold the current theme

    def set_theme(self, theme):
        self.theme = theme
        for child in self.children:
            child.background_color = self.theme['input_bg_color']
            child.color = self.theme['text_color']


# Custom Spinner Class
class CustomSpinner(Spinner):
    dropdown_cls = CustomDropDown  # Set the dropdown_cls to the class type

    def __init__(self, theme, **kwargs):
        super(CustomSpinner, self).__init__(**kwargs)
        self.theme = theme  # Store the theme
        self.bind(on_select=self.on_select)  # Bind selection event
        self.dropdown = self.dropdown_cls()  # Create dropdown instance
        self.dropdown.set_theme(self.theme)  # Set theme for dropdown

    def on_select(self, instance, value):
        self.text = value
        print(f'Selected category: {value}')

    def set_theme(self, theme):
        self.theme = theme
        self.background_color = theme['input_bg_color']
        self.color = theme['text_color']
        self.dropdown.set_theme(theme)  # Set theme for dropdown


class LoginScreen(Screen):
    themes = shared_themes  # Use shared themes for light and dark modes

    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.current_mode = 'light'  # Default theme mode
        self.create_ui()  # Initialize the UI

    def create_ui(self):
        # Create the layout for the login form
        layout = BoxLayout(orientation='vertical', padding=50, spacing=20)

        # Username input field
        self.username_input = TextInput(hint_text="Username")
        layout.add_widget(self.username_input)

        # Password input field
        self.password_input = TextInput(hint_text="Password", password=True)
        layout.add_widget(self.password_input)

        # Login button
        self.login_button = Button(text="Login", on_press=self.verify_credentials)
        layout.add_widget(self.login_button)

        # Theme toggle button
        self.theme_toggle_button = Button(text="Dark Mode", on_press=self.toggle_theme)
        layout.add_widget(self.theme_toggle_button)

        # Add the layout to the screen
        self.add_widget(layout)
        self.apply_theme()  # Apply the initial theme

    def verify_credentials(self, instance):
        username = self.username_input.text.strip()
        password = self.password_input.text.strip()

        # Simple authentication logic
        if username == 'user' and password == 'pass':
            # Clear inputs
            self.username_input.text = ''
            self.password_input.text = ''
            # Switch to WalletScreen
            self.manager.current = 'wallet'
        else:
            # Show an error popup if login fails
            popup = Popup(
                title="Login Failed",
                content=Label(text="Invalid username or password"),
                size_hint=(None, None),
                size=(300, 200)
            )
            popup.open()

    def toggle_theme(self, instance):
        # Toggle between light and dark mode
        if self.current_mode == 'light':
            self.current_mode = 'dark'
            self.theme_toggle_button.text = "Light Mode"
        else:
            self.current_mode = 'light'
            self.theme_toggle_button.text = "Dark Mode"

        # Apply the selected theme
        self.apply_theme()

    def apply_theme(self):
        theme = self.themes[self.current_mode]
        Window.clearcolor = theme['bg_color']

        # Update text input and button colors
        self.username_input.background_color = theme['input_bg_color']
        self.username_input.foreground_color = theme['text_color']

        self.password_input.background_color = theme['input_bg_color']
        self.password_input.foreground_color = theme['text_color']

        self.login_button.background_color = theme['btn_bg_color']
        self.login_button.color = theme['text_color']

        self.theme_toggle_button.background_color = theme['btn_bg_color']
        self.theme_toggle_button.color = theme['text_color']

    def on_pre_enter(self):
        # Ensure the theme is applied when entering the screen
        self.apply_theme()


KV = '''
<WalletScreen>:
    BoxLayout:
        orientation: 'vertical'

        Label:
            text: 'Income: $' + str(root.total_income)
        Label:
            text: 'Expense: $' + str(root.total_expense)
        Label:
            text: 'Remaining Amount: $' + str(root.remaining_amount)

        BoxLayout:
            orientation: 'horizontal'
            Label:
                text: 'From:'
            Button:
                text: root.from_date.strftime('%Y-%m-%d') if root.from_date else 'Select Date'
                on_release: root.open_calendar('from')
            Label:
                text: 'To:'
            Button:
                text: root.to_date.strftime('%Y-%m-%d') if root.to_date else 'Select Date'
                on_release: root.open_calendar('to')

        Button:
            text: 'Show Overview'
            on_release: root.show_overview()

        Label:
            id: overview_label
            text: ''
'''

class CustomSpinnerOption(Button):
    def __init__(self, **kwargs):
        super(CustomSpinnerOption, self).__init__(**kwargs)
        self.background_color = [0.3, 0.2, 0.5, 1]
        self.color = [0.9, 0.9, 0.9, 1]


class WalletScreen(Screen):
    themes = DictProperty({
        'light': {
            'bg_color': [0.2, 0.1, 0.4, 1],
            'text_color': [1, 1, 1, 1],
            'btn_bg_color': [0.1, 0.6, 0.9, 1],
            'input_bg_color': [0.3, 0.2, 0.5, 1],
            'border_color': [0.5, 0.3, 0.8, 1]
        },
        'dark': {
            'bg_color': [0.05, 0.02, 0.1, 1],
            'text_color': [0.9, 0.9, 0.9, 1],
            'btn_bg_color': [0.15, 0.45, 0.75, 1],
            'input_bg_color': [0.2, 0.1, 0.3, 1],
            'border_color': [0.4, 0.3, 0.6, 1]
        }
    })

    data_file = "data.json"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.expenses = []
        self.incomes = []

        self.current_mode = 'light'

        self.load_data()

        # Main Layout
        self.main_layout = BoxLayout(orientation="vertical", padding=20, spacing=20)

        # Top Layout (Save, Load, Theme Toggle)
        self.top_layout = BoxLayout(size_hint_y=None, height="40dp")

        # Save Button
        self.save_btn = Button(
            text="Save",
            on_press=self.save_notify,
            size_hint_x=None,
            width="100dp",
            background_color=self.themes['light']['btn_bg_color'],
            color=self.themes['light']['text_color'],
            background_normal=''
        )

        # Load Button
        self.load_btn = Button(
            text="Load",
            on_press=self.load_notify,
            size_hint_x=None,
            width="100dp",
            background_color=self.themes['light']['btn_bg_color'],
            color=self.themes['light']['text_color'],
            background_normal=''
        )

        self.top_layout.add_widget(self.save_btn)
        self.top_layout.add_widget(self.load_btn)
        self.top_layout.add_widget(BoxLayout())  # Spacer

        # Theme Toggle Button
        self.theme_toggle_btn = Button(
            text="Dark Mode",
            size_hint_x=None,
            width="150dp",
            on_press=self.toggle_theme,
            background_color=self.themes['light']['btn_bg_color'],
            color=self.themes['light']['text_color'],
            background_normal='',
            background_down=''
        )
        self.top_layout.add_widget(self.theme_toggle_btn)

        self.main_layout.add_widget(self.top_layout)

        # Expense Input Layout
        self.expense_input_layout = BoxLayout(size_hint_y=None, height="50dp", spacing=10)
        self.expense_input = TextInput(
            hint_text="Enter Expense Amount",
            multiline=False,
            background_color=self.themes['light']['input_bg_color'],
            foreground_color=self.themes['light']['text_color'],
            padding=(10, 10)
        )
        self.expense_category = Spinner(
            text='Select Category',
            values=('Food', 'Transportation', 'Entertainment', 'Bills', 'Others'),
            #option_cls=CustomSpinnerOption,
           
            background_color=self.themes['light']['btn_bg_color'],
            color=self.themes['light']['text_color'],
            background_normal=''
            
           
        )

        self.add_expense_btn = Button(
            text="Add Expense",
            on_press=self.add_expense,
            background_color=self.themes['light']['btn_bg_color'],
            color=self.themes['light']['text_color'],
            background_normal='',
        )
        self.expense_input_layout.add_widget(self.expense_input)
        self.expense_input_layout.add_widget(self.expense_category)
        self.expense_input_layout.add_widget(self.add_expense_btn)

        self.main_layout.add_widget(self.expense_input_layout)

        # Income Input Layout
        self.income_input_layout = BoxLayout(size_hint_y=None, height="50dp", spacing=10)
        self.income_input = TextInput(
            hint_text="Enter Income Amount",
            multiline=False,
            background_color=self.themes['light']['input_bg_color'],
            foreground_color=self.themes['light']['text_color'],
            padding=(10, 10)
        )
        self.add_income_btn = Button(
            text="Add Income",
            on_press=self.add_income,
            background_color=self.themes['light']['btn_bg_color'],
            color=self.themes['light']['text_color'],
            background_normal=''
        )
        self.income_input_layout.add_widget(self.income_input)
        self.income_input_layout.add_widget(self.add_income_btn)

        self.main_layout.add_widget(self.income_input_layout)

        # Buttons Layout (Overview and Calendar)
        self.buttons_layout = BoxLayout(size_hint_y=None, height="40dp", spacing=10)

        self.overview_btn = Button(
            text="Show Overview",
            on_press=self.show_overview,
            background_color=self.themes['light']['btn_bg_color'],
            color=self.themes['light']['text_color'],
            background_normal=''
        )

        self.calendar_btn = Button(
            text="Select Date Range",
            on_press=self.open_calendar_popup,
            background_color=self.themes['light']['btn_bg_color'],
            color=self.themes['light']['text_color'],
            background_normal=''
        )

        self.buttons_layout.add_widget(self.overview_btn)
        self.buttons_layout.add_widget(self.calendar_btn)

        self.main_layout.add_widget(self.buttons_layout)

        self.add_widget(self.main_layout)

        self.apply_theme()

    def toggle_theme(self, instance):
        if self.current_mode == 'light':
            self.current_mode = 'dark'
            self.theme_toggle_btn.text = "Light Mode"
        else:
            self.current_mode = 'light'
            self.theme_toggle_btn.text = "Dark Mode"
        self.apply_theme()

    def apply_theme(self):
        theme = self.themes[self.current_mode]
        Window.clearcolor = theme['bg_color']

        # Apply theme to expense input
        self.expense_input.background_color = theme['input_bg_color']
        self.expense_input.foreground_color = theme['text_color']
        self.expense_category.background_color = theme['btn_bg_color']
        self.expense_category.color = theme['text_color']

        # Apply theme to add expense button
        self.add_expense_btn.background_color = theme['btn_bg_color']
        self.add_expense_btn.color = theme['text_color']

        # Apply theme to income input
        self.income_input.background_color = theme['input_bg_color']
        self.income_input.foreground_color = theme['text_color']

        # Apply theme to add income button
        self.add_income_btn.background_color = theme['btn_bg_color']
        self.add_income_btn.color = theme['text_color']

        # Apply theme to overview and calendar buttons
        self.overview_btn.background_color = theme['btn_bg_color']
        self.overview_btn.color = theme['text_color']
        self.calendar_btn.background_color = theme['btn_bg_color']
        self.calendar_btn.color = theme['text_color']

        # Apply theme to top buttons
        self.save_btn.background_color = theme['btn_bg_color']
        self.save_btn.color = theme['text_color']
        self.load_btn.background_color = theme['btn_bg_color']
        self.load_btn.color = theme['text_color']

        # Update theme toggle button directly
        self.theme_toggle_btn.background_color = theme['btn_bg_color']
        self.theme_toggle_btn.color = theme['text_color']

    def add_expense(self, instance):
        try:
            amount = float(self.expense_input.text)
            category = self.expense_category.text
            if category == 'Select Category':
                raise ValueError("Category not selected")
            date_str = datetime.now().strftime('%Y-%m-%d')
            self.expenses.append({'amount': amount, 'category': category, 'date': date_str})
            self.expense_input.text = ""
            self.expense_category.text = "Select Category"
            self.show_message("Expense Added Successfully!")
        except ValueError as e:
            self.show_message(f"Invalid Input: {str(e)}")

    def add_income(self, instance):
        try:
            amount = float(self.income_input.text)
            date_str = datetime.now().strftime('%Y-%m-%d')
            self.incomes.append({'amount': amount, 'date': date_str})
            self.income_input.text = ""
            self.show_message("Income Added Successfully!")
        except ValueError:
            self.show_message("Invalid Input: Please enter a valid amount.")

    def show_message(self, message):
        theme = self.themes[self.current_mode]
        popup = Popup(
            title='Message',
            content=Label(text=message, color=theme['text_color']),
            size_hint=(None, None),
            size=(300, 200)
        )
        popup.open()

    def show_overview(self, instance):
        total_expenses = sum(item['amount'] for item in self.expenses)
        total_income = sum(item['amount'] for item in self.incomes)
        remaining_budget = total_income - total_expenses

        self.create_pie_chart()

        overview_message = (
            f"Total Income: ${total_income:.2f}\n"
            f"Total Expenses: ${total_expenses:.2f}\n"
            f"Remaining Budget: ${remaining_budget:.2f}"
        )
        theme = self.themes[self.current_mode]
        overview_popup = Popup(
            title='Budget Overview',
            content=Label(text=overview_message, color=theme['text_color']),
            size_hint=(None, None),
            size=(300, 200)
        )
        overview_popup.open()

    def create_pie_chart(self):
        categories = {}
        for item in self.expenses:
            category = item['category']
            amount = item['amount']
            categories[category] = categories.get(category, 0) + amount

        if categories:
            labels = list(categories.keys())
            sizes = list(categories.values())

            plt.figure(figsize=(5, 5))
            plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
            plt.axis('equal')
            plt.title('Expense Distribution')
            plt.savefig('expense_chart.png')
            plt.close()

            if os.name == 'nt':  # Windows
                os.startfile('expense_chart.png')
            elif os.name == 'Darwin':  # macOS
                os.system('open expense_chart.png')
            else:  # Linux and others
                os.system('xdg-open expense_chart.png')

    def save_data(self, instance):
        data = {
            'expenses': self.expenses,
            'incomes': self.incomes
        }

        try:
            with open(self.data_file, 'w') as f:
                json.dump(data, f)
            self.show_message("Data saved successfully!")
        except Exception as e:
            self.show_message(f"Error saving data: {str(e)}")

    def save_notify(self, instance):
        self.save_data(instance)

    def load_data(self):
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    data = json.load(f)
                    self.expenses = data.get('expenses', [])
                    self.incomes = data.get('incomes', [])
            except Exception as e:
                self.show_message(f"Error loading data: {str(e)}")
                self.expenses = []
                self.incomes = []
        else:
            self.expenses = []
            self.incomes = []

    def load_notify(self, instance):
        self.load_data()
        self.show_message("Data loaded successfully!")

    def open_calendar_popup(self, instance):
        # Initialize the CustomDatePicker for From Date
        self.date_picker_from = CustomDatePicker(callback=self.on_save_from_date)
        self.date_picker_from.open()

    def on_save_from_date(self, selected_date_str):
        self.from_date_str = selected_date_str
        self.show_message(f"From Date Selected: {self.from_date_str}")

        # Initialize the CustomDatePicker for To Date
        self.date_picker_to = CustomDatePicker(callback=self.on_save_to_date)
        self.date_picker_to.open()

    def on_save_to_date(self, selected_date_str):
        self.to_date_str = selected_date_str
        self.show_message(f"To Date Selected: {self.to_date_str}")
        self.filter_date_range()

    def filter_date_range(self):
        from_date_str = getattr(self, 'from_date_str', None)
        to_date_str = getattr(self, 'to_date_str', None)

        if not from_date_str or not to_date_str:
            self.show_message("Please select both From and To dates.")
            return

        try:
            from_date = datetime.strptime(from_date_str, '%Y-%m-%d').date()
            to_date = datetime.strptime(to_date_str, '%Y-%m-%d').date()

            if from_date > to_date:
                raise ValueError("From Date cannot be after To Date.")

            # Filter expenses
            filtered_expenses = [
                item for item in self.expenses
                if from_date <= datetime.strptime(item['date'], '%Y-%m-%d').date() <= to_date
            ]

            # Filter incomes
            filtered_incomes = [
                item for item in self.incomes
                if from_date <= datetime.strptime(item['date'], '%Y-%m-%d').date() <= to_date
            ]

            total_expenses = sum(item['amount'] for item in filtered_expenses)
            total_income = sum(item['amount'] for item in filtered_incomes)
            amount_saved = total_income - total_expenses

            message = (
                f"From: {from_date_str}\nTo: {to_date_str}\n\n"
                f"Total Income: ${total_income:.2f}\n"
                f"Total Expenses: ${total_expenses:.2f}\n"
                f"Amount Saved: ${amount_saved:.2f}"
            )

            theme = self.themes[self.current_mode]
            overview_popup = Popup(
                title="Date Range Overview",
                content=Label(text=message, color=theme['text_color']),
                size_hint=(None, None),
                size=(400, 300)
            )
            overview_popup.open()

        except ValueError as ve:
            self.show_message(f"Invalid Date: {str(ve)}")

    def on_pre_enter(self):
        self.apply_theme()

class MyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(WalletScreen(name='wallet'))
        return sm


if __name__ == '__main__':
    MyApp().run()
