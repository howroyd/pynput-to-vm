import abc
import dataclasses
import enum
import importlib.metadata
import json
import time
from typing import Self

# import pynput
import pynput.keyboard as pykeyboard
import pynput.mouse as pymouse
import semantic_version

VERSION = semantic_version.Version.coerce(importlib.metadata.version("pynput-to-vm-drgreengiant"))


@enum.unique
class DeviceType(enum.IntEnum):
    """Enumeration of device types."""

    KEYBOARD = 1
    MOUSE_MOVE = 2
    MOUSE_BUTTON = 3


@dataclasses.dataclass(frozen=True, slots=True)
class Header:
    """Header for messages sent between the pynput-to-vm-drgreengiant and the VM."""

    version: semantic_version.Version
    device_type: DeviceType

    def as_dict(self) -> dict:
        """Convert to a dictionary."""
        return dataclasses.asdict(self)

    def toJSON(self) -> str:
        """Convert to a JSON string."""
        return json.dumps(self.as_dict(), default=str)

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        """Create from a dictionary."""
        return cls(semantic_version.Version.coerce(data["version"]), DeviceType(data["device_type"]))

    @classmethod
    def fromJSON(cls, jsonStr: str) -> Self:
        """Create from a JSON string."""
        data = json.loads(jsonStr)
        return cls.from_dict(data)


def make_header(device_type: DeviceType, *, version: semantic_version = None) -> Header:
    """Create a Header with the given device type and version."""
    return Header(version or VERSION, device_type)


@dataclasses.dataclass(frozen=True, slots=True)
class EventBase(abc.ABC):
    """Base class for events."""

    ts: float

    def as_dict(self) -> dict:
        """Convert to a dictionary."""
        return dataclasses.asdict(self)

    def toJSON(self) -> str:
        """Convert to a JSON string."""
        return json.dumps(self.as_dict(), default=str)

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        """Create from a dictionary."""
        return cls(data["ts"])

    @classmethod
    def fromJSON(cls, jsonStr: str) -> Self:
        """Create from a JSON string."""
        data = json.loads(jsonStr)
        return cls.from_dict(data)


@dataclasses.dataclass(frozen=True, slots=True)
class KeyboardEvent(EventBase):
    key: pykeyboard.Key
    pressed: bool

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        """Create from a dictionary."""
        return cls(data["ts"], pykeyboard.Key[data["key"]], data["pressed"])


def make_keyboard_event(key: pykeyboard.Key, pressed: bool, *, ts: float = None) -> KeyboardEvent:
    """Create a KeyboardEvent with the given key, pressed state."""
    return KeyboardEvent(ts or time.time(), key, pressed)


@dataclasses.dataclass(frozen=True, slots=True)
class MouseMoveEvent(EventBase):
    x: int
    y: int

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        """Create from a dictionary."""
        return cls(data["ts"], data["x"], data["y"])


def make_mouse_move_event(x: int, y: int, *, ts: float = None) -> MouseMoveEvent:
    """Create a MouseMoveEvent with the given x, y coordinates."""
    return MouseMoveEvent(ts or time.time(), x, y)


@dataclasses.dataclass(frozen=True, slots=True)
class MouseButtonEvent(EventBase):
    button: pymouse.Button
    pressed: bool

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        """Create from a dictionary."""
        return cls(data["ts"], pymouse.Button[data["button"]], data["pressed"])


def make_mouse_button_event(button: pymouse.Button, pressed: bool, *, ts: float = None) -> MouseButtonEvent:
    """Create a MouseButtonEvent with the given button, pressed state."""
    return MouseButtonEvent(ts or time.time(), button, pressed)


@dataclasses.dataclass(frozen=True, slots=True)
class Message:
    header: Header
    message: EventBase

    def as_dict(self) -> dict:
        """Convert to a dictionary."""
        return {"header": self.header.as_dict(), "message": self.message.as_dict()}

    def toJSON(self) -> str:
        """Convert to a JSON string."""
        return json.dumps(self.as_dict(), default=str)

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        """Create from a dictionary."""
        header = Header.from_dict(data["header"])
        if header.device_type == DeviceType.KEYBOARD:
            message = KeyboardEvent.from_dict(data["message"])
        elif header.device_type == DeviceType.MOUSE_MOVE:
            message = MouseMoveEvent.from_dict(data["message"])
        elif header.device_type == DeviceType.MOUSE_BUTTON:
            message = MouseButtonEvent.from_dict(data["message"])
        else:
            raise ValueError(f"Unknown device type: {header.device_type}")
        return cls(header, message)

    @classmethod
    def fromJSON(cls, jsonStr: str) -> Self:
        """Create from a JSON string."""
        data = json.loads(jsonStr)
        return cls.from_dict(data)


def make_message(message: EventBase, *, header: Header = None) -> Message:
    header = header or make_header(
        DeviceType.KEYBOARD
        if isinstance(message, KeyboardEvent)
        else DeviceType.MOUSE_MOVE
        if isinstance(message, MouseMoveEvent)
        else DeviceType.MOUSE_BUTTON
        if isinstance(message, MouseButtonEvent)
        else None
    )
    if header is None:
        raise ValueError(f"Unknown message type: {message}")
    return Message(header, message)
