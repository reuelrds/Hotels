import { Component, OnInit } from '@angular/core';
import { FormGroup, FormBuilder, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { AuthService } from 'src/app/services/auth.service';

@Component({
  selector: 'hotels-signup',
  templateUrl: './signup.component.html',
  styleUrls: ['./signup.component.scss'],
})
export class SignupComponent implements OnInit {
  signupForm: FormGroup;
  isLoading: boolean;

  constructor(
    private router: Router,
    private formBuilder: FormBuilder,
    private authService: AuthService
  ) {
    this.signupForm = this.formBuilder.group({
      email: ['', [Validators.required, Validators.email]],
      username: ['', Validators.required],
      password: ['', [Validators.required, Validators.minLength(6)]],
    });
    this.isLoading = false;
  }

  ngOnInit(): void {}

  onSubmit() {
    if (this.signupForm.valid) {
      console.log(this.signupForm.valid);
      this.isLoading = true;

      this.authService
        .registerUser(this.signupForm.value)
        .subscribe((response) => {
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
