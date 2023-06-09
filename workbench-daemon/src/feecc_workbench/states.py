import enum


class State(enum.Enum):
    """Supported states"""

    AWAIT_LOGIN_STATE = "AwaitLogin"
    AUTHORIZED_IDLING_STATE = "AuthorizedIdling"
    UNIT_ASSIGNED_IDLING_STATE = "UnitAssignedIdling"
    GATHER_COMPONENTS_STATE = "GatherComponents"
    PRODUCTION_STAGE_ONGOING_STATE = "ProductionStageOngoing"


S = State
STATE_TRANSITION_MAP: dict[State, list[State]] = {
    S.AWAIT_LOGIN_STATE: [S.AUTHORIZED_IDLING_STATE],
    S.AUTHORIZED_IDLING_STATE: [S.UNIT_ASSIGNED_IDLING_STATE, S.AWAIT_LOGIN_STATE, S.GATHER_COMPONENTS_STATE],
    S.GATHER_COMPONENTS_STATE: [S.AUTHORIZED_IDLING_STATE, S.UNIT_ASSIGNED_IDLING_STATE],
    S.UNIT_ASSIGNED_IDLING_STATE: [S.AUTHORIZED_IDLING_STATE, S.AWAIT_LOGIN_STATE, S.PRODUCTION_STAGE_ONGOING_STATE],
    S.PRODUCTION_STAGE_ONGOING_STATE: [S.UNIT_ASSIGNED_IDLING_STATE],
}
