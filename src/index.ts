import { JupyterFrontEnd, JupyterFrontEndPlugin } from '@jupyterlab/application';
import { IThemeManager } from '@jupyterlab/apputils';

const NAME = '@gt-coar/jupyterlab-theme'
const VARIANTS = ['light', 'dark'];

function makeTheme(variant: string): JupyterFrontEndPlugin<void> {
  return {
    id: `${NAME}:${variant}`,
    requires: [IThemeManager],
    autoStart: true,
    activate: (app: JupyterFrontEnd, manager: IThemeManager) => {
      const style = `${NAME}/${variant}.css`;

      manager.register({
        name: `GT COAR (${variant[0]})`,
        isLight: true,
        load: () => manager.loadCSS(style),
        unload: () => Promise.resolve(undefined)
      });
    }
  }
}

const extensions = VARIANTS.map(makeTheme);

export default extensions;

