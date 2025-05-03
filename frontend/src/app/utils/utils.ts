import { Activity, Participant } from '@models/activity.model';

export function parseJSON<T>(jsonString: string): T {
  try {
    return JSON.parse(jsonString) as T;
  } catch (error) {
    throw new Error('Invalid JSON format');
  }
}

export function getActivityFromLocalStorage(): Activity | null {
  const raw = localStorage.getItem('activity');
  return (raw) ? parseJSON<Activity>(raw) : null;
}

export function setActivityToLocalStorage(activity: Activity): void {
  localStorage.setItem('activity', JSON.stringify(activity));
}

export function getParticipantFromLocalStorage(): Participant | null {
  const raw = localStorage.getItem('participant');
  return (raw) ? parseJSON<Participant>(raw) : null;
}

export function setParticipantToLocalStorage(participant: Participant): void {
  localStorage.setItem('participant', JSON.stringify(participant));
}