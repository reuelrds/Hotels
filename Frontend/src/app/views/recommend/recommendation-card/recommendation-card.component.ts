import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'hotels-recommendation-card',
  templateUrl: './recommendation-card.component.html',
  styleUrls: ['./recommendation-card.component.scss']
})
export class RecommendationCardComponent implements OnInit {

  reviews = 4.9
  review_count = 524

  hotel_name = "Lorem"
  hotel_address = "Dolor Sit Amet, Lorem Ipsum Dolor Sit Amet, Lorem Ipsum Dolor Sit Amet, Lorem IpsumDolor Sit Amet, Lorem Ipsum Dolor Sit Amet, Lorem IpsumDolor Sit Amet, Lorem Ipsum"
  price = 120

  hotel_image = "/assets/images/hotel_room1.jpg"

  constructor() { }

  ngOnInit(): void {
  }

}
