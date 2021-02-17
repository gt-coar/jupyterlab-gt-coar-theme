/*
  Copyright (c) 2021 University System of Georgia and jupyterlab-gt-coar-theme contributors
| Distributed under the terms of the BSD-3-Clause License.
*/

import WORDMARK_SVG from '../style/img/wordmark.svg';
import WORDMARK_URL from '!!file-loader?name=[path][name].[ext]&context=.!../style/img/wordmark.svg';
import CHEVRONS_URL from '!!file-loader?name=[path][name].[ext]&context=.!../style/img/chevrons.svg';

export const NS = '@gt-coar/jupyterlab-theme';
export const NAME = 'GT COAR';

export const WORDMARK_ICON_ID = `${NS}:wordmark`;

export { WORDMARK_URL, CHEVRONS_URL, WORDMARK_SVG };
