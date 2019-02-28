import { environment } from 'src/environments/environment';

export const API_URL = environment.apiUrl;

export default {
  PRODUCTS: API_URL + 'product/',
  SHOPS: API_URL + 'shop/',
  FAQ: API_URL + 'faq/'
};
