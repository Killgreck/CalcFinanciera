import numpy as np


def nominal_to_effective_periodic(nominal_rate, frequency):
    return nominal_rate / frequency


def effective_periodic_to_nominal(effective_rate, frequency):
    return effective_rate * frequency


def anticipada_to_efectiva(ia):
    return ia / (1 - ia)


def efectiva_to_anticipada(ie):
    return ie / (1 + ie)


def equivalent_rate(rate, periods):
    return (1 + rate) ** periods - 1


def effective_rate_for_period(nominal_rate, rate_type, payment_type, annual_frequency, payment_frequency):
    if rate_type == "Efectiva":
        if annual_frequency == payment_frequency:
            base_rate = nominal_rate
        else:
            periods_ratio = annual_frequency / payment_frequency
            base_rate = equivalent_rate(nominal_rate / annual_frequency, periods_ratio)
    else:
        periodic_rate = nominal_rate / annual_frequency
        base_rate = periodic_rate
        
        if annual_frequency != payment_frequency:
            periods_ratio = annual_frequency / payment_frequency
            base_rate = equivalent_rate(periodic_rate, periods_ratio)
    
    if payment_type == "Anticipada":
        base_rate = anticipada_to_efectiva(base_rate)
    
    return base_rate


def calculate_payment(principal, rate, periods):
    if rate == 0:
        return principal / periods
    return principal * (rate * (1 + rate) ** periods) / ((1 + rate) ** periods - 1)


def present_value_annuity(payment, rate, periods):
    if rate == 0:
        return payment * periods
    return payment * (1 - (1 + rate) ** -periods) / rate


def future_value_annuity(payment, rate, periods):
    if rate == 0:
        return payment * periods
    return payment * ((1 + rate) ** periods - 1) / rate
