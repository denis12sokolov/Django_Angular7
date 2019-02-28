import { Component } from '@angular/core';
import { OnInit } from '@angular/core';
import { faInfinity } from '@fortawesome/free-solid-svg-icons';
import { map, tap } from 'rxjs/operators';

import { ProductParams, ProductResponse } from './interfaces/common';
import { ApiService } from './services/api.service';
import { ActivatedRoute } from '@angular/router';
import { Product } from './interfaces/product';
import { Shop } from './interfaces/shop';
import { currencyItems } from 'src/app/constants/currency';
import { Currency } from 'src/app/constants/currency';
import { Observable } from 'rxjs';
import { CurrencyService } from 'src/app/services/currency.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements OnInit {
  faCoffee = faInfinity;
  nextPage: string;
  products: Product[] = [];
  shops: Shop[] = [];
  menuItems = [
    {name: 'Shops'},
    {name: 'FAQ'}
  ];
  activeMenuItem = '';
  currency = [...currencyItems];
  currentCurrency: Observable<Currency>;

  constructor(
    private apiService: ApiService,
    private activatedRoute: ActivatedRoute,
    private currencyService: CurrencyService,
  ) {
    this.currentCurrency = this.currencyService.current;
  }

  ngOnInit() {
    this.apiService.getShops().subscribe((shops: Shop[]) => this.shops = shops);
    this.activatedRoute.queryParams.pipe().subscribe(params => {
      this.products = [];
      this.apiService.getFilteredProducts(<ProductParams>{...params})
        .pipe(
          tap((response: ProductResponse) => this.nextPage = response.next),
          map((response: ProductResponse) => response.results),
        ).subscribe(products => this.products = products);
    });
  }

  openMenuForItem(menuItem: string) {
    if (this.activeMenuItem === menuItem) {
      this.activeMenuItem = '';
    } else {
      this.activeMenuItem = menuItem;
    }
  }

  changeCurrency(currency): void {
    this.currencyService.setCurrentCurrency(currency.code);
  }
}
