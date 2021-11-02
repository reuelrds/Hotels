import { Component, OnInit } from '@angular/core';
import { FormGroup, FormBuilder, Validators } from '@angular/forms';
import { NavigationEnd, Router } from '@angular/router';
import { AuthService } from 'src/app/services/auth.service';

@Component({
  selector: 'hotels-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss'],
})
export class LoginComponent implements OnInit {
  loginForm: FormGroup;
  isLoading: boolean;

  constructor(
    private router: Router,
    private formBuilder: FormBuilder,
    private authService: AuthService
  ) {
    this.loginForm = this.formBuilder.group({
      email: ['', [Validators.required, Validators.email]],
      password: ['', [Validators.required, Validators.minLength(6)]],
    });
    this.isLoading = false;
  }

  ngOnInit(): void {}

  onSubmit() {
    if (this.loginForm.valid) {
      console.log(this.loginForm.valid);
      this.isLoading = true;
      this.authService.login(this.loginForm.value).subscribe((response) => {
        console.log(history.state);

        if (!('searchFormValues' in history.state)) {
          this.router.navigate(['/']);
        } else {
          console.log(history.state?.searchFormValues);
          this.router.navigate(['/recommend'], {
            state: {
              searchFormValues: history.state?.searchFormValues,
            },
          });
        }
        this.isLoading = false;
      });
    }
  }
}
