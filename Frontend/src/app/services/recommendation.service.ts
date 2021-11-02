import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { map, tap } from 'rxjs/operators';
import { environment } from 'src/environments/environment';
import { Hotel } from '../models/hotel';

@Injectable({
  providedIn: 'root',
})
export class RecommendationService {
  BACKEND_URL = environment.BACKEND_URL;

  hotels: Hotel[] = [];

  constructor(private httpClient: HttpClient) {}

  getHotel(hotel_id: string): Hotel {

    const hotel = this.hotels.find((hotel) => {
      return hotel.hotel_id == hotel_id;
    });

    if (hotel) {
      return hotel;
    } else {
      return {
        id: '',
        hotel_id: '',
        name: '',
        address: '',
        unit_price: 0,
        rating: 0,
        review_count: 0,
        description: '',
        city: '',
        country: '',
        total_price: 0,
        image_url: '',
      };
    }
  }

  getHotels() {
    return this.httpClient
      .get<{ message: string; hotels: Hotel[] }>(`${this.BACKEND_URL}/hotels`)
      .pipe(
        map((result) => result.hotels),
        tap((hotels) => (this.hotels = hotels))
      );
  }

  getHotelRecommendations(searchForm: any) {
    const queryParams = {
      ...searchForm,
      checkinDate: searchForm.checkinDate.toISOString(),
      checkoutDate: searchForm.checkoutDate.toISOString(),
    };

    return this.httpClient
      .get<{ message: string; hotels: Hotel[] }>(`${this.BACKEND_URL}/hotels`, {
        params: queryParams,
      })
      .pipe(
        map((result) => {
          result.hotels = result.hotels.map((hotel) => {
            return {
              ...hotel,
              image_url: `${this.BACKEND_URL}/${hotel.image_url}`,
            };
          });
          return result;
        }),
        tap((result) => (this.hotels = result.hotels))
      );
  }
}
