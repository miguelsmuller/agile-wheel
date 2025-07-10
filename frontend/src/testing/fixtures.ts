import { ActivatedRouteSnapshot } from '@angular/router';

import { Activity, DimensionWithScores, Participant } from 'domain/model';

export const regularParticipantFixture: Participant = {
  id: 'p1',
  name: 'Regular',
  email: 'j@x',
};

export const ownerParticipantFixture: Participant = {
  id: 'o1',
  name: 'Owner',
  email: 'j@x',
};

export const listParticipantsFixture: Participant[] = [
  regularParticipantFixture,
  ownerParticipantFixture,
  { id: 'p2', name: 'Second', email: 's@x' },
];

export const dimensionsFixture: DimensionWithScores[] = [
  {
    id: 'd1',
    name: 'dim',
    principles: [{ id: 'p', name: 'p', score: 2 }],
  },
];

export const activityFixture: Activity = {
  activity_id: 'a1',
  created_at: 'now',
  is_opened: true,
  owner: ownerParticipantFixture,
  participants: [],
  dimensions: [],
  evaluations: [],
};

export function createRoute(id?: string): ActivatedRouteSnapshot {
  return {
    paramMap: { get: (key: string) => (key === 'id' ? (id ?? null) : null) },
  } as ActivatedRouteSnapshot;
}

export function mockLocalStorage(
  activity: Activity | null,
  participant: Participant | null
): void {
  spyOn(localStorage, 'getItem').and.callFake((key: string) => {
    if (key === 'activity') {
      return activity ? JSON.stringify(activity) : null;
    }
    if (key === 'participant') {
      return participant ? JSON.stringify(participant) : null;
    }
    return null;
  });
}
