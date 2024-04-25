import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import Tk, filedialog, messagebox, Button, Entry, Label, StringVar,Frame ,OptionMenu
import os

#defining the Focasting Case Analysis function
def load_data(filepath):
    return pd.read_csv(filepath)

def calculate_monthly_effective_rate(nominal_rate):
    return (1 + nominal_rate / 12) ** 12 - 1

def calculate_future_worth(data, rate):
    future_worths = {}
    for case in data['FORECASTING CASE'].unique():
        amounts = data[data['FORECASTING CASE'] == case]['AMOUNT']
        monthly_effective_rate = calculate_monthly_effective_rate(rate)
        future_amounts = amounts * (1 + monthly_effective_rate) ** (12 - data[data['FORECASTING CASE'] == case]['MONTH'].astype(int))
        future_worths[case] = future_amounts.sum()
    return future_worths

def plot_cash_flows(data, rate, folder_path):
    for case in data['FORECASTING CASE'].unique():
        fig, ax = plt.subplots()
        amounts = data[data['FORECASTING CASE'] == case]['AMOUNT']
        monthly_effective_rate = calculate_monthly_effective_rate(rate)
        future_amounts = -amounts * (1 + monthly_effective_rate) ** (12 - data[data['FORECASTING CASE'] == case]['MONTH'].astype(int))
        bars = ax.bar(range(1, 13), future_amounts, color='blue')
        future_worth_bar = ax.bar(12, -future_amounts.sum(), color='orange')
        for bar in future_worth_bar:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2, height, f'{height:.0f}', ha='center', va='bottom', color='black', fontsize=8)
        ax.set_xlabel('Month')
        ax.set_ylabel('Future Worth')
        ax.set_xticks(range(1, 13))  
        title = f'Cash Flow Diagram for Forecasting Case {case}'
        ax.set_title(title)
        plt.tight_layout()
        plt.savefig(os.path.join(folder_path, f'{title}.png'))
        plt.close(fig)

def plot_summary(future_worths, folder_path):
    fig, ax = plt.subplots()
    cases = list(future_worths.keys())
    values = list(future_worths.values())
    bars = ax.bar(cases, values)
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, height, f'{height:.0f}', ha='center', va='bottom', color='black', fontsize=8)
    ax.set_xlabel('Forecasting Case')
    ax.set_ylabel('Future Worth')
    ax.set_xticks(cases)  
    title = 'Summary of Future Worth by Forecasting Case'
    ax.set_title(title)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(os.path.join(folder_path, f'{title}.png'))
    plt.close(fig)

#defining the functions for the economic equivalence calculator
def calculate_future_worth_calculator(P, r, n):
    FW = P * ((1+r)**n)
    return FW
def calculate_present_worth(F, r, n):
    PW = F / (1 + r)** n
    return PW
def calculate_future_worth_annual_series(A, r, n):
    FW = A * ((1 + r)**n - 1) / r
    return FW
def calculate_period_payment_from_future_worth(F, r, n):
    A = F * (r / ((1 + r)**n - 1))
    return A
def calculate_present_worth_annual_series(A, r, n):
    PW = A * ((1 + r)**n - 1) / (r * (1 + r)**n)
    return PW
def calculate_period_payment_from_present_worth(P, r, n):
    A = P * ((r * (1 + r)**n) / ((1 + r)**n - 1))
    return A

