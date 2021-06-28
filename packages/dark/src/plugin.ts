/*
  Copyright (c) 2021 University System of Georgia and jupyterlab-gt-coar-theme contributors
| Distributed under the terms of the BSD-3-Clause License.
*/
import { makeTheme } from '@gt-coar/jupyterlab-theme-brand';

import { NS } from './tokens';

const plugin = makeTheme({ ns: NS, variant: 'Dark', isLight: false });

export default [plugin];
