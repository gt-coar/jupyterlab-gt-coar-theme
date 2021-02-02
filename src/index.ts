import { JupyterFrontEnd, JupyterFrontEndPlugin } from '@jupyterlab/application';
import { IThemeManager } from '@jupyterlab/apputils';

const NAME = '@gt-coar/jupyterlab-theme';

const extension: JupyterFrontEndPlugin<void> = {
  id: `${NAME}:light`,
  requires: [IThemeManager],
  autoStart: true,
  activate: (app: JupyterFrontEnd, manager: IThemeManager) => {
    const style = `${NAME}/index.css`;

    manager.register({
      name: `GT COAR Light`,
      isLight: true,
      load: () => manager.loadCSS(style),
      unload: () => Promise.resolve(undefined),
    });
  },
};

export default extension;
