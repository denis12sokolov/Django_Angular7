import { Pipe, PipeTransform } from '@angular/core';
import { Currency } from 'src/app/constants/currency';

@Pipe({
  name: 'currencyChange'
})
export class CurrencyChangePipe implements PipeTransform {

  constructor() {}

  transform(value: string, currency: Currency, coefficient: number): any {
    return parseFloat(value) * coefficient;
  }

}
