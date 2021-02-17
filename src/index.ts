/*
  Copyright (c) 2021 University System of Georgia and jupyterlab-gt-coar-theme contributors
| Distributed under the terms of the BSD-3-Clause License.
*/

import { JupyterFrontEnd, JupyterFrontEndPlugin } from '@jupyterlab/application';
import { IThemeManager } from '@jupyterlab/apputils';
import { PageConfig } from '@jupyterlab/coreutils';
import { LabIcon, jupyterFaviconIcon } from '@jupyterlab/ui-components';

import {
  NS,
  NAME,
  WORDMARK_SVG,
  WORDMARK_ICON_ID,
  CHEVRONS_URL,
  WORDMARK_URL,
} from './tokens';

export const GT_ICON = new LabIcon({ name: WORDMARK_ICON_ID, svgstr: WORDMARK_SVG });

const OG_FAVICON = jupyterFaviconIcon.svgstr;
const OG_FAVICON_MIME = 'image/x-icon';
const GT_FAVICON_MIME = 'image/svg+xml';

function makeTheme(value: string): JupyterFrontEndPlugin<void> {
  return {
    id: `${NS}:${value.toLowerCase()}`,
    requires: [IThemeManager],
    autoStart: true,
    activate: (app: JupyterFrontEnd, manager: IThemeManager) => {
      let wasLoaded = false;
      const isLight = value == 'Light';
      let faviconIdle: HTMLLinkElement;
      let faviconBusy: HTMLLinkElement;

      let ogFaviconIdle: string;
      let ogFaviconBusy: string;
      const baseUrl = PageConfig.getBaseUrl();

      function toggleFavicons(restore = false) {
        if (faviconIdle == null) {
          faviconIdle = document.querySelector('link.favicon.idle');
          ogFaviconIdle = `${baseUrl}static/favicons/favicon.ico`;
          faviconBusy = document.querySelector('link.favicon.busy');
          ogFaviconBusy = `${baseUrl}static/favicons/favicon-busy-1.ico`;
        }
        if (restore) {
          faviconIdle.href = ogFaviconIdle;
          faviconBusy.href = ogFaviconBusy;
          faviconIdle.type = faviconBusy.type = OG_FAVICON_MIME;
          jupyterFaviconIcon.svgstr = OG_FAVICON;
        } else {
          faviconIdle.href = WORDMARK_URL;
          faviconBusy.href = CHEVRONS_URL;
          faviconIdle.type = faviconBusy.type = GT_FAVICON_MIME;
          jupyterFaviconIcon.svgstr = WORDMARK_SVG;
        }
      }

      manager.register({
        name: `${NAME} ${value}`,
        isLight,
        themeScrollbars: !isLight,
        load: async () => {
          toggleFavicons();
          // avoid loading twice
          wasLoaded ? void 0 : manager.loadCSS(`${NS}/index.css`);
          wasLoaded = true;
        },
        unload: async () => {
          if (jupyterFaviconIcon.svgstr === WORDMARK_SVG) {
            toggleFavicons(true);
          }
        },
      });
    },
  };
}

const extensions = ['Light', 'Dark'].map(makeTheme);

export default extensions;
