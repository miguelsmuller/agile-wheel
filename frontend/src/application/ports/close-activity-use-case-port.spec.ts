import { CLOSE_ACTIVITY_USE_CASE_PORT } from './close-activity-use-case-port';

describe('CLOSE_ACTIVITY_USE_CASE_PORT', () => {
  it('should be defined as an InjectionToken', () => {
    expect(CLOSE_ACTIVITY_USE_CASE_PORT).toBeDefined();
    expect(CLOSE_ACTIVITY_USE_CASE_PORT.toString()).toContain('CloseActivityUseCasePort');
  });
});
