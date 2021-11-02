import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core';

@Component({
  selector: 'hotels-recommendation-card',
  templateUrl: './recommendation-card.component.html',
  styleUrls: ['./recommendation-card.component.scss'],
})
export class RecommendationCardComponent implements OnInit {
  @Input() price = 120;
  @Input() unit_price = 120;
  @Input() rating = 4.9;
  @Input() review_count = 524;
  @Input() hotel_name = 'Lorem';
  @Input() image_url = '/assets/images/hotel_room1.jpg';
  @Input() hotel_id = '';

  @Input() hotel_address =
    'Lorem ipsum dolor sit amet consectetur adipisicing elit.';

  @Output() hotelDetailsEvent = new EventEmitter();

  constructor() {}

  ngOnInit(): void {}

  onViewHotelDetails() {
    this.hotelDetailsEvent.emit(this.hotel_id);
  }
}
