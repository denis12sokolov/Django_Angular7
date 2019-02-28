import { Categories } from '../../interfaces/categories';
import { Component } from '@angular/core';
import { faInfinity } from '@fortawesome/free-solid-svg-icons';
import { ProductParams, ProductResponse } from '../../interfaces/common';
import { map, tap } from 'rxjs/operators';
import { ApiService } from '../../services/api.service';
import { ActivatedRoute } from '@angular/router';
import { Product } from '../../interfaces/product';
import { Shop } from '../../interfaces/shop';

@Component({
  selector: 'app-main',
  templateUrl: './main.component.html',
  styleUrls: ['./main.component.scss']
})
export class MainComponent {
  faCoffee = faInfinity;
  nextPage: string;
  products: Product[] = [];
  shops: Shop[] = [];
  categories: Categories[] = [];

  constructor(
    private apiService: ApiService,
    private activatedRoute: ActivatedRoute
  ) {
    this.apiService.getShops().subscribe((shops: Shop[]) => this.shops = shops);
    this.apiService.getCategories().subscribe((categories: Categories[]) => this.categories = categories);
    this.activatedRoute.queryParams.pipe().subscribe(params => {
      this.products = [];
      this.apiService.getFilteredProducts(<ProductParams>{...params})
        .pipe(
          tap((response: ProductResponse) => this.nextPage = response.next),
          map((response: ProductResponse) => response.results),
        ).subscribe(products => this.products = products);
    });
  }

  getNextPage(): void {
    this.apiService.getProductsByUrl(this.nextPage)
      .pipe(
        tap((response: ProductResponse) => this.nextPage = response.next),
        map((response: ProductResponse) => response.results)
      ).subscribe(products => this.products = [...this.products, ...products]);
  }

}
