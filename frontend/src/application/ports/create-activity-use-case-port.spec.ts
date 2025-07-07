import { CREATE_ACTIVITY_USE_CASE_PORT } from './create-activity-use-case-port';

describe('CREATE_ACTIVITY_USE_CASE_PORT', () => {
  it('should be defined as an InjectionToken', () => {
    expect(CREATE_ACTIVITY_USE_CASE_PORT).toBeDefined();
    expect(CREATE_ACTIVITY_USE_CASE_PORT.toString()).toContain('CreateActivityUseCasePort');
  });
});
