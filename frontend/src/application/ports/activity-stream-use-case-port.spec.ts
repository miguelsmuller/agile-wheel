import { ACTIVITY_STREAM_USE_CASE_PORT } from './activity-stream-use-case-port';

describe('ACTIVITY_STREAM_USE_CASE_PORT', () => {
  it('should be defined as an InjectionToken', () => {
    expect(ACTIVITY_STREAM_USE_CASE_PORT).toBeDefined();
    expect(ACTIVITY_STREAM_USE_CASE_PORT.toString()).toContain('ActivityStreamUseCasePort');
  });
});
