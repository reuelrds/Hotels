import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'hotels-auth',
  templateUrl: './auth.component.html',
  styleUrls: ['./auth.component.scss'],
})
export class AuthComponent implements OnInit {
  isLoginFormVisible = true;

  constructor(private router: Router) {}

  ngOnInit(): void {
    console.log(this.router.url);

    if (this.router.url === '/auth/signup') {
      this.toggleOverlay();
    }
  }

  toggleOverlay() {
    console.log(this.isLoginFormVisible);
    this.isLoginFormVisible = !this.isLoginFormVisible;

    console.log(this.isLoginFormVisible);
  }
}
