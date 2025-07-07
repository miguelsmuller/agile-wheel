import { SUBMIT_EVALUATION_USE_CASE_PORT } from './submit-evaluation-use-case-port';

describe('SUBMIT_EVALUATION_USE_CASE_PORT', () => {
  it('should be defined as an InjectionToken', () => {
    expect(SUBMIT_EVALUATION_USE_CASE_PORT).toBeDefined();
    expect(SUBMIT_EVALUATION_USE_CASE_PORT.toString()).toContain('SubmitEvaluationUseCasePort');
  });
});
