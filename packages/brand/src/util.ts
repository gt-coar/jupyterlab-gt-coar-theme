/*
  Copyright (c) 2021 University System of Georgia and jupyterlab-gt-coar-theme contributors
| Distributed under the terms of the BSD-3-Clause License.
*/

import { LabIcon, jupyterFaviconIcon } from '@jupyterlab/ui-components';
import { JupyterFrontEnd, JupyterFrontEndPlugin } from '@jupyterlab/application';
import { IThemeManager } from '@jupyterlab/apputils';
import { PageConfig } from '@jupyterlab/coreutils';

import {
  NAME,
  WORDMARK_SVG,
  WORDMARK_ICON_ID,
  CHEVRONS_URL,
  WORDMARK_URL,
  IThemeOptions,
} from './tokens';

export const GT_ICON = new LabIcon({ name: WORDMARK_ICON_ID, svgstr: WORDMARK_SVG });

export const OG_FAVICON = jupyterFaviconIcon.svgstr;
export const OG_FAVICON_MIME = 'image/x-icon';
export const GT_FAVICON_MIME = 'image/svg+xml';

export function makeTheme(opts: IThemeOptions): JupyterFrontEndPlugin<void> {
  return {
    id: `${opts.ns}:${opts.variant.toLowerCase()}`,
    requires: [IThemeManager],
    autoStart: true,
    activate: async (app: JupyterFrontEnd, manager: IThemeManager) => {
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
        if (faviconIdle && faviconBusy) {
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
      }

      manager.register({
        name: `${NAME} (${opts.variant})`,
        isLight: opts.isLight,
        themeScrollbars: true,
        load: async () => {
          toggleFavicons();
          return manager.loadCSS(`${opts.ns}/index.css`);
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
