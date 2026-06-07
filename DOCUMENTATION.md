# DOCUMENTATION

## Forks 

When a user forks a public deck, we support two modes: **shallow fork** and **hard copy**. The user is prompted to choose at fork time.

### Shallow Fork

A lightweight fork that creates a single record in the `deck_forks` table pointing to the original deck.

- No duplication of deck or card records

- Since `card_reviews` are scoped to `user_id`, the forking user starts with a clean review history for that deck's cards

- If the user deletes the fork, we delete from `deck_forks` + `card_reviews` by `user_id` and `deck_id`

- The user sees updates to the original deck automatically (new/edited/deleted cards)

**Caveats:**
- If the original owner deletes the deck, the fork record should cascade delete and the user should be notified
- If the original owner edits or removes a card, the forking user is affected silently

### Hard Copy

A full duplication of the deck and all its cards, owned independently by the forking user.

- New `deck` record created with `user_id` set to the forking user

- All cards duplicated with new IDs pointing to the new deck

- Completely independent — original deck changes have no effect

### Deletion Optimization

By storing `deck_id` directly on `card_reviews`, cleanup on fork deletion is a single query:

```sql
DELETE FROM card_reviews WHERE deck_id = <deck_id> AND user_id = <user_id>
DELETE FROM deck_forks WHERE deck_id = <deck_id> AND user_id = <user_id>
```

No need to traverse individual cards.
