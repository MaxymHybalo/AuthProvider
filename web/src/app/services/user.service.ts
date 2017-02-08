import { Injectable } from '@angular/core';
import { Http, Headers, RequestOptions, Response } from '@angular/http';

import { User } from '../models/user';

@Injectable()
export class UserService {
    url:string;
    constructor(private http: Http) {
       this.url = "http://localhost:5001"
     }

    getVerifyToken() {
        return this.http.get(`${this.url}/api/profile/`, this.jwt()).map((response: Response) => response.json());
    }
    // getById(id: number) {
    //     return this.http.get('/api/users/' + id, this.jwt()).map((response: Response) => response.json());
    // }
    create(user: User) {
        return this.http.post(`${this.url}/signup/`, user, this.jwt()).map((response: Response) => response.json());
    }
    // update(user: User) {
    //     return this.http.put('/api/users/' + user.id, user, this.jwt()).map((response: Response) => response.json());
    // }

    // delete(id: number) {
    //     return this.http.delete('/api/users/' + id, this.jwt()).map((response: Response) => response.json());
    // }

    private jwt() {
        let currentUser = JSON.parse(localStorage.getItem('currentUser'));
        if (currentUser) {
            let headers = new Headers({ 'Authorization': 'Bearer ' + currentUser });
            return new RequestOptions({ headers: headers });
        }
    }
}
