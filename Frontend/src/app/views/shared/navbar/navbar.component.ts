import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'hotels-navbar',
  templateUrl: './navbar.component.html',
  styleUrls: ['./navbar.component.scss']
})
export class NavbarComponent implements OnInit {

  constructor() { }

  ngOnInit(): void {
  }

  onLogout() {
    // this.authService.logout();
  }

}
