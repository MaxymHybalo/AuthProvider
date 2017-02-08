import {Component} from "@angular/core";
import {Router} from "@angular/router";
import {UserService} from "../../services/user.service";
import {AlertService} from "../../services/alert.service";


@Component({
  selector:"app-register",
  templateUrl: "register.component.html",
  styleUrls:['register.component.scss']
})
export class RegisterComponent {
  model: any = {};
  loading = false;
  password : any;

  constructor(
    private router: Router,
    private userService: UserService,
    private alertService: AlertService
  ) { }

  onChangeType(pass:any){
    let passs = pass;
    if(passs.type == 'password'){
      pass.type = "text";
    }else if(passs.type == 'text'){
      pass.type = "password";
    }
  }

  register() {
    this.loading = true;
    this.userService.create(this.model)
      .subscribe(
        data => {
          this.alertService.success('Registration successful', true);
          this.router.navigate(['/login']);
        },
        error => {
          this.alertService.error(error);
          this.loading = false;
        });
  }
}
