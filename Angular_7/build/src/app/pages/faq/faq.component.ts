import { FAQ } from './../../interfaces/faq';
import { ApiService } from './../../services/api.service';
import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-faq',
  templateUrl: './faq.component.html',
  styleUrls: ['./faq.component.scss']
})
export class FaqComponent implements OnInit {
  faqItems: FAQ[];

  constructor(
    private apiService: ApiService,
  ) {
    this.apiService.getFAQs().subscribe((faqs: FAQ[]) => this.faqItems = faqs);
  }

  ngOnInit() {
  }

}
