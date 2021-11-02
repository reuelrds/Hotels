import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { Observable } from 'rxjs';
import { finalize, map, tap } from 'rxjs/operators';
import { Destination } from 'src/app/models/destination';
import { Hotel } from 'src/app/models/hotel';
import { AuthService } from 'src/app/services/auth.service';
import { DestinationService } from 'src/app/services/destination.service';
import { RecommendationService } from 'src/app/services/recommendation.service';
import { SnackbarService } from 'src/app/services/snackbar.service';

@Component({
  selector: 'hotels-recommend',
  templateUrl: './recommend.component.html',
  styleUrls: ['./recommend.component.scss'],
})
export class RecommendComponent implements OnInit {
  room_count = 1;
  guest_count = 2;

  searchForm: FormGroup;
  destinations: string[];
  filteredDestinations!: string[];
  hotels!: Hotel[];

  aspectFilters: string[];
  filteredAspects!: string[];

  mincheckoutDate: Date;
  mincheckinDate: Date;
  message: string;
  isLoading: boolean;

  // filters = [
  //   { name: 'Chip 1', selected: false },
  //   { name: 'Chip 2', selected: false },
  // ];

  constructor(
    private router: Router,
    private formBuilder: FormBuilder,
    private authService: AuthService,
    private destinationService: DestinationService,
    private snackbarService: SnackbarService,
    private recommendationService: RecommendationService
  ) {
    this.searchForm = this.formBuilder.group({
      destination: ['', Validators.required],
      checkinDate: ['', Validators.required],
      checkoutDate: ['', Validators.required],
      rooms: [this.room_count, Validators.required],
      guests: [this.guest_count, Validators.required],
      aspectFilter: '',
    });
    this.destinations = [];
    this.message = '';
    this.isLoading = false;

    this.mincheckinDate = new Date();
    this.mincheckoutDate = new Date();
    this.mincheckoutDate.setDate(this.mincheckoutDate.getDate() + 1);

    this.aspectFilters = [
      'Bussiness',
      'Value',
      'Clean',
      'Location',
      'Service',
      'Sleep',
      'Rooms',
    ];

    this.filteredAspects = this.aspectFilters;
  }

  ngOnInit(): void {
    this.searchForm.patchValue({ ...history.state?.searchFormValues });

    this.destinationService
      .getDestinations()
      .subscribe((destinations: Destination[]) => {
        this.destinations = destinations.map((value) => {
          return value.city + ', ' + value.country;
        });

        this.filteredDestinations = this.destinations;
      });

    console.log(this.searchForm);

    this.searchForm.controls.destination.valueChanges
      .pipe(map((value) => this._filter(value, this.destinations)))
      .subscribe((value) => {
        this.filteredDestinations = value;
      });
    this.searchForm.controls.aspectFilter.valueChanges
      .pipe(map((value) => this._filter(value, this.aspectFilters)))
      .subscribe((value) => {
        this.filteredAspects = value;
      });

    this.searchForm.controls.checkinDate.valueChanges.subscribe((newDate) => {
      this.mincheckoutDate = new Date(newDate);
      this.mincheckoutDate.setDate(this.mincheckoutDate.getDate() + 1);
    });

    const hotels = localStorage.getItem('hotel_list');

    if (hotels) {
      this.hotels = JSON.parse(hotels);
      localStorage.removeItem('hotel_list');
    }

    const search_form_values = localStorage.getItem('search_form_values');

    if (search_form_values) {
      this.searchForm.patchValue({
        ...JSON.parse(search_form_values),
      });
      localStorage.removeItem('search_form_values');
    }

    const _mincheckinDate = localStorage.getItem('mincheckinDate');

    if (_mincheckinDate) {
      this.mincheckinDate = JSON.parse(_mincheckinDate);
      localStorage.removeItem('mincheckinDate');
    }

    const _mincheckoutDate = localStorage.getItem('mincheckoutDate');

    if (_mincheckoutDate) {
      this.mincheckinDate = JSON.parse(_mincheckoutDate);
      localStorage.removeItem('mincheckoutDate');
    }

    if (!this.hotels) {
      // this.isLoading = true;
      // this.recommendationService.getHotels().subscribe(
      //   (result) => {
      //     this.hotels = result;
      //     this.isLoading = false;
      //   },
      //   (error) => {
      //     this.message = 'Error Fetching Hotel List';
      //     this.isLoading = false;
      //   }
      // );
      this.onSubmit();
    } else {
      console.log('error');
      console.log(this.hotels);
    }
  }

  private _filter(value: string, initialArray: string[]): string[] {
    return initialArray.filter((arrayValue) => {
      return arrayValue.toLowerCase().includes(value.toLowerCase());
    });
  }

  openGuestsMenu() {}

  increaseCount(fieldName: string) {
    const current_value: number = this.searchForm.get(fieldName)?.value;
    this.searchForm.patchValue({ [fieldName]: current_value + 1 });
  }

  decreaseCount(fieldName: string) {
    const current_value: number = this.searchForm.get(fieldName)?.value;

    if (current_value === 1) {
      return;
    }
    this.searchForm.patchValue({ [fieldName]: current_value - 1 });
  }

  updateRoomsAndGuests() {
    this.guest_count = this.searchForm.get('guests')?.value;
    this.room_count = this.searchForm.get('rooms')?.value;
  }

  onSubmit() {
    console.log(this.searchForm.value);
    console.log(this.searchForm.valid);

    this.hotels = [];

    if (this.searchForm.valid) {
      this.isLoading = true;
      this.recommendationService
        .getHotelRecommendations(this.searchForm.value)
        .subscribe(
          (result) => {
            this.message = result.message;
            this.hotels = result.hotels;
            this.isLoading = false;
          },
          (error) => {
            this.message = 'Error Fetching Hotel List';
            this.isLoading = false;
          }
        );
    } else {
      this.snackbarService.displaySnackBar('Incomplete Searcn Form', 'Ok');
    }
  }

  onDisplayHotelDetails(hotel_id: string) {
    localStorage.setItem('hotel_list', JSON.stringify(this.hotels));
    localStorage.setItem(
      'search_form_values',
      JSON.stringify(this.searchForm.value)
    );
    localStorage.setItem('mincheckinDate', JSON.stringify(this.mincheckinDate));
    localStorage.setItem(
      'mincheckoutDate',
      JSON.stringify(this.mincheckoutDate)
    );

    this.router.navigateByUrl(`/hotel/${hotel_id}`);
  }

  // onClick(filter_name: string) {
  //   this.filters.filter((filter_obj) => {
  //     if (filter_obj.name == filter_name) {
  //       filter_obj.selected = true;
  //     } else {
  //       filter_obj.selected = false;
  //     }
  //   });
  // }
}
