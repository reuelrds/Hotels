import { Injectable } from '@angular/core';
import {
  MatSnackBar,
  MatSnackBarRef,
  TextOnlySnackBar,
} from '@angular/material/snack-bar';
import { Subject } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class SnackbarService {
  private _message = new Subject<{ message: String; action: String }>();
  $snackBarMessage = this._message.asObservable();

  private snackBarRef: MatSnackBarRef<TextOnlySnackBar> | undefined;

  constructor(private _snackBar: MatSnackBar) {}

  displaySnackBar(message: String, action: String) {
    this.snackBarRef = this._snackBar.open(
      message as string,
      action as string,
      {
        duration: 2000,
      }
    );
  }

  closeSnackBar() {
    this.snackBarRef?.dismiss();
  }
}
