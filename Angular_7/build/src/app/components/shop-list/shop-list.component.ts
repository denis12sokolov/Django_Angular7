import { Component, Input } from '@angular/core';
import { Shop } from '../../interfaces/shop';

@Component({
  selector: 'app-shop-list',
  templateUrl: './shop-list.component.html',
  styleUrls: ['./shop-list.component.scss']
})
export class ShopListComponent {
  @Input() shops: Shop[];
  @Input() gender: 'M' | 'W';

  constructor() {
  }
}
