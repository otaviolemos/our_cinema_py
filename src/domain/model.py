from dataclasses import dataclass, field
from enum import Enum
from domain.errors import DuplicateRoomName, OverlappingSessionsOnSameRoom, SeatAlreadyReservedError, SeatDoesNotExistInSessionError
from datetime import datetime, timedelta
