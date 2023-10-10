from django.shortcuts import render
import pandas as pd
import numpy
import tinkoffapp.TinkoffBack.General_Inf as General_Inf

df_Global = pd.DataFrame()

def ListForDonut(pnd):
    pnd['amount'] = pnd['price'] * pnd['quantity']

    del pnd['price']
    del pnd['quantity']
    pnd.reset_index(inplace=True)

    pnd = pnd.sort_values(by='amount', ascending=False)
    pnd['amount'] = pnd['amount'].astype(numpy.int64)

    List = []

    for i in range(len(pnd)):
        if pnd.loc[i, 'amount'] != '':
            pnd.loc[i, 'amount'] = pnd.loc[i, 'amount']
            List.append((pnd.iloc[i]))

    return List



def TinkoffDiagramActives():
    activ = df_Global['instrument_type']
    actives = pd.DataFrame()
    actives['instrument_type'] = activ
    actives['quantity'] = df_Global['quantity']
    actives['price'] = df_Global['current_price']
    actives['active_rus'] = ""
    actives['amount'] = ""

    for el in range(len(actives)):
        if actives.iloc[el].instrument_type == 'currency':
            actives.at[el, 'active_rus'] = 'Валюта'

        elif actives.iloc[el].instrument_type == "share":
            actives.loc[el, 'active_rus'] = "Акции"

        elif actives.iloc[el].instrument_type == "etf":
            actives.loc[el, 'active_rus'] = "Фонды"

        elif actives.iloc[el].instrument_type == "bond":
            actives.loc[el, 'active_rus'] = "Облигации"

    actives = actives.groupby('active_rus').sum()
    actives.reset_index(inplace=True)

    ActiveList = ListForDonut(actives)

    return ActiveList

def TinkoffDiagramSectors():
    sector = df_Global['sector']
    quantity = df_Global['quantity']
    price = df_Global['current_price']
    sectors = pd.DataFrame()
    sectors['sector'] = sector
    sectors['sector_rus'] = ""
    sectors['price'] = price
    sectors['quantity'] = quantity
    sectors['amount'] = ""

    sectors['instrument_type'] = df_Global['instrument_type']
    sectors.drop(sectors[sectors['instrument_type'] == 'etf'].index, inplace=True)
    sectors.reset_index(drop=True, inplace=True)

    for el in range(len(sectors)):
        if sectors.iloc[el].instrument_type == 'currency':
            sectors.at[el, 'sector_rus'] = 'Валюта'

        elif sectors.iloc[el].sector == "municipal":
            sectors.loc[el, 'sector_rus'] = "Муниципальный"

        elif sectors.iloc[el].sector == "financial":
            sectors.loc[el, 'sector_rus'] = "Финансовый"

        elif sectors.iloc[el].sector == "industrials":
            sectors.loc[el, 'sector_rus'] = "Машиностроение и транспорт"

        elif sectors.iloc[el].sector == "consumer":
            sectors.loc[el, 'sector_rus'] = "Потребительский"

        elif sectors.iloc[el].sector == "telecom":
            sectors.loc[el, 'sector_rus'] = "Телекоммуникации"

        elif sectors.iloc[el].sector == "materials":
            sectors.loc[el, 'sector_rus'] = "Сырьевая промышленность"

        elif sectors.iloc[el].sector == "energy":
            sectors.loc[el, 'sector_rus'] = "Энергетика"

    sectors = sectors.groupby('sector_rus').sum()
    sectors.reset_index(inplace=True)

    del sectors['sector']
    del sectors['instrument_type']

    SectorsList = ListForDonut(sectors)

    return SectorsList
def TinkoffDiagramCompanies():
    company = df_Global['name']
    quantity = df_Global['quantity']
    price = df_Global['current_price']
    companies = pd.DataFrame()
    companies['compname'] = company
    companies['price'] = price
    companies['quantity'] = quantity
    companies['amount'] = ""

    CompaniesList = ListForDonut(companies)

    return CompaniesList

def tinkoffapp(request):
    GenTinkoffData = General_Inf.Hola().GeneralInfo()
    DetalInfo = General_Inf.Hola().DetalInfo()
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
        'total_amount_currencies': round(General_Inf.Hola().cast_money(GenTinkoffData.total_amount_currencies),1),
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
    ShareList = []
    df = df_Global
    for el in range(len(df)):
        if df.iloc[el].instrument_type == 'share':
            ShareList.append(df.iloc[el])
            TotalYield = TotalYield + df.iloc[el].expected_yield

    ShareDick= {
        'ShareList': ShareList,
        'TotalShareYield': round(TotalYield,1),
    }
    return ShareDick

def render_tinkoff_shares(request):
    ShareDick = tinkoff_shares()

    return render(request, 'tinkoffapp/TinkoffShares.html', ShareDick)

def tinkoff_bonds():
    TotalYield = 0
    BondList = []
    df = df_Global
    for el in range(len(df)):
        if df.iloc[el].instrument_type == 'bond':
            BondList.append(df.iloc[el])
            TotalYield = TotalYield + df.iloc[el].expected_yield

    BondDick= {
        'BondList': BondList,
        'TotalBondYield': round(TotalYield,1),
    }
    return BondDick

def render_tinkoff_bonds(request):
    BondDick = tinkoff_bonds()

    return render(request, 'tinkoffapp/TinkoffBonds.html', BondDick)

def tinkoff_etf():
    TotalYield = 0
    ETFList = []
    df = df_Global
    for el in range(len(df)):
        if df.iloc[el].instrument_type == 'etf':
            ETFList.append(df.iloc[el])
            TotalYield = TotalYield + df.iloc[el].expected_yield

    ETFDick= {
        'ETFList': ETFList,
        'TotalETFYield': round(TotalYield,1),
    }
    return ETFDick

def render_tinkoff_etf(request):
    ETFDick = tinkoff_etf()

    return render(request, 'tinkoffapp/TinkoffETF.html', ETFDick)

def tinkoff_curr():
    TotalYield = 0
    CurrList = []
    df = df_Global
    for el in range(len(df)):
        if df.iloc[el].instrument_type == 'currency':
            CurrList.append(df.iloc[el])
            TotalYield = TotalYield + df.iloc[el].expected_yield

    CurrDick= {
        'CurrList': CurrList,
        'TotalCurrYield': round(TotalYield,1),
    }
    return CurrDick

def render_tinkoff_curr(request):
    CurrDick = tinkoff_curr()

    return render(request, 'tinkoffapp/TinkoffCurrency.html', CurrDick)



