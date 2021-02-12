/*
  Copyright (c) 2021 University System of Georgia and jupyterlab-gt-coar-theme contributors
| Distributed under the terms of the BSD-3-Clause License.
*/

import { JupyterFrontEnd, JupyterFrontEndPlugin } from '@jupyterlab/application';
import { IThemeManager } from '@jupyterlab/apputils';
import { LabIcon, jupyterFaviconIcon } from '@jupyterlab/ui-components';

import { NS, NAME, GT_SVG, GT_ICON_ID } from './tokens';

export const GT_ICON = new LabIcon({ name: GT_ICON_ID, svgstr: GT_SVG });

const OG_FAVICON = jupyterFaviconIcon.svgstr;

function makeTheme(value: string): JupyterFrontEndPlugin<void> {
  return {
    id: `${NS}:${value.toLowerCase()}`,
    requires: [IThemeManager],
    autoStart: true,
    activate: (app: JupyterFrontEnd, manager: IThemeManager) => {
      let wasLoaded = false;
      const isLight = value == 'Light';

      manager.register({
        name: `${NAME} ${value}`,
        isLight,
        themeScrollbars: !isLight,
        load: async () => {
          jupyterFaviconIcon.svgstr = GT_SVG;
          // avoid loading twice
          wasLoaded ? void 0 : manager.loadCSS(`${NS}/index.css`);
          wasLoaded = true;
        },
        unload: async () => {
          if (jupyterFaviconIcon.svgstr === GT_SVG) {
            jupyterFaviconIcon.svgstr = OG_FAVICON;
          }
        },
      });
    },
  };
}

const extensions = ['Light', 'Dark'].map(makeTheme);

export default extensions;
