import {NgModule}      from '@angular/core';
import {BrowserModule} from '@angular/platform-browser';

import {AppComponent} from "./app.component";
import {routing, appRoutingProviders} from './app.routing';
import {FormsModule} from "@angular/forms";
import {HomeComponent} from "./component/home/home.component";
import {LoginComponent} from "./component/login/login.component";
import {RegisterComponent} from "./component/register/register.component";

import {AuthGuard} from "./guards/auth.guards";
import {AlertService} from "./services/alert.service";
import {AuthenticationService} from "./services/authentication.service";
import {UserService} from "./services/user.service";

import {BaseRequestOptions, HttpModule} from "@angular/http";
import {AlertComponent} from "./directives/alert.component";


@NgModule({
    imports: [
        BrowserModule,
        FormsModule,
        routing,
        HttpModule
    ],
    declarations: [
        AppComponent,
        AlertComponent,
        HomeComponent,
        LoginComponent,
        RegisterComponent
    ],
    providers: [
        BaseRequestOptions,

        AuthGuard,
        AlertService,
        AuthenticationService,
        UserService,
        appRoutingProviders
    ],
    bootstrap: [AppComponent]
})
export class AppModule {
}
