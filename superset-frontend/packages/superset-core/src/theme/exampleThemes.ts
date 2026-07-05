/**
 * Licensed to the Apache Software Foundation (ASF) under one
 * or more contributor license agreements.  See the NOTICE file
 * distributed with this work for additional information
 * regarding copyright ownership.  The ASF licenses this file
 * to you under the Apache License, Version 2.0 (the
 * "License"); you may not use this file except in compliance
 * with the License.  You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing,
 * software distributed under the License is distributed on an
 * "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
 * KIND, either express or implied.  See the License for the
 * specific language governing permissions and limitations
 * under the License.
 */
/* eslint-disable theme-colors/no-literal-colors */
import { type SerializableThemeConfig, ThemeAlgorithm } from './types';

const exampleThemes: Record<string, SerializableThemeConfig> = {
  superset: {
    token: {
      colorBgElevated: '#fafafa',
    },
  },
  supersetDark: {
    token: {},
    algorithm: ThemeAlgorithm.DARK,
  },
  supersetCompact: {
    token: {},
    algorithm: ThemeAlgorithm.COMPACT,
  },
  funky: {
    token: {
      colorPrimary: '#f759ab', // hot pink
      colorSuccess: '#52c41a',
      colorWarning: '#faad14',
      colorError: '#ff4d4f',
      colorInfo: '#40a9ff',
      borderRadius: 12,
      fontFamily: 'Comic Sans MS, cursive',
    },
    algorithm: ThemeAlgorithm.DEFAULT,
  },
  funkyDark: {
    token: {
      colorPrimary: '#f759ab', // hot pink
      colorSuccess: '#52c41a',
      colorWarning: '#faad14',
      colorError: '#ff4d4f',
      colorInfo: '#40a9ff',
      borderRadius: 12,
      fontFamily: 'Comic Sans MS, cursive',
    },
    algorithm: ThemeAlgorithm.DARK,
  },
  catppuccinMocha: {
    token: {
      colorPrimary: '#89b4fa', // Blue
      colorSuccess: '#a6e3a1', // Green
      colorWarning: '#f9e2af', // Yellow
      colorError: '#f38ba8', // Red
      colorInfo: '#74c7ec', // Sapphire
      colorLink: '#89b4fa', // Blue
      colorTextBase: '#cdd6f4', // Text
      colorBgBase: '#1e1e2e', // Base
      colorBgContainer: '#1e1e2e', // Base
      colorBgElevated: '#313244', // Surface0
      colorBgLayout: '#181825', // Mantle
      colorBorder: '#585b70', // Surface2
      colorBorderSecondary: '#45475a', // Surface1
      colorText: '#cdd6f4', // Text
      colorTextSecondary: '#bac2de', // Subtext1
      colorTextTertiary: '#a6adc8', // Subtext0
      colorTextQuaternary: '#9399b2', // Overlay2
      colorFill: '#45475a', // Surface1
      colorFillSecondary: '#313244', // Surface0
      colorFillTertiary: '#1e1e2e', // Base
      colorSplit: '#45475a', // Surface1
    },
    algorithm: ThemeAlgorithm.DARK,
  },
};
export default exampleThemes;
