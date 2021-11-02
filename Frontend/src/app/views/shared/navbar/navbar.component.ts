import { Component, OnInit } from '@angular/core';
import { AuthService } from 'src/app/services/auth.service';

@Component({
  selector: 'hotels-navbar',
  templateUrl: './navbar.component.html',
  styleUrls: ['./navbar.component.scss'],
})
export class NavbarComponent implements OnInit {
  username!: String;

  constructor(private authService: AuthService) {}

  ngOnInit(): void {
    this.username = this.authService.userName;
  }

  onLogout() {
    this.authService.logout();
  }
}
