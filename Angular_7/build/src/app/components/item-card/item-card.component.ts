import { Component, Input, OnInit } from '@angular/core';
import { Product } from '../../interfaces/product';
import { environment } from 'src/environments/environment';
import { Currency } from 'src/app/constants/currency';

@Component({
  selector: 'app-item-card',
  templateUrl: './item-card.component.html',
  styleUrls: ['./item-card.component.scss']
})
export class ItemCardComponent implements OnInit {
  @Input() item: Product;
  @Input() currency: Currency;
  @Input() coefficient: number;

  constructor() {}

  ngOnInit() {

  }

  public routeToProductURL() {
    window.open(`${environment.vigLink}?u=${encodeURIComponent(this.item.url_original)}&key=${environment.vigKey}`);
  }

}
