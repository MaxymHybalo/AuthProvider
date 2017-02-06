import {Component, OnInit} from "@angular/core";
import {Router} from "@angular/router";
import {UserService} from "../../services/user.service";
import {User} from "../../models/user";
import {AlertService} from "../../services/alert.service"

@Component({
    selector: "app-home",
    templateUrl: "home.component.html"
})
export class HomeComponent implements OnInit {
    currentUser: User;
    user: User;

    constructor(
     private userService: UserService,
     private alertService: AlertService,
     private router: Router) {
        this.currentUser = JSON.parse(localStorage.getItem('currentUser'));
    }

    ngOnInit() {
        this.verifyToken();
    }

    // deleteUser(id: number) {
    //     this.userService.delete(id).subscribe(() => { this.loadAllUsers(); });
    // }
    private verifyToken(){
        this.userService.getVerifyToken().subscribe(
        user => { 
            this.user = user; 
        }, 
        error => {
          this.alertService.error(error);
          localStorage.removeItem('currentUser');
          this.router.navigate(['/login']);

        } )
    }

    // private loadUser() {
    //     this.userService.getAll().subscribe(users => { this.users = users; });
    // }
}
