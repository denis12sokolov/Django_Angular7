import { Categories } from './categories';
import { Product } from './product';
import { Shop } from './shop';

export interface ProductResponse {
  count: number;
  next: null | string;
  previous: null| string;
  results: Product[];
}

interface BaseOptions {
  page?: string;
}

export interface ProductParams extends BaseOptions {
  shop_name?: string;
}

export interface ShopResponse {
  shops: Shop[];
  categories: Categories[];
}
