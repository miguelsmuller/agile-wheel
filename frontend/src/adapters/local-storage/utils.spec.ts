import { Activity, Participant } from 'domain/model';
import {
  parseJSON,
  getActivityFromLocalStorage,
  setActivityToLocalStorage,
  getParticipantFromLocalStorage,
  setParticipantToLocalStorage,
  clearDataFromLocalStorage,
} from './utils';

describe('utils', () => {
  beforeEach(() => localStorage.clear());

  const mockActivity: Activity = {
    activity_id: 'id',
    created_at: 'now',
    is_opened: true,
    owner: { id: 'p1', name: 'x', email: 'y' },
    participants: [],
    dimensions: [],
    evaluations: [],
  };

  const mockParticipant: Participant = { id: 'p1', name: 'x', email: 'y' };

  describe('parseJSON', () => {
    it('should correctly parse a valid JSON string', () => {
      // WHEN/THEN
      expect(parseJSON<{ a: number }>('{"a":1}')).toEqual({ a: 1 });
    });

    it('should throw an error when parsing an invalid JSON string', () => {
      // WHEN/THEN
      expect(() => parseJSON('notjson')).toThrowError('Invalid JSON format');
    });
  });

  describe('Activity localStorage utils', () => {
    it('getActivityFromLocalStorage should return null when there is no activity stored', () => {
      // WHEN/THEN
      expect(getActivityFromLocalStorage()).toBeNull();
    });

    it('set/get Activity should store and retrieve an activity correctly', () => {
      // WHEN
      setActivityToLocalStorage(mockActivity);

      // THEN
      expect(getActivityFromLocalStorage()).toEqual(mockActivity);
    });
  });

  describe('Participant localStorage utils', () => {
    it('getParticipantFromLocalStorage should return null when there is no participant stored', () => {
      // WHEN/THEN
      expect(getParticipantFromLocalStorage()).toBeNull();
    });

    it('set/get Participant should store and retrieve a participant correctly', () => {
      // WHEN
      setParticipantToLocalStorage(mockParticipant);

      // THEN
      expect(getParticipantFromLocalStorage()).toEqual(mockParticipant);
    });
  });

  describe('clearDataFromLocalStorage', () => {
    it('clearDataFromLocalStorage should clear both activity and participant data from localStorage', () => {
      // GIVEN
      setActivityToLocalStorage(mockActivity);
      setParticipantToLocalStorage(mockParticipant);

      //WHEN
      clearDataFromLocalStorage();

      // THEN
      expect(getActivityFromLocalStorage()).toBeNull();
      expect(getParticipantFromLocalStorage()).toBeNull();
    });
  });
});
