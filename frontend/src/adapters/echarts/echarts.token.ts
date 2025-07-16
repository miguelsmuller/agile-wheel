import { InjectionToken } from '@angular/core';

import * as echarts from 'echarts/core';

export const ECHARTS_TOKEN = new InjectionToken<typeof echarts>('ECharts');

export const echartsProvider = {
  provide: ECHARTS_TOKEN,
  useValue: echarts,
};
