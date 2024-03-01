from django.contrib.auth.decorators import login_required
from django.shortcuts import render
import pandas as pd
import numpy
import tinkoffapp.TinkoffBack.General_Inf as General_Inf

df_Global = pd.DataFrame()

@login_required
def tinkoffapp(request):

    ButtonName =  request.GET.get("ButtonName")

    GenTinkoffData = General_Inf.GeneralInfo(ButtonName)
    DetalInfo = General_Inf.Hola().DetalInfo(GenTinkoffData.positions)
    Details = pd.DataFrame(DetalInfo.DetInf)
    global df_Global
    df_Global = pd.DataFrame(Details)
    FreeRub = DetalInfo.FreeRub[0].tolist()[0]
    TotalYield = DetalInfo.TotalYield
    TotalShareYield = tinkoff_shares()['TotalShareYield']
    TotalBondYield = tinkoff_bonds()['TotalBondYield']
    TotalETFYield = tinkoff_etf()['TotalETFYield']
    TotalCurrYield = tinkoff_curr()['TotalCurrYield']
    SectorsList = TinkoffDiagramSectors()
    ActivesList = TinkoffDiagramActives()
    CompaniesList = TinkoffDiagramCompanies()

    data = {
        'total_amount_portfolio': round(General_Inf.Hola().cast_money(GenTinkoffData.total_amount_portfolio),1),
        'expected_yield': round(General_Inf.Hola().cast_money(GenTinkoffData.expected_yield),1),
        'total_amount_shares':round(General_Inf.Hola().cast_money(GenTinkoffData.total_amount_shares),1),
        'total_amount_bonds': round(General_Inf.Hola().cast_money(GenTinkoffData.total_amount_bonds),1),
        'total_amount_etf': round(General_Inf.Hola().cast_money(GenTinkoffData.total_amount_etf),1),
        'total_amount_currencies': round((General_Inf.Hola().cast_money(GenTinkoffData.total_amount_currencies) - FreeRub),1),
        'FreeRub': round(FreeRub,1),
        'TotalYield': round(TotalYield,1),
        'TotalShareYield': round(TotalShareYield,1),
        'TotalBondYield': round(TotalBondYield,1),
        'TotalETFYield': round(TotalETFYield,1),
        'TotalCurrYield': round(TotalCurrYield,1),
        'SectorsList': SectorsList,
        'ActivesList': ActivesList,
        'CompaniesList': CompaniesList,
    }

    return render(request, 'tinkoffapp/Tinkoff.html', data)

def tinkoff_shares():
    TotalYield = 0
    BuyAmount = 0
    CurrentAmount = 0
    ShareList = []
    df = df_Global
    for el in range(len(df)):
        if df.iloc[el].instrument_type == 'share':
            ShareList.append(df.iloc[el])
            TotalYield = TotalYield + df.iloc[el].expected_yield
            BuyAmount = BuyAmount + df.iloc[el].average_buy_price * df.iloc[el].quantity
            CurrentAmount = CurrentAmount + df.iloc[el].current_price * df.iloc[el].quantity

    ShareDick= {
        'ShareList': ShareList,
        'TotalShareYield': round(TotalYield,1),
        'BuyAmount': round(BuyAmount, 1),
        'CurrentAmount': round(CurrentAmount, 1),
    }
    return ShareDick

@login_required
def render_tinkoff_shares(request):
    ShareDick = tinkoff_shares()

    return render(request, 'tinkoffapp/TinkoffShares.html', ShareDick)

def tinkoff_bonds():
    TotalYield = 0
    BuyAmount = 0
    CurrentAmount = 0
    TotalNKD = 0
    BondList = []
    df = df_Global
    for el in range(len(df)):
        if df.iloc[el].instrument_type == 'bond':
            BondList.append(df.iloc[el])
            TotalYield = TotalYield + df.iloc[el].expected_yield
            BuyAmount = BuyAmount + df.iloc[el].average_buy_price * df.iloc[el].quantity
            CurrentAmount = CurrentAmount + df.iloc[el].current_price * df.iloc[el].quantity
            TotalNKD = TotalNKD + df.iloc[el].aci_value

    BondDick= {
        'BondList': BondList,
        'TotalBondYield': round(TotalYield,1),
        'BuyAmount': round(BuyAmount, 1),
        'CurrentAmount': round(CurrentAmount, 1),
        'TotalNKD': round(TotalNKD, 1),

    }
    return BondDick

@login_required
def render_tinkoff_bonds(request):
    BondDick = tinkoff_bonds()

    return render(request, 'tinkoffapp/TinkoffBonds.html', BondDick)

