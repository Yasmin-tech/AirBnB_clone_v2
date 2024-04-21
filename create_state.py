#!/usr/bin/python3
from models.state import State
from models import storage
from datetime import datetime


# Create a new State instance
new_state = State()
new_state.id = "421a55f1-7d82-45d9-b54c-a76916479545"
new_state.created_at = datetime.utcnow()
new_state.updated_at = datetime.utcnow()
new_state.name = "Alabama"

# Add the new state to the session and commit
storage.new(new_state)
storage.save()