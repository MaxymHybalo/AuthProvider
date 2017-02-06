import { Injectable } from '@angular/core';
import { Http, Headers, Response } from '@angular/http';
import { Observable } from 'rxjs/Observable';
import 'rxjs/add/operator/map';

@Injectable()
export class AuthenticationService {
  constructor(private http: Http) { }

  login(username: string, password: string) {
    let headers = new Headers();
    headers.append('Content-Type', 'application/json');
    return this.http.post('http://ac532bd0.ngrok.io/auth/', JSON.stringify({ username: username, password: password }),{headers:headers})
      .map((response: Response) => {
        // Если успех, то возврощается
        let token = response.json().access_token;
          // Храним данные юзера и токен для перемищения по старницам
          localStorage.setItem('currentUser', JSON.stringify(token));
        
      });
  }



  logout() {
    // Удаляем юзера с localStorage
    localStorage.removeItem('currentUser');
  }
}
