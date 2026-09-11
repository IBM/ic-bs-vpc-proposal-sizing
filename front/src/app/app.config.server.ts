import { mergeApplicationConfig, ApplicationConfig } from '@angular/core';
import { provideServerRendering } from '@angular/platform-server';
import { provideServerRoutesConfig, RenderMode } from '@angular/ssr';
import { appConfig } from './app.config';

const serverConfig: ApplicationConfig = {
  providers: [
    provideServerRendering(),
    provideServerRoutesConfig([
      { path: '**', renderMode: RenderMode.Server }
    ])
  ]
};

export const config = mergeApplicationConfig(appConfig, serverConfig);
