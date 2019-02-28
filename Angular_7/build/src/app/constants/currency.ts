import { getCurrencySymbol } from '@angular/common';

export enum Currency {
  CAD = 'CAD',
  USD = 'USD',
  EUR = 'EUR',
  GBP = 'GBP'
}

export const currencyItems = [
  {
    code: Currency.CAD,
    label: getCurrencySymbol(Currency.CAD, 'narrow') + Currency.CAD
  },
  {
    code: Currency.USD,
    label: getCurrencySymbol(Currency.USD, 'narrow') + Currency.USD
  },
  {
    code: Currency.EUR,
    label: getCurrencySymbol(Currency.EUR, 'narrow') + Currency.EUR
  },
  {
        code: Currency.GBP,
    label: getCurrencySymbol(Currency.GBP, 'narrow') + Currency.GBP
  }
];
