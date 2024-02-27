import pandas as pd
from tinkoff.invest.services import InstrumentsService
from tinkoff.invest import Client, RequestError, InstrumentIdType, PortfolioPosition
from . import creds



############################### <=== CLASS ===> ############################

class TinkResp:
    def __init__(self,DetInf, FreeRub, TotalYield, CurrentAmount):
        self.DetInf = DetInf
        self.FreeRub = FreeRub,
        self.TotalYield = TotalYield
        self.CurrentAmoult = CurrentAmount


def GeneralInfo():
    try:
        with Client(creds.tinkoff_invest_token_read) as client:
            r = client.operations.get_portfolio(account_id=creds.Account_id)
            return r

    except RequestError as e:
        print(str(e))


class Hola:
    def __init__(self):
        self.usdrur = None
        self.client = Client(creds.tinkoff_invest_token_read)
        self.accounts = []
        self.total_amount_portfolio = None
        self.total_amount_shares = None
        self.total_amount_bonds = None
        self.total_amount_etf = None
        self.total_amount_currencies = None
        self.expected_yield = None

    def TaxInfo(self):

        df = pd.DataFrame(self.DetalInfo().DetInf)

        # суммы продаж, налоги и комиссии
        df['sell_sum'] = (df['current_price'] + df['current_nkd']) * df['quantity']
        df['comission'] = df['current_price'] * df['quantity'] * 0.003
        df['tax'] = df.apply(lambda row: row['expected_yield'] * 0.013 if row['expected_yield'] > 0 else 0, axis=1)

        return df

    def get_usdrur(self):
        """
        Получаю курс только если он нужен
        :return:
        """
        if not self.usdrur:
            # т.к. есть валютные активы (у меня etf), то нужно их отконвертить в рубли
            # я работаю только в долл, вам возможно будут нужны и др валюты
            u = self.client.market_data.get_last_prices(figi=['USD000UTSTOM'])
            self.usdrur = self.cast_money(u.last_prices[0].price)

        return self.usdrur

    def portfolio_pose_todict(self, p : PortfolioPosition):

        r = {
            'figi': p.figi,
            'quantity': self.cast_money(p.quantity),
            'expected_yield': self.cast_money(p.expected_yield),
            'instrument_type': p.instrument_type,
            'average_buy_price': self.cast_money(p.average_position_price),
            'current_price': self.cast_money(p.current_price),
            'currency': p.average_position_price.currency,
            'current_nkd': self.cast_money(p.current_nkd),
            'amount': round(self.cast_money(p.current_price) * self.cast_money(p.quantity),2)

        }

        if r['currency'] == 'usd':
            # expected_yield в Quotation а там нет currency
            r['expected_yield'] *= self.get_usdrur()
        return r

    def cast_money(self, v, to_rub=True):

        r = v.units + v.nano / 1e9
        if to_rub and hasattr(v, 'currency') and getattr(v, 'currency') == 'usd':
            r *= self.get_usdrur()

        return r

    def DetalInfo(self):
        try:
            with Client(creds.tinkoff_invest_token_read) as cl:
                TotalYield = 0
                CurrentAmount = 0
                r = GeneralInfo()
                if len(r.positions) < 1: return None
                DetailTinkoffData = pd.DataFrame([Hola().portfolio_pose_todict(p) for p in r.positions])

                FreeRub = DetailTinkoffData[DetailTinkoffData['figi'] == 'RUB000UTSTOM']
                DetailTinkoffData.drop(DetailTinkoffData[DetailTinkoffData['figi'] == 'RUB000UTSTOM'].index,
                                       inplace=True)
                Alldf = DetailTinkoffData.reset_index()
                Alldf['name'] = ""
                Alldf['CupQuaPerYear'] = ""
                Alldf['aci_value'] = ""
                Alldf['sector'] = ""

                InstrumentList = []

                x = len(Alldf)
                for n in range(x):
                    instruments: InstrumentsService = cl.instruments

                    if Alldf.iloc[n].instrument_type == "share":
                        Details = instruments.share_by(id_type=InstrumentIdType.INSTRUMENT_ID_TYPE_FIGI,
                                                       id=Alldf.iloc[n].figi)
                        ShareName = Details.instrument.name
                        Alldf.loc[n, 'name'] = ShareName
                        Sector = Details.instrument.sector
                        Alldf.loc[n, 'sector'] = Sector
                        TotalYield = TotalYield + Alldf.iloc[n].expected_yield
                        CurrentAmount = CurrentAmount + Alldf.iloc[n].current_price * Alldf.iloc[n].quantity

                    elif Alldf.iloc[n].instrument_type == "bond":
                        Details = instruments.bond_by(id_type=InstrumentIdType.INSTRUMENT_ID_TYPE_FIGI,
                                                      id=Alldf.iloc[n].figi)
                        BondName = Details.instrument.name
                        CupQuaPerYear = Details.instrument.coupon_quantity_per_year
                        aci_value = Details.instrument.aci_value
                        Alldf.loc[n, 'name'] = BondName
                        Alldf.loc[n, 'CupQuaPerYear'] = CupQuaPerYear              # Количество выплат по купонам в год.
                        Alldf.loc[n, 'aci_value'] = self.cast_money(aci_value)     #Значение НКД
                        Alldf.loc[n, 'sector'] = Details.instrument.sector

                    elif Alldf.iloc[n].instrument_type == "etf":
                        Details = instruments.etf_by(id_type=InstrumentIdType.INSTRUMENT_ID_TYPE_FIGI,
                                                     id=Alldf.iloc[n].figi)
                        EtfName = Details.instrument.name
                        Alldf.loc[n, 'name'] = EtfName
                        Sector = Details.instrument.sector
                        Alldf.loc[n, 'sector'] = Sector

                    elif Alldf.iloc[n].instrument_type == "currency":
                        Details = instruments.currency_by(id_type=InstrumentIdType.INSTRUMENT_ID_TYPE_FIGI,
                                                          id=Alldf.iloc[n].figi)
                        CurName = Details.instrument.name
                        Alldf.loc[n, 'name'] = CurName

                    Instrument = {
                        'name': Alldf.loc[n, "name"],
                        'figi': Alldf.loc[n, "figi"],
                        'quantity': Alldf.loc[n, "quantity"],
                        'expected_yield': Alldf.loc[n, "expected_yield"],
                        'average_buy_price': Alldf.loc[n, "average_buy_price"],
                        'current_price': Alldf.loc[n, "current_price"],
                        'currency': Alldf.loc[n, "currency"],
                        'CupQuaPerYear': Alldf.loc[n, "CupQuaPerYear"],
                        'aci_value': Alldf.loc[n, "aci_value"],
                        'amount': Alldf.loc[n, "amount"],
                        'instrument_type': Alldf.loc[n,"instrument_type"],
                        'sector': Alldf.loc[n, "sector"],
                    }

                    InstrumentList.append(Instrument)

                    a = TinkResp(DetInf = InstrumentList,FreeRub = FreeRub.quantity, TotalYield = TotalYield, CurrentAmount = CurrentAmount)

            return a
        except RequestError as e:
            print(str(e))