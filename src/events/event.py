from typing import List, Self
from abc import abstractmethod, ABC


class Event:
    """Represents an event in the truck control system."""

    ON_ALREADY = "onalready"  # Event when a truck has no task.
    ON_CONTINUE = (
        "oncontinue"  # Event when a truck is waiting and should continue.
    )
    ON_GET_FIRE = "onfire"  # Event when a vertex catches fire.
    ON_PUT_OUT = "onputout"  # Event when a truck puts out fire in a vertex.
    ON_REFUEL = "onrefuel"  # Event when a truck needs to refuel its water tank.
    ON_START = "onstart"  # Event indicating the beginning of an operation.
    ON_WAIT = "onwait"  # Event when a truck must wait for another.
    ON_SET = "onset"  # Event when a manager sets a target for a truck.
    ON_MOVE = "onmove"  # Event when a fire truck move to a vertex.

    def __init__(
        self,
        event_type: str,
        target: str | None = None,
        sender_index: int | None = None,
        receiver_index: int | None = None,
    ):
        """Initializes an Event instance.

        Args:
            event_type (str): The type of the event.
            target (str, optional): The target vertex or entity of the event.
            sender_index (int, optional): The index of the sender truck.
        """
        self._target = target
        self._type = event_type
        self._sender = sender_index
        self._receiver = receiver_index

    @property
    def target(self) -> str:
        """Returns the event target.

        Returns:
            str: The target of the event.
        """
        return self._target

    @property
    def type(self) -> str:
        """Returns the event type.

        Returns:
            str: The type of the event.
        """
        return self._type

    @property
    def sender_id(self) -> int | None:
        """Returns the ID of the event sender.

        Returns:
            int: The index of the sender truck.
        """
        return self._sender

    @property
    def receiver_id(self) -> int | None:
        """Returns the ID of the event receiver.

        Returns:
            int: The index of the sender truck.
        """
        return self._receiver

    @classmethod
    def on_start(
        cls,
        target: str | None = None,
        sender_index: int | None = None,
        receiver_index: int | None = None,
    ) -> Self:
        """Creates a 'start' event.

        Args:
            target (str, optional): Event target.
            sender_index (int, optional): Sender index.

        Returns:
            Event: A new start event.
        """
        return Event(cls.ON_START, target, sender_index, receiver_index)

    @classmethod
    def on_wait(
        cls,
        target: str | None = None,
        sender_index: int | None = None,
        receiver_index: int | None = None,
    ) -> Self:
        """Creates a 'wait' event."""
        return Event(cls.ON_WAIT, target, sender_index, receiver_index)

    @classmethod
    def on_continue(
        cls,
        target: str | None = None,
        sender_index: int | None = None,
        receiver_index: int | None = None,
    ) -> Self:
        """Creates a 'continue' event."""
        return Event(cls.ON_CONTINUE, target, sender_index, receiver_index)

    @classmethod
    def on_get_fire(
        cls,
        target: str | None = None,
        sender_index: int | None = None,
        receiver_index: int | None = None,
    ) -> Self:
        """Creates a 'fire' event."""
        return Event(cls.ON_GET_FIRE, target, sender_index, receiver_index)

    @classmethod
    def on_put_out(
        cls,
        target: str | None = None,
        sender_index: int | None = None,
        receiver_index: int | None = None,
    ) -> Self:
        """Creates a 'put out' fire event."""
        return Event(cls.ON_PUT_OUT, target, sender_index, receiver_index)

    @classmethod
    def on_refuel(
        cls,
        target: str | None = None,
        sender_index: int | None = None,
        receiver_index: int | None = None,
    ) -> Self:
        """Creates a 'refuel' event."""
        return Event(cls.ON_REFUEL, target, sender_index, receiver_index)

    @classmethod
    def on_already(
        cls,
        target: str | None = None,
        sender_index: int | None = None,
        receiver_index: int | None = None,
    ) -> Self:
        """Creates an 'already' event indicating no pending tasks.

        Args:
            target (str, optional): Event target.
            sender_index (int, optional): Sender index.

        Returns:
            Event: A new 'already' event.
        """
        return Event(cls.ON_ALREADY, target, sender_index, receiver_index)

    @classmethod
    def on_set(
        cls,
        target: str | None = None,
        sender_index: int | None = None,
        receiver_index: int | None = None,
    ) -> Self:
        """Creates an 'set' event indicating a attribution from manager to truck.

        Args:
            target (str, optional): Event target.
            sender_index (int, optional): Sender index.

        Returns:
            Event: A new 'already' event.
        """
        return Event(cls.ON_SET, target, sender_index, receiver_index)

    def __repr__(self):
        return f"Event({self.type}, {self.target}, {self.sender_id}, {self.receiver_id})"


class EventListener(ABC):
    """Abstract base class for any object that listens to events."""

    @abstractmethod
    def handle(self, event: Event):
        """Handles an incoming event.

        Args:
            event (Event): The event to handle.
        """
        pass


class EventPool(ABC):
    """Manages event state and notifies listeners of changes."""

    def __init__(self):
        """Initializes the EventPool with an initial start event."""
        self._listeners: List[EventListener] = []
        self._state = Event.on_start()

    @property
    def event(self) -> Event:
        """Returns the current event state.

        Returns:
            Event: The current event.
        """
        return self._state

    @property
    def listeners(self) -> List[EventListener]:
        """Returns all registered event listeners.

        Returns:
            List[EventListener]: A list of event listeners.
        """
        return self._listeners

    def listen(self, event_listener: EventListener):
        """Registers a new event listener.

        Args:
            event_listener (EventListener): The listener to register.
        """
        self._listeners.append(event_listener)

    def unlisten(self, event_listener: EventListener):
        """Unregisters an existing event listener.

        Args:
            event_listener (EventListener): The listener to remove.
        """
        self._listeners.remove(event_listener)

    def notify(self, event: Event):
        """Notifies all listeners about a new event and updates state.

        Args:
            event (Event): The event to dispatch.
        """
        self._state = event

        for i in self.listeners:
            i.handle(event)

    def __repr__(self):
        return f"EventPool({self._listeners})"
