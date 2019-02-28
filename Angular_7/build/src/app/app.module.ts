import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { NgSelectModule } from '@ng-select/ng-select';
import { ProductListComponent } from './components/product-list/product-list.component';
import { ItemCardComponent } from './components/item-card/item-card.component';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';
import { HttpClientModule } from '@angular/common/http';
import { InfiniteScrollModule } from 'ngx-infinite-scroll';
import { ShopListComponent } from './components/shop-list/shop-list.component';
import { MainComponent } from './pages/main/main.component';
import { CategoriesListComponent } from './components/categories-list/categories-list.component';
import { FaqComponent } from './pages/faq/faq.component';
import { ContactComponent } from './pages/contact/contact.component';
import { AboutComponent } from './pages/about/about.component';
import { UnderscoreKillerPipe } from './pipes/underscore-killer.pipe';
import { FormsModule } from '@angular/forms';
import { CurrencyChangePipe } from './pipes/currency-change.pipe';

@NgModule({
  declarations: [
    AppComponent,
    ProductListComponent,
    ItemCardComponent,
    ShopListComponent,
    MainComponent,
    CategoriesListComponent,
    FaqComponent,
    ContactComponent,
    AboutComponent,
    UnderscoreKillerPipe,
    CurrencyChangePipe,
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    FontAwesomeModule,
    InfiniteScrollModule,
    NgSelectModule,
    FormsModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
