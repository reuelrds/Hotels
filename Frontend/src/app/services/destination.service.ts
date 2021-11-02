import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';

import { environment } from 'src/environments/environment';

import { Destination } from '../models/destination';

@Injectable({
  providedIn: 'root',
})
export class DestinationService {
  BACKEND_URL = environment.BACKEND_URL;

  constructor(private httpClient: HttpClient) {}

  getDestinations(): Observable<Destination[]> {
    return this.httpClient
      .get<{ destinations: Destination[] }>(`${this.BACKEND_URL}/destinations`)
      .pipe(
        map((result) => {
          return result.destinations;
        })
      );
  }
}
