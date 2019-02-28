import { Component, EventEmitter, Input, Output } from '@angular/core';
import { Product } from '../../interfaces/product';
import { CurrencyService } from 'src/app/services/currency.service';
import { Observable } from 'rxjs';
import { Currency } from 'src/app/constants/currency';

@Component({
  selector: 'app-product-list',
  templateUrl: './product-list.component.html',
  styleUrls: ['./product-list.component.scss']
})
export class ProductListComponent {
  @Input() products: Product[];
  @Output() scrollEnd: EventEmitter<void> = new EventEmitter();
  currency: Observable<Currency>;

  constructor(private currencyService: CurrencyService) {
    this.currency = this.currencyService.current;
  }

  trackByProductId(product: Product): number {
    return product.id;
  }

  sendScrollEvent(): void {
    this.scrollEnd.emit();
  }

  getCoefficient(): number {
    return this.currencyService.getCurrentCoefficient();
  }
}
