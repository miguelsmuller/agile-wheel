import { TestBed } from '@angular/core/testing';

import { listParticipantsFixture } from '@test/fixtures';

import { ListParticipantsComponent } from './list-participants.component';

describe('ListParticipantsComponent', () => {
  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ListParticipantsComponent],
    }).compileComponents();
  });

  it('should display all participant names', () => {
    // Given
    const fixture = TestBed.createComponent(ListParticipantsComponent);

    const component = fixture.componentInstance;

    component.participants = listParticipantsFixture;

    // When
    fixture.detectChanges();

    // Then
    const names = [
      ...fixture.nativeElement.querySelectorAll('p.text-sm.font-semibold.text-gray-900'),
    ].map(el => el.textContent?.trim());

    expect(names).toEqual(listParticipantsFixture.map(p => p.name));
  });

  it('should track participant by id', () => {
    // Given
    const fixture = TestBed.createComponent(ListParticipantsComponent);

    const component = fixture.componentInstance;

    const participant = listParticipantsFixture[0];

    // When
    const id = component.trackById(0, participant);

    // Then
    expect(id).toBe(participant.id);
  });
});
