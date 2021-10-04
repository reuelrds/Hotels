import { Component, OnInit, ViewChild } from '@angular/core';

@Component({
  selector: 'hotels-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss'],
})
export class HomeComponent implements OnInit {

  room_count = 1;
  guest_count = 2;

  constructor() {}

  ngOnInit(): void {}

  openGuestsMenu(){}
}
