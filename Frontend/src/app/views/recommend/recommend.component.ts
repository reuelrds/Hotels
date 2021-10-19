import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup } from '@angular/forms';

@Component({
  selector: 'hotels-recommend',
  templateUrl: './recommend.component.html',
  styleUrls: ['./recommend.component.scss'],
})
export class RecommendComponent implements OnInit {
  room_count = 1;
  guest_count = 2;

  searchForm: FormGroup;

  filters = [
    { name: 'Chip 1', selected: false },
    { name: 'Chip 2', selected: false },
  ];

  constructor(private formBuilder: FormBuilder) {
    this.searchForm = this.formBuilder.group({
      destination: '',
      checkinDate: '',
      checkoutDate: '',
      rooms: this.room_count,
      guests: this.guest_count,
    });
  }

  ngOnInit(): void {}

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
  }

  onClick(filter_name: string) {
    this.filters.filter((filter_obj) => {
      if (filter_obj.name == filter_name) {
        filter_obj.selected = true;
      } else {
        filter_obj.selected = false;
      }
    });
  }
}
