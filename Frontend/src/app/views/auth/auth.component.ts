import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'hotels-auth',
  templateUrl: './auth.component.html',
  styleUrls: ['./auth.component.scss'],
})
export class AuthComponent implements OnInit {
  isLoginFormVisible = true;

  constructor() {}

  ngOnInit(): void {}

  toggleOverlay() {
    console.log(this.isLoginFormVisible);
    this.isLoginFormVisible = !this.isLoginFormVisible;

    console.log(this.isLoginFormVisible);
  }
}
