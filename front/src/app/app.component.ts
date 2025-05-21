import { Component, OnInit } from '@angular/core';
import { RouterOutlet, Router } from '@angular/router';
import { HttpClient, HttpHeaders, HttpParams, HttpErrorResponse } from '@angular/common/http';
import { firstValueFrom } from 'rxjs';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { environment } from '../environments/environment';
import { response } from 'express';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet, FormsModule, CommonModule],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css'
})
export class AppComponent implements OnInit {

  //JWT_TOKENS = "JWT_TOKENS"

  //OAUTH_PROCESS = `${environment.appIDEndpoint}/authorization?client_id=91ddd557-b2f2-4077-9373-81646ba6cc19&scope=openid&response_type=code&redirect_uri=${environment.appIDRedirectURL}&code_challenge=NDkxZjk3YTBjNjQyMjMzY2JlNzdiYTU1YjlmY2M4ZDI1OGY1OGYzZDdmYjEzYmFlMGNlZGE2OGY5MzZiYzhlYg==&code_challenge_method=S256&nonce=2f39074cf7166dc67344`

  title = ''

  menuItems = [
    {
      "link": "/",
      "label": "Home"
    },
  {
    "link": "/disks",
    "label": "Volume calculation"
  }]

  constructor(private http: HttpClient, private router: Router) {
    router.events.subscribe(() => {
      this.title = this.getLabelFromLink(this.router.url);
    });
  }

  private getLabelFromLink(link: string){
    link = link.split("?")[0]
    for(let i=0; i<this.menuItems.length; i++){
      if(this.menuItems[i].link == link){
        return this.menuItems[i].label;
      }
    }
    return "UNDEFINED";
  }

  ngOnInit() {
    console.log("Version 1.0");
    /*let jwtToken = this.getFromLocalStorage(this.JWT_TOKENS);
    if(jwtToken != null){
      this.valid(JSON.parse(jwtToken)['access_token']).subscribe({
          error: e => {
            if(e.status == 401){
              this.initializeOAuthProcess();
            }
          },
      });
      return;
    }
    const queryString = window.location.search;
    const urlParams = new URLSearchParams(queryString);
    const code = urlParams.get('code');
    if(code != null){
      this.getJWTTokens(code).subscribe(values => {
        this.saveToLocalStorage(this.JWT_TOKENS, JSON.stringify(values));
        window.location.href = "/disks"
      });
    }
    else{
      if(this.getFromLocalStorage(this.JWT_TOKENS) == null){
        this.initializeOAuthProcess();
      }
    }*/
  }

  /*valid(jwt: string){
    const headers = new HttpHeaders({
      'Authorization': 'Bearer ' + jwt,
      'Accept': 'application/json'
    });
    return this.http.get(`${environment.apiEndpoint}/token`, { headers: headers });
  }*/

  /*
  getJWTTokens(code: string){
    // Set the URL
    const url = `${environment.appIDEndpoint}/token`;
    const codeVerifier = '30445b3d69509aa3b40534d8fed41a9085bb103604f0'

    const headers = new HttpHeaders({
      'Content-Type': 'application/x-www-form-urlencoded',
      'Authorization': 'Basic ' + btoa(`91ddd557-b2f2-4077-9373-81646ba6cc19:${codeVerifier}`)
    });

    const body = new HttpParams()
      .set('grant_type', 'authorization_code')
      .set('code', code)
      .set('redirect_uri', environment.appIDRedirectURL)
      .set('code_verifier', codeVerifier)
      .set('client_id', '91ddd557-b2f2-4077-9373-81646ba6cc19');

    return this.http.post(url, body.toString(), { headers: headers });
  }

  initializeOAuthProcess(){
    this.removeFromLocalStorage(this.JWT_TOKENS);
    window.location.href = this.OAUTH_PROCESS
  }

  saveToLocalStorage(key: string, value: string) {
    localStorage.setItem(key, value);
  }

  getFromLocalStorage(key: string) {
    return localStorage.getItem(key);
  }

  removeFromLocalStorage(key: string) {
    return localStorage.removeItem(key);
  }*/
}
