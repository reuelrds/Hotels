import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { AuthComponent } from './views/auth/auth.component';
import { HomeComponent } from './views/home/home.component';
import { RecommendComponent } from './views/recommend/recommend.component';

const routes: Routes = [
  { path: '', component: HomeComponent },
  { path: 'auth/login', component: AuthComponent },
  { path: 'auth/signup', component: AuthComponent },
  { path: 'recommend', component: RecommendComponent },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule],
})
export class AppRoutingModule {}
