import { ENTER_ACTIVITY_USE_CASE_PORT } from './enter-activity-use-case-port';

describe('ENTER_ACTIVITY_USE_CASE_PORT', () => {
  it('should be defined as an InjectionToken', () => {
    expect(ENTER_ACTIVITY_USE_CASE_PORT).toBeDefined();
    expect(ENTER_ACTIVITY_USE_CASE_PORT.toString()).toContain('EnterActivityUseCasePort');
  });
});