def tinkoff_etf():
    TotalYield = 0
    BuyAmount = 0
    CurrentAmount = 0
    ETFList = []
    df = df_Global
    for el in range(len(df)):
        if df.iloc[el].instrument_type == 'etf':
            ETFList.append(df.iloc[el])
            TotalYield = TotalYield + df.iloc[el].expected_yield
            BuyAmount = BuyAmount + df.iloc[el].average_buy_price * df.iloc[el].quantity
            CurrentAmount = CurrentAmount + df.iloc[el].current_price * df.iloc[el].quantity

    ETFDick= {
        'ETFList': ETFList,
        'TotalETFYield': round(TotalYield,1),
        'BuyAmount': round(BuyAmount, 1),
        'CurrentAmount': round(CurrentAmount, 1),
    }
    return ETFDick

@login_required
def render_tinkoff_etf(request):
    ETFDick = tinkoff_etf()

    return render(request, 'tinkoffapp/TinkoffETF.html', ETFDick)

def tinkoff_curr():
    TotalYield = 0
    BuyAmount = 0
    CurrentAmount = 0
    CurrList = []
    df = df_Global
    for el in range(len(df)):
        if df.iloc[el].instrument_type == 'currency':
            CurrList.append(df.iloc[el])
            TotalYield = TotalYield + df.iloc[el].expected_yield
            BuyAmount = BuyAmount + df.iloc[el].average_buy_price * df.iloc[el].quantity
            CurrentAmount = CurrentAmount + df.iloc[el].current_price * df.iloc[el].quantity

    CurrDick= {
        'CurrList': CurrList,
        'TotalCurrYield': round(TotalYield,1),
        'BuyAmount': round(BuyAmount, 1),
        'CurrentAmount': round(CurrentAmount, 1),
    }
    return CurrDick

@login_required
def render_tinkoff_curr(request):
    CurrDick = tinkoff_curr()

    return render(request, 'tinkoffapp/TinkoffCurrency.html', CurrDick)

def ListForDonut(actives):

    actives['amount'] = actives['price'] * actives['quantity']

    actives = actives.groupby('selection_field').sum()
    actives.reset_index(inplace=True)

    actives['amount'] = actives['amount'].astype(numpy.int64)

    DonutList = []

    for i in range(len(actives)):
        if actives.loc[i, 'amount'] != '':
            actives.loc[i, 'amount'] = actives.loc[i, 'amount']
            DonutList.append((actives.iloc[i]))

    return DonutList

def TinkoffDiagramActives():
    actives_mapping = {
       "currency" : "Валюта",
        "share" : "Акции",
        "etf" : "Фонды",
        "bond" : "Облигации",
    }

    activ = df_Global['instrument_type']
    actives = pd.DataFrame()
    actives['instrument_type'] = activ
    actives['quantity'] = df_Global['quantity']
    actives['price'] = df_Global['current_price']
    actives['selection_field'] = ""
    actives['amount'] = ""

    actives.reset_index(drop=True, inplace=True)

    actives['selection_field'] = actives['instrument_type'].map(actives_mapping).fillna("???")

    ActiveList = ListForDonut(actives)

    return ActiveList

def TinkoffDiagramSectors():
    sector_mapping = {
        "municipal": "Муниципальный",
        "financial": "Финансовый",
        "industrials": "Машиностроение и транспорт",
        "consumer": "Потребительский",
        "telecom": "Телекоммуникации",
        "materials": "Сырьевая промышленность",
        "energy": "Энергетика",
        "it": "Информационные технологии",
        "utilities": "Электроэнергетика"
    }

    sector = df_Global['sector']
    quantity = df_Global['quantity']
    price = df_Global['current_price']
    sectors = pd.DataFrame()
    sectors['sector'] = sector
    sectors['selection_field'] = ""
    sectors['price'] = price
    sectors['quantity'] = quantity
    sectors['amount'] = ""

    sectors['instrument_type'] = df_Global['instrument_type']
    #sectors.drop(sectors[sectors['instrument_type'] == 'etf'].index, inplace=True)
    sectors.drop(sectors[sectors['instrument_type'] == 'currency'].index, inplace=True)
    sectors.reset_index(drop=True, inplace=True)

    sectors['selection_field'] = sectors['sector'].map(sector_mapping).fillna("???")

    SectorsList = ListForDonut(sectors)

    return SectorsList

def TinkoffDiagramCompanies():
    company = df_Global['name']
    quantity = df_Global['quantity']
    price = df_Global['current_price']
    companies = pd.DataFrame()
    companies['selection_field'] = company
    companies['price'] = price
    companies['quantity'] = quantity
    companies['amount'] = ""

    companies.sort_values(by='amount', inplace=False)

    CompaniesList = ListForDonut(companies)

    return CompaniesList
