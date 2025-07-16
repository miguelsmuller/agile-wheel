import { ECHARTS_TOKEN, echartsProvider } from './echarts.token';

describe('ECHARTS_TOKEN', () => {
  it('should be defined', () => {
    expect(ECHARTS_TOKEN).toBeDefined();
    expect(ECHARTS_TOKEN.toString()).toContain('ECharts');
  });

  it('provider should reference the echarts namespace', () => {
    expect(echartsProvider.provide).toBe(ECHARTS_TOKEN);
    expect(echartsProvider.useValue).toBeDefined();
  });
});
