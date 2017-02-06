import {Component, OnInit} from "@angular/core";

@Component({
    selector: "app",
    templateUrl: "app.html",
    styleUrls:['app.scss']
})
export class AppComponent implements OnInit {
    ngOnInit() {
        console.log("Application component initialized ...");
    }

}
