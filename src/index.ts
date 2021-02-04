/*
  Copyright (c) 2021 University System of Georgia and jupyterlab-gt-coar-theme contributors
| Distributed under the terms of the BSD-3-Clause License.
*/

import { JupyterFrontEnd, JupyterFrontEndPlugin } from '@jupyterlab/application';
import { IThemeManager } from '@jupyterlab/apputils';

const NS = '@gt-coar/jupyterlab-theme';

function makeTheme(value: string): JupyterFrontEndPlugin<void> {
  return {
    id: `${NS}:${value.toLowerCase()}`,
    requires: [IThemeManager],
    autoStart: true,
    activate: (app: JupyterFrontEnd, manager: IThemeManager) => {
      const style = `${NS}/index.css`;

      manager.register({
        name: `GT COAR ${value}`,
        isLight: value == 'Light',
        load: () => manager.loadCSS(style),
        unload: () => Promise.resolve(undefined),
      });
    },
  };
}

const extensions = ['Light', 'Dark'].map(makeTheme);

export default extensions;
