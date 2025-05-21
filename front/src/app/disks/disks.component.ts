import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { environment } from '../../environments/environment';

@Component({
  selector: 'disks-root',
  standalone: true,
  imports: [RouterOutlet, FormsModule, CommonModule],
  templateUrl: './disks.component.html',
  styleUrl: './disks.component.css'
})
export class DisksComponent {
  tiers = [
    { value: 'custom', label: 'custom' },
    { value: 'tier3', label: 'tier3' },
    { value: 'tier5', label: 'tier5' },
    { value: 'tier10', label: 'tier10' }
  ];
  tierValue = this.tiers[0].value;

  sizeValue: number = 50;

  IOPSValue: number = 182000;

  throughputValue: number = 3.7;

  disks:any = []

  avgBlockSize = 0;

  constructor(private http: HttpClient) {
    this.calculateAvgBlocksize();
  }

  calculateDisks(){
    this.calculateAvgBlocksize();
    const url = `${environment.apiEndpoint}/volumes`;

    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      'Authorization': 'Bearer ' + this.getAccessToken()
    });

    const body = {
      "thoughput": this.throughputValue, "iops": this.IOPSValue, "size": this.sizeValue, "tier": this.tierValue
    };

    this.http.post(url, JSON.stringify(body), { headers: headers }).subscribe(response => {
      console.log(response);
      this.disks = response;
    });
  }

  calculateAvgBlocksize(){
    this.avgBlockSize = this.throughputValue * 1000 * 1000 / this.IOPSValue;
  }

  getAccessToken(){
    return JSON.parse(localStorage.getItem("JWT_TOKENS") ?? "{}").access_token;
  }
}
