import { Component, Input, OnInit } from '@angular/core';
import { FormBuilder, FormGroup } from '@angular/forms';
import { ActivatedRoute } from '@angular/router';
import { Hotel } from 'src/app/models/hotel';
import { Review } from 'src/app/models/review';
import { AuthService } from 'src/app/services/auth.service';
import { RecommendationService } from 'src/app/services/recommendation.service';
import { ReviewService } from 'src/app/services/review.service';

interface ExtendedReview extends Review {
  reviewText?: string;
}

@Component({
  selector: 'hotels-hotel',
  templateUrl: './hotel.component.html',
  styleUrls: ['./hotel.component.scss'],
})
export class HotelComponent implements OnInit {
  hotel!: Hotel;
  // hotel: Hotel = {
  //   id: '6145b3e95b2044db8191717cf55e2dad',
  //   hotel_id: 'Cornstalk_Hotel-New_Orleans_Louisiana',
  //   name: 'The Cornstalk Hotel',
  //   address: '915 Royal St, New Orleans, LA 70116-2701',
  //   unit_price: 91,
  //   rating: 4.5,
  //   review_count: 693,
  //   description:
  //     "The Cornstalk Hotel has been renovated and refurbished featuring fourteen exquisite guest rooms. Brilliant crystal chandeliers, antique mirrors and furnishings adorn the entrance hall, beautifully set off by high vaulted ceilings. The rosette scrolls, cherubs, medallions, stained-glass windows, fireplaces and canopy beds are all relics of a Louisiana plantation home. We are in the heart of the Vieux Carre' (French Quarter), with the sights, the sounds, the gourmet food and night life of old New Orleans.",
  //   city: 'New Orleans',
  //   country: 'United States',
  //   total_price: 118.07,
  //   image_url: 'http://localhost:5000/alex-hall-SS-d4nMNwiQ-unsplash.jpg',
  // };

  reviews!: ExtendedReview[];

  // reviews!: ExtendedReview[] = [
  //   {
  //     id: 1,
  //     review_text:
  //       "We came here with some of our friends and our baby. The staff was very nice to all of us. They spoke Italian and English which made things easier for us. We came back late one night from taking the train to Florence and we asked the staff if the restaurant was still open. They called the chef and had him come in to make a dish for us that wasn't even on the menu! The bar had a wide variety of drinks to choose from also. The bedroom was very clean and neat! We had a balcony with tables and chairs so we could sit outside. The Air Conditioning was AMAZING I haven't experienced a/c like this anywhere else in Italy! The Residence San Rossore was close to Pisa we brought our car and it was only like a 5 min drive. Overall we had a great time but the only problem we had was that we had to pay 5$ per person for the pool. I would definitely visit this place again next time I come back!! ",
  //     review_date: '2016-08-21T00:00:00',
  //     reviewer_name: 'Heather Cox',
  //     reviewer_profile_image:
  //       'https://randomuser.me/api/portraits/women/33.jpg',
  //   },
  //   {
  //     id: 2,
  //     review_text:
  //       "The premises are very peaceful and well maintained. The apartment was spacious though basically equipped. We enjoyed the fine pool and good food. But the hospitality was overwhelming! These people are so friendly and helpful that you'd never want to leave again. After a small accident with a child that needed stitching in the hospital the brought us there and picked us up again and arranged some snacks during the waiting. Arriving back at the hotel after midnight we found the complete staff waiting to welcome us and then preparing dinner. Really a moment never to forget",
  //     review_date: '2016-08-19T00:00:00',
  //     reviewer_name: 'Jorge Harrison',
  //     reviewer_profile_image: 'https://randomuser.me/api/portraits/men/63.jpg',
  //   },
  // ];

  totalStars = 5;
  readonly = true;

  room_count = 1;
  guest_count = 2;

  bookingForm: FormGroup;
  mincheckoutDate: Date;
  mincheckinDate: Date;
  isLoading: boolean;

  constructor(
    private route: ActivatedRoute,
    private formBuilder: FormBuilder,
    private recoommendationService: RecommendationService,
    private authService: AuthService,
    private reviewService: ReviewService
  ) {
    this.bookingForm = this.formBuilder.group({
      hotel_id: this.hotel?.hotel_id,
      checkinDate: '',
      checkoutDate: '',
      rooms: this.room_count,
      guests: this.guest_count,
    });

    this.isLoading = false;

    this.reviews = [];

    this.mincheckinDate = new Date();
    this.mincheckoutDate = new Date();
    this.mincheckoutDate.setDate(this.mincheckoutDate.getDate() + 1);
  }

  ngOnInit(): void {
    this.bookingForm.controls.checkinDate.valueChanges.subscribe((newDate) => {
      this.mincheckoutDate = new Date(newDate);
      this.mincheckoutDate.setDate(this.mincheckoutDate.getDate() + 1);
    });

    const hotel_id = this.route.snapshot.params['id'];
    this.hotel = this.recoommendationService.getHotel(hotel_id);

    this.reviewService
      .getReviews(this.hotel?.hotel_id)
      ?.subscribe((reviews) => {
        this.reviews = reviews.map((review) => {
          let reviewText = review.review_text;
          const limit = reviewText.substr(0, 200).lastIndexOf(' ');

          reviewText = `${reviewText.substr(0, limit)} ...`;

          return {
            ...review,
            reviewText: reviewText,
          };
        });
      });
  }

  openGuestsMenu() {}

  increaseCount(fieldName: string) {
    const current_value: number = this.bookingForm.get(fieldName)?.value;
    this.bookingForm.patchValue({ [fieldName]: current_value + 1 });
  }

  decreaseCount(fieldName: string) {
    const current_value: number = this.bookingForm.get(fieldName)?.value;

    if (current_value === 1) {
      return;
    }
    this.bookingForm.patchValue({ [fieldName]: current_value - 1 });
  }

  updateRoomsAndGuests() {
    this.guest_count = this.bookingForm.get('guests')?.value;
    this.room_count = this.bookingForm.get('rooms')?.value;
  }

  onSubmit() {
    console.log(this.bookingForm.value);
  }
}
