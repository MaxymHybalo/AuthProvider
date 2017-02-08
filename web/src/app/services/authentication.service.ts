import { Injectable } from '@angular/core';
import { Http, Headers, Response } from '@angular/http';
import { Observable } from 'rxjs/Observable';
import 'rxjs/add/operator/map';

@Injectable()
export class AuthenticationService {
  constructor(private http: Http) { }

  login(username: string, password: string) {
    let headers = new Headers();
    let url:string = "http://localhost:5001"; 
    headers.append('Content-Type', 'application/json');
    return this.http.post(`${url}/auth/`, JSON.stringify({ username: username, password: password }),{headers:headers})
      .map((response: Response) => {
        let token = response.json().access_token;

          localStorage.setItem('currentUser', JSON.stringify(token));
        
      });
  }

  logout() {
    localStorage.removeItem('currentUser');
  }
}
