import {Routes, RouterModule} from "@angular/router";
import {AboutComponent} from "./about/components/about.component";
import {ModuleWithProviders} from "@angular/core";
import {HomeComponent} from "./component/home/home.component";
import {AuthGuard} from "./guards/auth.guards";
import {LoginComponent} from "./component/login/login.component";
import {RegisterComponent} from "./component/register/register.component";
// import {ContactsComponent} from "./contacts/components/contacts.component";

const appRoutes: Routes = [
    { path: '', component: HomeComponent, canActivate: [AuthGuard] },
    { path: 'login', component: LoginComponent },
    { path: 'register', component: RegisterComponent },

    // otherwise redirect to home
    { path: '**', redirectTo: '' },
    { path: 'about', component: AboutComponent }
];

export const appRoutingProviders: any[] = [];
export const routing: ModuleWithProviders = RouterModule.forRoot(appRoutes, { useHash: true });
