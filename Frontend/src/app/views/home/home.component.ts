import { Component, OnInit, ViewChild } from '@angular/core';
import { FormBuilder, FormGroup } from '@angular/forms';
import { Router } from '@angular/router';
import { Observable, of } from 'rxjs';
import {
  defaultIfEmpty,
  first,
  map,
  pairwise,
  startWith,
  tap,
} from 'rxjs/operators';
import { Destination } from 'src/app/models/destination';
import { AuthService } from 'src/app/services/auth.service';
import { DestinationService } from 'src/app/services/destination.service';

@Component({
  selector: 'hotels-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss'],
})
export class HomeComponent implements OnInit {
  room_count = 1;
  guest_count = 2;
  isLoggedIn = false;

  searchForm: FormGroup;
  destinations: string[];
  filteredDestinations!: string[];

  mincheckoutDate: Date;
  mincheckinDate: Date;
  username!: String;

  constructor(
    private router: Router,
    private formBuilder: FormBuilder,
    private authService: AuthService,
    private destinationService: DestinationService
  ) {
    this.searchForm = this.formBuilder.group({
      destination: '',
      checkinDate: '',
      checkoutDate: '',
      rooms: this.room_count,
      guests: this.guest_count,
    });
    this.destinations = [];

    this.mincheckinDate = new Date();
    this.mincheckoutDate = new Date();
    this.mincheckoutDate.setDate(this.mincheckoutDate.getDate() + 1);
  }

  ngOnInit(): void {
    this.isLoggedIn = this.authService.isLoggedIn;
    this.username = this.authService.userName;

    this.destinationService
      .getDestinations()
      .subscribe((destinations: Destination[]) => {
        this.destinations = destinations.map((value) => {
          return value.city + ', ' + value.country;
        });

        this.filteredDestinations = this.destinations;
      });

    this.searchForm.controls.destination.valueChanges
      .pipe(map((value) => this._filter(value)))
      .subscribe((value) => {
        this.filteredDestinations = value;
      });

    this.searchForm.controls.checkinDate.valueChanges.subscribe((newDate) => {
      this.mincheckoutDate = new Date(newDate);
      this.mincheckoutDate.setDate(this.mincheckoutDate.getDate() + 1);
    });
  }

  private _filter(value: string): string[] {
    return this.destinations.filter((destination) => {
      return destination.toLowerCase().includes(value.toLowerCase());
    });
  }

  openGuestsMenu() {}

  increaseCount(fieldName: string) {
    const current_value: number = this.searchForm.get(fieldName)?.value;
    this.searchForm.patchValue({ [fieldName]: current_value + 1 });
  }

  decreaseCount(fieldName: string) {
    const current_value: number = this.searchForm.get(fieldName)?.value;

    if (current_value === 0) {
      return;
    }
    this.searchForm.patchValue({ [fieldName]: current_value - 1 });
  }

  updateRoomsAndGuests() {
    this.guest_count = this.searchForm.get('guests')?.value;
    this.room_count = this.searchForm.get('rooms')?.value;
  }

  onFormSubmit() {
    console.log(this.searchForm.value);

    if (!this.authService.isLoggedIn) {
      this.router.navigate(['/auth/login'], {
        state: {
          searchFormValues: this.searchForm.value,
        },
      });
    } else {
      this.router.navigate(['/recommend'], {
        state: {
          searchFormValues: this.searchForm.value,
        },
      });
    }
  }

  onLogout() {
    this.isLoggedIn = false;
    this.authService.logout();
  }
}
