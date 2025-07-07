import { ACTIVITY_FLOW_USE_CASE_PORT } from './activity-flow-use-case-port';

describe('ACTIVITY_FLOW_USE_CASE_PORT', () => {
  it('should be defined as an InjectionToken', () => {
    expect(ACTIVITY_FLOW_USE_CASE_PORT).toBeDefined();
    expect(ACTIVITY_FLOW_USE_CASE_PORT.toString()).toContain('ActivityFlowUseCasePort');
  });
});
