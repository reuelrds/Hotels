import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import { environment } from 'src/environments/environment';
import { Review } from '../models/review';

@Injectable({
  providedIn: 'root',
})
export class ReviewService {
  BACKEND_URL = environment.BACKEND_URL;

  constructor(private httpClient: HttpClient) {}

  getReviews(hotel_id: string | undefined): Observable<Review[]> | undefined {
    if (hotel_id) {
      return this.httpClient
        .get<{ reviews: Review[] }>(`${this.BACKEND_URL}/reviews`, {
          params: {
            hotel_id: hotel_id,
          },
        })
        .pipe(
          map((result) => {
            return result.reviews;
          })
        );
    } else {
      return undefined;
    }
  }
}