#defining the main function
def main():
    root = Tk()
    root.title("Time Series Economic Analyzer")
    
    # Create frames for each section
    main_frame = Frame(root)
    econ_frame = Frame(root)

    def open_file():
        filepath = filedialog.askopenfilename(title="Select CSV file", filetypes=[("CSV files", "*.csv")])
        if filepath:
            data[0] = load_data(filepath)
            file_label.config(text=filepath)

    def save_to():
        folder_path = filedialog.askdirectory(title="Select Folder to Save Figures")
        if folder_path:
            folder.set(folder_path)
            folder_label.config(text=folder_path)

    def calculate():
        if data[0] is not None and rate.get() and folder.get():
            future_worths = calculate_future_worth(data[0], float(rate.get()))
            plot_cash_flows(data[0], float(rate.get()), folder.get())
            plot_summary(future_worths, folder.get())
            messagebox.showinfo("Complete", "Analysis and plotting complete!")

    def switch_frame(frame):
        frame.tkraise()

    data = [None]  # Use a list to hold the DataFrame
    folder = StringVar()
    rate = StringVar()

    # Focasting Case Analysis section
    Button(main_frame, text="Open File", command=open_file).pack(pady=5, padx=100)
    file_label = Label(main_frame, text="")
    file_label.pack(pady=5, padx=100)
    Label(main_frame, text="Enter the nominal interest rate (annual):").pack(pady=5, padx=100)
    Entry(main_frame, textvariable=rate).pack(pady=1, padx=100)
    Button(main_frame, text="Save to", command=save_to).pack(pady=5, padx=100)
    folder_label = Label(main_frame, text="")
    folder_label.pack(pady=5, padx=100)
    Button(main_frame, text="Calculate", command=calculate).pack(pady=5, padx=100)
    Button(main_frame, text="Switch to Economic Equivalence Calculator", command=lambda: switch_frame(econ_frame)).pack(pady=5, padx=100)

    # Economic Equivalence Calculator section
    Label(econ_frame, text="Select Analysis Mode:").pack(pady=5, padx=100)
    analysis_mode = StringVar()
    analysis_mode.set("calculate_future_worth")  # default value
    modes = ["calculate_future_worth", "calculate_present_worth", "calculate_future_worth_annual_series", 
            "calculate_period_payment_from_future_worth", "calculate_present_worth_annual_series", 
            "calculate_period_payment_from_present_worth"]
    OptionMenu(econ_frame, analysis_mode, *modes).pack(pady=5, padx=100)

    Label(econ_frame, text="Enter P (Principal/Annual Payment):").pack(pady=5, padx=100)
    P = StringVar()
    Entry(econ_frame, textvariable=P).pack(pady=5, padx=100)

    Label(econ_frame, text="Enter r (Rate of interest per period):").pack(pady=5, padx=100)
    r = StringVar()
    Entry(econ_frame, textvariable=r).pack(pady=5, padx=100)

    Label(econ_frame, text="Enter n (Number of periods):").pack(pady=5, padx=100)
    n = StringVar()
    Entry(econ_frame, textvariable=n).pack(pady=5, padx=100)

    def calculate_calculator():
        Pc = float(P.get())
        rc = float(r.get())
        nc = int(n.get())
        func = analysis_mode.get()

        # Initialize the values and result
        result = None
        values = [0] * (nc + 1)  

        if analysis_mode.get() == "calculate_future_worth":
            result = calculate_future_worth_calculator(Pc, rc, nc)
            values[0] = -Pc
            values[-1] = result  # Show result at the last period
        elif analysis_mode.get() == "calculate_present_worth":
            result = calculate_present_worth(Pc, rc, nc)
            values[0] = Pc  # Initial cash flow
            values[-1] = Pc
            values[0] = -result  # Show negative cash flow at the first period
        elif analysis_mode.get() == "calculate_future_worth_annual_series":
            result = calculate_future_worth_annual_series(Pc, rc, nc)
            values = [-Pc] * nc + [0]  # Payments for n periods
            values[-1] = result  # Show accumulation at the last period
        elif analysis_mode.get() == "calculate_period_payment_from_future_worth":
            result = calculate_period_payment_from_future_worth(Pc, rc, nc)
            values = [-result] * nc + [Pc]  # Payments for n periods and future value
        elif analysis_mode.get() == "calculate_present_worth_annual_series":
            result = calculate_present_worth_annual_series(Pc, rc, nc)
            values = [-result] + [Pc] * nc  # Payments for n periods and present worth
        elif analysis_mode.get() == "calculate_period_payment_from_present_worth":
            result = calculate_period_payment_from_present_worth(Pc, rc, nc)
            values = [-Pc] + [result] * nc  # Payments for n periods and present worth
        
        # Destroy the previous canvas if it exists
        if hasattr(econ_frame, 'canvas'):
            econ_frame.canvas.get_tk_widget().destroy()

        # Create a new figure and plot the cash flow diagram
        fig, ax = plt.subplots()
        periods = list(range(nc + 1))
        ax.bar(periods, values, color='blue')
        ax.set_title(f'{func} = {result}')
        ax.set_xlabel('Periods')
        ax.set_ylabel('Cash Flow')

        # Embedding the plot into the tkinter window
        econ_frame.canvas = FigureCanvasTkAgg(fig, master=econ_frame) 
        econ_frame.canvas.draw()
        econ_frame.canvas.get_tk_widget().pack()
            

    Button(econ_frame, text="Calculate", command=calculate_calculator).pack(pady=10, padx=100)
    Button(econ_frame, text="Switch to Focasting Case Analysis", command=lambda: switch_frame(main_frame)).pack(pady=10, padx=100)

    # Place frames on top of each other
    main_frame.grid(row=0, column=0, sticky='news')
    econ_frame.grid(row=0, column=0, sticky='news')

    # Raise the main frame to the top
    main_frame.tkraise()

    # Close all matplotlib plots when the window is closed
    def on_closing():
        plt.close('all')
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

if __name__ == "__main__":
    main()