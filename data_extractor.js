let namesBySlot = AvailableAtSlot.map(ids => ids.map(id => PeopleNames[PeopleIDs.indexOf(id)]));
let slotsPerDay = 11 * 4; // hours in the legal range * number of quarter-hour periods in the when2meet interface per hour
let numDays = 5;
let days = [];
for (let i = 0; i < numDays; i++) {
  days.push(namesBySlot.slice(i * slotsPerDay, (i+1) * slotsPerDay));
}
copy(JSON.parse(JSON.stringify(days)));

//AvailableAtSlot[TimeOfSlot.indexOf(Time)] // gives IDs of who's available at the slot identified by data-time=Time in HTML

//AvailableAtSlot is a flat array of who's available at each slot, from top->bottom then left->right
//only has IDs but can look these up by:
//PeopleNames[PeopleIDs.indexOf( peopleID )]

// to get names of who's available at each slot
//AvailableAtSlot.map(ids => ids.map(id => PeopleNames[PeopleIDs.indexOf(id)]))

//TimeOfSlot is an array of the same shape
//AvailableAtSlot[TimeOfSlot.indexOf(Time)] // gives IDs of who's available at the slot identified by data-time=Time in HTML
