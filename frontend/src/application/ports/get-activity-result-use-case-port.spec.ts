import { GET_ACTIVITY_RESULT_USE_CASE_PORT } from './get-activity-result-use-case-port';

describe('GET_ACTIVITY_RESULT_USE_CASE_PORT', () => {
  it('should be defined as an InjectionToken', () => {
    expect(GET_ACTIVITY_RESULT_USE_CASE_PORT).toBeDefined();
    expect(GET_ACTIVITY_RESULT_USE_CASE_PORT.toString()).toContain('GetActivityResultUseCasePort');
  });
});
