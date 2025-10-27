import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta
from .interest_rates import calculate_payment


def generate_amortization_table(principal, rate, periods, start_date, frequency):
    payment = calculate_payment(principal, rate, periods)
    
    table = []
    balance = principal
    
    frequency_map = {
        "Mensual": 1,
        "Bimestral": 2,
        "Trimestral": 3,
        "Cuatrimestral": 4,
        "Semestral": 6,
        "Anual": 12
    }
    
    months_increment = frequency_map.get(frequency, 1)
    
    for period in range(1, periods + 1):
        interest = balance * rate
        principal_payment = payment - interest
        balance -= principal_payment
        
        if balance < 0.01:
            balance = 0
        
        payment_date = start_date + relativedelta(months=months_increment * (period - 1))
        
        table.append({
            "Periodo": period,
            "Fecha": payment_date.strftime("%Y-%m-%d"),
            "Saldo Inicial": round(balance + principal_payment, 2),
            "Cuota": round(payment, 2),
            "Interés": round(interest, 2),
            "Abono a Capital": round(principal_payment, 2),
            "Saldo Final": round(balance, 2)
        })
    
    return pd.DataFrame(table)


def recalculate_with_extra_payment(table, period, extra_payment, strategy="reducir_plazo"):
    df = table.copy()
    
    if period > len(df):
        return df
    
    period_idx = period - 1
    current_balance = df.loc[period_idx, "Saldo Final"]
    new_balance = current_balance - extra_payment
    
    if new_balance <= 0:
        df.loc[period_idx, "Saldo Final"] = 0
        df = df.iloc[:period]
        return df
    
    df.loc[period_idx, "Saldo Final"] = round(new_balance, 2)
    
    if period < len(df):
        rate = df.loc[period_idx, "Interés"] / df.loc[period_idx, "Saldo Inicial"]
        
        if strategy == "reducir_plazo":
            original_payment = df.loc[period_idx, "Cuota"]
            remaining_periods = len(df) - period
            new_periods = calculate_new_periods(new_balance, rate, original_payment)
            
            if new_periods < remaining_periods:
                df = df.iloc[:period + new_periods]
        
        balance = new_balance
        for i in range(period, len(df)):
            payment = df.loc[i, "Cuota"]
            interest = balance * rate
            principal_payment = payment - interest
            balance -= principal_payment
            
            if balance < 0.01:
                balance = 0
            
            df.loc[i, "Saldo Inicial"] = round(balance + principal_payment, 2)
            df.loc[i, "Interés"] = round(interest, 2)
            df.loc[i, "Abono a Capital"] = round(principal_payment, 2)
            df.loc[i, "Saldo Final"] = round(balance, 2)
            
            if balance == 0:
                df = df.iloc[:i+1]
                break
    
    return df


def calculate_new_periods(balance, rate, payment):
    if rate == 0:
        return int(balance / payment) + 1
    
    import math
    periods = math.log(payment / (payment - balance * rate)) / math.log(1 + rate)
    return int(periods) + 1


def add_extra_payment_row(table, period, extra_payment, description="Abono extraordinario"):
    df = table.copy()
    
    if period > len(df):
        return df
    
    period_idx = period - 1
    
    extra_row = {
        "Periodo": f"{period}*",
        "Fecha": df.loc[period_idx, "Fecha"],
        "Saldo Inicial": df.loc[period_idx, "Saldo Final"],
        "Cuota": extra_payment,
        "Interés": 0,
        "Abono a Capital": extra_payment,
        "Saldo Final": df.loc[period_idx, "Saldo Final"] - extra_payment
    }
    
    df = pd.concat([
        df.iloc[:period],
        pd.DataFrame([extra_row]),
        df.iloc[period:]
    ], ignore_index=True)
    
    return df
