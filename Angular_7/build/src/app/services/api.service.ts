import { FAQ } from './../interfaces/faq';
import { Categories } from './../interfaces/categories';
import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { ProductParams, ProductResponse, ShopResponse } from '../interfaces/common';
import { map } from 'rxjs/operators';
import urls from '../constants/urls';
import { Shop } from '../interfaces/shop';

@Injectable({
  providedIn: 'root'
})
export class ApiService {

  constructor(
    private http: HttpClient,
  ) {
  }

  getShops(): Observable<Shop[]> {
    return this.http.get<ShopResponse>(urls.SHOPS)
      .pipe(
        map((response: ShopResponse) => response.shops)
      );
  }

  getFAQs(): Observable<FAQ[]> {
    return this.http.get(urls.FAQ)
      .pipe(
        map((response: FAQ[]) => response)
      );
  }

  getCategories(): Observable<Categories[]> {
    return this.http.get<ShopResponse>(urls.SHOPS)
      .pipe(
        map((response: ShopResponse) => response.categories)
      );
  }

  getFilteredProducts(params: ProductParams = {}): Observable<ProductResponse> {
    let httpParams = new HttpParams();
    Object.keys(params).forEach(key => httpParams = httpParams.set(key, params[key]));
    return this.http.get<ProductResponse>(urls.PRODUCTS, {params: httpParams});
  }

  getProductsByUrl(url: string): Observable<ProductResponse> {
    return this.http.get<ProductResponse>(url);
  }
}
