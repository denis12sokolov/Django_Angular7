import { Component, Input, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-categories-list',
  templateUrl: './categories-list.component.html',
  styleUrls: ['./categories-list.component.scss']
})
export class CategoriesListComponent implements OnInit {
  @Input() categories;
  all_categories_buff = [];
  product_type: string;
  subscribe;

  ngOnInit() {
    this.subscribe = this.activatedRoute.queryParams.subscribe(queryParams => {
      this.product_type = queryParams['product_type'];
  });
  }

  constructor(
    private activatedRoute: ActivatedRoute
  ) {
  }

  getCategoryLink(category: string) {
    if (category === this.product_type) {
      return {...this.activatedRoute.snapshot.queryParams, product_type: undefined, subcategory: undefined};
    } else {
      return {...this.activatedRoute.snapshot.queryParams, product_type: category};
    }
  }

  getSubcategoryLink(subcategory: string) {
    return {...this.activatedRoute.snapshot.queryParams, subcategory: subcategory};
  }

}
