import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Router } from '@angular/router';
import { environment } from 'src/environments/environment';
import { User } from '../models/user';
import { SnackbarService } from './snackbar.service';

import { tap } from 'rxjs/operators';

@Injectable({
  providedIn: 'root',
})
export class AuthService {
  BACKEND_URL = environment.BACKEND_URL;

  private _jwtToken: String | null;
  private _jwtExpiration: Number | null;
  isLoggedIn: boolean;

  private _userName: String;

  get jwtToken() {
    return this._jwtToken;
  }

  get userName() {
    return this._userName;
  }

  constructor(
    private httpClient: HttpClient,
    private router: Router,
    private snackBarService: SnackbarService
  ) {
    this._jwtToken = null;
    this._jwtExpiration = null;
    this.isLoggedIn = false;
    this._userName = '';
  }

  registerUser(user: { name: String; email: String; password: String }) {
    // console.log(user);
    return this.httpClient
      .post<{
        message: String;
        user: User;
        jwtToken: String;
        expiresin: Number;
      }>(`${this.BACKEND_URL}/auth/signup`, user)
      .pipe(
        tap(
          (res) => {
            if (res.message === 'Signup Successful') {
              console.log(res);
              this.snackBarService.displaySnackBar(res.message, 'Done');
              this._jwtToken = res.jwtToken;
              this._jwtExpiration = (res.expiresin as number) * 1000;

              this.isLoggedIn = true;

              this._userName = res.user.name;

              setTimeout(() => {
                this.logout();
              }, this._jwtExpiration as number);

              // this.router.navigate(['/']);
            }
          },
          (error) => {
            console.log(error);
            this.snackBarService.displaySnackBar(error.error.message, 'OK');
          }
        )
      );
  }

  login(loginDetails: { email: String; password: String }) {
    return this.httpClient
      .post<{
        message: String;
        user: User;
        jwtToken: String;
        expiresin: Number;
      }>(`${this.BACKEND_URL}/auth/login`, loginDetails)
      .pipe(
        tap(
          (res) => {
            if (res.message === 'Login Successful') {
              this.snackBarService.displaySnackBar(res.message, 'Done');
              this._jwtToken = res.jwtToken;
              this._jwtExpiration = (res.expiresin as number) * 1000;

              this.isLoggedIn = true;
              this._userName = res.user.name;

              setTimeout(() => {
                this.logout();
              }, this._jwtExpiration as number);

              // this.router.navigate(['/']);
            }
          },
          (error) => {
            // console.log(error);
            this.snackBarService.displaySnackBar(error.error.message, 'OK');
          }
        )
      );
  }

  logout() {
    this._jwtToken = null;
    this._jwtExpiration = null;

    this.isLoggedIn = false;

    this.snackBarService.displaySnackBar('Logout Successfull', 'Done');
    this.router.navigate(['/']);
    localStorage.clear();
  }
}
