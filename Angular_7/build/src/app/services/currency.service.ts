import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';
import { Observable } from 'rxjs';
import { forkJoin } from 'rxjs';
import { Currency } from 'src/app/constants/currency';
import { HttpClient } from '@angular/common/http';
import { API_URL } from 'src/app/constants/urls';
import { tap } from 'rxjs/operators';
import { pluck } from 'rxjs/operators';
import { catchError } from 'rxjs/operators';
import { of } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class CurrencyService {
  current: Observable<Currency>;
  private _currentCurrency: BehaviorSubject<Currency> = new BehaviorSubject(<Currency>localStorage.getItem('currency') || Currency.CAD);
  private coefficients: { [key: string]: number } = {
    [Currency.CAD]: 1,
    [Currency.GBP]: 1,
    [Currency.EUR]: 1,
    [Currency.USD]: 1
  };

  constructor(
    private http: HttpClient
  ) {
    this.current = this._currentCurrency.asObservable();
    this.getCoefficients();
  }

  setCurrentCurrency(currency: Currency): void {
    localStorage.setItem('currency', currency);
    this._currentCurrency.next(currency);
  }

  getCurrentCoefficient(): number {
    return this.coefficients[this._currentCurrency.getValue()];
  }

  getCoefficients(): void {
    const requests: Observable<any>[] = [Currency.EUR, Currency.GBP, Currency.USD].map(currency => {
      return this.http.get(`${API_URL}currency/?from=CAD&to=${currency}`)
        .pipe(
          pluck('value'),
          tap((coefficient: number) => this.coefficients[currency] = coefficient),
          catchError(() => of(true))
        );
    });
    forkJoin(requests).subscribe();
  }
}
